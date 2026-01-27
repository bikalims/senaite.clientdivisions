# -*- coding: utf-8 -*-

from Products.CMFPlone.utils import safe_unicode
from collections import OrderedDict
from zope.component import getAdapters

from bika.lims import api
from bika.lims.interfaces import IAddSampleRecordsValidator
from senaite.core.catalog import CONTACT_CATALOG

from senaite.clientdivisions.config import _
from senaite.clientdivisions.config import logger


def get_client_queries(self, obj, record=None):
    """Returns the filter queries to be applied to other fields based on
    both the Client object and record
    """
    # UID of the client
    uid = api.get_uid(obj)
    path = api.get_path(obj)

    queries = {
        "Contact": {
            "getParentUID": [uid, ""]
        },
        "CCContact": {
            "getParentUID": [uid, ""]
        },
        "SamplePoint": {
            "getClientUID": [uid, ""],
        },
        "Template": {
            "getClientUID": [uid, ""],
        },
        "Profiles": {
            "getClientUID": [uid, ""],
        },
        "Specification": {
            "getClientUID": [uid, ""],
        },
        "Sample": {
            "getClientUID": [uid],
        },
        "Batch": {
            "getClientUID": [uid, ""],
        },
        "Division": {
            "path": {
                "query": path,
                "depth": 1
            },
        },
        "PrimaryAnalysisRequest": {
            "getClientUID": [uid, ""],
        }
    }

    if self.context.portal_type == "Division":
        queries["Contact"] = {"getParentUID": record.get("Division")}
        queries["CCContact"] = {"getParentUID": record.get("Division")}
    # additional filtering by sample type
    record = record if record else {}
    sample_type_uid = record.get("SampleType")
    if api.is_uid(sample_type_uid):
        st_queries = self.get_sampletype_queries(sample_type_uid, record)
        queries.update(st_queries)

    return queries


def get_default_contact(self, client=None):
    """Logic refactored from JavaScript:

    * If client only has one contact, and the analysis request comes from
    * a client, then Auto-complete first Contact field.
    * If client only has one contect, and the analysis request comes from
    * a batch, then Auto-complete all Contact field.

    :returns: The default contact for the AR
    :rtype: Client object or None
    """
    from senaite.clientdivisions.interfaces import IDivision
    context = self.context
    client = client or self.get_client()
    if client:
        path = api.get_path(client)
    if IDivision.providedBy(context):
        path = api.get_path(context)
    query = {
        "portal_type": "Contact",
        "path": {
            "query": path,
            "depth": 1
        },
        "is_active": True,
    }
    catalog = api.get_tool(CONTACT_CATALOG)
    contacts = catalog(query)
    if len(contacts) == 1:
        return api.get_object(contacts[0])
    elif client == api.get_current_client():
        # Current user is a Client contact. Use current contact
        current_user = api.get_current_user()
        return api.get_user_contact(current_user,
                                    contact_types=["Contact"])

    return None


def ajax_submit(self):
    """Create samples and redirect to configured actions
    """
    # Check if there is the need to display a confirmation pane
    confirmation = self.check_confirmation()
    if confirmation:
        return {"confirmation": confirmation}

    # Get the maximum number of samples to create per record
    max_samples_record = self.get_max_samples_per_record()

    # Get AR required fields (including extended fields)
    fields = self.get_ar_fields()
    required_keys = [field.getName() for field in fields if field.required]

    # extract records from request
    records = self.get_records()

    fielderrors = {}
    errors = {"message": "", "fielderrors": {}}

    valid_records = []

    # Validate required fields
    for num, record in enumerate(records):

        # Extract file uploads (fields ending with _file)
        # These files will be added later as attachments
        file_fields = filter(lambda f: f.endswith("_file"), record)
        uploads = map(lambda f: record.pop(f), file_fields)
        attachments = [self.to_attachment_record(f) for f in uploads]

        # Required fields and their values
        required_values = [record.get(key) for key in required_keys]
        required_fields = dict(zip(required_keys, required_values))

        # Client field is required but hidden in the AR Add form. We remove
        # it therefore from the list of required fields to let empty
        # columns pass the required check below.
        if record.get("Client", False):
            required_fields.pop("Client", None)

        # Check if analyses are required for sample registration
        if not self.analyses_required():
            required_fields.pop("Analyses", None)

        # Contacts get pre-filled out if only one contact exists.
        # We won't force those columns with only the Contact filled out to
        # be required.
        contact = required_fields.pop("Contact", None)

        # None of the required fields are filled, skip this record
        if not any(required_fields.values()):
            continue

        # Re-add the Contact
        required_fields["Contact"] = contact

        # Check if the contact belongs to the selected client or is global
        contact_obj = api.get_object(contact, None)
        if not contact_obj:
            fielderrors["Contact"] = _("No valid contact")
        else:
            parent = api.get_parent(contact_obj)
            parent_uid = api.get_uid(parent)
            # Allow contacts that belong to the client or are global
            from bika.lims.interfaces import IClient
            is_client_contact = parent_uid == record.get("Client")
            if record.get("Division", ""):
                is_client_contact = parent_uid == record.get("Division")
            is_global_contact = not IClient.providedBy(parent)
            if not (is_client_contact or is_global_contact):
                msg = _("Contact doesa not belong to the selected client")
                fielderrors["Contact"] = msg

        # Auto-add CCContact when hidden on Sample Add form
        field = self.get_field("CCContact")
        hidden_fields = self.get_fields_with_visibility("hidden", mode="add")
        if field in hidden_fields and contact_obj:
            cc_contacts = contact_obj.getCCContact()
            if cc_contacts:
                record["CCContact"] = [cc.UID() for cc in cc_contacts]

        # Check if the number of samples per record is permitted
        num_samples = self.get_num_samples(record)
        if num_samples > max_samples_record:
            msg = _(u"error_analyssirequest_numsamples_above_max",
                    u"The number of samples to create for the record "
                    u"'Sample ${record_index}' (${num_samples}) is above "
                    u"${max_num_samples}",
                    mapping={
                        "record_index": num + 1,
                        "num_samples": num_samples,
                        "max_num_samples": max_samples_record,
                    })
            fielderrors["NumSamples"] = self.context.translate(msg)

        # Missing required fields
        missing = [f for f in required_fields if not record.get(f, None)]

        # Handle fields from Service conditions
        for condition in record.get("ServiceConditions", []):
            if condition.get("type") == "file":
                # Add the file as an attachment
                file_upload = condition.get("value")
                att = self.to_attachment_record(file_upload)
                if att:
                    # Add the file as an attachment
                    att.update({
                        "Service": condition.get("uid"),
                        "Condition": condition.get("title"),
                    })
                    attachments.append(att)
                # Reset the condition value
                filename = file_upload and file_upload.filename or ""
                condition.value = filename

            if condition.get("required") == "on":
                if not condition.get("value"):
                    title = condition.get("title")
                    if title not in missing:
                        missing.append(title)

        # If there are required fields missing, flag an error
        for field in missing:
            fieldname = "{}-{}".format(field, num)
            label = self.get_field_label(field) or field
            msg = self.context.translate(_("Field '{}' is required"))
            fielderrors[fieldname] = msg.format(label)

        # Process and validate field values
        valid_record = dict()
        tmp_sample = self.get_ar()
        for field in fields:
            field_name = field.getName()
            field_value = record.get(field_name)
            if field_value in ['', None]:
                continue

            # process the value as the widget would usually do
            process_value = field.widget.process_form
            value, msgs = process_value(tmp_sample, field, record)
            if not value:
                continue

            # store the processed value as the valid record
            valid_record[field_name] = value

            # validate the value
            error = field.validate(value, tmp_sample)
            if error:
                field_name = "{}-{}".format(field_name, num)
                fielderrors[field_name] = error

        # add the attachments to the record
        valid_record["attachments"] = filter(None, attachments)

        # keep the `_source_uid` in the record for the create process
        valid_record["_source_uid"] = record.get("_source_uid")

        # append the valid record to the list of valid records
        valid_records.append(valid_record)

    # return immediately with an error response if some field checks failed
    if fielderrors:
        errors["fielderrors"] = fielderrors
        return {'errors': errors}

    # do a custom validation of records. For instance, we may want to rise
    # an error if a value set to a given field is not consistent with a
    # value set to another field
    validators = getAdapters((self.request, ), IAddSampleRecordsValidator)
    for name, validator in validators:
        validation_err = validator.validate(valid_records)
        if validation_err:
            # Not valid, return immediately with an error response
            return {"errors": validation_err}

    # create the samples
    try:
        samples = self.create_samples(valid_records)
    except Exception as e:
        errors["message"] = str(e)
        logger.error(e, exc_info=True)
        return {"errors": errors}

    # We keep the title to check if AR is newly created
    # and UID to print stickers
    ARs = OrderedDict()
    for sample in samples:
        ARs[sample.Title()] = sample.UID()

    level = "info"
    if len(ARs) == 0:
        message = _('No Samples could be created.')
        level = "error"
    elif len(ARs) > 1:
        message = _('Samples ${ARs} were successfully created.',
                    mapping={'ARs': safe_unicode(', '.join(ARs.keys()))})
    else:
        message = _('Sample ${AR} was successfully created.',
                    mapping={'AR': safe_unicode(ARs.keys()[0])})

    # Display a portal message
    self.context.plone_utils.addPortalMessage(message, level)

    return self.handle_redirect(ARs.values(), message)

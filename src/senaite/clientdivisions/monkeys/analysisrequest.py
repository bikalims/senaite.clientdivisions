from bika.lims import api
# from senaite.samplepointlocations import check_installed
# from senaite.samplepointlocations import logger
from bika.lims.interfaces import IGetDefaultFieldValueARAddHook
from senaite.core.catalog import SETUP_CATALOG
from senaite.clientdivisions.config import logger
from bika.lims.interfaces import IAddSampleFieldsFlush
from zope.component import getAdapters
from zope.component import queryAdapter


def is_field_visible(self, field):
    """Check if the field is visible
    """
    context = self.context
    fieldname = field.getName()

    import pdb; pdb.set_trace()
    # hide the Client field on client and batch contexts
    if fieldname == "Client" and context.portal_type in ("Client", "Division"):
        return False

    # hide the Batch field on batch contexts
    if fieldname == "Batch" and context.portal_type in ("Batch", ):
        return False

    # hide the Batch field on batch contexts
    if fieldname == "Division" and context.portal_type in ("Division", ):
        return False

    return True


def get_client_info(self, obj):
    """Returns the client info of an object
    """
    info = self.get_base_info(obj)

    # Set the default contact, but only if empty. The Contact field is
    # flushed each time the Client changes, so we can assume that if there
    # is a selected contact, it belongs to current client already
    default_contact = self.get_default_contact(client=obj)
    if default_contact:
        contact_info = self.get_contact_info(default_contact)
        contact_info.update({"if_empty": True})
        info["field_values"].update({
            "Contact": contact_info
        })

    default_division = self.get_default_division(client=obj)
    import pdb; pdb.set_trace()
    if default_division:
        division_info = self.get_division_info(default_division)
        division_info.update({"if_empty": True})
        info["field_values"].update({
            "Division": division_info
        })

    # Set default CC Email field
    info["field_values"].update({
        "CCEmails": {"value": obj.getCCEmails(), "if_empty": True}
    })

    return info

def get_default_value(self, field, context, arnum):
    """Get the default value of the field
    """
    import pdb; pdb.set_trace()
    name = field.getName()
    default = field.getDefault(context)
    if name == "Batch":
        batch = self.get_batch()
        if batch is not None:
            default = batch
    if name == "Client":
        client = self.get_client()
        if client is not None:
            default = client
    # only set default contact for first column
    if name == "Contact" and arnum == 0:
        contact = self.get_default_contact()
        if contact is not None:
            default = contact
    if name == "Sample":
        sample = self.get_sample()
        if sample is not None:
            default = sample
    if name == "Division":
        division = self.get_division()
        if division is not None:
            default = division
    # Querying for adapters to get default values from add-ons':
    # We don't know which fields the form will render since
    # some of them may come from add-ons. In order to obtain the default
    # value for those fields we take advantage of adapters. Adapters
    # registration should have the following format:
    # < adapter
    #   factory = ...
    #   for = "*"
    #   provides = "bika.lims.interfaces.IGetDefaultFieldValueARAddHook"
    #   name = "<fieldName>_default_value_hook"
    # / >
    hook_name = name + '_default_value_hook'
    adapter = queryAdapter(
        self.request,
        name=hook_name,
        interface=IGetDefaultFieldValueARAddHook)
    if adapter is not None:
        default = adapter(self.context)
    logger.debug("get_default_value: context={} field={} value={} arnum={}"
                 .format(context, name, default, arnum))
    return default


def get_division(self):
    """Returns the Division
    """
    context = self.context
    parent = api.get_parent(context)
    if context.portal_type == "Division":
        return context
    elif parent.portal_type == "Division":
        return parent
    return None


def get_default_division(self, client=None):
    """Logic refactored from JavaScript:

    * If client only has one contact, and the analysis request comes from
    * a client, then Auto-complete first Contact field.
    * If client only has one contect, and the analysis request comes from
    * a batch, then Auto-complete all Contact field.

    :returns: The default contact for the AR
    :rtype: Client object or None
    """
    catalog = api.get_tool(SETUP_CATALOG)
    client = client or self.get_client()
    path = api.get_path(self.context)
    if client:
        path = api.get_path(client)
    query = {
        "portal_type": "Division",
        "path": {
            "query": path,
            "depth": 1
        },
        "is_active": True,
    }
    contacts = catalog(query)
    if len(contacts) == 1:
        return api.get_object(contacts[0])

    return None


def get_client_queries(self, obj, record=None):
    """Returns the filter queries to be applied to other fields based on
    both the Client object and record
    """
    # UID of the client
    uid = api.get_uid(obj)
    path = api.get_path(obj)

    # catalog queries for UI field filtering
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

    # additional filtering by sample type
    record = record if record else {}
    sample_type_uid = record.get("SampleType")
    if api.is_uid(sample_type_uid):
        st_queries = self.get_sampletype_queries(sample_type_uid, record)
        queries.update(st_queries)

    return queries


def get_division_info(self, obj):
    """Returns the client info of an object"""

    info = self.get_base_info(obj)

    return info


def ajax_get_flush_settings(self):
    """Returns the settings for fields flush

    NOTE: We automatically flush fields if the current value of a dependent
          reference field is *not* allowed by the set new query.
          -> see self.ajax_is_reference_value_allowed()
          Therefore, it makes only sense for non-reference fields!
    """
    flush_settings = {
        "Client": [
        ],
        "Contact": [
        ],
        "SampleType": [
        ],
        "PrimarySample": [
            "EnvironmentalConditions",
        ],
        "Supplier": [
            "SupplierContact",
            "SupplierLocation",
        ]
    }

    # Maybe other add-ons have additional fields that require flushing
    for name, ad in getAdapters((self.context,), IAddSampleFieldsFlush):
        logger.info("Additional flush settings from {}".format(name))
        additional_settings = ad.get_flush_settings()
        for key, values in additional_settings.items():
            new_values = flush_settings.get(key, []) + values
            flush_settings[key] = list(set(new_values))

    return flush_settings

# @check_installed(None)
# def getDivision(self):  # noqa camelcase
#     """Returns the AR's location"""
#     return self.getField("Division").get(self)

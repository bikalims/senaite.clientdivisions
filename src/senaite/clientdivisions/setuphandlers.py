# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer

from bika.lims import api
from senaite.clientdivisions.config import PROFILE_ID
from senaite.clientdivisions.config import logger


ID_FORMATTING = [
    {
        "portal_type": "Division",
        "form": "DVN{seq:06d}",
        "prefix": "location",
        "sequence_type": "generated",
        "counter_type": "",
        "split_length": 1,
    }
]


@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            'senaite.clientdivisions:uninstall',
        ]


def post_install(context):
    """Post install script"""
    # Do something at the end of the installation of this package.
    logger.info("SENAITE.CLIENTDIVISIONS post install handler [BEGIN]")
    profile_id = PROFILE_ID
    context = context._getImportContext(profile_id)
    portal = context.getSite()
    setup_id_formatting(portal)
    add_division_to_client(portal)


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.


def setup_id_formatting(portal, format_definition=None):
    """Setup default ID formatting"""
    if not format_definition:
        logger.info("Setting up ID formatting ...")
        for formatting in ID_FORMATTING:
            setup_id_formatting(portal, format_definition=formatting)
        logger.info("Setting up ID formatting [DONE]")
        return

    bs = portal.bika_setup
    p_type = format_definition.get("portal_type", None)
    if not p_type:
        return

    form = format_definition.get("form", "")
    if not form:
        logger.info("Param 'form' for portal type {} not set [SKIP")
        return

    logger.info("Applying format '{}' for {}".format(form, p_type))
    ids = list()
    for record in bs.getIDFormatting():
        if record.get("portal_type", "") == p_type:
            continue
        ids.append(record)
    ids.append(format_definition)
    bs.setIDFormatting(ids)


def add_division_to_client(portal):
    pt = api.get_tool("portal_types", context=portal)
    fti = pt.get("Client")

    # add to allowed types
    allowed_types = fti.allowed_content_types
    if allowed_types:
        allowed_types = list(allowed_types)
        if "Divisions" not in allowed_types:
            allowed_types.append("Divisions")
            fti.allowed_content_types = allowed_types

    if allowed_types:
        allowed_types = list(allowed_types)
        if "Division" not in allowed_types:
            allowed_types.append("Division")
            fti.allowed_content_types = allowed_types

    actions = fti.listActions()
    action_ids = [a.id for a in actions]
    if "divisions" not in action_ids:
        fti.addAction(
            id="divisions",
            name="Divisions",
            permission="View",
            category="object",
            visible=True,
            icon_expr="string:${portal_url}/images/samplepoint.png",
            action="string:${object_url}/divisions",
            condition="",
            link_target="",
        )

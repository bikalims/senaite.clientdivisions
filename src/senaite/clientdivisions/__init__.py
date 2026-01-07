# -*- coding: utf-8 -*-

from Products.Archetypes.atapi import listTypes
from Products.Archetypes.atapi import process_types
from Products.CMFCore.permissions import AddPortalContent
from Products.CMFCore.utils import ContentInit

# Implicit module imports used by others
# XXX Refactor these dependencies to explicit imports!
from senaite.clientdivisions.config import PRODUCT_NAME
from senaite.clientdivisions.config import logger


def initialize(context):
    logger.info("*** Initializing SENAITE.CLIENTDIVISIONS ***")
    from senaite.clientdivisions.content.division import Division
    from senaite.clientdivisions.content.divisions import Divisions

    from senaite.core import permissions

    content_types, constructors, ftis = process_types(
        listTypes(PRODUCT_NAME), PRODUCT_NAME)

    # Register each type with it's own Add permission
    # use "Add portal content" as default
    allTypes = zip(content_types, constructors)
    for atype, constructor in allTypes:
        kind = "%s: Add %s" % (PRODUCT_NAME, atype.portal_type)
        perm_name = "Add{}".format(atype.portal_type)
        perm = getattr(permissions, perm_name, AddPortalContent)
        ContentInit(kind,
                    content_types=(atype,),
                    permission=perm,
                    extra_constructors=(constructor, ),
                    fti=ftis,
                    ).initialize(context)

# -*- coding: utf-8 -*-

from AccessControl import ClassSecurityInfo
from Products.Archetypes.public import Schema
from Products.Archetypes.public import StringField
from Products.Archetypes.public import StringWidget
from Products.Archetypes.public import registerType
from Products.ATContentTypes.content import schemata
from zope.interface import implements

from bika.lims.content.client import Client
from bika.lims.interfaces import IDeactivable
from senaite.clientdivisions.config import _
from senaite.clientdivisions.config import PRODUCT_NAME
from senaite.clientdivisions.interfaces import IDivision

schema = Client.schema.copy() + Schema((
    StringField(
        "DivisionID",
        required=1,
        searchable=True,
        validators=("uniquefieldvalidator", "standard_id_validator"),
        widget=StringWidget(
            label=_("Division ID"),
            description=_(
                "Short and unique identifier of this client. Besides fast "
                "searches by client in Samples listings, the purposes of this "
                "field depend on the laboratory needs. For instance, the "
                "Division ID can be included as part of the Sample identifier, "
                "so the lab can easily know the client a given sample belongs "
                "to by just looking to its ID.")
        ),
    ),
))

schema["title"].widget.visible = False
schema["description"].widget.visible = False
schema["ClientID"].widget.visible = False
schema["ClientID"].required = False
schema["EmailAddress"].schemata = "default"

schema.moveField("DivisionID", after="Name")


class Division(Client):
    implements(IDivision, IDeactivable)

    security = ClassSecurityInfo()
    schema = schema
    # GROUP_KEY = "_client_division_group_id"

    def _renameAfterCreation(self, check_auto_id=False):
        from senaite.core.idserver import renameAfterCreation
        renameAfterCreation(self)


schemata.finalizeATCTSchema(schema, folderish=True, moveDiscussion=False)

registerType(Division, PRODUCT_NAME)

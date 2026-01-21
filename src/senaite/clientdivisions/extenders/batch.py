# -*- coding: utf-8 -*-

from Products.CMFCore.permissions import View
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from archetypes.schemaextender.interfaces import ISchemaExtender
from zope.component import adapts
from zope.interface import implementer

from bika.extras.extenders.fields import ExtUIDReferenceField
from bika.lims.interfaces import IBatch
from senaite.core.browser.widgets import ReferenceWidget
from senaite.core.permissions import FieldEditBatch

from senaite.clientdivisions.config import _
from senaite.clientdivisions.interfaces import ISenaiteClientdivisionsLayer

division_field = ExtUIDReferenceField(
    'Division',
    required=0,
    allowed_types=('Division',),
    relationship='BatchDivision',
    mode="r",
    write_permission=FieldEditBatch,
    read_permission=View,
    widget=ReferenceWidget(
        label=_("Division"),
        render_own_label=False,
        catalog_name='senaite_catalog_client',
        base_query={"is_active": True,
                    "sort_on": "sortable_title",
                    "getClientUID": "",
                    "sort_order": "ascending",
                    "portal_type": "Division"},
        showOn=True,
    ),
)


@implementer(ISchemaExtender, IBrowserLayerAwareExtender)
class BatchSchemaExtender(object):
    adapts(IBatch)
    layer = ISenaiteClientdivisionsLayer

    fields = [
        division_field,
    ]

    def __init__(self, context):
        self.context = context

    def getOrder(self, schematas):
        return schematas

    def getFields(self):
        return self.fields

# -*- coding: utf-8 -*-

from Products.CMFCore.permissions import View
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from archetypes.schemaextender.interfaces import ISchemaExtender
from archetypes.schemaextender.interfaces import ISchemaModifier
from zope.component import adapts
from zope.interface import implementer
from zope.interface import implements

from bika.lims.interfaces import IAnalysisRequest
from senaite.core.browser.widgets import ReferenceWidget
from senaite.core.permissions import FieldEditBatch

from .fields import ExtUIDReferenceField
from senaite.clientdivisions.config import _
from senaite.clientdivisions.config import is_installed
from senaite.clientdivisions.interfaces import ISenaiteClientdivisionsLayer

division_field = ExtUIDReferenceField(
    'Division',
    required=0,
    allowed_types=('Division',),
    relationship='AnalysisRequestDivision',
    mode="rw",
    write_permission=FieldEditBatch,
    read_permission=View,
    widget=ReferenceWidget(
        label=_("Division"),
        render_own_label=True,
        visible={
            'add': 'edit',
            'secondary': 'disabled',
        },
        catalog_name='senaite_catalog_setup',
        base_query={"is_active": True,
                    "sort_on": "sortable_title",
                    "getClientUID": "",
                    "sort_order": "ascending",
                    "portal_type": "Division"},
        showOn=True,
    ),
)


@implementer(ISchemaExtender, IBrowserLayerAwareExtender)
class AnalysisRequestSchemaExtender(object):
    adapts(IAnalysisRequest)
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


class AnalysisRequestSchemaModifier(object):
    adapts(IAnalysisRequest)
    implements(ISchemaModifier)
    layer = ISenaiteClientdivisionsLayer

    def __init__(self, context):
        self.context = context

    def fiddle(self, schema):
        """
        """
        if is_installed():
            schema.moveField('Division', before='Batch')

        return schema

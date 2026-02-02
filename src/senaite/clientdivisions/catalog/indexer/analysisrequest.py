# -*- coding: utf-8 -*-

from plone.indexer import indexer
from bika.lims.interfaces import IAnalysisRequest
from senaite.clientdivisions.interfaces import IDivision


@indexer(IAnalysisRequest)
def division_uid(instance):
    division = instance.Division
    if division:
        return division
    division = instance.aq_parent
    if IDivision.providedBy(division):
        return division.UID()
    return ""

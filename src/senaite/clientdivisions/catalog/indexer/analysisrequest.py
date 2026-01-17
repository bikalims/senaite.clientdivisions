# -*- coding: utf-8 -*-

from bika.lims.interfaces import IAnalysisRequest
from plone.indexer import indexer


@indexer(IAnalysisRequest)
def division_uid(instance):
    division = instance.Division
    if division:
        return division
    return ""

# -*- coding: utf-8 -*-

from bika.lims.interfaces import IAnalysisRequest
from plone.indexer import indexer


@indexer(IAnalysisRequest)
def division_uid(instance):
    division = instance.Division
    import pdb; pdb.set_trace()
    if division:
        return division
    return None

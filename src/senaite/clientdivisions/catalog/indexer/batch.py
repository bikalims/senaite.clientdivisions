# -*- coding: utf-8 -*-

from bika.lims.interfaces import IBatch
from plone.indexer import indexer


@indexer(IBatch)
def batch_division_uid(instance):
    if instance.aq_parent.portal_type == "Division":
        division = instance.aq_parent
        if division and not instance.Division:
            return division.UID()
    return ""

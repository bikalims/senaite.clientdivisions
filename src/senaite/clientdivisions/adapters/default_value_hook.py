# -*- coding: utf-8 -*-

from zope.interface import implements
from bika.lims import api
from bika.lims.interfaces import IGetDefaultFieldValueARAddHook


class DivisionDefaultValueHook(object):
    implements(IGetDefaultFieldValueARAddHook)

    def __init__(self, request):
        self.request = request

    def __call__(self, context):
        return self.get_division(context)

    def get_division(self, context):
        """Returns the Division
        """

        parent = api.get_parent(context)
        if context.portal_type == "Division":
            return context
        elif parent.portal_type == "Division":
            return parent
        elif context.portal_type == "Batch" and parent.portal_type == "Division":
            return parent
        return None

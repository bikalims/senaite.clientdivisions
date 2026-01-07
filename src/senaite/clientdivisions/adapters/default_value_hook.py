# -*- coding: utf-8 -*-

from zope.interface import implements

from bika.lims import api
from bika.lims.interfaces import IGetDefaultFieldValueARAddHook
from senaite.core.catalog import CLIENT_CATALOG


class DivisionDefaultValueHook(object):
    implements(IGetDefaultFieldValueARAddHook)

    def __init__(self, request):
        self.request = request

    def __call__(self, context):
        return self.get_division(context)

    def get_division(self, context):
        """Returns the Division
        """

        if context.portal_type == "Division":
            return context
        if context.portal_type == "Client":
            catalog = api.get_tool(CLIENT_CATALOG)
            path = api.get_path(context)
            query = {
                "portal_type": "Division",
                "path": {
                    "query": path,
                    "depth": 1
                },
            }
            divisions = catalog(query)
            if len(divisions) == 1:
                return api.get_object(divisions[0])
        return None

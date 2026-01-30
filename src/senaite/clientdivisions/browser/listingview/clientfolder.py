# -*- coding: utf-8 -*-

from zope.component import adapts
from zope.interface import implements

from bika.lims import api
from senaite.app.listing.interfaces import IListingView
from senaite.app.listing.interfaces import IListingViewAdapter
from senaite.core.catalog import CLIENT_CATALOG

from senaite.clientdivisions.config import is_installed


class ClientsListingViewAdapter(object):
    adapts(IListingView)
    implements(IListingViewAdapter)

    def __init__(self, listing, context):
        self.listing = listing
        self.context = context

    def before_render(self):
        if not is_installed():
            return

    def folder_item(self, brain, item, index):
        if not is_installed():
            return item
        path = api.get_path(brain)
        catalog = api.get_tool(CLIENT_CATALOG)
        query = {
            "portal_type": "Division",
            "path": {
                "query": path,
                "depth": 1}
        }
        divisions = catalog(query)
        if divisions:
            item["parent"] = ''
            item["children"] = [div.UID for div in divisions]
        return item

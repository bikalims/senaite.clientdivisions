# -*- coding: utf-8 -*-

from zope.component import adapts
from zope.interface import implements

from senaite.app.listing.interfaces import IListingView
from senaite.app.listing.interfaces import IListingViewAdapter
from senaite.clientdivisions.config import is_installed


class ClientContactsViewAdapter(object):
    adapts(IListingView)
    implements(IListingViewAdapter)

    def __init__(self, listing, context):
        self.listing = listing
        self.context = context

    def before_render(self):
        if not is_installed():
            return
        self.listing.contentFilter = {
            "portal_type": "Contact",
            "sort_on": "sortable_title",
            "path": {
                "query": "/".join(self.context.getPhysicalPath()),
                "depth": 1
            }
        }

    def folder_item(self, obj, item, index):
        if not is_installed():
            return item

        return item

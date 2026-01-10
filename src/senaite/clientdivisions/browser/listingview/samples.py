# -*- coding: utf-8 -*-

from collections import OrderedDict
from zope.component import adapts
from zope.interface import implements

from bika.lims import api
from bika.lims.utils import get_link
from senaite.app.listing.interfaces import IListingView
from senaite.app.listing.interfaces import IListingViewAdapter
from senaite.clientdivisions.config import _, is_installed


class SamplesListingViewAdapter(object):
    adapts(IListingView)
    implements(IListingViewAdapter)

    def __init__(self, listing, context):
        self.listing = listing
        self.context = context

    def before_render(self):
        if not is_installed():
            return

        def insert_after(od, after_key, new_key, value):
            new = OrderedDict()
            for k, v in od.items():
                new[k] = v
                if k == after_key:
                    new[new_key] = value
            return new

        division = [
            (
                "Division",
                {
                    "toggle": True,
                    "sortable": True,
                    "title": _("Division"),
                },
            )
        ]

        self.listing.columns = insert_after(
            self.listing.columns, "ClientID", "Division", division[0][1])

        for i in range(len(self.listing.review_states)):
            self.listing.review_states[i]["columns"].append("Division")

    def folder_item(self, obj, item, index):
        if not is_installed():
            return item

        obj = api.get_object(obj)
        division = obj.Schema()["Division"].getAccessor(obj)()
        if division:
            division_title = division.Title()  # or DivisionID
            division_url = division.absolute_url()
            division_link = get_link(division_url, division_title)
            item["Division"] = division_title
            item["replace"]["Division"] = division_link

        return item

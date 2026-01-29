# -*- coding: utf-8 -*-


from collections import OrderedDict
from zope.component import adapts
from zope.interface import implements

from bika.lims import api
from bika.lims.interfaces import IBatchFolder
from bika.lims.utils import get_link
from senaite.app.listing.interfaces import IListingView
from senaite.app.listing.interfaces import IListingViewAdapter

from senaite.clientdivisions.config import _
from senaite.clientdivisions.config import is_installed


class BatchesListingViewAdapter(object):
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

        if IBatchFolder.providedBy(self.context):
            self.listing.context_actions = {}
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

        if self.context.portal_type == "Client":
            self.listing.contentFilter['getBatchDivisionUID'] = ""
            self.listing.contentFilter['getClientUID'] = self.context.UID()

    def folder_item(self, brain, item, index):
        if not is_installed():
            return item
        division_uid = brain.getBatchDivisionUID
        if not division_uid:
            return item
        division = api.get_object_by_uid(division_uid)
        if division:
            division_title = division.Title()  # or DivisionID
            division_url = division.absolute_url()
            division_link = get_link(division_url, division_title)
            item["Division"] = division_title
            item["replace"]["Division"] = division_link
        return item

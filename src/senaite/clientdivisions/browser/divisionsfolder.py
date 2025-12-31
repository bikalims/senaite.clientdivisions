# -*- coding: utf-8 -*-

import collections

from bika.lims import api
from bika.lims import bikaMessageFactory as _
from bika.lims.browser.bika_listing import BikaListingView
from bika.lims.utils import get_link
from senaite.core.catalog import SETUP_CATALOG
from senaite.core.permissions import AddDepartment


class DivisionsView(BikaListingView):
    """Controlpanel Listing for Departments
    """

    def __init__(self, context, request):
        super(DivisionsView, self).__init__(context, request)

        self.catalog = SETUP_CATALOG
        self.show_select_row = False
        self.show_select_column = True
        self.pagesize = 25

        self.contentFilter = {
            "portal_type": "Division",
            "sort_order": "ascending",
            "sort_on": "sortable_title"
        }
        self.contentFilter["path"] = {
            "query": api.get_path(context),
            "level": 0}

        self.context_actions = {
            _("Add"): {
                "url": "++add++Division",
                "permission": AddDepartment,
                "icon": "++resource++bika.lims.images/add.png"}
        }

        self.title = self.context.translate(_("Divisions"))
        self.icon = "{}/{}".format(
            self.portal_url,
            "/++resource++bika.lims.images/department_big.png"
        )

        self.columns = collections.OrderedDict((
            ("Title", {
                "title": _("Division"),
                "index": "sortable_title"}),
            ("Description", {
                "title": _("Description"),
                "toggle": True}),
        ))

        self.review_states = [
            {
                "id": "default",
                "title": _("Active"),
                "contentFilter": {"is_active": True},
                "columns": self.columns.keys(),
            }, {
                "id": "inactive",
                "title": _("Inactive"),
                "contentFilter": {"is_active": False},
                "columns": self.columns.keys(),
            }, {
                "id": "all",
                "title": _("All"),
                "contentFilter": {},
                "columns": self.columns.keys(),
            },
        ]

    def folderitem(self, obj, item, index):
        """Service triggered each time an item is iterated in folderitems.
        The use of this service prevents the extra-loops in child objects.
        :obj: the instance of the class to be foldered
        :item: dict containing the properties of the object to be used by
            the template
        :index: current index of the item
        """
        obj = api.get_object(obj)
        title = obj.Title()
        description = obj.Description()
        url = obj.absolute_url()

        # Division Title
        item["replace"]["Title"] = get_link(url, value=title)
        item["Description"] = description

        return item

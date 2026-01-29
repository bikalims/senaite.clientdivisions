# -*- coding: utf-8 -*-

from Products.CMFCore.permissions import View
from bika.lims.browser.batchfolder import BatchFolderContentsView
from senaite.clientdivisions.config import _


class DivisionBatchesView(BatchFolderContentsView):

    def __init__(self, context, request):
        super(DivisionBatchesView, self).__init__(context, request)
        self.view_url = self.context.absolute_url() + "/batches"
        self.contentFilter['getBatchDivisionUID'] = self.context.UID()

    def update(self):
        """Before template render hook
        """
        super(BatchFolderContentsView, self).update()

        if self.can_add():
            # Add button. Note we set "View" as the permission, cause when no
            # permission is set, system fallback to "Add portal content" for
            # current context
            add_ico = "{}{}".format(self.portal_url, "/senaite_theme/icon/plus")
            url = self.context.absolute_url()
            self.context_actions = {
                _("Add"): {
                    "url": "{}/createObject?type_name=Batch".format(url),
                    "permission": View,
                    "icon": add_ico
                }
            }

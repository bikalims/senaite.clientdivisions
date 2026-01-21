# -*- coding: utf-8 -*-

from bika.lims.adapters.widgetvisibility import SenaiteATWidgetVisibility
from bika.lims.interfaces import IBatch
from bika.lims.interfaces import IClient
from senaite.core.interfaces import ISamples
from senaite.clientdivisions.interfaces import IDivision


class DivisionFieldVisibility(SenaiteATWidgetVisibility):
    """The Division field is editable by default in ar_add.  This adapter
    will force the Client field to be hidden when it should not be set
    by the user.
    """
    def __init__(self, context):
        super(DivisionFieldVisibility, self).__init__(
            context=context, sort=10, field_names=["Division"])

    def isVisible(self, field, mode="view", default="visible"):
        if mode == "add":
            parent = self.context.aq_parent
            if IDivision.providedBy(parent):
                # Note we return "hidden" here instead of "invisible": we want
                # the field to be auto-filled and processed on submit
                return "hidden"

            if IClient.providedBy(parent):
                # Note we return "hidden" here instead of "invisible": we want
                # the field to be auto-filled and processed on submit
                return "hidden"

            if ISamples.providedBy(parent):
                # Note we return "hidden" here instead of "invisible": we want
                # the field to be auto-filled and processed on submit
                return "hidden"

            if IBatch.providedBy(parent):
                # Note we return "hidden" here instead of "invisible": we want
                # the field to be auto-filled and processed on submit
                return "hidden"

            if IBatch.providedBy(parent) and parent.getClient():
                # The Batch has a Client assigned already!
                # Note we can have Batches without a client assigned
                return "hidden"
        elif mode == "edit":
            # This is already managed by wf permission, but is **never** a good
            # idea to allow the user to change the Client from an AR (basically
            # because otherwise, we'd need to move the object from one client
            # folder to another!).
            return "invisible"
        return default

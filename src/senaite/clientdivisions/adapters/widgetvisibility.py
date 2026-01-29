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


class BatchClientDivisionFieldVisibility(SenaiteATWidgetVisibility):
    """Client field in a Batch on the Division context in only editable
    while it is being created or when the Batch does not contain any sample
    """
    def __init__(self, context):
        super(BatchClientDivisionFieldVisibility, self).__init__(
            context=context, sort=3, field_names=["Client"])

    def isVisible(self, field, mode="view", default="visible"):
        """Returns whether the field is visible in a given state
        """
        if self.context.aq_parent.getClient():
            # This batch has a client assigned already and this cannot be
            # changed to prevent inconsistencies (client contacts can access
            # to batches that belong to their same client)
            return "invisible"

        if mode == "edit":
            # This batch does not have a client assigned, but allow the client
            # field to be editable only if does not contain any sample
            if self.context.aq_parent.getAnalysisRequestsBrains():
                return "invisible"

        return default

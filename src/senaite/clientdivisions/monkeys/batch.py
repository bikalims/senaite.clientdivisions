# -*- coding: utf-8 -*-

from senaite.clientdivisions.interfaces import IDivision


def getClient(self):
    """Retrieves the Client the current Batch is assigned to
    """
    # We override here getClient from ClientAwareMixin because te schema's
    # field Client is only used to allow the user to assign the batch to a
    # client in edit form. The entered value is used in
    # ObjectModifiedEventHandler to move the batch to the Client's folder,
    # so the value stored in the Schema's is not used anymore
    # See https://github.com/senaite/senaite.core/pull/1450
    client = self.aq_parent
    if client.portal_type == "Client":
        return client
    if client.aq_parent.portal_type == "Client":
        return client.aq_parent
    return None


def getDivision(self):
    """Retrieves the Division the current Batch is assigned to
    """
    # We override here getClient from ClientAwareMixin because te schema's
    # field Client is only used to allow the user to assign the batch to a
    # client in edit form. The entered value is used in
    # ObjectModifiedEventHandler to move the batch to the Client's folder,
    # so the value stored in the Schema's is not used anymore
    # See https://github.com/senaite/senaite.core/pull/1450
    division = self.aq_parent
    if IDivision.providedBy(division):
        return division
    return None

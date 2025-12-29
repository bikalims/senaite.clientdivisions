# -*- coding: utf-8 -*-

from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer

from senaite.clientdivisions.interfaces import IDivisions
from senaite.core.interfaces import IHideActionsMenu


class IDivisionsSchema(model.Schema):
    """Schema interface
    """


@implementer(IDivisions, IDivisionsSchema, IHideActionsMenu)
class Divisions(Container):
    """A folder/container for brands
    """

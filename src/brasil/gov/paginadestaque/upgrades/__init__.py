# -*- coding: utf-8 -*-
from plone import api


def csscookresources(portal_setup=None):

    api.portal.get_tool('portal_css').cookResources()

# -*- coding: utf-8 -*-
from brasil.gov.paginadestaque.config import PROJECTNAME
from plone import api

import logging

logger = logging.getLogger(PROJECTNAME)


def remove_tiles():
    """Remove tiles manually as registry uninstall profile is not working."""
    tiles = api.portal.get_registry_record('plone.app.tiles')
    if u'spacer' in tiles:
        logger.info('tiles still present on registry; applying nuke option')
        tiles.remove(u'spacer')


def uninstall(portal, reinstall=False):
    if not reinstall:
        profile = 'profile-{0}:uninstall'.format(PROJECTNAME)
        setup_tool = api.portal.get_tool('portal_setup')
        setup_tool.runAllImportStepsFromProfile(profile)

        remove_tiles()  # HACK: nuke option

        return 'Ran all uninstall steps.'

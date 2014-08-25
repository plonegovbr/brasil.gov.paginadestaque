# -*- coding: utf-8 -*-
from brasil.gov.paginadestaque.behaviors.interfaces import IBackgroundImage
from brasil.gov.paginadestaque.config import PROJECTNAME
from plone import api
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import queryUtility

import logging

logger = logging.getLogger(PROJECTNAME)


def disable_background_image_behavior():
    """Remove IBackgroundImage behavior from collective.cover."""
    fti = queryUtility(IDexterityFTI, name='collective.cover.content')
    behaviors = list(fti.behaviors)
    if IBackgroundImage.__identifier__ in behaviors:
        behaviors.remove(IBackgroundImage.__identifier__)
        fti.behaviors = tuple(behaviors)
        logger.info('IBackgroundImage disabled from collective.cover')


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

        disable_background_image_behavior()
        remove_tiles()  # HACK: nuke option

        return 'Ran all uninstall steps.'

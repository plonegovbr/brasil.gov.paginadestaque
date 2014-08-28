# -*- coding: utf-8 -*-
from brasil.gov.paginadestaque.behaviors.interfaces import IBackgroundImage
from brasil.gov.paginadestaque.config import PROJECTNAME
from brasil.gov.paginadestaque.interfaces import IBrowserLayer
from brasil.gov.paginadestaque.testing import INTEGRATION_TESTING
from plone import api
from plone.app.theming.utils import getTheme
from plone.browserlayer.utils import registered_layers
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import queryUtility

import unittest


class BaseTestCase(unittest.TestCase):
    """Base test case to be used by other tests."""

    layer = INTEGRATION_TESTING

    profile = 'brasil.gov.paginadestaque:default'

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']
        self.wt = self.portal['portal_workflow']
        self.st = self.portal['portal_setup']


class TestInstall(BaseTestCase):

    """Ensure product is properly installed."""

    def test_installed(self):
        self.assertTrue(self.qi.isProductInstalled(PROJECTNAME))

    def test_browser_layer_installed(self):
        self.assertIn(IBrowserLayer, registered_layers())

    def test_diazo_theme_installed(self):
        theme = getTheme('destaques-cinza')
        self.assertTrue(theme is not None)
        self.assertEqual(theme.__name__, 'destaques-cinza')
        self.assertEqual(theme.title, 'Página de Destaque - Tema Cinza')
        self.assertEqual(theme.description,
                         'Tema para Página de Destaque do Portal Padrão')
        self.assertEqual(theme.rules, '/++theme++destaques-cinza/rules.xml')
        self.assertEqual(theme.absolutePrefix, '/++theme++destaques-cinza')
        self.assertEqual(theme.doctype, '<!DOCTYPE html>')

    def test_background_image_behavior_enabled(self):
        fti = queryUtility(IDexterityFTI, name='collective.cover.content')
        self.assertIn(IBackgroundImage.__identifier__, fti.behaviors)

    def test_tiles_installed(self):
        tiles = api.portal.get_registry_record('plone.app.tiles')
        self.assertIn(u'spacer', tiles)

    def test_types_not_searched(self):
        site_properties = api.portal.get_tool('portal_properties')['site_properties']
        types_not_searched = site_properties.types_not_searched
        self.assertTrue(len(types_not_searched) > 1)
        self.assertIn(u'sc.microsite', types_not_searched)

    def test_types_not_listed(self):
        navtree_prop = api.portal.get_tool('portal_properties')['navtree_properties']
        metaTypesNotToList = navtree_prop.metaTypesNotToList
        self.assertTrue(len(metaTypesNotToList) > 1)
        self.assertIn(u'sc.microsite', metaTypesNotToList)

    def test_cover_styles(self):
        record = 'collective.cover.controlpanel.ICoverSettings.styles'
        styles = api.portal.get_registry_record(record)
        self.assertIn(u'-Default-|tile-default', styles)

    def test_tile_enabled(self):
        record = 'collective.cover.controlpanel.ICoverSettings.available_tiles'
        available_tiles = api.portal.get_registry_record(record)
        self.assertIn(u'spacer', available_tiles)

    def test_version(self):
        self.assertEqual(
            self.st.getLastVersionForProfile(self.profile),
            (u'1000',)
        )


class TestUninstall(BaseTestCase):

    """Ensure product is properly uninstalled."""

    def setUp(self):
        BaseTestCase.setUp(self)
        self.qi.uninstallProducts(products=[PROJECTNAME])

    def test_uninstalled(self):
        self.assertFalse(self.qi.isProductInstalled(PROJECTNAME))

    def test_browser_layer_removed(self):
        self.assertNotIn(IBrowserLayer, registered_layers())

    def test_background_image_behavior_disabled(self):
        fti = queryUtility(IDexterityFTI, name='collective.cover.content')
        self.assertNotIn(IBackgroundImage.__identifier__, fti.behaviors)

    def test_tile_removed(self):
        tiles = api.portal.get_registry_record('plone.app.tiles')
        self.assertNotIn(u'spacer', tiles)

    def test_tile_disabled(self):
        record = 'collective.cover.controlpanel.ICoverSettings.available_tiles'
        available_tiles = api.portal.get_registry_record(record)
        self.assertNotIn(u'spacer', available_tiles)

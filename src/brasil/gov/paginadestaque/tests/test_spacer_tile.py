# -*- coding: utf-8 -*-
from brasil.gov.paginadestaque.testing import INTEGRATION_TESTING
from brasil.gov.paginadestaque.tiles.spacer import SpacerTile
from collective.cover.tiles.base import IPersistentCoverTile
from mock import Mock
from plone.tiles.interfaces import ITileDataManager
from plone.tiles.interfaces import ITileType
from zope.component import getUtility
from zope.interface.verify import verifyClass
from zope.interface.verify import verifyObject

import unittest


class SpacerTileTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.name = 'spacer'
        self.tile = self.portal.restrictedTraverse(
            '@@{0}/{1}'.format(self.name, 'test'))

    def test_interface(self):
        self.assertTrue(IPersistentCoverTile.implementedBy(SpacerTile))
        self.assertTrue(verifyClass(IPersistentCoverTile, SpacerTile))

        tile = SpacerTile(None, None)
        self.assertTrue(IPersistentCoverTile.providedBy(tile))
        self.assertTrue(verifyObject(IPersistentCoverTile, tile))

    def test_tile_registration(self):
        tile_type = getUtility(ITileType, self.name)
        self.assertIsNotNone(tile_type)
        self.assertTrue(issubclass(tile_type.schema, IPersistentCoverTile))

    def test_default_configuration(self):
        self.assertFalse(self.tile.is_configurable)
        self.assertTrue(self.tile.is_editable)
        self.assertFalse(self.tile.is_droppable)

    def test_accepted_content_types(self):
        self.assertEqual(self.tile.accepted_ct(), [])

    def test_render_no_text(self):
        self.tile.is_compose_mode = Mock(return_value=True)
        warn_msg = u'Remember to add a text describing the background image for accessibility reasons.'
        self.assertIn(warn_msg, self.tile())

    def test_render_text(self):
        text = u'Achievement Unlocked: a11y'
        data_mgr = ITileDataManager(self.tile)
        data_mgr.set({'title': text})
        self.tile = self.portal.restrictedTraverse(
            '@@{0}/{1}'.format(self.name, 'test'))
        self.assertIn(text, self.tile())

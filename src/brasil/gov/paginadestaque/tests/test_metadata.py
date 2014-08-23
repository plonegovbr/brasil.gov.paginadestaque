# -*- coding: utf-8 -*-
from brasil.gov.paginadestaque.behaviors.metadata import IPaginaDestaque
from brasil.gov.paginadestaque.behaviors.metadata import PaginaDestaque
from brasil.gov.paginadestaque.testing import INTEGRATION_TESTING
from plone import api
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest


class PaginaDestaqueTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_behavior_enabled_by_default(self):
        fti = queryUtility(IDexterityFTI, name='sc.microsite')
        behaviors = fti.behaviors
        self.assertIn(
            'brasil.gov.paginadestaque.behaviors.metadata.IPaginaDestaque',
            behaviors
        )
        with api.env.adopt_roles(['Manager', ]):
            microsite = api.content.create(
                type='sc.microsite',
                id='microsite',
                container=self.portal
            )
        behavior = IPaginaDestaque(microsite, None)
        self.assertIsNotNone(
            behavior
        )

    def test_behavior_title(self):
        fti = queryUtility(IDexterityFTI, name='sc.microsite')
        factory = fti.factory
        new_object = createObject(factory)
        behavior = PaginaDestaque(new_object)
        behavior.title_1 = u'Portal Brasil'
        behavior.title_2 = u'7 de Setembro'

        self.assertEqual(
            behavior.title_1,
            u'Portal Brasil'
        )

        self.assertEqual(
            behavior.title_2,
            u'7 de Setembro'
        )

        self.assertEqual(
            new_object.title,
            u'Portal Brasil 7 de Setembro'
        )

        def set_title_1(value):
            behavior.title_1 = value
        self.assertRaises(ValueError, set_title_1, 'Uma string qualquer')

        def set_title_2(value):
            behavior.title_2 = value
        self.assertRaises(ValueError, set_title_2, 'Uma string qualquer')

    def test_behavior_description(self):
        fti = queryUtility(IDexterityFTI, name='sc.microsite')
        factory = fti.factory
        new_object = createObject(factory)
        behavior = PaginaDestaque(new_object)
        behavior.description = u'Microsite para o 7 de Setembro'
        # Armazenamento da data eh em property do objeto
        self.assertEqual(
            behavior.description,
            new_object.Description()
        )

        def set_description(value):
            behavior.description = value

        self.assertRaises(ValueError, set_description, 'Uma string qualquer')

    def test_behavior_links(self):
        fti = queryUtility(IDexterityFTI, name='sc.microsite')
        factory = fti.factory
        new_object = createObject(factory)
        behavior = PaginaDestaque(new_object)
        behavior.links = [
            {'title_1': u'Min.', 'title_2': u'dos Esportes', 'url': u'http://esportes.gov.br'},
            {'title_1': u'Min.', 'title_2': u'da Justiça', 'url': u'http://justiça.gov.br'},
        ]
        # Armazenamos dois itens
        self.assertEqual(len(behavior.links), 2)
        # Para cada item, computamos um title
        self.assertIn('title', behavior.links[0])
        self.assertEqual(u'Min. dos Esportes', behavior.links[0].get('title'))

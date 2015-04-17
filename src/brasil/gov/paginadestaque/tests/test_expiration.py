# -*- coding: utf-8 -*-

from brasil.gov.paginadestaque.behaviors.expiration import ISmartExpiration
from brasil.gov.paginadestaque.behaviors.expiration import SmartExpiration
from brasil.gov.paginadestaque.behaviors.expiration import default_expires
from brasil.gov.paginadestaque.behaviors.expiration import validate_url
from brasil.gov.paginadestaque.testing import INTEGRATION_TESTING

from plone import api
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility
from zope.interface import Invalid

import datetime
import unittest


class SmartExpirationTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_behavior_enabled_by_default(self):
        fti = queryUtility(IDexterityFTI, name='sc.microsite')
        behaviors = fti.behaviors
        self.assertIn(
            'brasil.gov.paginadestaque.behaviors.expiration.ISmartExpiration',
            behaviors
        )
        with api.env.adopt_roles(['Manager', ]):
            microsite = api.content.create(
                type='sc.microsite',
                id='microsite',
                container=self.portal
            )
        behavior = ISmartExpiration(microsite, None)
        self.assertIsNotNone(
            behavior
        )

    def test_behavior_expires(self):
        fti = queryUtility(IDexterityFTI, name='sc.microsite')
        factory = fti.factory
        new_object = createObject(factory)
        behavior = SmartExpiration(new_object)
        behavior.expires = datetime.datetime(2014, 9, 7, 12, 0, 0)
        # Armazenamento da data eh em property do objeto
        self.assertEqual(
            behavior.expires.strftime('%Y-%m-%d'),
            new_object.expiration_date.strftime('%Y-%m-%d')
        )

    def test_default_expires(self):
        today = datetime.datetime.today()
        expected = today + datetime.timedelta(60)
        # default_factory eh executado sempre no container
        default = default_expires(api.portal.get())
        # Comparamos ano-mes-dia
        self.assertEqual(
            expected.strftime('%Y-%m-%d'),
            default.strftime('%Y-%m-%d')
        )

    def test_behavior_expires_redirect(self):
        fti = queryUtility(IDexterityFTI, name='sc.microsite')
        factory = fti.factory
        new_object = createObject(factory)
        behavior = SmartExpiration(new_object)
        behavior.expires_redirect = u'http://www.simplesconsultoria.com.br'
        # Armazenamento da data eh em property do objeto
        self.assertEqual(
            behavior.expires_redirect,
            new_object.expires_redirect
        )

    def test_validate_url_success(self):
        # Testes validos para url
        self.assertTrue(validate_url(u'http://www.simplesconsultoria.com.br'))
        self.assertTrue(validate_url(u'https://www.simplesconsultoria.com.br'))
        self.assertTrue(validate_url(u'http://docs.plone.org/'))
        self.assertTrue(validate_url(u'https://plone.org/foundation/'))
        # Como o campo nao eh obrigatorio, podemos passar um valor vazio
        self.assertTrue(validate_url(u''))

    def test_validate_url_fail(self):
        # Erros de valor
        self.assertRaises(Invalid, validate_url, u'http//www.simplesconsultoria.com.br')  # NOQA
        # Protocolos invalidos
        self.assertRaises(Invalid, validate_url, u'ftp://ftp.funet.fi/pub/msx/')  # NOQA
        self.assertRaises(Invalid, validate_url, u'mailto://site@foo.bar')

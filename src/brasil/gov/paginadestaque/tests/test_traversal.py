# -*- coding: utf-8 -*-
from brasil.gov.paginadestaque.behaviors.expiration import ISmartExpiration
from brasil.gov.paginadestaque.behaviors.metadata import IPaginaDestaque
from brasil.gov.paginadestaque.interfaces import IBrowserLayer
from brasil.gov.paginadestaque.traversal.hooks import _is_expired
from brasil.gov.paginadestaque.testing import FUNCTIONAL_TESTING
from DateTime import DateTime
from plone import api
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.testing.z2 import Browser
from zope.interface.declarations import directlyProvides

import datetime
import transaction
import unittest


EXPIRES = datetime.datetime.today() + datetime.timedelta(60)
EXPIRED = datetime.datetime.today() - datetime.timedelta(60)


class TraversalTestCase(unittest.TestCase):

    layer = FUNCTIONAL_TESTING

    def setup_microsite(self):
        with api.env.adopt_roles(['Manager', 'Reviewer']):
            microsite = api.content.create(
                type='sc.microsite',
                id='microsite',
                container=self.portal
            )
            behavior = IPaginaDestaque(microsite)
            behavior.title_1 = u'Portal Brasil'
            behavior.title_2 = u'7 de Setembro'
            behavior.description = u'Pagina Destaque para 7 de Setembro'
            behavior.links = [
                {'title_1': u'Min.', 'title_2': u'dos Esportes', 'url': u'http://esportes.gov.br'},
                {'title_1': u'Min.', 'title_2': u'da Justiça', 'url': u'http://justiça.gov.br'},
            ]
            behavior = ISmartExpiration(microsite)
            behavior.expires = EXPIRES
            behavior.expires_url = api.portal.get().absolute_url()
        return microsite

    def setup_page(self, microsite):
        with api.env.adopt_roles(['Manager', 'Reviewer']):
            microsite.invokeFactory('Document', id='a-page')
            page = microsite['a-page']
        return page

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        directlyProvides(self.request, IBrowserLayer)
        self.portal.portal_workflow.setChainForPortalTypes(
            ['Document', 'sc.microsite', ],
            ['one_state_workflow'],
        )
        self.microsite = self.setup_microsite()
        transaction.commit()
        self.page = self.setup_page(self.microsite)
        transaction.commit()
        self.browser = Browser(self.layer['app'])
        transaction.commit()

    def test_plone_root_viewlets(self):
        browser = self.browser
        browser.open('{0}'.format(self.portal.absolute_url()))
        self.assertEqual(browser.headers['status'], '200 Ok')
        contents = browser.contents.decode('utf-8')
        # Viewlet padrao do logo
        self.assertIn(u'/logo.png"', contents)
        # Viewlet padrao de busca
        self.assertIn(u'input name="SearchableText"', contents)
        # Viewlet padrao de footer
        self.assertIn(u'<a href="http://plone.org/foundation">Plone Foundation</a>',
                      contents)

    def test_microsite_viewlets(self):
        browser = self.browser
        browser.open('{0}'.format(self.microsite.absolute_url()))
        self.assertEqual(browser.headers['status'], '200 Ok')
        contents = browser.contents.decode('utf-8')
        # Viewlet do logo
        self.assertIn(u'span id="portal-title-1"', contents)
        # Viewlet de busca
        self.assertNotIn(u'input name="SearchableText"', contents)
        # Viewlet de footer
        self.assertIn(u'class="footer_links"', contents)

    def test_microsite_expired_manager_access(self):
        microsite = self.microsite
        with api.env.adopt_roles(['Manager', ]):
            behavior = ISmartExpiration(microsite)
            behavior.expires = EXPIRED
            microsite.reindexObject()
            transaction.commit()
        browser = self.browser
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        browser.open('{0}'.format(microsite.absolute_url()))
        self.assertEqual(browser.headers['status'], '200 Ok')
        self.assertEqual(browser.url, microsite.absolute_url())

    def test_microsite_expired_anonymous_access(self):
        microsite = self.microsite
        with api.env.adopt_roles(['Manager', ]):
            behavior = ISmartExpiration(microsite)
            behavior.expires = EXPIRED
            microsite.reindexObject()
            transaction.commit()
        browser = self.browser
        browser.open('{0}'.format(microsite.absolute_url()))
        self.assertEqual(browser.headers['status'], '200 Ok')
        # Nao estamos dentro do microsite
        self.assertNotEqual(browser.url, microsite.absolute_url())
        # Voltamos para a raiz do portal
        self.assertEqual(browser.url, self.portal.absolute_url())

    def test_microsite_expired_sub_contents(self):
        microsite = self.microsite
        with api.env.adopt_roles(['Manager', ]):
            behavior = ISmartExpiration(microsite)
            behavior.expires = EXPIRED
            microsite.reindexObject()
            transaction.commit()
        browser = self.browser
        browser.open('{0}'.format(self.page.absolute_url()))
        self.assertEqual(browser.headers['status'], '200 Ok')
        # Nao vemos a pagina
        self.assertNotEqual(browser.url, self.page.absolute_url())
        # Voltamos para a raiz do portal
        self.assertEqual(browser.url, self.portal.absolute_url())

    def test_is_expired(self):
        # Passando DateTime de data no passado
        self.assertTrue(_is_expired(DateTime(2012, 2, 5, 12, 33, 1)))
        # Passando DateTime de data no futuro
        self.assertFalse(_is_expired(DateTime() + 100))
        # Passando datetime de data no passado
        self.assertTrue(_is_expired(datetime.datetime(2012, 2, 5, 12, 33, 1)))
        # Passando datetime de data no futuro
        self.assertFalse(_is_expired(
            datetime.datetime.today() + datetime.timedelta(100))
        )
        # Passando None
        self.assertFalse(_is_expired(None))

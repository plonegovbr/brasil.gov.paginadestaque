# -*- coding: utf-8 -*-

from brasil.gov.paginadestaque.behaviors.metadata import IPaginaDestaque
from brasil.gov.paginadestaque.interfaces import IBrowserLayer
from brasil.gov.paginadestaque.testing import FUNCTIONAL_TESTING

from plone import api
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.app.textfield import RichTextValue
from plone.testing.z2 import Browser
from zope.interface.declarations import directlyProvides


import transaction
import unittest


class AcessibilidadeTestCase(unittest.TestCase):

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
        return microsite

    def setup_acessibilidade(self):
        with api.env.adopt_roles(['Manager', 'Reviewer']):
            pasta = api.content.create(
                type='Folder',
                id='acessibilidade',
                title='Pasta de Acessibilidade',
                description='Acessibilidade no Portal',
                container=self.portal
            )
            acessibilidade = api.content.create(
                type='Document',
                id='acessibilidade',
                title='Documento de Acessibilidade',
                description='Acessibilidade no Brasil',
                container=pasta
            )
            acessibilidade.text = RichTextValue(u'Homenagem à @garotadpi')
        return acessibilidade

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        directlyProvides(self.request, IBrowserLayer)
        self.portal.portal_workflow.setChainForPortalTypes(
            ['Document', 'Folder', 'sc.microsite', ],
            ['one_state_workflow'],
        )
        self.microsite = self.setup_microsite()
        self.acessibilidade = self.setup_acessibilidade()
        self.browser = Browser(self.layer['app'])
        transaction.commit()

    def test_acessibilidade_document_by_line(self):
        browser = self.browser
        browser.open('{0}/acessibilidade'.format(self.microsite.absolute_url()))
        self.assertEqual(browser.headers['status'], '200 Ok')
        contents = browser.contents.decode('utf-8')
        # Nao presente em acessibilidade
        self.assertNotIn(u'class="documentByLine"', contents)

    def test_acessibilidade_title(self):
        browser = self.browser
        browser.open('{0}/acessibilidade'.format(self.microsite.absolute_url()))
        self.assertEqual(browser.headers['status'], '200 Ok')
        contents = browser.contents.decode('utf-8')
        # Titulo
        self.assertIn(u'Documento de Acessibilidade</h1>', contents)

    def test_acessibilidade_description(self):
        browser = self.browser
        browser.open('{0}/acessibilidade'.format(self.microsite.absolute_url()))
        self.assertEqual(browser.headers['status'], '200 Ok')
        contents = browser.contents.decode('utf-8')
        # Descricao
        self.assertIn(u'Acessibilidade no Brasil</div>', contents)

    def test_acessibilidade_text(self):
        browser = self.browser
        browser.open('{0}/acessibilidade'.format(self.microsite.absolute_url()))
        self.assertEqual(browser.headers['status'], '200 Ok')
        contents = browser.contents.decode('utf-8')
        # Texto esta presente
        self.assertIn(u'id="parent-fieldname-text"', contents)
        self.assertIn(u'@garotadpi</div>', contents)

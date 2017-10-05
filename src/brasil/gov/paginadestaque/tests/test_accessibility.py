# -*- coding: utf-8 -*-
from brasil.gov.paginadestaque.behaviors.metadata import IPaginaDestaque
from brasil.gov.paginadestaque.interfaces import IBrowserLayer
from brasil.gov.paginadestaque.testing import FUNCTIONAL_TESTING
from collective.behavior.localdiazo.behavior import ILocalDiazo
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.theming.interfaces import IThemeSettings
from plone.app.theming.utils import applyTheme
from plone.app.theming.utils import getTheme
from plone.registry.interfaces import IRegistry
from plone.testing.z2 import Browser
from zope.component import getUtility
from zope.interface.declarations import directlyProvides

import Globals
import transaction
import unittest


class AccessibilityTestCase(unittest.TestCase):

    layer = FUNCTIONAL_TESTING

    def setup_microsite(self):
        with api.env.adopt_roles(['Manager', 'Reviewer']):
            microsite = api.content.create(
                container=self.portal,
                type='sc.microsite',
                id='microsite',
            )
            behaviorDefault = IPaginaDestaque(microsite)
            behaviorDefault.title_1 = u'Portal Brasil'
            behaviorDefault.title_2 = u'7 de Setembro'
            behaviorDefault.description = u'Página Destaque para 7 de Setembro'

            behaviorLocalDiazo = ILocalDiazo(microsite)
            behaviorLocalDiazo.theme = '/++theme++destaques-cinza/rules.xml'
        return microsite

    def setUp(self):
        Globals.DevelopmentMode = True
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        directlyProvides(self.request, IBrowserLayer)
        self.portal.portal_workflow.setChainForPortalTypes(
            ['Document', 'Folder', 'sc.microsite'], ['one_state_workflow'])
        self.microsite = self.setup_microsite()
        self.settings = getUtility(IRegistry).forInterface(IThemeSettings)
        self.browser = Browser(self.layer['app'])
        transaction.commit()

    def test_portal_logo(self):
        theme = getTheme('destaques-cinza')
        applyTheme(theme)
        self.settings.enabled = True
        transaction.commit()

        browser = self.browser
        browser.open(self.microsite.absolute_url())
        self.assertEqual(browser.headers['status'], '200 Ok')
        contents = browser.contents.decode('utf-8')

        # Testa se title_1 aparece no portal_logo.
        self.assertIn(
            '<span id="portal-title-1">Portal Brasil</span>', contents)

        # Testa se title_2 aparece no portal_logo.
        self.assertIn(
            '<div id="portal-title" class="corto">7 de Setembro</div>',
            contents,
        )

    def test_links_acessibilidade(self):
        theme = getTheme('destaques-cinza')
        applyTheme(theme)
        self.settings.enabled = True
        transaction.commit()

        browser = self.browser
        browser.open(self.microsite.absolute_url())
        self.assertEqual(browser.headers['status'], '200 Ok')
        contents = browser.contents.decode('utf-8')

        # Testa se a âncora para o conteúdo aparece.
        self.assertIn(
            '<a name="acontent" id="acontent" class="anchor">',
            contents,
        )

        # Testa se a âncora para o menu aparece.
        self.assertIn(
            '<a name="anavigation" id="anavigation" class="anchor">',
            contents,
        )

        # Testa se a âncora para o rodapé aparece.
        self.assertIn(
            '<a name="afooter" id="afooter" class="anchor">',
            contents,
        )

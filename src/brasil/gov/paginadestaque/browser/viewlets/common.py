# -*- coding: utf-8 -*-
""" Modulo que implementa viewlets basicos para Pagina Destaque"""
from plone.app.layout.viewlets.common import GlobalSectionsViewlet as GlobalNavBase
from plone.app.layout.viewlets.common import SiteActionsViewlet as SiteActionsBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

ACCESSKEYS = {
    'accessibility': '5',
    'contraste': '6',
    'mapadosite': '7',
}


class GlobalSectionsViewlet(GlobalNavBase):
    """Viewlet que implementa o global nav bar para a Pagina Destaque
    """

    def update(self):
        super(GlobalSectionsViewlet, self).update()
        tabs = self.portal_tabs
        # A primeira tab deve ser a da pagina inicial, que deve ser removida
        if tabs and tabs[0].get('id', '') == 'index_html':
            tabs.pop(0)
        self.portal_tabs = tabs


class SiteActionsViewlet(SiteActionsBase):
    """Viewlet que implementa o site_actions para a Pagina Destaque
    """

    index = ViewPageTemplateFile('templates/site_actions.pt')

    def update(self):
        super(SiteActionsViewlet, self).update()
        base_site_actions = self.site_actions
        site_actions = []
        for action in base_site_actions:
            action_id = action.get('id', '')
            action['accesskey'] = ACCESSKEYS.get(action_id, '')
            if action_id == 'mapadosite':
                continue
            site_actions.append(action)
        self.site_actions = site_actions

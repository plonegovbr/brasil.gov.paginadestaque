# -*- coding: utf-8 -*-

""" Modulo que implementa o viewlet de rodape da Pagina Destaque"""

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api
from plone.app.layout.viewlets.common import ViewletBase


class FooterViewlet(ViewletBase):
    """Viewlet que implementa o rodape da Pagina Destaque
    """
    # Indica qual o template sera usado por este viewlet
    index = ViewPageTemplateFile('templates/footer.pt')

    def root(self):
        root = api.portal.get_navigation_root(self.context)
        return root

    def links(self):
        """Retorna a lista de links para o rodape
           para este destaque
        """
        root = self.root()
        return getattr(root, 'links', [])

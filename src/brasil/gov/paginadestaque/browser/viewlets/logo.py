# -*- coding: utf-8 -*-

""" Modulo que implementa o viewlet de logo da Pagina Destaque"""

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api
from plone.app.layout.viewlets.common import LogoViewlet as ViewletBase


class LogoViewlet(ViewletBase):
    """Viewlet que implementa o logo da Pagina Destaque
    """
    # Indica qual o template sera usado por este viewlet
    index = ViewPageTemplateFile('templates/logo.pt')

    def root(self):
        root = api.portal.get_navigation_root(self.context)
        return root

    def title_1(self):
        """Retorna a primeira linha do titulo da Pagina Destaque
        """
        root = self.root()
        return getattr(root, 'title_1', 'Portal Brasil')

    def title_2(self):
        """Retorna a primeira linha do titulo da Pagina Destaque
        """
        root = self.root()
        return getattr(root, 'title_2', u'7 de Setembro')

    def title_2_class(self):
        """Definimos a classe a ser aplicada ao title_2
           com base no tamanho da string
        """
        title_2 = self.title_2()
        return 'luongo' if len(title_2) > 22 else 'corto'

    def description(self):
        """Retorna uma breve descricao da Pagina Destaque
        """
        root = self.root()
        return getattr(root, 'description', '')

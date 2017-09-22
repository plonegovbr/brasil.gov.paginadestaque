# -*- coding: utf-8 -*-
from plone import api
from plone.memoize import view
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class AcessibilidadeView(BrowserView):
    """Adiciona uma view chamada acessibilidade a raiz de um microsite."""

    index = ViewPageTemplateFile('templates/acessibilidade.pt')

    def __call__(self):
        return self.index()

    @view.memoize
    def content(self):
        """ Em um portal padrao temos o conteudo com id acessibilidade
            criado por padrao.
        """
        o_id = 'acessibilidade'
        portal = api.portal.get()
        content = None
        if o_id in portal.objectIds():
            content = portal[o_id]
            if content.portal_type == 'Folder' and o_id in content.objectIds():
                content = content[o_id]
        return content

    @property
    def title(self):
        """Retorna o titulo da pagina de acessibilidade.
        """
        content = self.content()
        return content.Title() if content else u'Acessibilidade'

    @property
    def description(self):
        """Retorna a descricao da pagina de acessibilidade.
        """
        content = self.content()
        return content.Description() if content else u''

    @property
    def text(self):
        """Retorna o corpo da pagina de acessibilidade.
        """
        content = self.content()
        text = None
        if content.portal_type == 'Document':
            text = content.text
        return text

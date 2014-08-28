# -*- coding: utf-8 -*-
""" Modulo que implementa o viewlet de document byline para Pagina Destaque"""
from Acquisition import aq_base
from plone.app.layout.viewlets.content import DocumentBylineViewlet as ViewletBase
from sc.microsite.interfaces import IMicrosite


class DocumentBylineViewlet(ViewletBase):
    """Viewlet que sobreescreve o document by license
       para oculta-lo na raiz do microsite
    """

    def show(self):
        context = aq_base(self.context)
        if IMicrosite.providedBy(context):
            return False
        return super(DocumentBylineViewlet, self).show()

# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from brasil.gov.paginadestaque.behaviors.interfaces import IBackgroundImage
from brasil.gov.paginadestaque.interfaces import IBrowserLayer
from collective.cover.browser.cover import View as CoverBaseView
from collective.cover.interfaces import ICover
from five import grok
from plone.memoize import view

grok.templatedir('templates')


class CoverOverridesView(CoverBaseView):

    """Overrides collective.cover default view."""

    grok.context(ICover)
    grok.layer(IBrowserLayer)
    grok.name('view')
    grok.require('zope2.View')
    grok.template('cover_overrides_view')

    @view.memoize
    def background(self):
        """Return the style to be used on the item, if the IBackgroundImage
        behavior is enabled and a background image has been set.
        """
        context = aq_inner(self.context)
        background = IBackgroundImage(context, None)
        if background is not None and background.background_image is not None:
            return '#content {background: url("@@images/background_image") no-repeat}'

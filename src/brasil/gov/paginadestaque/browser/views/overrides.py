# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from brasil.gov.paginadestaque.behaviors.interfaces import IBackgroundImage
from collective.cover.browser.cover import View as CoverBaseView
from plone.memoize import view
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class CoverOverridesView(CoverBaseView):
    """Overrides collective.cover default view."""

    index = ViewPageTemplateFile('templates/cover_overrides_view.pt')

    @view.memoize
    def background(self):
        """Return the style to be used on the item, if the IBackgroundImage
        behavior is enabled and a background image has been set.
        """
        context = aq_inner(self.context)
        background = IBackgroundImage(context, None)
        if background is not None and background.background_image is not None:
            return '#content {background: url("@@images/background_image") no-repeat}'

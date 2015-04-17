# -*- coding: utf-8 -*-

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from brasil.gov.paginadestaque import _

from collective.cover.tiles.base import IPersistentCoverTile
from collective.cover.tiles.base import PersistentCoverTile

from zope import schema
from zope.interface import implements


class ISpacerTile(IPersistentCoverTile):

    """Tile to leave some free space to unveil the background image."""

    height = schema.Int(
        title=_(u'Height'),
        description=_(u'Height of the tile, in pixels.'),
        required=True,
        default=400,
    )

    title = schema.Text(
        title=_(u'Title'),
        description=_(
            u'Text used to describe the background image. '
            u'For accessibility reasons, you should not use background images as the sole method of conveying important information.'
        ),
        required=False,
    )


class SpacerTile(PersistentCoverTile):

    """Tile to leave some free space to unveil the background image."""

    implements(ISpacerTile)

    index = ViewPageTemplateFile('spacer.pt')
    is_configurable = False
    is_editable = True
    is_droppable = False
    short_name = _(u'msg_short_name_file', default=u'Spacer')

    @property
    def height(self):
        return self.data['height']

    @property
    def Title(self):
        return self.data['title']

    def accepted_ct(self):
        return []

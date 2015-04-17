# -*- coding: utf-8 -*-

from Acquisition import aq_base

from brasil.gov.paginadestaque import _

from collective.z3cform.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield import DictRow
from plone.app.dexterity.behaviors.metadata import MetadataBase
from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from z3c.form.interfaces import IAddForm
from z3c.form.interfaces import IEditForm
from zope import schema
from zope.interface import Interface
from zope.interface import alsoProvides


class ILinkRow(Interface):
    title_1 = schema.TextLine(title=_(u'Title 1'), required=False)
    title_2 = schema.TextLine(title=_(u'Title 2'), required=False)
    url = schema.TextLine(title=_(u'URL'), required=False)


class IPaginaDestaque(model.Schema):
    """Behavior adding a two-line title, a description and a links field
    """

    title_1 = schema.TextLine(
        title=_(u'label_title_1', default=u'Title 1'),
        required=True
    )

    title_2 = schema.TextLine(
        title=_(u'label_title_2', default=u'Title 2'),
        required=True
    )

    description = schema.Text(
        title=_(u'label_description', default=u'Summary'),
        description=_(
            u'help_description',
            default=u'Used in item listings and search results.'
        ),
        required=False,
        missing_value=u'',
    )

    form.widget(links=DataGridFieldFactory)
    links = schema.List(
        title=_(u'Footer links'),
        value_type=DictRow(title=_(u'Link'), schema=ILinkRow),
        required=False,
    )

    form.order_before(links='*')
    form.order_before(description='*')
    form.order_before(title_2='*')
    form.order_before(title_1='*')

    form.omitted('title_1', 'title_2', 'description', 'links')
    form.no_omit(IEditForm, 'title_1', 'title_2', 'description', 'links')
    form.no_omit(IAddForm, 'title_1', 'title_2', 'description', 'links')


class PaginaDestaque(MetadataBase):
    """Behavior adding a two-line title, a description and a links field
    """

    def _set_title(self):
        context = aq_base(self.context)
        title_1 = getattr(context, 'title_1', u'')
        title_2 = getattr(context, 'title_2', u'')
        title = u'{0} {1}'.format(title_1, title_2)
        self.context.title = title

    def _get_title_1(self):
        title_1 = self.context.title_1
        return title_1

    def _set_title_1(self, value):
        if isinstance(value, str):
            raise ValueError('Title must be unicode.')
        self.context.title_1 = value
        self._set_title()
    title_1 = property(_get_title_1, _set_title_1)

    def _get_title_2(self):
        title_2 = self.context.title_2
        return title_2

    def _set_title_2(self, value):
        if isinstance(value, str):
            raise ValueError('Title must be unicode.')
        self.context.title_2 = value
        self._set_title()
    title_2 = property(_get_title_2, _set_title_2)

    def _get_description(self):
        return self.context.description

    def _set_description(self, value):
        if isinstance(value, str):
            raise ValueError('Description must be unicode.')
        self.context.description = value
    description = property(_get_description, _set_description)

    def _get_links(self):
        links = getattr(self.context, 'links', [])
        return links

    def _set_links(self, value):
        links = []
        for item in value:
            item['title'] = u'{0} {1}'.format(
                item.get('title_1', u''),
                item.get('title_2', u''),
            )
            links.append(item)
        self.context.links = links
    links = property(_get_links, _set_links)

alsoProvides(IPaginaDestaque, IFormFieldProvider)

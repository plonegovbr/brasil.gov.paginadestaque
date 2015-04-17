# -*- coding: utf-8 -*-

from brasil.gov.paginadestaque import _

from datetime import datetime
from datetime import timedelta

from plone.app.dexterity.behaviors.metadata import DCFieldProperty
from plone.app.dexterity.behaviors.metadata import MetadataBase
from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from z3c.form.interfaces import IAddForm
from z3c.form.interfaces import IEditForm
from zope import schema
from zope.interface import Invalid
from zope.interface import alsoProvides
from zope.interface import provider
from zope.schema.interfaces import IContextAwareDefaultFactory

import re


valid_protocols = ('http', )


@provider(IContextAwareDefaultFactory)
def default_expires(context):
    """Retornamos sessenta dias no futuro
    """
    return datetime.today() + timedelta(60)


def validate_url(value):
    """Checagem simples se o valor informado representa um site"""
    if not value:
        return True
    regex = re.compile(r'(%s)s?://[^\s\r\n]+' % '|'.join(valid_protocols))
    if not regex.match(value):
        raise Invalid(_(u'Invalid URL.'))
    return True


class ISmartExpiration(model.Schema):
    """Behavior providing an expiration date and an expiration url
    """
    expires = schema.Datetime(
        title=_(u'label_expiration_date', u'Expiration Date'),
        defaultFactory=default_expires,
        description=_(
            u'help_expiration_date',
            default=u'When this date is reached, the content will no '
                    u'longer be visible in listings and searches.'),
        required=False
    )

    expires_redirect = schema.TextLine(
        title=_(u'label_expires_redirect', default=u'Redirect to'),
        description=_(
            u'help_expires_redirect',
            default=u'After expiration, requests will be redirected '
                    u'to the url filled in here.'),
        constraint=validate_url,
        required=False
    )

    form.omitted('expires', 'expires_redirect')
    form.no_omit(IEditForm, 'expires', 'expires_redirect')
    form.no_omit(IAddForm, 'expires', 'expires_redirect')


class SmartExpiration(MetadataBase):
    """Behavior providing an expiration date and an expiration url
    """
    expires = DCFieldProperty(
        ISmartExpiration['expires'],
        get_name='expiration_date'
    )

    def _get_expires_redirect(self):
        return self.context.expires_redirect

    def _set_expires_redirect(self, value):
        self.context.expires_redirect = value
    expires_redirect = property(_get_expires_redirect, _set_expires_redirect)


alsoProvides(ISmartExpiration, IFormFieldProvider)

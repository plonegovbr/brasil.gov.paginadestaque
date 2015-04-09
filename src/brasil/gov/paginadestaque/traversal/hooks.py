# -*- coding: utf-8 -*-

from AccessControl import getSecurityManager
from DateTime import DateTime
from Products.CMFCore.permissions import ModifyPortalContent
from ZPublisher.interfaces import IPubBeforeCommit

from brasil.gov.paginadestaque.behaviors.expiration import ISmartExpiration
from brasil.gov.paginadestaque.interfaces import IPaginaDestaque

from plone import api
from zExceptions import Redirect
from zope.component import adapter
from zope.interface import directlyProvidedBy
from zope.interface import directlyProvides

import datetime


def _is_expired(expiration_date):
    """Podemos receber um valor datetime, um valor DateTime
       ou None.
    """
    if isinstance(expiration_date, datetime.datetime):
        today = datetime.datetime.today()
        return expiration_date < today
    elif isinstance(expiration_date, DateTime):
        return expiration_date.isPast()
    else:
        return False


def process_microsite(object, event):
    """Interceptamos a requisicao antes do traversal ser feito em um
       microsite. Desabilitamos a coluna da esquerda e armazenamos
       o microsite no request
    """
    request = event.request

    # Disable columns
    request.set('disable_plone.leftcolumn', 1)
    # request.set('disable_plone.rightcolumn', 1)

    # Put microsite on request
    # so we can use it on our IPubBeforeCommit subscriber

    if 'microsite' not in request:
        request.set('microsite', object)
        # Also add our marker interface to the top of the list
        ifaces = [IPaginaDestaque, ] + list(directlyProvidedBy(request))
        directlyProvides(request, *ifaces)


@adapter(IPubBeforeCommit)
def microsite_expiration_enforcer(event):
    """Validamos se estamos dentro de um microsite e se ele esta
       expirado. Se estiver, validamos se o usuario pode editar o
       microsite, se nao puder redirecionamos para a url definida
       em expires_redirect
    """
    request = event.request
    object = request.get('microsite', None)

    if not IPaginaDestaque.providedBy(request):
        return

    behavior = ISmartExpiration(object, None)
    if behavior:
        expired = behavior.expires and _is_expired(behavior.expires)
        sm = getSecurityManager()
        if expired and not sm.checkPermission(ModifyPortalContent, object):
            portal = api.portal.get()
            expires_redirect = getattr(object, 'expires_redirect', '').strip()
            expires_redirect = (expires_redirect if expires_redirect
                                else portal.absolute_url())
            raise Redirect(expires_redirect)

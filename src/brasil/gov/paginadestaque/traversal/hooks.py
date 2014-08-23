# -*- coding: utf-8 -*-
from AccessControl import getSecurityManager
from brasil.gov.paginadestaque.behaviors.expiration import ISmartExpiration
from brasil.gov.paginadestaque.interfaces import IBrowserLayer
from brasil.gov.paginadestaque.interfaces import IPaginaDestaque
from DateTime import DateTime
from plone import api
from Products.CMFCore.permissions import ModifyPortalContent
from sc.microsite.interfaces import IMicrosite
from zExceptions import Redirect
from zope.component import adapter
from zope.interface import directlyProvidedBy
from zope.interface import directlyProvides
from ZPublisher.interfaces import IPubBeforeCommit

import datetime


def _is_request_for_microsite(object, request):
    return (IBrowserLayer.providedBy(request) and IMicrosite.providedBy(object))


def process_microsite(object, event):
    """Interceptamos a requisicao antes do traversal ser feito em um
       microsite. Desabilitamos a coluna da esquerda e armazenamos
       o microsite no request
    """
    request = event.request

    # Must have our package installed
    if not _is_request_for_microsite(object, request):
        return

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

    expires = getattr(object, 'expires', None)
    if expires and expires().isPast():
        sm = getSecurityManager()
        if not sm.checkPermission(ModifyPortalContent, object):
            portal = api.portal.get()
            expires_redirect = getattr(object, 'expires_redirect', portal.absolute_url())
            raise Redirect(expires_redirect)

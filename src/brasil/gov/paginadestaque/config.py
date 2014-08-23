# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implements

PROJECTNAME = 'brasil.gov.paginadestaque'


class HiddenProfiles(object):
    implements(INonInstallable)

    def getNonInstallableProfiles(self):
        return [
            u'brasil.gov.paginadestaque:uninstall',
            u'sc.microsite:default',
            u'sc.microsite:uninstall',
        ]

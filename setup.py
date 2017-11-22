# -*- coding:utf-8 -*-

from setuptools import find_packages
from setuptools import setup

version = '1.3.dev0'
description = 'Complemento ao Portal Padrao para criacao de microsites e campanhas'
long_description = (
    open('README.rst').read() + '\n' +
    open('CONTRIBUTORS.rst').read() + '\n' +
    open('CHANGES.rst').read()
)

setup(
    name='brasil.gov.paginadestaque',
    version=version,
    description=description,
    long_description=long_description,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Plone',
        'Framework :: Plone :: 4.3',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='plone microsite destaque brasil egov',
    author='PloneGov.Br',
    author_email='gov@plone.org.br',
    url='https://github.com/plonegovbr/brasil.gov.paginadestaque',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['brasil', 'brasil.gov'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'AccessControl',
        'collective.behavior.localdiazo',
        'collective.behavior.localregistry',
        'collective.cover',
        'collective.z3cform.datagridfield >=1.3',  # avoid dependency on five.grok
        'plone.api',
        'plone.app.content',
        'plone.app.dexterity',
        'plone.app.tiles',
        'plone.app.layout',
        'plone.app.upgrade',
        'plone.autoform',
        'plone.behavior',
        'plone.dexterity',
        'plone.memoize',
        'plone.namedfile',
        'plone.resource',
        'plone.supermodel',
        'Products.CMFPlone >=4.3',
        'Products.GenericSetup',
        'sc.microsite >=1.0b4',
        'setuptools',
        'z3c.form',
        'zope.component',
        'zope.i18nmessageid',
        'zope.interface',
        'zope.schema',
    ],
    extras_require={
        'test': [
            'mock',
            'plone.app.robotframework',
            'plone.app.theming',
            'plone.app.testing [robot]',
            'plone.browserlayer',
            'plone.registry',
            'plone.testing',
            'plone.tiles',
            'robotsuite',
            'transaction',
        ],
    },
    entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
)

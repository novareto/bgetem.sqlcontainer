# -*- coding: utf-8 -*-

from five import grok
from zope.interface import implementer, Interface
from zope.publisher.interfaces.browser import IBrowserView
from zope.traversing.interfaces import TraversalError
from zope.traversing.namespace import SimpleHandler
from zope.traversing.interfaces import ITraversable
from .container import Users, SQLContainer
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import queryMultiAdapter, queryUtility
from Acquisition import ImplicitAcquisitionWrapper
from Products.CMFPlone.interfaces.constrains import IConstrainTypes


class UsersConstraints(grok.Adapter):
    grok.context(Users)
    grok.provides(IConstrainTypes)
    
    def getConstrainTypesMode(self):
        return 0

    def getLocallyAllowedTypes(self):
        return ['test_users',]

    def getImmediatelyAddableTypes(self):
        return ['test_users',]

    def getDefaultAddableTypes(self):
        return ['test_users',]

    def allowedContentTypes(self):
        return ['test_users',]



@implementer(IBrowserView)
class users(SimpleHandler, grok.MultiAdapter):
    grok.name('users')
    grok.adapts(Interface, Interface)
    grok.provides(ITraversable)

    def __init__(self, context, request):
        self.context = context
        self.request = request
        
    def traverse(self, name, ignored):
        users = Users(self.context, '++users++', 'sqlsession')
        users.__of__(self.context)
        if not name:
            return users
        else:
            try:
                return users[name]
            except KeyError:
                raise TraversalError(self.context, name)


@implementer(IBrowserView)
class AddViewTraverser(SimpleHandler, grok.MultiAdapter):
    grok.name('add')
    grok.adapts(SQLContainer, Interface)
    grok.provides(ITraversable)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def traverse(self, name, ignored):
        ti = queryUtility(IDexterityFTI, name=name)

        if ti is not None:
            
            add_view = queryMultiAdapter(
                (self.context, self.request, ti), name=name)

            if add_view is None:
                add_view = queryMultiAdapter((self.context, self.request, ti))
                
            if add_view is not None:
                add_view.__name__ = name
                view = ImplicitAcquisitionWrapper(add_view, self.context)
                import pdb
                pdb.set_trace()
                return view
            
        raise TraversalError(self.context, name)

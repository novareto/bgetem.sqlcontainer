# -*- coding: utf-8 -*-

from .container import SQLContainer
from Acquisition import ImplicitAcquisitionWrapper
from Products.CMFPlone.interfaces.constrains import IConstrainTypes
from five import grok
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import queryMultiAdapter, queryUtility
from zope.interface import implementer, Interface
from zope.publisher.interfaces.browser import IBrowserView
from zope.traversing.interfaces import ITraversable
from zope.traversing.interfaces import TraversalError
from zope.traversing.namespace import SimpleHandler


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
                return view
            
        raise TraversalError(self.context, name)

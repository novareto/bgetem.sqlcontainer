# -*- coding: utf-8 -*-

from Acquisition import Implicit
from OFS.interfaces import ITraversable
from Products.CMFCore.interfaces import ISiteRoot
from plone.dexterity.interfaces import IDexterityContent
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from zope.globalrequest import getRequest
from zope.interface import implementer, Attribute
from zope.location import locate, Location


class IModel(IDexterityContent, ITraversable):
    __schema__ = Attribute('Schema interface')


class IWrapper(IModel):
    content = Attribute('Content object being wrapped')

    
@implementer(IModel)
class PloneContent(Implicit, Location):

    portal_type = None
    
    def getPhysicalPath(self):
        return self.__parent__.getPhysicalPath() + (self.__name__,)

    def absolute_url(self, relative=0):
        if relative:
            return self.virtual_url_path()
        return getRequest().physicalPathToURL(self.getPhysicalPath())

    def virtual_url_path(self):
        return getRequest().physicalPathToVirtualPath(self.getPhysicalPath())

    def __contains__(self, id):
        return False


@implementer(IWrapper)
class PloneSQLModel(PloneContent):

    @property
    def portal_type(self):
        return self.content.portal_type
    
    def __init__(self, content, container=None, name=None):
        self.content = content
        self.__name__ = name
        self.__parent__ = container

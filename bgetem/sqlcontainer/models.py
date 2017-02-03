# -*- coding: utf-8 -*-

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation
from OFS.interfaces import ITraversable
from zope.interface import implementer, Interface, Attribute
from zope.globalrequest import getRequest
from zope.location import locate, Location
from Products.CMFCore.interfaces import ISiteRoot
from plone.dexterity.interfaces import IDexterityContent
from zope.schema import TextLine


Base = declarative_base()


class IModel(IDexterityContent, ITraversable):

    __schema__ = Attribute('Schema interface')



@implementer(IModel)
class PloneModel(Location):

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

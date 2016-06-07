# -*- coding: utf-8 -*-

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation
from OFS.interfaces import ITraversable
from zope.interface import implementer, Interface
from zope.globalrequest import getRequest
from zope.location import locate, Location
from Products.CMFCore.interfaces import ISiteRoot
from plone.dexterity.interfaces import IDexterityContent
from zope.schema import TextLine

Base = declarative_base()


class IUser(Interface):

    name = TextLine(
        title=u"Name",
        required=True)


@implementer(IDexterityContent, ITraversable)
class PloneModel(Location):

     def getPhysicalPath(self):
          stack = []
          current = self
          while current is not None and not ISiteRoot.providedBy(current):
               stack.append(getattr(current, '__name__', ''))
               current = getattr(current, '__parent__', None)
               stack.reverse()
          return tuple(list(self.__parent__.getPhysicalPath()) + stack)

     def absolute_url(self, relative=0):
          if relative:
               return self.virtual_url_path()
          return getRequest().physicalPathToURL(self.getPhysicalPath())

     def virtual_url_path(self):
          return getRequest().physicalPathToVirtualPath(self.getPhysicalPath())


@implementer(IUser)
class User(PloneModel, Base):
     portal_type = __tablename__ = 'test_users'

     id = Column('id', Integer, primary_key=True)
     name = Column('name', String(50))
     addresses = relation("Address", backref="user")

     def getId(self):
          return self.name


class Address(PloneModel, Base):
     portal_type = __tablename__ = 'test_addresses'

     id = Column('id', Integer, primary_key=True)
     email = Column('email', String(50))
     user_id = Column('user_id', Integer, ForeignKey('test_users.id'))

     def getId(self):
          return self.email

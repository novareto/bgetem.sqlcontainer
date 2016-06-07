# -*- coding: utf-8 -*-

import Acquisition
from OFS.Traversable import Traversable
from Acquisition import ImplicitAcquisitionWrapper
from zope.container.interfaces import IContainer
from zope.location import ILocation, Location, LocationProxy, locate
from zope.interface import implementer
from z3c.saconfig import named_scoped_session
from .models import PloneModel, User
from OFS.SimpleItem import SimpleItem
from zope.location import locate
from zope.publisher.interfaces import IPublishTraverse
from Products.CMFCore.interfaces import IFolderish


@implementer(IPublishTraverse, IContainer, IFolderish)
class SQLContainer(Acquisition.Implicit, PloneModel, Location):

    model = None

    def __init__(self, parent, name, db_key):
        self.__parent__ = parent
        self.__name__ = name
        self.db_key = db_key

    def key_reverse(self, obj):
        return str(obj.id)

    def key_converter(self, id):
        return id

    @property
    def session(self):
        return named_scoped_session(self.db_key)

    def locate(self, item):        
        proxy = ILocation(item, None)
        if proxy is None:
            proxy = LocationProxy(item)
        locate(proxy, self, self.key_reverse(item))
        proxy = ImplicitAcquisitionWrapper(proxy, self)
        return proxy

    def __getitem__(self, id):
        try:
            key = self.key_converter(id)
        except ValueError:
            return None
        model = self.query_filters(self.session.query(self.model)).get(key)
        if model is None:
            raise KeyError(key)
        return self.locate(model)

    def query_filters(self, query):
        return query

    def __iter__(self):
        models = self.query_filters(self.session.query(self.model)).all()
        for model in models:
            yield self.locate(model)

    def add(self, item):
        try:
            self.session.add(item)
        except Exception, e:
            # This might be a bit too generic
            return e

    def delete(self, item):
        self.session.delete(item)

    def __delitem__(self, key):
        item = self.__getitem__(key)
        return self.delete(item)

    def getId(self):
        return self.title

    def publishTraverse(self, request, name):
        return self[name]


class Users(SQLContainer):
    model = User
    title = u"Users"
    
    def key_converter(self, id):
        return int(id)

    def allowedContentTypes(self):
        return ['test_users']

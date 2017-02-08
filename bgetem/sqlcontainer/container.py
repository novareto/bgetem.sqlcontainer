# -*- coding: utf-8 -*-

from .models import PloneContent, PloneSQLModel
from Acquisition import IAcquirer
from Products.CMFCore.interfaces import IFolderish
from Products.CMFPlone.interfaces.constrains import IConstrainTypes
from z3c.saconfig import named_scoped_session
from zope.container.interfaces import IContainer
from zope.interface import implementer
from zope.location import LocationProxy
from zope.publisher.interfaces import IPublishTraverse


@implementer(IPublishTraverse, IContainer, IFolderish, IConstrainTypes)
class SQLContainer(PloneContent):

    model = None
    wrapper = LocationProxy

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
        key = self.key_reverse(item)
        if self.wrapper is not None:
            proxy = self.wrapper(item, name=key, container=self)
            if IAcquirer.providedBy(proxy):
                return proxy.__of__(self)
            return proxy
        return item

    def __getitem__(self, id):
        try:
            key = self.key_converter(id)
        except ValueError:
            return None
        model = self.query_filters(self.session.query(self.model)).get(key)
        if model is None:
            raise KeyError(key)
        return self.locate(model)

    def __contains__(self, id):
        return self.__getitem__(id) is not None

    def query_filters(self, query):
        return query

    def __iter__(self):
        models = self.query_filters(self.session.query(self.model)).all()
        for model in models:
            yield self.locate(model)

    def add(self, item):
        try:
            if isinstance(item, PloneSQLModel):
                item = item.content
            self.session.add(item)
        except Exception, e:
            # This might be a bit too generic
            return e

    def delete(self, item):
        if isinstance(item, PloneSQLModel):
            item = item.content
        self.session.delete(item)

    def __delitem__(self, key):
        item = self.__getitem__(key)
        if isinstance(item, PloneSQLModel):
            item = item.content
        return self.delete(item)

    def getId(self):
        return self.title

    def publishTraverse(self, request, name):
        return self[name]

    # IConstrainTypes
    def getConstrainTypesMode(self):
        return 0

    # IConstrainTypes
    def getLocallyAllowedTypes(self):
        return [self.model.portal_type,]

    # IConstrainTypes
    def getImmediatelyAddableTypes(self):
        return [self.model.portal_type,]

    # IConstrainTypes
    def getDefaultAddableTypes(self):
        return [self.model.portal_type,]

    # IConstrainTypes
    def allowedContentTypes(self):
        return [self.model.portal_type,]

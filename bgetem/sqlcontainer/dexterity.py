# -*- coding: utf-8 -*-

from .menus import Action
from .models import IModel
from Acquisition import Implicit, ImplicitAcquisitionWrapper
from .container import SQLContainer

from Acquisition import aq_base, aq_inner, aq_acquire
from five import grok
from plone.app.dexterity.interfaces import ITypeSettings, ITypeStats
from plone.dexterity.browser import add, edit
from plone.dexterity.interfaces import IDexterityContent
from plone.dexterity.interfaces import IDexterityFTI
from zope.interface import implementer, Interface
from zope.publisher.interfaces.browser import IBrowserPage
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

"""
ACTION EXAMPLE :
from Products.CMFCore.interfaces import IActionInfo

@grok.subscribe(CONTENTTYPE)
@implementer(IActionInfo)
def edit(context):
    return Action(
        context, id='edit', title='Edit', url='{object_url}/edit',
        category='object', visible=True, available=True,
        permissions=['zope2.View'])
"""

# Base class for the add form
# Give it the content type name
class AddForm(add.DefaultAddForm, grok.MultiAdapter):
    grok.baseclass()
    grok.adapts(SQLContainer, IDefaultBrowserLayer, IDexterityFTI)
    grok.provides(IBrowserPage)

    index_html = None
    
    def __init__(self, *args, **kwargs):
        super(AddForm, self).__init__(*args, **kwargs)
        self.portal_type = grok.name.bind().get(self)

    def create(self, data):
        container = aq_inner(self.context)
        content = self.ti.factory(**data)
        content.__parent__ = container
        content = ImplicitAcquisitionWrapper(content, container)
        return content

    def add(self, object):
        fti = self.ti
        container = aq_inner(self.context)
        container.add(object)
        self.immediate_view = None

    
class AddView(Implicit, add.DefaultAddView, grok.MultiAdapter):
    form = AddForm
    grok.name('')
    grok.adapts(IModel, IDefaultBrowserLayer, IDexterityFTI)
    grok.provides(IBrowserPage)


    
# Base class for the FTI.
# Give it the content type name
@implementer(IDexterityFTI, ITypeSettings, ITypeStats)
class ContentFTI(grok.GlobalUtility):
    """The Factory Type Information for Dexterity content objects
    """
    grok.baseclass()
    grok.provides(IDexterityFTI)

    __model__ = None
    schema = None
    klass = None

    @classmethod
    def Title(cls):
        return grok.title.bind().get(cls.__model__)

    @classmethod
    def Description(cls):
        return grok.description.bind().get(cls.__model__)
    
    @classmethod
    def lookupSchema(cls):
        return cls.schema

    @classmethod
    def lookupModel(cls):
        return cls.__model__

    @classmethod
    def getId(cls):
        return grok.name.bind().get(cls)

    @property
    def factory(self):
        return self.lookupModel()
    
    @property
    def __name__(self):
        return self.getId()
    
    @property
    def title(self):
        return self.Title()

    @property
    def id(self):
        return self.getId()

    @property
    def count(self):
        return 0

    def isConstructionAllowed(self, container):
        return True

    @classmethod
    def getIconExprObject(cls):
        return None

    add_permission = 'zope.View'
    allowed_content_types = set()
    behaviors = list()
    container = False
    filter_content_types = 'none'
    hasDynamicSchema = False
    model_file = None
    model_source = None

    # trick
    _p_mtime = None

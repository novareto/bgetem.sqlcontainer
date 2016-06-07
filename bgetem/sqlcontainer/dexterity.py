# -*- coding: utf-8 -*-

from .models import User, IUser
from .container import Users
from five import grok
from plone.dexterity.interfaces import IDexterityFTI
from plone.dexterity.browser import add
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.publisher.interfaces.browser import IBrowserPage


class UserFTI(grok.GlobalUtility):
    """The Factory Type Information for Dexterity content objects
    """
    grok.name('test_users')
    grok.provides(IDexterityFTI)

    def Title(self):
        return u'User'
    
    def lookupSchema(self):
        return IUser

    def lookupModel(self):
        return User

    def getId(self):
        return 'test_users'
    
    add_permission = 'zope.View'
    behaviors = list()
    schema = IUser
    model_source = None
    model_file = None
    hasDynamicSchema = False
    
    # trick
    _p_mtime = None


class AddForm(add.DefaultAddForm, grok.MultiAdapter):
    portal_type = 'test_users'

    grok.name('test_users')
    grok.adapts(Users, IDefaultBrowserLayer, UserFTI)
    grok.provides(IBrowserPage)


class AddView(add.DefaultAddView, grok.MultiAdapter):
    form = AddForm
    grok.name('')
    grok.adapts(Users, IDefaultBrowserLayer, UserFTI)
    grok.provides(IBrowserPage)

from five import grok
from .models import PloneModel
from plone.app.layout.globals.interfaces import IContextState
from plone.app.layout.globals.context import ContextState
from Products.CMFCore.interfaces import IActionInfo
from UserDict import UserDict
from zope import component
from zope.interface import Interface
from plone.memoize.view import memoize
from Products.CMFCore.utils import _checkPermission


class Action(UserDict):

    def __init__(self, context, id, title, url, category, visible, available, permissions):
        UserDict.__init__(self)
        self.data.setdefault('id', id)
        self.data.setdefault('title', title)
        self.data.setdefault('link_target', None)
        self.data.setdefault('icon', '')
        self.data.setdefault('category', category)
        self.data.setdefault('visible', visible)
        self.data.setdefault('available', available)

        self._url = url
        self.context = context
        self.permissions = permissions

    def __getitem__(self, key):
        if key == 'allowed':
            return self.is_allowed()
        if key == 'url':
                return self.get_url()
        return UserDict.__getitem__(self, key)

    def get_url(self):
        object_url = self.context.absolute_url()
        return self._url.format(object_url=object_url)

    def is_allowed(self):
        # All permissions need to check out                                                                                                                                                            
        for permission in self.permissions:
            if not _checkPermission(permission, self.context):
                return False
        return True



def custom_actions(context, category=None, max=-1):
    actions = component.subscribers((context,), IActionInfo)
    for action in actions:
        if category == action['category']:
            if action['visible'] and action['available'] and action['allowed']:
                yield action


class Contextual(ContextState, grok.MultiAdapter):
    grok.adapts(PloneModel, Interface)
    grok.provides(IContextState)
    grok.name('plone_context_state')

    @memoize
    def actions(self, category=None, max=-1):
        actions = ContextState.actions(self, category=category, max=max)
        customs = custom_actions(self.context, category, max)
        actions.extend(list(customs))
        return actions

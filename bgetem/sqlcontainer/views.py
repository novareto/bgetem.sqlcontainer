# -*- coding: utf-8 -*-

from five import grok
from uvc.plone.api import View
from zope.component import getMultiAdapter
from .container import Users
from .models import User


grok.templatedir('templates')


class UsersView(View):
    grok.name('index')
    grok.context(Users)

    def update(self):
        self.mt = getMultiAdapter(
            (self.context, self.request), name="main_template")
    
    def all_users(self):
        url = self.context.absolute_url_path()
        for user in self.context:
            yield {
                'object': user,
                'id': user.id,
                'title': user.name,
                'url': '%s/++users++%s' % (url, user.__name__),
                }


class UserView(View):
    grok.name('index')
    grok.context(User)

    def update(self):
        self.mt = getMultiAdapter(
            (self.context, self.request), name="main_template")

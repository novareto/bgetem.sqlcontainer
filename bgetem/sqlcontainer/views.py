# -*- coding: utf-8 -*-

from five import grok
from uvc.plone.api import View
from zope.component import getMultiAdapter
from .container import SQLContainer


grok.templatedir('templates')


class ContainerView(View):
    grok.name('index')
    grok.context(SQLContainer)

    def update(self):
        self.mt = getMultiAdapter(
            (self.context, self.request), name="main_template")
  
    def contents(self):
        url = self.context.absolute_url_path()
        for content in self.context:
            yield {
                'object': content,
                'id': content.id,
                'title': content.name,
                'url': '%s/%s%s' % (url, self.context.__name__, content.__name__),
                }


# class UserView(View):
#     grok.name('index')
#     grok.context(User)

#     def update(self):
#         self.mt = getMultiAdapter(
#             (self.context, self.request), name="main_template")

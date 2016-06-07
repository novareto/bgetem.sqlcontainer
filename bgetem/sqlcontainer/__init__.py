# -*- coding: utf-8 -*-

import transaction
from five import grok
from z3c.saconfig.interfaces import IEngineFactory, IEngineCreatedEvent
from zope.interface import Interface
from z3c.saconfig import named_scoped_session
from zope.component import getUtility
from zope.processlifetime import IProcessStarting
from .models import Base, User


@grok.subscribe(IEngineCreatedEvent)
def create_engine_created(event):
    Base.metadata.create_all(event.engine)
    print "Created"


@grok.subscribe(IProcessStarting)
def startedHandler(event):
    pass
    #with transaction.manager:
    #    session = named_scoped_session('sqlsession')
    #    user = User(name='Christian')
    #    session.add(user)
    #    print "Created user"


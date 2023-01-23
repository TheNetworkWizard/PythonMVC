#!/usr/bin/python3

from Lib import Controller
import cgi

import logging
logger = logging.getLogger(__name__)


class Index(Controller):

    model = None
    session = None

    def __init__(self, request):
        super(Index, self).__init__(request)
        self.model = super(Index, self).loadModel("index")
        
        
    def index(self, parameters=None, method=None):
        self.session = super(Index, self).getSession()
        try:
            if(self.session[0]['sid']):
                super(Index, self).addParamater("userLevel", self.session[0]['userLevel'])
                super(Index, self).addParamater("userID", self.session[0]['userID'])
                super(Index, self).addParamater('devices', self.model.getDashboard())
                super(Index, self).addParamater('deviceIssues', self.model.getDeviceIssues())
                super(Index, self).addParamater('interfaceIssues', self.model.getInterfaceIssues())
                return super(Index, self).render("index/index")
        except:
            return super(Index, self).redirect("/nmspy/login")
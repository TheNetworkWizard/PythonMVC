from Lib import Controller

import logging
logger = logging.getLogger(__name__)


class Error(Controller):

    def __init__(self, request):
        super(Error, self).__init__(request)
    """
    def load404(self):
        super().addParamater('error', "404 - Page not found")
        super().render("error/index")

    def load403(self):
        super().addParamater('error', "403 - Forbidden")
        super().render("error/index")

    def loadMethodNotFound(self):

        super().addParamater('error', "Method not found")
        super().render("error/index")
    """

    def ControllerNotFound(self, controllerName):
        self.displayError(404, f"Page {controllerName} not found")

    
    def displayError(self, errorCode, message):
        super(Error, self).startSession()
        session = super(Error, self).getSession()
        if(session[0]['sid']):
            super(Error, self).addParamater("userLevel", session[0]['userLevel'])
            super(Error, self).addParamater("userID", session[0]['userID'])

        if errorCode == 404:
            super(Error, self).setRequestStatus("404 Not Found")
        elif errorCode == 403:
            super(Error, self).setRequestStatus("403 Forbidden")
        else:
            super(Error, self).setRequestStatus("400 Bad Request")

        super(Error, self).addParamater("message", message)
        super(Error, self).addParamater("code", errorCode)
        
        return super(Error, self).render("error/index")


    def systemError(self, details):
        super().addHeader("Status: 400 Bad Request")
        super().render("error/400")
        print(details)
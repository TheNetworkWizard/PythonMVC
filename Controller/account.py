#!/usr/bin/python3

from Lib import Controller
import cgi

import logging
logger = logging.getLogger(__name__)


class Account(Controller):

    model = None
    session = None

    def __init__(self, request):
        super(Account, self).__init__(request)
        self.model = super(Account, self).loadModel("account")

    def index(self, parameters=None, method=None):
        return super(Account, self).redirect("/nmspy")

    def login(self, parameters=None, method=None):
        session = super(Account, self).getSession()
        if(session is not None and len(session) > 0):
            return super(Account, self).redirect("/nmspy")

        if(method=="GET"):
            return super(Account, self).render("account/login")
        
        if(method=="POST"):
            POST = super(Account, self).getPOSTData()
            #Check username/password exists
            if(not 'username' in POST or not 'password' in POST):
                super(Account, self).addParamater("error", "Invalid form data")
                return super(Account, self).render("account/login")

            username = POST['username'].value
            password = POST['password'].value
            try:
                userLevel = self.model.loginUser(username, password)

                logger.debug(f"Retrieved {userLevel} for {username}")
                if(userLevel is not False):
                    if("remember" in POST):
                        super(Account, self).createSession(username, userLevel, True)
                    else:
                        super(Account, self).createSession(username, userLevel, False)
                    return super(Account, self).redirect("/nmspy")
                else:
                    logger.debug("UserID is False - Login Failed")
                    super(Account, self).addParamater("error", self.model.getLDAPFailureReason())
                    return super(Account, self).render("account/login")
            except Exception as ex:
                print(str(ex))
                super(Account, self).addParamater("error", "Invalid username or password")
                return super(Account, self).render("account/login")

    def logout(self, parameters=None, method=None):
        try:
            super(Account, self).destroySession()
            super(Account, self).addHeader(("Location", "/nmspy"))
            super(Account, self).setRequestStatus("302 Found")
            return ""
        except:
            errorDetails = {
                'controller': 'logout',
                'sessionID': super(Account, self).getSession(),
                'details': 'Failed to destroy session'
            }
            mod = __import__('Controller.error', fromlist=['error'])
            controller = getattr(mod, 'Error')
            c = controller()
            return c.systemError(errorDetails)
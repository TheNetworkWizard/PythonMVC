from Lib.View import View

import logging
logger = logging.getLogger(__name__)

class Controller:

    view = ""
    session = None
    model = ""

    GUEST_USER = 0
    NORMAL_USER = 1
    SUPER_USER = 2

    current_access = 0

    request = None

    def __init__(self, request):
        self.request = request
        self.view = View()
        

    def render(self, viewFile):
        logger.debug(self.session)
        if(not self.session):
            return self.view.renderView(viewFile)

        #Add parameters for userID and user Level
        try:
            if("userLevel" in self.session):
                self.addParamater("userLevel", self.session['userLevel'])

            if("userID" in self.session):
                self.addParamater("userID", self.session['userID'])
        except:
            pass

        return self.view.renderView(viewFile)

    def addHeader(self, header):
        self.request.addHeader(header)

    def getHeaders(self):
        return self.headers

    def getRequestStatus(self):
        return self.request.getRequestStatus()

    def setRequestStatus(self, status):
        self.request.setRequestStatus(status)

    def getPOSTData(self):
        return self.request.getPOSTData()

    def getGETData(self):
        return self.request.getGETData()
    
    def addParamater(self, key, value):
        self.view.parameters[key] = value

    def loadModel(self, modelName):
        #print("Loading model  " + modelName + "_model<br /><br />")
        mod = __import__('Model.' + modelName, fromlist=[modelName + "_model"])
        model = getattr(mod, modelName.lower().title() + '_model')
        self.model = model()
        return self.model

    def getDatabaseStatus(self):
        return self.model.getDatabaseStatus()

    def startSession(self):
        logger.debug("Starting Session")
        mod = __import__('Lib.Session', fromlist=['Session'])
        session = getattr(mod, 'Session')
        self.session = session(self.request)

    def setCookie(self, cookieName, cookieValue):
        return self.session.setCookie(cookieName, cookieValue)

    def createSession(self, user_id, user_level, persist_session):
        if(not self.session):
            self.startSession()
        logger.debug(f"Creating session for {user_id}")
        sid = self.session.createSession(str(user_id), user_level)
        self.request.addHeader(self.session.setCookie("sessionID", sid, persist_session))


    def destroySession(self):
        logger.debug("Destroying session")
        try:
            if(self.session is None):
                self.startSession()
            sid = self.session.getCookie("sessionID")
            logger.debug(f"Found cookie with sessionID: {sid}")
            session = self.session.destroySession(sid)
            self.request.addHeader(self.session.deleteCookie("sessionID", sid))
            return session
        except:
            return False

    def getSession(self):
        try:
            if(self.session is None):
                self.startSession()

            logger.debug("Getting cookie for sessionID")
            sid = self.session.getCookie("sessionID")
            logger.debug(f"Found SID: {sid}")
            session = self.session.getSession(sid)
            logger.debug(f"Found session: {session}")
            return session
        except:
            logger.debug("Failed to get session")
            self.session = None
            return None

    def getRequestData(self):
        return self.request.environ

    def getRequest(self):
        return self.request

    def redirect(self, url):
        self.addHeader(("Location", url))
        self.setRequestStatus("302 Found")
        return ""

    def renderError(self, errorCode, message):
        mod = __import__('Controller.error', fromlist=['error'])
        controller = getattr(mod, 'Error')
        c = controller(self.getRequest())
        return c.displayError(errorCode, message)

    def checkAccessLevel(self, sessison, requiredLevel):
        logger.debug(f"Checking permissions for {sessison['userID']} - {sessison['userLevel']} with {requiredLevel}")
        try: 
            if(sessison['userLevel'] == requiredLevel): 
                return True
            else:
                mod = __import__('Controller.error', fromlist=['error'])
                controller = getattr(mod, 'Error')
                c = controller(self.getRequest())
                return c.displayError(403, "Invalid permission to requested resource")
        except Exception as e:
            return False
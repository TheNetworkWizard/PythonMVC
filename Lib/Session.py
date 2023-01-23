import os
import sys
import cgi

import datetime
import hashlib
import time

from http import cookies
import requests

from Lib import Database


import logging
logger = logging.getLogger(__name__)

class Session:

    form = ""
    cookie = ""
    useCookies = 1
    request = None
    session_duration = 7776000

    #Session Constructor
    #request = instance of the Request class
    #
    def __init__(self, request):
        self.request = request
    
    #----------- Cookie Functions -----------#

    def setCookie(self, cookieName, cookieValue, persist_session):
        cookie = cookies.SimpleCookie()
        cookie[cookieName] = cookieValue
        cookie[cookieName]['path'] = '/'
        if(persist_session):
            expiry_date = datetime.datetime.now() + datetime.timedelta(seconds=self.session_duration)
            cookie[cookieName]['expires'] = expiry_date.strftime("%a, %d %b %Y %H:%M:%S GMT")
        return ("Set-Cookie", cookie[cookieName].OutputString())
        
    def getCookie(self, cookieName):
        cookie = cookies.SimpleCookie()
        if self.request.HTTP_COOKIE is not None:
            cookie.load(self.request.HTTP_COOKIE)
            return cookie[cookieName].value
        else:
            return False
         
    def deleteCookie(self, cookieName, cookieValue):
        cookie = cookies.SimpleCookie()
        cookie[cookieName] = cookieValue
        cookie[cookieName]['path'] = '/'
        cookie[cookieName]['expires'] = 'Thu, 01 Jan 1970 00:00:00 GMT'
        return ("Set-Cookie", cookie[cookieName].OutputString())
    

    #----------- Session Functions -----------#

    def createSession(self, user_id, user_level):
        hashString = (str(datetime.datetime.now()) + str(user_id)).encode('utf-8')
        session_id = hashlib.sha1(hashString).hexdigest()
        session_ip = self.request.HTTP_X_REAL_IP
        session_date = datetime.datetime.now()
        expiry_date = datetime.datetime.now() + datetime.timedelta(seconds=self.session_duration)
        expiry = time.time() + self.session_duration
        strSQL = f"INSERT INTO tbl_sessions (sid, userID, userLevel, expires) VALUES ('{session_id}', '{user_id}', {user_level}, {expiry})"
        database = Database()
        database.connect()
        rowCount = database.insertQuery(strSQL)
        database.disconnect()

        if(rowCount == 1):
            return session_id


    def destroySession(self, sessionID):
        if(sessionID):
            database = Database()
            database.connect()
            session_ip = self.request.HTTP_X_REAL_IP
            strSQL = f"DELETE FROM tbl_sessions WHERE sid = '{sessionID}'"
            result = database.deleteQuery(strSQL)
            database.disconnect()
            return result

    
    def getSession(self, sessionID):
        if(sessionID):
            database = Database()
            database.connect()
            session_ip = self.request.HTTP_X_REAL_IP
            strSQL = f"SELECT sid, userID, userLevel FROM tbl_sessions WHERE sid = '{sessionID}'"
            result = database.selectQuery(strSQL)
            database.disconnect()
            return result

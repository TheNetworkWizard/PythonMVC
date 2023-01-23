#!/usr/bin/python3
import cgi

import logging
logger = logging.getLogger(__name__)

class Request: 
    QUERY_STRING = None
    HTTP_COOKIE = None
    REQUEST_URI = ""
    POST_DATA = None
    HTTP_X_REAL_IP = None
    request_status = "200 OK"
    headers = [('Content-Type', 'text/html')]
    REQUEST_METHOD = None
    
    def __init__(self, environ):
        if("/" in environ['REQUEST_URI'][0]):
            self.REQUEST_URI = environ['REQUEST_URI'][1:]
        else:
            self.REQUEST_URI = environ['REQUEST_URI']
        
        if(len(self.REQUEST_URI) > 0):
            if("/" in self.REQUEST_URI[-1]):
                self.REQUEST_URI = self.REQUEST_URI[:-1]
            
        if("QUERY_STRING" in environ):
            self.QUERY_STRING = environ['QUERY_STRING']

        self.REQUEST_METHOD = environ['REQUEST_METHOD'].upper()
        
        if environ['REQUEST_METHOD'].upper() == 'POST':
            if("wsgi.input" in environ):
                self.POST_DATA = cgi.FieldStorage(
                    fp=environ['wsgi.input'],
                    environ=environ,
                    keep_blank_values=True
                )

        if("HTTP_COOKIE" in environ):
            self.HTTP_COOKIE = environ['HTTP_COOKIE']

        if('HTTP_X_REAL_IP' in environ):
            self.HTTP_X_REAL_IP = environ['HTTP_X_REAL_IP']

    #----------- Header Functions -----------#

    def addHeader(self, header):
        self.headers.insert(0, header)

    def getHeaders(self):
        return self.headers

    def resetHeaders(self):
        if(".css" in self.REQUEST_URI):
            self.headers = [('Content-Type', 'text/css')]
        else:
            self.headers = [('Content-Type', 'text/html')]

    #----------- Status Functions -----------#

    def setRequestStatus(self, status):
        self.request_status = status
    
    def getRequestStatus(self):
        return self.request_status

    def getRequestMethod(self):
        return self.REQUEST_METHOD

    #----------- CGI Functions -----------#

    def getPOSTData(self):
        if(not self.POST_DATA):
            raise Exception('No POST Data')
        return self.POST_DATA

    def getGETData(self):
        return self.QUERY_STRING

    
#!/usr/bin/python3

from Lib import Dispatcher
from Lib import Request
import sys
import logging
logger = logging.getLogger(__name__)

class Application(object):
    def __call__(self, environ, startResponse):
        logging.basicConfig(level=logging.DEBUG)        

        status = "200 OK"
        content = ""
        
        request = Request(environ)
        request.resetHeaders()
        logger.debug(f"Processing request for '{request.REQUEST_URI}'")

        dispatcher = Dispatcher(request)
        logger.debug("Calling Dispatcher")
        content = dispatcher.dispatch() 

        logger.debug(request.getRequestStatus())
        logger.debug(request.getHeaders())

        startResponse(request.getRequestStatus(), request.getHeaders())

        try:
            content = content.encode("utf-8")
        except:
            pass
        
        return [content]

app = Application()

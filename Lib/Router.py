#!/usr/bin/python3
import re

import logging
logger = logging.getLogger(__name__)

class Router:

    routes = {}
    route = {}
    request = None

    def __init__(self, request):
        self.request = request

    def addRoute(self, route, method):
        self.routes[route] = method

    def findRoute(self):
        self.resetRoute()
        
        if(self.request.REQUEST_URI == ""):
            return self.route

        for key in self.routes:
            result = re.match(key, self.request.REQUEST_URI)
            logger.debug(f"Found: {result} {key} - {self.routes[key].split('@')[1]}")
            if(result):
                self.route['controller'] = self.routes[key].split('@')[0]
                self.route['method'] = self.routes[key].split('@')[1]
                
                if(len(result.groups()) > 0):
                    logger.debug(f"Groups: {result.groups()}")
                    self.route['parameters'] = result.groups()[0]
                else:
                    self.route['parameters'] = False
                break
            else:
                self.route['controller'] = 'error'
                self.route['method'] = 'ControllerNotFound'
                self.route['parameters'] = self.request.REQUEST_URI
        return self.route
    
    def resetRoute(self):
        self.route = {
            "controller": "index",
            "method": "index",
            "parameters": False
        }
#!/usr/bin/python3
from Lib.Router import Router

from os import path

import logging
logger = logging.getLogger(__name__)

class Dispatcher:
    request = None
    router = None
    controllerName = "index"
    methodName = "index"
    parameters = False

    def __init__(self, request):
        self.request = request
        self.router = Router(self.request)
        self.router.addRoute('^$', 'index@index')

        self.router.addRoute('login$', 'account@login')
        self.router.addRoute('logout$', 'account@logout')
        self.router.addRoute('account$', 'account@index')
   

    def dispatch(self):

        if("assets" in self.request.REQUEST_URI):
            if(self.request):
                logger.debug(f"Loading {self.request.REQUEST_URI} for static content")
                with open(f"/var/www/html/{self.request.REQUEST_URI}", 'rb') as static_content:
                    return static_content.read()
        
        route = self.router.findRoute()
        logger.debug(route)
        self.controllerName = route['controller']
        self.methodName = route['method']
        self.parameters = route['parameters']

        logger.debug(f"Opening controller {self.controllerName}@{self.methodName}/{self.parameters}")
    
        if(self.controllerName == "error"):
            mod = __import__('Controller.error', fromlist=['error'])
            controller = getattr(mod, 'Error')
            c = controller(self.request)
            return c.ControllerNotFound(self.parameters)
        else:
            mod = __import__(f'Controller.{self.controllerName}', fromlist=[f'{self.controllerName}'])
            controller = getattr(mod, f'{str(self.controllerName).capitalize()}')
            c = controller(self.request)
            method = getattr(c, self.methodName)
            
            if(self.parameters):
                return method(parameters=self.parameters, method=self.request.getRequestMethod())
            else:
                return method(parameters=None, method=self.request.getRequestMethod())

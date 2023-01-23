from jinja2 import Environment, FileSystemLoader

import logging
logger = logging.getLogger(__name__)

class View:

    headers = []
    parameters = {}
    
    def __init__(self):
        logger.debug("View Class Init")
        self.parameters = {'base_url' : '/'}
        pass

    def addHeader(self, header):
        self.headers.append(str(header))

    def printHeaders(self):
        if(len(self.headers) > 0):
            print(*self.headers, sep='\r\n')
        print("Content-Type: text/html; charset=utf-8\r\n")

    def renderView(self, viewFile):
        logger.debug(f"Rendering View {viewFile}")
        env = Environment(loader=FileSystemLoader('/var/www/html/View'))
        
        return str(env.get_template(viewFile + '.html').render(**self.parameters))
       

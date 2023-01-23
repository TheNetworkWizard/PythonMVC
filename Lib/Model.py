from Lib import Database

import logging
logger = logging.getLogger(__name__)

class Model:
    db_conn = None

    def __init__(self):
        self.db_conn = Database()

    def getDatabaseStatus(self):
        return self.db_conn.getStatus()

    def getDatabaseError(self):
        return self.db_conn.database_error

    def selectQuery(self, query):
        self.db_conn.connect()
        result = self.db_conn.selectQuery(query)
        self.db_conn.disconnect()
        return result

    def insertQuery(self, query):
        self.db_conn.connect()
        result = self.db_conn.insertQuery(query)
        self.db_conn.disconnect()
        return result

    def insertQueryParameters(self, query, data):
        self.db_conn.connect()
        result = self.db_conn.insertQuery(query, data)
        self.db_conn.disconnect()
        return result

    def deleteQuery(self, query):
        self.db_conn.connect()
        result = self.db_conn.deleteQuery(query)
        self.db_conn.disconnect()
        return result

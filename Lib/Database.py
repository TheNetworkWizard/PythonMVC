import mysql.connector

import logging
logger = logging.getLogger(__name__)

class Database:

    host = 'HOST'
    username = 'USERNAME'
    password = 'PASSWORD'
    database = 'DATABASE'
    
    connection = None
    database_status = False
    database_error = ""


    def __init__(self):
        pass
    
    def connect(self):
        try:
            self.connection = mysql.connector.connect(user=self.username, password=self.password, host=self.host, database=self.database)
            self.database_status = True
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                this.database_error = "Something is wrong with your user name or password"
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                this.database_error = "Database does not exist"
            else:
                this.database_error = err

    def disconnect(self):
        if(self.connection is not None):
            self.connection.close()
            self.database_status = False
    
    def getStatus(self):
        return self.database_status


    def selectQuery(self, query):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result

    def insertQuery(self, query):
        rowCount = 0
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            self.connection.commit()
            rowCount = cursor.rowcount
            cursor.close()
        except Exception as ex:
            print(str(ex)) 
        return rowCount

    def insertQueryParameters(self, query, data):
        rowCount = 0
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, data)
            self.connection.commit()
            rowCount = cursor.rowcount
            cursor.close()
        except Exception as ex:
            print(str(ex)) 
        return rowCount

    def deleteQuery(self, query):
        logger.debug(f"Delete Query: {query}")
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()
        rowCount = cursor.rowcount
        cursor.close()
        return rowCount

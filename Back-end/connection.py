
import mysql.connector
from config import Config


class Connection:

    def __init__(self):
        self.__mydb = None
        self.__cursor = None
        self.__config = Config.dbinfo()

    def open_conn(self):
        self.__mydb = mysql.connector.connect(**self.__config)
        self.__cursor = self.__mydb.cursor()

    def get_cursor(self):
        return self.__cursor

    def commit_changes(self):
        if self.__mydb.is_connected():
            self.__mydb.commit()
        else:
            raise RuntimeError("MySQL connection is not open.")
        
    def close_conn(self):
        self.__cursor.close()
        self.__cursor = None
        self.__mydb.close()
        self.__mydb = None

    def run_select(self, sql, values=None):
        # open a connection (by calling the appropriate function)
        self.open_conn()
        # obtain a cursor from the connection
        query = self.get_cursor()
        # execute the sql with the values provided as parameters
        query.execute(sql, values)
        # fetch the results into a list variable
        result = query.fetchall()
        # close the connection
        self.close_conn()
        # return the resulting list
        return result

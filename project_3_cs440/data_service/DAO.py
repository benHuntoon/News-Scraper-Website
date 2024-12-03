from connection import Connection 
import time 
from flask import Flask

app = Flask(__name__)

# Define the class
class PrevSearch:
    
    def __init__(self, search_term):
        self.search_term = search_term

    # Getters 
    def get_search(self):
        return self.__search 
    
    def get_time(self):
        return self.__time 

    # Setters 
    def set_search(self, search):
        self.__search = search
        
    def set_time(self, time_value=None):
        if time_value is None:
            time_value = time.time()  # Use the current time if none is provided
        self.__time = time_value  # Assign the time to self.__time

    def open_connection(self):
        if self.__conn is None:  # Only open if it's not already open
            self.__conn = Connection(self.__config)
            self.__conn.open_conn()

    def close_connection(self):
        if self.__conn is not None:
            self.__conn.close_conn()
            self.__conn = None

    def save(self):
        conn = Connection()
        sql = "INSERT INTO Prev_search (search, time_searched) VALUES (%s, CURRENT_TIME)"
        values = (self.search_term,)
        conn.open_conn()
        cursor = conn.get_cursor()
        cursor.execute(sql, values)
        conn.commit_changes()
        conn.close_conn()

    @staticmethod
    def get_all_searches():
        conn = Connection()
        sql = "SELECT search FROM Prev_search"
        return conn.run_select(sql)
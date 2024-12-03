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
        #self.open_connection()  # Open the connection
        # Insert the new search term into the database
        #sql = "INSERT INTO Prev_search (search, time_searched) VALUES (%s, %s)"
        #values = [self.get_search(), self.get_time()]

        #cursor = self.__conn.get_cursor()
        #cursor.execute(sql, values)
        #self.__conn.commit_changes()
    @staticmethod
    def get_all_searches():
        conn = Connection()
        sql = "SELECT search FROM Prev_search"
        return conn.run_select(sql)
    #@app.route('/get_last_search.html', methods=['GET'])
    #def get_last_search(self):
        #self.open_connection()  # Open the connection
        # Fetch the last search from the database
        #sql = "SELECT search FROM Prev_search ORDER BY time_searched DESC LIMIT 1"
        #result = self.__conn.run_select(sql)

        #if result:
            #return jsonify({'last_search': result[0][0]})
        #else:
            #return jsonify({'last_search': None})

    #def __del__(self):
        #self.close_connection()  # Ensure connection is closed when the object is deleted
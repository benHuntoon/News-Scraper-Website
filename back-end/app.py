from flask import Flask, render_template, request, jsonify
import requests
import mysql.connector
import time

#begin hosting
app = Flask(__name__, static_folder='public')

#standard database login
class Config(object):
    HOST = '142.11.219.155'      
    DATABASE = 'news_scraper'  # fill with database name
    USER = 'dbguy'      
    PASSWORD = 'P@ssword69'  
    PORT = 3306

    CHARSET = 'utf8'
    UNICODE = True
    WARNINGS = True

    @classmethod
    def dbinfo(cls):
        return {
            'host': cls.HOST,
            'database': cls.DATABASE,
            'user': cls.USER,
            'password': cls.PASSWORD,
            'port': cls.PORT,
        }

#database access and retrival functions
class Connection:

    def __init__(self):
        self.__mydb = None
        self.__cursor = None
        self.__config = Config.dbinfo()

    def open_conn(self):
        self.__mydb = mysql.connector.connect(
            **self.__config)
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

#API stuff
API_URL = "https://newsapi.org/v2/everything"
API_KEY = "7f4b76d59b4f49ff94d3fa7b473a5d23"


#route to default homepage
@app.route('/')
def index():
    return render_template('index.html')

#function to collect all users previous seraches
@app.route('/previous_searches', methods=['GET'])
def previous_searches():
    #finds the search queries in chronological order
    searches = PrevSearch.get_all_searches()
    #returns the queries back to the html
    return jsonify({"previous_searches": [search[0] for search in searches]})

#finds user searches
@app.route('/search.html')
def search():
    #collects user search from URL
    query = request.args.get("q")
    if query:
        #set the query as a database entry and save it
        search = PrevSearch(query)
        search.save()
        #collect API results 
        search_results = news_search(query)
        #send the user to the search page with the articles listed
        return render_template("search.html", articles=search_results)
    #otherwise default to the homepage
    else:
        return render_template("index.html")

#search result finder function
@app.route('/get_previous_searches', methods=['GET'])
def get_previous_searches():
    #attempt to retrieve all searches from the database
    try:
        previous_searches = PrevSearch.get_all_searches()
        #return all searches back into the index.html
        return jsonify([search[0] for search in previous_searches])
    #otherwise assume error
    except Exception as e:
        return jsonify({'error': str(e)})
    
#news searching function
def news_search(query):
    #formats the search parameters
    parameters = {"q": query, "apiKey": API_KEY, "language": "en", "pageSize": 20}
    news = []
    #gets a response from the NewsAPI
    res = requests.get(API_URL, params = parameters)
    #returns a search if the API is successful
    if(res.status_code == 200):
        news = res.json().get("articles", [])
    return news

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

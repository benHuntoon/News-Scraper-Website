#import database functions and requests
from DAO import PrevSearch
from flask import jsonify, request
import requests

#API Info
API_URL = "https://newsapi.org/v2/everything"
API_KEY = "7f4b76d59b4f49ff94d3fa7b473a5d23"

#get news function
def get_news(query):
    #set api search parameters
    parameters = {"q": query, "apiKey": API_KEY, "language": "en", "pageSize": 20}
    # collect raw results from API
    results = requests.get(API_URL, params = parameters)
    #check for successful search
    if results.status_code == 200:
        #return the jsonified articles
        return results.json().get("articles", [])
    #otherwise assume search failed, return empty results
    return []

# collect unformatted previous searches from ssql server
def get_all_prev_searches():
    searches = PrevSearch.get_all_searches()
    #return jsonify({"previous_searches": [search[0] for search in searches]})
    return searches

#retrieve user search and save search query to database
def save_search(query):
    search = PrevSearch(query)
    search.save()
    return get_news(query)

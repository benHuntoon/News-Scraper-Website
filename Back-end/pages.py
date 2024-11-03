from flask import Blueprint, render_template, request, jsonify
from processing import get_all_prev_searches, save_search

#collect page data to send to app.py
routes = Blueprint("pages", __name__)

#home page routing
@routes.route("/")
def home_page():
    return render_template("index.html")

#search page routing
@routes.route("/search.html")
def search_page():
    #collects user search from URL
    query = request.args.get("q")
    #check for search input
    if query:
        #begin search process by sending query to processing layer
        search = save_search(query)
        #serve the results page
        return render_template("search.html", articles=search)
    #if no query is entered, serve homepage as default
    else:
        return render_template("index.html")

#previous search retrival function
@routes.route("/get_previous_searches", methods=["GET"])
def get_previous_searches():
    try:
        prev_searches = get_all_prev_searches()
        #return formatted previous searches back to page
        return jsonify({"previous_searches": [search[0] for search in prev_searches]})
    #otherwise return database retrival error
    except Exception as e:
        return jsonify({"Error Loading Searches": str(e)})
    

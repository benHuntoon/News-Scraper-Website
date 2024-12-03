from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__, static_folder='public', template_folder="templates")

#service urls
DATA_SERVICE = "http://localhost:3001"
API_SERVICE = "http://localhost:3000/search"

#initialize the home page (meant for initial search bar)
@app.route("/")
def homepage():
    return render_template("index.html")

#function to retrieve the previous searches
@app.route("/get_previous_searches", methods=["GET"])
def get_prev_searches():
    #attempt to collect the searches
    res = requests.get(f"{DATA_SERVICE}/get_previous_searches")
    #check for successful collection
    if res.status_code == 200:
        return jsonify(res.json())
    #otherwise assume failure
    else:
        return jsonify({"notification": "Error, could not get previous searches."}), 500

#routing function for search feature
@app.route("/search", methods=["GET"])
def search_and_save():
    #get the query from the search
    query = request.args.get("q")
    #check for query entered
    if query:
        #attempt to pass control to the API for search
        api_url = "http://api_service:3000/search?q=" + query
        api_res = requests.get(api_url)
        #api_res = requests.get(API_SERVICE, params={"q": query})
        #check for search success
        if api_res.status_code == 200:
            #collect the articles
            articles = api_res.json().get("articles", [])
            #attempt to save the search to the database
            requests.post(f"http://data_service:3001/save_search", json = {"query":query})
            #requests.post(f"{DATA_SERVICE}/save_search", json={"query": query})
            #display search results
            return render_template("search.html", articles=articles)

        #otherwise assume search failed
        else:
            return jsonify({"notification": "Error, failed to search query"})
        
    #otherwise assume no query is provided and redirect to homepage
    else:
        return render_template("index.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3002)
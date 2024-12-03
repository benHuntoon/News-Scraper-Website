from flask import Flask, render_template, request, jsonify
import requests


app = Flask(__name__, static_folder='public')

#API stuff
API_URL = "https://newsapi.org/v2/everything"
API_KEY = "7f4b76d59b4f49ff94d3fa7b473a5d23"

#finds user searches
@app.route('/search', methods=["GET"])
def search():
    #collects user search from URL
    query = request.args.get("q")
    if query:
        #collect API results 
        search_results = news_search(query)
        #send the user to the search page with the articles listed
        return jsonify({"articles": search_results})
        #return render_template("search.html", articles=search_results)
    #otherwise default to the homepage
    else:
        return jsonify({"articles": []})
        #return render_template("index.html")
    
#news searching function
def news_search(query):
    #formats the search parameters
    parameters = {"q": query, "apiKey": API_KEY, "language": "en", "pageSize": 20}
    json_news = []
    #gets a response from the NewsAPI
    res = requests.get(API_URL, params = parameters)
    #returns a search if the API is successful
    if(res.status_code == 200):
        json_news = res.json().get("articles", [])
    return json_news

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
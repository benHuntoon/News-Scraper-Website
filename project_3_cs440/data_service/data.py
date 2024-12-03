from flask import Flask, render_template, request, jsonify
import requests
from DAO import PrevSearch


app = Flask(__name__, static_folder='public')

#finds user searches
@app.route('/save_search', methods=["POST"])
def save_search():
    #collect the requested json search data
    req = request.json
    #get the search query
    query = req.get("query")
    #check for query
    if query:
        #save the search
        search = PrevSearch(query)
        search.save()
        #return successful save
        return jsonify({"notification": "Search Saved."}), 200
    #otherwise assume no query
    else:
        return jsonify({"notification": "Error, failed to save string"}), 400
    
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
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3001)
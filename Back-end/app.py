from flask import Flask
from pages import routes

app = Flask(__name__, static_folder='public')

#collect page data from pages.py
app.register_blueprint(routes)

#begin hosting
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

from flask import Flask, request,render_template
import requests
from bs4 import BeautifulSoup

from waitress import serve

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')
@app.route("/flaskFunction")
def returnSimpleFlaskFunc():
    i = 12.2+8129.4
    return str(i)

if __name__ == "__main__":
    serve(app,host='0.0.0.0',port=50100)

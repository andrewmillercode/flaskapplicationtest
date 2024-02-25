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
    response = requests.get('https://pastebin.com/Xe9bsnF1')
    soup = BeautifulSoup(response.text, 'html.parser')
    key = soup.find("div", class_ ="de1").text
    return str(key.strip())

if __name__ == "__main__":
    serve(app,host='0.0.0.0',port=50100)

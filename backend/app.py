from flask import Flask
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

#from waitress import serve

app = Flask(__name__)
CORS(app)
i=1
@app.route("/flaskFunction")
def returnSimpleFlaskFunc():
    global i
    i+=1
    return str(i)
    

if __name__ == "__main__":
#serve(app,host='0.0.0.0',port=50100)
    app.run()

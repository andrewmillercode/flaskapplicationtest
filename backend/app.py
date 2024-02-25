from flask import Flask
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import joblib
from waitress import serve
import predictionmodel as predictionmodel
from predictionmodel import FightPredictor
import fightanalyzer as fa

app = Flask(__name__)
CORS(app)
predictor = None

@app.route("/flaskFunction")
def returnSimpleFlaskFunc():
    global predictor
    print("checking model init")
    if predictor:
        return 'model found already'
    else:
        predictor = joblib.load('prediction_model.joblib')
        return 'model created'

@app.route('/fighterstats')
def getfighterstats(fighternameFirst='Conor',fighternameLast='McGregor'):
    fighternameFirst,fighternameLast = fighternameFirst.strip(),fighternameLast.strip()
    print("fighter name received:",fighternameFirst,fighternameLast)
    global predictor
   
    if predictor:
        if predictor.doesFighterExist(fighternameFirst,fighternameLast):
            print('fighter found')
            fighter = fa.Fighter(fighternameFirst,fighternameLast)
            fighter.printStats = True
            response = fighter.do()
        
            response = f"{fighter.fullName} 's stats:\n\n" + '\n'.join(response)
            return response
        else:
            print('NO fighter found')
            return 'error'


if __name__ == "__main__":
    serve(app,host='0.0.0.0',port=50100)
    
    

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import numpy as np
import fightanalyzer as fa
import time
import os
import requests
from bs4 import BeautifulSoup
from sklearn.model_selection import GridSearchCV
import math
import joblib
def clearScreen():
    if(os.name == 'posix'):
        os.system('clear')
    else:
        os.system('cls')
        
class FightPredictor:
    def __init__(self, data_path):
        self.train_data_path = data_path
        self.df_train = pd.read_csv(self.train_data_path) 
        self.X_train = self.df_train.drop('outcome', axis=1) 
        self.y_train = self.df_train['outcome'] 
        self.rf_regressor = RandomForestRegressor(n_estimators=2650, random_state=42,max_depth=5)
        self.trained = False

    def formatCalculation(self,f1,f2,percentage):
        ans = []
        if percentage < 0.5: 
            ans.append(f"{round((1-percentage[0])*100,2)}% Chance:")
            ans.append(f'WINNER : {f2.fullName}')
            ans.append(f'LOSER : {f1.fullName}')
        elif percentage > 0.5:
            ans.append(f"{round((percentage[0])*100,2)}% Chance:")
            ans.append(f'WINNER : {f1.fullName}')
            ans.append(f"LOSER : {f2.fullName}")
        else:
            ans.append('The fight will be very close. The winner cannot be predicted.')
        #percentage < 0.5 means f2 will win, >0.5 means f1 will win
        return ans
    

    def train(self):
        #yield "Training Model"
        self.rf_regressor.fit(self.X_train.values, self.y_train.values)
        self.trained = True
        print("Training complete.")
        time.sleep(0.1)

    def doesFighterExist(self,firstN,lastN):
        fighter = fa.Fighter(firstN.strip(),lastN.strip())
        fighter.do()
        if fighter.fighterFound:
            return True
        else:
            return False
    
    def predict(self,f1=None,f2=None):
        
        self.fighter_data = list()
        #for non-user input
        if f1 and f2:
            responses=[]
            for i in range(2):
                if i==1:
                    f = f1
                    f1 = f2
                    f2 = f
                    f1.do()
                    f2.do()
                else:
                    f1.do(True)
                    f2.do(True)
                l1,l2 = f1.returnStatList(),f2.returnStatList()
                l1.extend(l2)
                self.fighter_data = l1
                response = self.rf_regressor.predict(np.array(self.fighter_data).reshape(1,len(self.fighter_data)))
                response += round((int(f1.getStat("Weight")[0])-int(f2.getStat("Weight")[0]))/350,1)
                
                if i==1:
                    response = 1-response
                    f = f1
                    f1 = f2
                    f2 = f
                responses.append(response)
                
            response = sum(responses)/len(responses)
            return response
        
        #for user inputs when predicting singular fights
        if f1 == None and f2 == None:
            f1 = fa.Fighter(str(input("Fighter1 First Name: ")).strip(),str(input("Fighter1 Last Name: ")).strip())
            f2 = fa.Fighter(str(input("Fighter2 First Name: ")).strip(),str(input("Fighter2 Last Name: ")).strip())
        responses=[]
        for i in range(2):
            if i==1:
                    f = f1
                    f1 = f2
                    f2 = f
                    f1.do()
                    f2.do()
            else:
                f1.do(True)
                f2.do(True)
            l1,l2 = f1.returnStatList(),f2.returnStatList()
            l1.extend(l2)
            self.fighter_data = l1
            response = self.rf_regressor.predict(np.array(self.fighter_data).reshape(1,len(self.fighter_data)))
            response += round((int(f1.getStat("Weight")[0])-int(f2.getStat("Weight")[0]))/350,1)
            
            if i==1:
                response = 1-response
                f = f1
                f1 = f2
                f2 = f
            responses.append(response)

        response = sum(responses)/len(responses)
        #65.87%
        clearScreen()
        print(f'Fight: {f1.fullName} vs {f2.fullName}'+"\n")
        print("\n".join(self.formatCalculation(f1, f2, response))+"\n")
        
    def testAccuracy(self):
        print("Testing model accuracy..\n")
        accuracy,fightsEvaluated = 0,None
        fightList = [
            ["Khabib Nurmagomedov","Conor McGregor"],
            ["Khabib Nurmagomedov","Al Iaquinta"],
            ["Max Holloway","Anthony Pettis"],
            ["Sean Strickland","Alex Pereira"],
            ["Miesha Tate","Amanda Nunes"],
            ["Ilia Topuria","Josh Emmett"],
            ["Neil Magny","Phil Rowe"],
            ["Jack Jenkins","Jamall Emmers"],
            ["Alexander Volkanovski","Yair Rodriguez"],
            ["Tom Aspinall","Marcin Tybura"],
            ["Ciryl Gane","Serghei Spivac"],
            ["Manon Fiorot","Rose Namajunas"],
            ["Volkan Oezdemir","Bogdan Guskov"],
            ["Shavkat Rakhmonov","Stephen Thompson"],
            ["Cody Garbrandt","Brian Kelleher"],
            ["Glover Teixeira","Jamahal Hill"],
            ["Josiane Nunes","Zarah Fairn"],
            ["Warlley Alves","Nicolas Dalby"],
            ["Rodolfo Vieira","Cody Brundage"],
            ["Trey Waters","Josh Quinlan"],
            ["Leon Edwards","Kamaru Usman"],
            ["Marvin Vettori","Roman Dolidze"],
            ["Anthony Hernandez","Edmen Shahbazyan"],
            ["Sean O'Malley","Kris Moutinho"],
            ["Sean O'Malley","Eddie Wineland"],
            ["Mike Malott","Adam Fugitt"],
            ["Marc-Andre Barriault","Eryk Anders"],
            ["Jasmine Jasudavicius","Miranda Maverick"],
            ["Steve Erceg","David Dvorak"],
            ["Jailton Almeida","Jairzinho Rozenstruik"]

        ]
        
        fightList = [[fa.Fighter(string[0].split()[0],' '.join(string[0].split()[1:])),fa.Fighter(string[1].split()[0],' '.join(string[1].split()[1:]))] for string in fightList]
        for fight in fightList:
            for fighter in fight: 
                fighter.do()
        predictions = []
        for x in fightList:
            
            a = self.predict(x[0],x[1])
            predictions.append(a)
            
        

        fightsEvaluated = len(predictions)
        #only get the first fighter
        results = [fight[0].getWinnerOfPastFight(fight[1].fName,fight[1].lName) for fight in fightList]

        #for i in range(len(predictions)):
        #    print("Prediction:",predictions[i])
        #    print("Result: ",results[i])



        for i,result in enumerate(results):
            if result == 'loss' and predictions[i]<0.5:
                accuracy+=1
            if result == 'win'and predictions[i]>0.5:
                accuracy+=1
        #clearScreen()
        print(f"This model is {round((accuracy/fightsEvaluated)*100,2)}% accurate.\nAnalyzed {fightsEvaluated} fights.")
        return f"This model is {round((accuracy/fightsEvaluated)*100,2)}% accurate.\nAnalyzed {fightsEvaluated} fights."

    def showOddsForUpcomingUfcFight(self,bettingAmount):

        
        info = []
        fighters = []
        allChances = []
        allNames = []
        response = requests.get("http://ufcstats.com/statistics/events/completed")
        soup = BeautifulSoup(response.text, 'html.parser')
        upcoming_event = soup.find("tr", class_ ="b-statistics__table-row_type_first")
        
        #add the ufc event name and date
        
        info.append(f"Event: {' '.join(upcoming_event.contents[1].text.split())}\n\n")
        print(info)
        response = requests.get(upcoming_event.find('a',class_="b-link b-link_style_white").get('href'))
        soup = BeautifulSoup(response.text, 'html.parser')
        allfights = soup.find_all("tr",class_="b-fight-details__table-row b-fight-details__table-row__hover js-fight-details-click")
        #print(len(allfights))
        for fight in allfights:
            if fight:
                names = fight.find('td',class_="b-fight-details__table-col l-page_align_left")
                names = [' '.join(names.contents[1].text.split()),' '.join(names.contents[3].text.split())]
                #print(names)
                #return
                #print(names.text.split())
                #names = names.text.split(' ', 1)
                #names = [[names[0],names[1:]],[names[2],names[3:]]]
                #print(names)
                allNames.append(names)
        #allNames = allNames[0]
        #print('d')
        for event in allNames:
            try:
                x = event[0].split(' ',1)
                f1 = fa.Fighter(x[0],x[1])
                x = event[1].split(' ',1)
                #print(x)
                f2 = fa.Fighter(x[0],x[1])
                prediction = self.predict(f1,f2)
                info.append(f"Fight: {f1.fullName} vs {f2.fullName} ->\n")
                info.append("\n".join(self.formatCalculation(f1, f2, prediction))+'\n')
                clearScreen()
                fighters.append([f1.fullName,f2.fullName])
                allChances.append(prediction)
            except:
                print('e')
        allChances = sum(allChances)*100
        #print(allChances)
        x = allChances/bettingAmount 
        clearScreen()
        returnThis = []
        for i in info:
            if "%" in i:
                chance = float(i[:i.index("%")])
                print("Bet this much: ",math.floor(chance/x))
                returnThis.append(f"Bet this much: {math.floor(chance/x)}\n")    
            print(i)
            returnThis.append(i)
            returnThis.append('\n')
        return ''.join(returnThis)
        
         
if __name__ == "__main__":
    print("Training model..")
    #print("Files in the current directory:", os.listdir('backend'))
    predictor = FightPredictor('backend/FighterStatistics.csv')
    
    predictor.train()
    joblib.dump(predictor,'prediction_model.joblib')
    #predictor = joblib.load('trained_model.joblib')
    #predictor.train()
    #predictor.testAccuracy()
'''
isRunning = True
while isRunning == True:
    
    print("\nMMA_Analyzer by Andrew Miller and Simon Xu\n")
    choice = input("What would you like use mma_analyzer for?\nType the corresponding number for the function\n1-Predict next ufc event\n2-Show Stats of UFC Fighter\n3-Predict a singular UFC fight(can be past or present)\n4-Show Analyzer Accuracy\n5-Exit MMA_Analyzer")
    if choice == "1":
        predictor.showOddsForUpcomingUfcFight()
    elif choice == "2":
        fighter = fa.Fighter(str(input("Enter First Name")).strip(),str(input("Enter Last Name")).strip())
        fighter.printStats = True
        fighter.do()
    elif choice == "3":
        predictor.predict()
    elif choice == "4":
        predictor.testAccuracy()
    elif choice == "5":
        clearScreen()
        print("Thanks for using MMA_Analyzer. Have a good day.")
        isRunning = False
    else:
        print("You entered the wrong command,please try again.")
        time.sleep(1.25)
'''

'''

Fight: Alexander Volkanovski vs Ilia Topuria ->      
65.74% Chance:
WINNER : Ilia Topuria
LOSER : Alexander Volkanovski

Fight: Robert Whittaker vs Paulo Costa ->
69.75% Chance:
WINNER : Robert Whittaker
LOSER : Paulo Costa

Fight: Merab Dvalishvili vs Henry Cejudo ->
60.49% Chance:
WINNER : Merab Dvalishvili
LOSER : Henry Cejudo

Fight: Anthony Hernandez vs Roman Kopylov ->
59.6% Chance:
WINNER : Roman Kopylov
LOSER : Anthony Hernandez

Fight: Amanda Lemos vs Mackenzie Dern ->
63.75% Chance:
WINNER : Mackenzie Dern
LOSER : Amanda Lemos

Fight: Marcos Rogerio de Lima vs Justin Tafa ->      
51.37% Chance:
WINNER : Justin Tafa
LOSER : Marcos Rogerio de Lima

Fight: Rinya Nakamura vs Carlos Vera ->
70.69% Chance:
WINNER : Rinya Nakamura
LOSER : Carlos Vera

Fight: Zhang Mingyang vs Brendson Ribeiro ->
50.43% Chance:
WINNER : Zhang Mingyang
LOSER : Brendson Ribeiro

Fight: Josh Quinlan vs Danny Barlow ->
68.12% Chance:
WINNER : Danny Barlow
LOSER : Josh Quinlan

Fight: Oban Elliott vs Val Woodburn ->
64.63% Chance:
WINNER : Oban Elliott
LOSER : Val Woodburn

Fight: Andrea Lee vs Miranda Maverick ->
51.72% Chance:
WINNER : Miranda Maverick
LOSER : Andrea Lee


It got 8 out of 11 Fights predicted right.

'''


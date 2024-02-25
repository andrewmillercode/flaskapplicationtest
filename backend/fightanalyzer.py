#modules
import requests
import json
import os
from bs4 import BeautifulSoup
import time
import openai
import re
import statistics
import random
from unidecode import unidecode
import datetime
import csv
def clearScreen():
    if(os.name == 'posix'):
        os.system('clear')
    else:
        os.system('cls')

#simple function to check if this code is updated on github
def check():
    clearScreen()
    response = requests.get(
        'https://github.com/andrewmillercode/mma_data_analyzer/blob/main/test.py')
    jsonfile = response.json()
    print("Current script on github:\n")
    for x in jsonfile['payload']['blob']['rawLines']:
        print(x)
#ai
def get_completion(prompt, model="gpt-3.5-turbo-0125"):

        messages = [{"role": "user", "content": prompt}]

        response = openai.ChatCompletion.create(model=model,messages=messages,temperature=0)
        return response.choices[0].message["content"]

#get ai key
response = requests.get('https://pastebin.com/Xe9bsnF1')
soup = BeautifulSoup(response.text, 'html.parser')
key = soup.find("div", class_ ="de1").text
openai.api_key = key.strip()


#time.sleep(100)
#clearScreen()

class Fighter:
    
    def __init__(self,fName,lName):
        fName = unidecode(fName)
        lName = unidecode(lName)
        self.fName = fName
        self.lName = lName
        self.sigStrikes = []
        self.genStats = []
        self.fullName = ' '.join([fName,lName])
        self.printStats = False
        self.fighterFound = False
    def do(self,printFighterFound=False):
        response = requests.get(f'http://ufcstats.com/statistics/fighters/search?query={self.lName}')
        soup = BeautifulSoup(response.text, 'html.parser')
        allLastNames = soup.find_all("td", class_ ="b-statistics__table-col")
        for index,name in enumerate(allLastNames):
            #if index>0:
            #    lastName = allLastNames[index-1]
            #else:lastName= allLastNames[index]
            x = name.find("a", class_ ="b-link b-link_style_black")
            
            
            if x and index>0:
                item = allLastNames[index-1].find("a", class_ ="b-link b-link_style_black")
                if x.text == self.lName and item:
                    if item.text == self.fName:
                        if printFighterFound==True:
                            print(f"Fighter found: {self.fName} {x.text}")
                        self.fighterFound = True
                        #print(f"{x.get('href')} \n")
                        response = requests.get(x.get('href'))
                        soup = BeautifulSoup(response.text, 'html.parser')
                        info = soup.find_all("li", class_ ="b-list__box-list-item b-list__box-list-item_type_block")
                        
                        if self.printStats:print("General Stats:")
                        for i in info:
                            y = i.text.split()
                            if y:
                                
                                #convert DOB to age, easier processing
                                if y[0] == "DOB:":
                                    year = datetime.date.today().year
                                    y = ["Age:",year-int(y[3])]
                                if y[0] in ["TD","Str.","Sub."]:
                                    y = [y[0]+y[1],y[2]]
                                self.genStats.append(y)

                                if self.printStats:
                                    print(*y)
        if self.printStats:
            newstats = []
            for x in self.genStats:
                x = [str(i) for i in x]
                newstats.append(''.join(x))
            return newstats
                    

    def getStat(self,statToFind):
        for stat in self.genStats:
            if statToFind in stat[0]:
                return stat[1:]
            
    def returnStatList(self):
        #height,weight,reach,significant_strikes,takedown_accuracy,stance,age,sapm,strike_defense,takedown_defense,average_submissions
        
        
        #print(f"{self.fullName}: {self.getStat('Height')}")
        h = ''.join(self.getStat("Height")).split("'")
        h = [h[0],h[1].replace('"','')]
        h = [int(x) for x in h]
        
        
        #conv to inches
        h = (int(h[0])*12)+(int(h[1]))
        w = int(' '.join(self.getStat("Weight")).split()[0])
        r = int(' '.join(self.getStat("Reach")).replace('"',''))

        ss = float(self.getStat("SLpM")[0])
        ta = round(float(''.join(self.getStat("TDAvg")))  * float(' '.join(self.getStat("TDAcc")).replace("%",''))/100,2)
        
        stance=str(self.getStat("STANCE")[0]).strip()
        if stance == "Switch":
            stance = 2
        elif stance == "Orthodox":
            stance = 1
        elif stance == "Southpaw":
            stance = 0
        age=int(self.getStat("Age")[0])
        SApM=float(self.getStat("SApM")[0])
        sDef=float(' '.join(self.getStat("Str.Def")).replace('%',''))
        tDef=float(' '.join(self.getStat("TDDef")).replace('%',''))
        avgSub=float(self.getStat("Sub.Avg")[0])
        return [str(x) for x in [h,w,r,ss,ta,stance,age,SApM,sDef,tDef,avgSub]]
    
    def getWinnerOfPastFight(self,otherFighterFirstName,otherFighterLastName):
        response = requests.get(f'http://ufcstats.com/statistics/fighters/search?query={self.lName}')
        soup = BeautifulSoup(response.text, 'html.parser')
        allLastNames = soup.find_all("td", class_ ="b-statistics__table-col")
        for index,name in enumerate(allLastNames):
            #if index>0:
            #    lastName = allLastNames[index-1]
            #else:lastName= allLastNames[index]
            x = name.find("a", class_ ="b-link b-link_style_black")
            
            
            if x and index>0:
                item = allLastNames[index-1].find("a", class_ ="b-link b-link_style_black")
                if x.text == self.lName and item:
                    if item.text == self.fName:
                        #print(f"Fighter found: {self.fName} {x.text}")
                        #print(f"{x.get('href')} \n")
                        response = requests.get(x.get('href'))
                        soup = BeautifulSoup(response.text, 'html.parser')
                        
                        info = soup.find_all("tr", class_ ="b-fight-details__table-row b-fight-details__table-row__hover js-fight-details-click")
                        for i in info:
                            winner = ' '.join(i.contents[3].contents[1].text.split())
                            loser = ' '.join(i.contents[3].contents[3].text.split())
                            #print(winner,loser)
                            outcome = ''.join(i.contents[1].text.split())
                            if ' '.join([otherFighterFirstName,otherFighterLastName]) in [winner,loser]:
                                #fight found, return outcome as 'loss' or 'win'
                                return outcome

    @classmethod
    def getFightStatsForCSV(self):
        #debug
        maxN = 1000

        numberoffights = 0
        f1,f2 = [],[]
        total = []
        response = requests.get("http://ufcstats.com/statistics/events/completed?page=all")
        soup = BeautifulSoup(response.text, 'html.parser')
        allevents= soup.find_all("tr", class_ ="b-statistics__table-row")
        for event in allevents:
            event = event.find("a", class_ ="b-link b-link_style_black")
            if event:
                #print(fight.get('href'))
                response = requests.get(event.get('href'))
                soup = BeautifulSoup(response.text, 'html.parser')
                fightDate = soup.find("li",class_="b-list__box-list-item").contents[2]
                fightDate = int(fightDate.text.split()[-1])
                
                allfights = soup.find_all("tr",class_="b-fight-details__table-row b-fight-details__table-row__hover js-fight-details-click")
                for fight in allfights:
                    if fight:
                        #we only get fights with a winner
                        if ''.join(fight.contents[1].text.split()) == "win":
                            numberoffights+=1
                            #fight = fight.find("td",class_="b-fight-details__table-col l-page_align_left").contents[1]
                            #on the fight page now
                            winner = ' '.join(fight.contents[3].contents[1].text.split())
                            loser = ' '.join(fight.contents[3].contents[3].text.split())
                            
                            fight = fight.contents[1].contents[1].contents[1]
                            
                            response = requests.get(fight.get('href'))
                            #print(response.text)
                            soup = BeautifulSoup(response.text, 'html.parser')
                            #info = soup.find("tr",class_="b-fight-details__table-row")
                            
                            #we need this to get proper numbers
                            fighterNumber = None 
                            
                            fighterNames = soup.find("td",class_="b-fight-details__table-col l-page_align_left").findChildren()
                            fighterNames = [name.text.strip() for name in fighterNames if "\n" not in name.text]
                            fighterNumber = fighterNames.index(winner)
                            loserNumber = fighterNames.index(loser)

                            fightInfoChilds = soup.find("td",class_="b-fight-details__table-col l-page_align_left").parent.findChildren()
                            
                            header = ['height1','weight1','reach1','ss1','ta1','stance1','age1','ssapm1','ssD1','tdD1','avg_sub1','height2','weight2','reach2','ss2','ta2','stance2','age2','sapm2','ssD2','tdD2','avg_sub2','outcome']     
                                   
                            
                            try:
                                    
                                #brute force fix
                                outcome = None
                                chance = random.randrange(2)

                                if chance == 0:
                                    #first fighter will be the loser
                                    outcome = 0
                                    zNum = fighterNumber
                                    z = winner
                                    fighterNumber = loserNumber
                                    winner = loser
                                    loserNumber = zNum
                                    loser = z
                                else:
                                    #first fighter will be the winner
                                    outcome = 1
                                #print("losermum:",loserNumber)
                                #print("winnwermum:",fighterNumber)
                                #ss%,td total,td
                                #print(winner.split(),outcome)
                                winnerReplaceData,loserReplaceData = [],[]
                                for id,child in enumerate(fightInfoChilds):
                                    #print(id,*child.text.split())
                                    
                                    #ss% ->
                                    if id == 12+fighterNumber:
                                        s = child.text.split()[0]
                                        if '-' not in s:
                                            s = int(s.replace('%',''))
                                        else:
                                            s = 0
                                        winnerReplaceData.append(s)
                                        
                                    if id == 13-fighterNumber:
                                        s = child.text.split()[0]
                                        if '-' not in s:
                                            s = int(s.replace('%',''))
                                        else:
                                            s = 0
                                        loserReplaceData.append(s)
                                    #td% ->
                                    if id == 21+fighterNumber:
                                        s = child.text.split()[0]
                                        if '-' not in s:
                                            s = int(s.replace('%',''))
                                        else:
                                            s = 0
                                        winnerReplaceData.append(s)
                                        
                                        
                                    if id == 22-fighterNumber:
                                        s = child.text.split()[0]
                                        if '-' not in s:
                                            s = int(s.replace('%',''))
                                        else:
                                            s = 0
                                            
                                        loserReplaceData.append(s)
                                    #subs ->
                                    if id == 24+fighterNumber:
                                        s = child.text.split()[0]
                                        s = int(s)
                                        winnerReplaceData.append(s)
                                        
                                    if id == 25-fighterNumber:
                                        s = child.text.split()[0]
                                        s = int(s)
                                        loserReplaceData.append(s)

                                #print(winnerReplaceData)
                                #print(loserReplaceData)
                                #0       1       2            3               4                5   6   7     8               9               10
                                #height,weight,reach,significant_strikes,takedown_accuracy,stance,age,sapm,strike_defense,takedown_defense,average_submissions
                                

                                fighter = Fighter(winner.split()[0],winner.split()[1])
                                fighter.do()
                                genStats = fighter.returnStatList()
                                #print(genStats)   
                                for index in range(len(genStats)):
                                    #print(index)
                                    if index == 3:
                                        #Significant strikes landed
                                        genStats[index] = winnerReplaceData[0]
                                    if index == 4:
                                        #sucessfull takedowns
                                        genStats[index] = winnerReplaceData[1]
                                    if index == 6:
                                        #age(we need to get their approximate age at the fight date because old fighters do worse)
                                        curYear = datetime.date.today().year
                                        
                                        differenceInYears = curYear - fightDate
                                        
                                        #ex: age=33, fight at 2020, subtract 4 from 33-> 29
                                        genStats[index] = int(genStats[index])+differenceInYears    
                                        
                                    if index == 8:
                                        #print(loserReplaceData[0])
                                        genStats[index] = 100-loserReplaceData[0]
                                    if index == 9:
                                        #TDD
                                        genStats[index] = 100-loserReplaceData[1]
                                    
                                genStats = [str(x) for x in genStats]    
                                #print(genStats)        
                                f1 = genStats
                                
                                fighter = Fighter(loser.split()[0],loser.split()[1])
                                fighter.do()
                                genStats = fighter.returnStatList()
                                for index in range(len(genStats)):
                                    if index == 3:
                                        #Significant strikes landed
                                        genStats[index] = loserReplaceData[0]
                                    if index == 4:
                                        #sucessfull takedowns
                                        genStats[index] = loserReplaceData[1]
                                    if index == 6:
                                        #age(we need to get their approximate age at the fight date because old fighters do worse)
                                        
                                        curYear = datetime.date.today().year
                                        differenceInYears = curYear - fightDate
                                        #ex: age=33, fight at 2020, subtract 4 from 33-> 29
                                        genStats[index] = int(genStats[index])+differenceInYears       
                                    if index == 8:
                                        #significant strikes defended
                                        #100-loser ss landed
                                        genStats[index] = 100-winnerReplaceData[0]
                                    if index == 9:
                                        #TDD
                                        genStats[index] = 100-winnerReplaceData[1]
                                    
                                    
                                genStats = [str(x) for x in genStats]         
                                f2 = genStats
                                f2.append(str(outcome))
                                f1.extend(f2)
                                total.append(f1)
                            except:
                                maxN-=1
                                if maxN <=0:
                                    print("Done")
                                    
                                    with open('FighterStatistics.csv', 'w', encoding='UTF8', newline='') as f:
                                        writer = csv.writer(f)

                                        #write the header
                                        writer.writerow(header)

                                        # write the data
                                        writer.writerows(total)
                                    print("fights in csv: ",numberoffights)
                                    return       

                            
                            maxN-=1
                            if maxN <=0:
                                print("Done")
                                
                                with open('FighterStatistics.csv', 'w', encoding='UTF8', newline='') as f:
                                    writer = csv.writer(f)

                                    # write the header
                                    writer.writerow(header)

                                    writer.writerows(total)
                                print("fights in csv: ",numberoffights)
                                return

        
        
    def compareFighters(self,f1,f2):
        print(f"\nComparison between {f1.fullName} and {f2.fullName}\n")
        print(f"{f1.fullName} sig strike : {statistics.median(f1.sigStrikes)}")
        print(f"{f2.fullName} sig strike : {statistics.median(f2.sigStrikes)}")
        if statistics.median(f1.sigStrikes) > statistics.median(f2.sigStrikes):
            print(f"{f1.fullName} wins.")
        else:
            print(f"{f2.fullName} wins.")

'''
fighter1 = Fighter("Alex","Pereira")
fighter2 = Fighter("Tom","Aspinall")
fighter1.do()
print('Next fighter..')
time.sleep(.2)              
fighter2.do()
fighter2.compareFighters(fighter1,fighter2)
'''
if __name__ == "__main__":
    #pass
    #Fighter.getFightStatsForCSV()
    fighter1 = Fighter("Ilia","Topuria")
    fighter1.printStats = True
    i = fighter1.do()
    print('\n'.join(i))
    #print(fighter1.getStat("Weight")[0])

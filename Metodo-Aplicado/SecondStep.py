import os #Criar pastas
import csv
import datetime
import pandas as pd
import calendar
from pathlib import Path

#contagem = df['categoria'].value_counts()
#df = df[df['categoria'].isin(contagem[contagem >= 3].index)]

#df = df[df["coluna"] == playerName]

#pd.to_datetime

#from sklearn.cluster import KMeans
#import numpy as np

#from sklearn.tree import DecisionTreeClassifier

#from scipy.stats import pearsonr, spearmanr

directory = r"C:\Users\marco\Documents\TCC\Metodo-Aplicado\\"
dataBasePath = directory+"\\DataBase\\"

dataBaseFiltred = "LOL_2023_Filtred.csv"
filtredData = pd.read_csv(dataBasePath+dataBaseFiltred)
filtredData["gameEndTimestampToDate"] = pd.to_datetime(filtredData["gameEndTimestampToDate"])

updateCount = 0
taxaForDay = False

column_tag = {
    "player" : "summonerName",
    "playerIdentifier": "playerIdRemaster",
    "regionCode" : "regionCode",
    "champion" : "championName",
    "function" : "individualPosition"
}

def MakeTimePassString(startTime,endTime):
    time = endTime-startTime; seconds = int(time.total_seconds())
    hours = seconds // 3600; minutes = (seconds % 3600) // 60; seconds = seconds % 60
    timePass = f" | {hours:02}:{minutes:02}:{seconds:02}"
    return timePass

#Use this to show your progress in terminal.
def ProgressBar(message1,value,maxValue,message2 = "%.",end = False, startTime=None):
    progress = (value / maxValue)
    progress = progress*100
    progress = round(progress)
    progress_str = str(progress)

    timePass = ""
    if startTime != None:
        timePass = MakeTimePassString(startTime,datetime.datetime.now())
        #time = datetime.datetime.now()-startTime; seconds = int(time.total_seconds())
        #hours = seconds // 3600; minutes = (seconds % 3600) // 60; seconds = seconds % 60
        #timePass = f" | {hours:02}:{minutes:02}:{seconds:02}"

    erasor = len(message1) + len(message1) + len(progress_str) + len(timePass)

    print(f"\r"*erasor,
          end="", flush=True)
    print(f"\r"+message1+progress_str+message2+timePass, end="", flush=True)
    if end and value >= maxValue: print("")
    
#This Function create CSV file if this don't is created before.
def CreateCSV(filePath,fieldnames):
    with open(filePath, mode="w",encoding="utf-16", newline="") as csvfile: 
        writer = csv.writer(csvfile)
        writer.writerow(fieldnames)

#This Function edit a created CSV.
def UpdateCSV(csvPath,write,updateCount,printCount = False) -> int:
    updateCount = updateCount+1
    if(printCount): print("Update CSV Count = "+str(updateCount)+".")
    with open(csvPath, mode="a",encoding="utf-16", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(write)
    return updateCount

#This Function is used for makin path and create all CSV about champions and functions of player.
def CreateTaxaForPlayer(player_identifier):

    player: pd.DataFrame = filtredData[filtredData[column_tag["playerIdentifier"]] == player_identifier]

    player["year"] = filtredData["gameEndTimestampToDate"].dt.year
    player["month"] = filtredData["gameEndTimestampToDate"].dt.month
    player["week"] = ((filtredData["gameEndTimestampToDate"].dt.day -1) // 7) + 1
    if taxaForDay: player["day"] = filtredData["gameEndTimestampToDate"].dt.day

    player_champions = player["championName"].unique()
    player_function = player["individualPosition"].unique()

    os.makedirs(directory+"TaxasDosJogadores", exist_ok=True)
    os.makedirs(directory+"TaxasDosJogadores\\"+player_identifier,exist_ok=True)
    os.makedirs(directory+"TaxasDosJogadores\\"+player_identifier+"\\Champions",exist_ok=True)
    os.makedirs(directory+"TaxasDosJogadores\\"+player_identifier+"\\Functions",exist_ok=True)

    playerDirectory = directory+"TaxasDosJogadores\\"+player_identifier+"\\"
    championsDirectory = directory+"TaxasDosJogadores\\"+player_identifier+"\\Champions\\"
    functionsDirectory = directory+"TaxasDosJogadores\\"+player_identifier+"\\Functions\\"

    if taxaForDay != True: CreateCSV(os.path.join(playerDirectory,"Player_Taxas.csv"),["Player",column_tag["regionCode"],
                                                                    "Champion/Function","Year","Month","Week","WeekParts","pick_rate","Wins","win_rate"])
    else: CreateCSV(os.path.join(playerDirectory,"Player_Taxas.csv"),["Player",column_tag["regionCode"],
                                                                    "Champion/Function","Year","Month","Week","Day","DayParts","pick_rate","Wins","win_rate"])

    CreateTaxaTo(column_tag["champion"],player_champions,player,player_identifier,championsDirectory,playerDirectory)
    CreateTaxaTo(column_tag["function"],player_function,player,player_identifier,functionsDirectory,playerDirectory)

#This is a generic function created to make CSV for the Champions and Functions just change the values.
def CreateTaxaTo(columTag,targetList,player,player_name,directory,player_directory):
    
    for tag in targetList:
        tagData = player[player[columTag] == tag]
        if taxaForDay != True: CreateCSV(os.path.join(directory,tag+".csv"),["Year","Month","Week","pick_rate","win_rate"])
        else: CreateCSV(os.path.join(directory,tag+".csv"),["Year","Month","Week","Day","pick_rate","win_rate"])

        years = tagData["year"].unique()
        for year in years:
            yearData = tagData[tagData["year"] == year]
            yearPlayerData = player[player["year"] == year]

            months = yearData["month"].unique()
            for month in months:
                monthData = yearData[yearData["month"] == month]
                monthPlayerData = yearPlayerData[yearPlayerData["month"] == month]

                weeks = monthData["week"].unique()
                for week in weeks:
                    regionCode = regionCode = "/".join(monthPlayerData[column_tag["regionCode"]].unique())

                    weekData = monthData[monthData["week"] == week]
                    weekPlayerData = monthPlayerData[monthPlayerData["week"] == week]

                    week_part_alls = len(weekPlayerData["win"])
                    week_part_total = len(weekData["win"])
                    
                    week_win_total = weekData["win"].sum()
                    
                    week_pick_rate = round(week_part_total/week_part_alls,2)
                    week_win_rate = round(week_win_total/week_part_total,2)

                    if taxaForDay:
                        days = weekData["day"].unique()
                        for day in days:
                            regionCode = "/".join(weekPlayerData[column_tag["regionCode"]].unique())

                            dayData = weekData[weekData["day"] == day]
                            dayPlayerData = weekPlayerData[weekPlayerData["day"] == day]

                            day_part_alls = len(dayPlayerData["win"])
                            day_part_total = len(dayData["win"])
                    
                            day_win_total = dayData["win"].sum()
                    
                            day_pick_rate = round(day_part_total/day_part_alls,2)
                            day_win_rate = round(day_win_total/day_part_total,2)

                            UpdateCSV(os.path.join(directory,tag+".csv"),
                                                          [year,month,week,day,day_pick_rate,day_win_rate],0,False
                                                          )
                            UpdateCSV(os.path.join(player_directory,"Player_Taxas.csv"),
                                      [player_name,regionCode,tag,year,month,week,day,day_part_total,day_pick_rate,day_win_total,day_win_rate],0,False
                                      )
                    else:
                        UpdateCSV(os.path.join(directory,tag+".csv"),
                                  [year,month,week,week_pick_rate,week_win_rate],0,False
                                  )
                        UpdateCSV(os.path.join(player_directory,"Player_Taxas.csv"),
                                  [player_name,regionCode,tag,year,month,week,week_part_total,week_pick_rate,week_win_total,week_win_rate],0,False
                                  )

players_all = filtredData[column_tag["playerIdentifier"]].unique()

print("==============================================================")
print("Start Second Step.")
i = 0; startTime = datetime.datetime.now()
for player in players_all:
    
    CreateTaxaForPlayer(player)

    i+= 1; ProgressBar("Analysis in ",i,len(players_all),startTime=startTime,end=True) #00:27:14 [Taxa For Week] | 00:34:00 [Taxa For Week]
print("==============================================================")
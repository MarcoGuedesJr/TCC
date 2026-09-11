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

directory = r"C:\Users\marco\Documents\TCC\Metodo-Aplicado\\"
dataBasePath = directory+"\\DataBase\\"

dataBaseFiltred = "LOL_2023_Filtred.csv"
filtredData = pd.read_csv(dataBasePath+dataBaseFiltred)
filtredData["gameEndTimestampToDate"] = pd.to_datetime(filtredData["gameEndTimestampToDate"])

updateCount = 0

#Use this to show your progress in terminal.
def ProgressBar(message1,value,maxValue,message2 = "%.",end = False):
    progress = (value / maxValue)
    progress = progress*100
    progress = round(progress)
    progress_str = str(progress)

    erasor = len(message1) + len(message1) + len(progress_str)

    print(f"\r"*erasor,
          end="", flush=True)
    print(f"\r"+message1+progress_str+message2, end="", flush=True)
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
def CreateTaxaForPlayer(player_name):

    player = filtredData[filtredData["summonerName"] == player_name]

    player["year"] = filtredData["gameEndTimestampToDate"].dt.year
    player["month"] = filtredData["gameEndTimestampToDate"].dt.month
    player["week"] = ((filtredData["gameEndTimestampToDate"].dt.day -1) // 7) + 1

    player_champions = player["championName"].unique()
    player_function = player["individualPosition"].unique()

    os.makedirs(directory+"TaxasDosJogadores", exist_ok=True)
    os.makedirs(directory+"TaxasDosJogadores\\"+player_name,exist_ok=True)
    os.makedirs(directory+"TaxasDosJogadores\\"+player_name+"\\Champions",exist_ok=True)
    os.makedirs(directory+"TaxasDosJogadores\\"+player_name+"\\Functions",exist_ok=True)

    playerDirectory = directory+"TaxasDosJogadores\\"+player_name+"\\"
    championsDirectory = directory+"TaxasDosJogadores\\"+player_name+"\\Champions\\"
    functionsDirectory = directory+"TaxasDosJogadores\\"+player_name+"\\Functions\\"

    CreateCSV(os.path.join(playerDirectory,"Player_Taxas.csv"),["Champion/Function","Year","Month","Week","pick_rate","win_rate"])

    CreateTaxaTo("championName",player_champions,player,championsDirectory,playerDirectory)
    CreateTaxaTo("individualPosition",player_function,player,functionsDirectory,playerDirectory)

#This is a generic function created to make CSV for the Champions and Functions just change the values.
def CreateTaxaTo(columTag,targetList,player,directory,player_directory):
    
    for tag in targetList:
        tagData = player[player[columTag] == tag]
        CreateCSV(os.path.join(directory,tag+".csv"),["Year","Month","Week","pick_rate","win_rate"])

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
                    weekData = monthData[monthData["week"] == week]
                    weekPlayerData = monthPlayerData[monthPlayerData["week"] == week]

                    week_part_alls = len(weekPlayerData["win"])
                    week_part_total = len(weekData["win"])

                    week_win_total = weekData["win"].sum()

                    week_pick_rate = week_part_total/week_part_alls
                    week_win_rate = week_win_total/week_part_total

                    UpdateCSV(os.path.join(directory,tag+".csv"),
                              [year,month,week,week_pick_rate,week_win_rate],0,False
                              )
                    UpdateCSV(os.path.join(player_directory,"Player_Taxas.csv"),
                              [tag,year,month,week,week_pick_rate,week_win_rate],0,False
                              )

players_all = filtredData["summonerName"].unique()

i = 0
for player in players_all:
    
    CreateTaxaForPlayer(player)

    i+= 1; ProgressBar("Analysis in ",i,len(players_all),end=True)
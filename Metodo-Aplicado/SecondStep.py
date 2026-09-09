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
dataBaseFiltred = "LOL_2023_Filtred.csv"
filtredData = pd.read_csv(directory+dataBaseFiltred)
filtredData["gameEndTimestampToDate"] = pd.to_datetime(filtredData["gameEndTimestampToDate"])

porcent = 0
old_porcent = 0
call_porcent = 0.01

updateCount = 0

def CreateTaxaForPlayer(player_name):

    player = filtredData[filtredData["summonerName"] == player_name]

    player["year"] = filtredData["gameEndTimestampToDate"].dt.year
    player["month"] = filtredData["gameEndTimestampToDate"].dt.month
    player["week"] = ((filtredData["gameEndTimestampToDate"].dt.day -1) // 7) + 1

    #player_parts = player.groupby(["year", "month", "week", "win"])
    player_champions = player["championName"].unique()

    os.makedirs(directory+"TaxasDosJogadores", exist_ok=True)
    os.makedirs(directory+"TaxasDosJogadores\\"+player_name,exist_ok=True)

    for champion in player_champions:
        championData = player[player["championName"] == champion]

        CreateCSV(os.path.join(directory+"TaxasDosJogadores\\"+player_name+"\\",champion+".csv"),["Year","Month","Week","pick_rate","win_rate"])

        years = championData["year"].unique()
        for year in years:
            yearData = championData[championData["year"] == year]
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

                    UpdateCSV(os.path.join(directory+"TaxasDosJogadores\\"+player_name+"\\",champion+".csv"),
                              [year,month,week,week_pick_rate,week_win_rate],0,False
                              )

#This Function create CSV file if this don't is created before.
def CreateCSV(filePath,fieldnames): 
    #print("Create CSV.")
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

players_all = filtredData["summonerName"].unique()

for player in players_all:

    updateCount = updateCount+1
    porcent = updateCount/len(players_all)

    if porcent >= old_porcent+call_porcent:
        old_porcent = porcent
        print("Progress : "+str(porcent)+".")

    CreateTaxaForPlayer(player)
import os #Criar pastas
import csv
import datetime
import pandas as pd
import calendar
from pathlib import Path
from scipy.stats import shapiro
import numpy as np

#contagem = df['categoria'].value_counts()
#df = df[df['categoria'].isin(contagem[contagem >= 3].index)]

#df = df[df["coluna"] == playerName]

#pd.to_datetime

#from sklearn.cluster import KMeans
#import numpy as np

#DecisionTreeClassifier

directory = "C:\\Users\\marco\\Documents\\TCC\\Metodo-Aplicado\\"
dataBasePath = directory+"\\DataBase\\"

dataBaseFiltred = "LOL_2023_Filtred.csv"
filtredData = pd.read_csv(dataBasePath+dataBaseFiltred)
filtredData["gameEndTimestampToDate"] = pd.to_datetime(filtredData["gameEndTimestampToDate"])

updateCount = 0

column_tag = {
    "player" : "summonerName",
    "playerIdentifier": "playerIdRemaster",
    "regionCode" : "regionCode",
    "champion" : "championName",
    "function" : "individualPosition"
}

clustersColumns = ["parts","rate_min","rate_max","rate_delta"]
treeColumn = "clusterLabel"

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

def GetAllPlayersBase(players):
    allPlayersBase = []; i = 0; startTime = datetime.datetime.now()
    for player in players:
        PlayerDirectory = directory+"TaxasDosJogadores\\"+player+"\\"
        target = pd.read_csv(PlayerDirectory+"Player_Taxas.csv",encoding="utf-16")
        allPlayersBase.append(target)
        i+= 1; ProgressBar("Making unifiqued players_base csv ",i,len(players_all),startTime=startTime,end=True)
    allPlayersBase = pd.concat(allPlayersBase,ignore_index=True)
    return allPlayersBase


def ShapiroWilk_ForEachPlayerStrategy(players):
    #["Player",column_tag["regionCode"],"Champion/Function","Year","Month","Week","WeekParts","pick_rate","Wins","win_rate"]
    AllPlayersResults = []; i = 0; startTime = datetime.datetime.now()
    for player in players:
        PlayerDirectory = directory+"TaxasDosJogadores\\"+player+"\\"
        playerData = pd.read_csv(PlayerDirectory+"Player_Taxas.csv",encoding="utf-16")
        playerData = playerData[["Player",column_tag["regionCode"],"Champion/Function","Year","Month","Week","WeekParts","pick_rate","Wins","win_rate"]]
        tags = playerData["Champion/Function"].unique(); regionCode = playerData["regionCode"].unique()
        playerAllResults = []; playerAllResultsForMonth = []
        for tag in tags:
            tagData = playerData[playerData["Champion/Function"] == tag]
            years = tagData["Year"].unique()
            for year in years:
                yearData = tagData[tagData["Year"] == year]
                months = yearData["Month"].unique()
                for month in months:
                    monthData = yearData[yearData["Month"] == month]
                    weeks = monthData["Week"].unique(); week_count = len(weeks)

                    part_stat, part_p = shapiro(monthData["WeekParts"]); pick_rate_stat, pick_rate_p = shapiro(monthData["pick_rate"])
                    win_stat, win_p = shapiro(monthData["Wins"]); win_rate_stat, win_rate_p = shapiro(monthData["win_rate"])

                    monthData["ShapiroStat_Parts"] = part_stat; monthData["ShapiroP_Parts"] = part_p
                    monthData["ShapiroStat_Pick_Rate"] = pick_rate_stat; monthData["ShapiroP_Pick_Rate"] = pick_rate_p

                    monthData["ShapiroStat_Wins"] = win_stat; monthData["ShapiroP_Wins"] = win_p
                    monthData["ShapiroStat_Win_Rate"] = win_rate_stat; monthData["ShapiroP_Win_Rate"] = win_rate_p

                    playerAllResults.append(monthData)
                    playerAllResultsForMonth.append(pd.DataFrame({
                        "Player": [player], column_tag["regionCode"] : regionCode, "Champion/Function" : [tag], "Year": [year], "Month": [month],
                        "ShapiroStat_Parts": monthData["ShapiroStat_Parts"].unique(),
                        "ShapiroP_Parts" : monthData["ShapiroP_Parts"].unique(),
                        "ShapiroStat_Pick_Rate": monthData["ShapiroStat_Pick_Rate"].unique(),
                        "ShapiroP_Pick_Rate" : monthData["ShapiroP_Pick_Rate"].unique(),
                        "ShapiroStat_Wins": monthData["ShapiroStat_Wins"].unique(),
                        "ShapiroP_Wins" : monthData["ShapiroP_Wins"].unique(),
                        "ShapiroStat_Win_Rate": monthData["ShapiroStat_Win_Rate"].unique(),
                        "ShapiroP_Win_Rate" : monthData["ShapiroP_Win_Rate"].unique()
                    }))
        playerAllResults:pd.DataFrame = pd.concat(playerAllResults,ignore_index=True)
        playerAllResults.to_csv(PlayerDirectory+"ShapiroWilk_ForEachPlayerStrategy.csv",encoding="utf-16")

        playerAllResultsForMonth:pd.DataFrame = pd.concat(playerAllResultsForMonth,ignore_index=True)
        AllPlayersResults.append(playerAllResultsForMonth)

        i+= 1; ProgressBar("Making Shapiro Test and Make csv ",i,len(players_all),startTime=startTime,end=True) #00:16:38
    startTime = datetime.datetime.now(); ProgressBar("Making all players Shapiro csv...",0,1,startTime=startTime)
    AllPlayersResults:pd.DataFrame = pd.concat(AllPlayersResults,ignore_index=True)
    AllPlayersResults.to_csv(dataBasePath+"ShapiroWilk_ForEachPlayerStrategy.csv",encoding="utf-16")
    ProgressBar("All Players Shapiro csv Maked.",1,1,startTime=startTime,end=True) #00:00:010
    return

def ShapiroWilk_ForAllPlayersStrategy(players):#Aqui vamos tirar o shapiro de todos os camps e func com relação a todos os jogadores.
    #["Player",column_tag["regionCode"],"Champion/Function","Year","Month","Week","WeekParts","pick_rate","Wins","win_rate"]
    baseFiltred = filtredData
    tags = filtredData["Champion/Function"].unique(); 
    playerAllResults = []; playerAllResultsForMonth = []
    i = 0; startTime = datetime.datetime.now()
    for tag in tags:
        AllPlayersResults = []; 
        PlayerDirectory = directory+"TaxasDosJogadores\\"+player+"\\"
        playerData = pd.read_csv(PlayerDirectory+"Player_Taxas.csv",encoding="utf-16")
        playerData = playerData[["Player",column_tag["regionCode"],"Champion/Function","Year","Month","Week","WeekParts","pick_rate","Wins","win_rate"]]
        tagData = playerData[playerData["Champion/Function"] == tag]
        regionCode = playerData["regionCode"].unique()
        years = tagData["Year"].unique()
        for player in players:
            for year in years:
                yearData = tagData[tagData["Year"] == year]
                months = yearData["Month"].unique()
                for month in months:
                    monthData = yearData[yearData["Month"] == month]
                    weeks = monthData["Week"].unique(); week_count = len(weeks)

                    part_stat, part_p = shapiro(monthData["WeekParts"]); pick_rate_stat, pick_rate_p = shapiro(monthData["pick_rate"])
                    win_stat, win_p = shapiro(monthData["Wins"]); win_rate_stat, win_rate_p = shapiro(monthData["win_rate"])

                    monthData["ShapiroStat_Parts"] = part_stat; monthData["ShapiroP_Parts"] = part_p
                    monthData["ShapiroStat_Pick_Rate"] = pick_rate_stat; monthData["ShapiroP_Pick_Rate"] = pick_rate_p

                    monthData["ShapiroStat_Wins"] = win_stat; monthData["ShapiroP_Wins"] = win_p
                    monthData["ShapiroStat_Win_Rate"] = win_rate_stat; monthData["ShapiroP_Win_Rate"] = win_rate_p

                    playerAllResults.append(monthData)
                    playerAllResultsForMonth.append(pd.DataFrame({
                        "Player": [player], column_tag["regionCode"] : regionCode, "Champion/Function" : [tag], "Year": [year], "Month": [month],
                        "ShapiroStat_Parts": monthData["ShapiroStat_Parts"].unique(),
                        "ShapiroP_Parts" : monthData["ShapiroP_Parts"].unique(),
                        "ShapiroStat_Pick_Rate": monthData["ShapiroStat_Pick_Rate"].unique(),
                        "ShapiroP_Pick_Rate" : monthData["ShapiroP_Pick_Rate"].unique(),
                        "ShapiroStat_Wins": monthData["ShapiroStat_Wins"].unique(),
                        "ShapiroP_Wins" : monthData["ShapiroP_Wins"].unique(),
                        "ShapiroStat_Win_Rate": monthData["ShapiroStat_Win_Rate"].unique(),
                        "ShapiroP_Win_Rate" : monthData["ShapiroP_Win_Rate"].unique()
                    }))
        playerAllResults:pd.DataFrame = pd.concat(playerAllResults,ignore_index=True)
        playerAllResults.to_csv(PlayerDirectory+"ShapiroWilk_ForAllPlayersStrategy.csv",encoding="utf-16")

        playerAllResultsForMonth:pd.DataFrame = pd.concat(playerAllResultsForMonth,ignore_index=True)
        AllPlayersResults.append(playerAllResultsForMonth)

        i+= 1; ProgressBar("Making Shapiro Test and Make csv ",i,len(players_all),startTime=startTime,end=True) #00:16:38
    startTime = datetime.datetime.now(); ProgressBar("Making all players Shapiro csv...",0,1,startTime=startTime)
    AllPlayersResults:pd.DataFrame = pd.concat(AllPlayersResults,ignore_index=True)
    AllPlayersResults.to_csv(dataBasePath+"ShapiroWilk_ForAllPlayersStrategy.csv",encoding="utf-16")
    ProgressBar("All Players Shapiro csv Maked.",1,1,startTime=startTime,end=True) #00:00:010
    return

players_all = filtredData[column_tag["playerIdentifier"]].unique()
champions_all = filtredData[column_tag["champion"]].unique()
functions_all = filtredData[column_tag["function"]].unique()

print("==============================================================")

print("Start Second Step.")

#players_base = GetAllPlayersBase(players_all)

step_shapiro1 = True
if step_shapiro1:
    ShapiroWilk_ForEachPlayerStrategy(players_all)

step_shapiro2 = True
if step_shapiro2:
    ShapiroWilk_ForAllPlayersStrategy(players_all)

print("==============================================================")
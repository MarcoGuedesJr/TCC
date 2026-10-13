import os #Criar pastas
import csv
import datetime
import pandas as pd
import calendar
from pathlib import Path
from scipy.stats import shapiro
from scipy.stats import pearsonr
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
stepBasePath = dataBasePath+"4º Step\\"

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

functions = ["TOP","JUNGLE","MIDDLE","BOTTOM","UTILITY"]

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

def MakeUnifiquedCsv(players):
    unifiqued_csv = []; i = 0; startTime = datetime.datetime.now()
    for player in players:
        PlayerDirectory = directory+"TaxasDosJogadores\\"+player+"\\"
        playerData = pd.read_csv(PlayerDirectory+"Player_Taxas.csv",encoding="utf-16")
        unifiqued_csv.append(playerData)
        i+= 1; ProgressBar("Making Unifiqued Taxa csv ",i,len(players_all),startTime=startTime,end=True)
    unifiqued_csv = pd.concat(unifiqued_csv,ignore_index=True)
    return unifiqued_csv

def ShapiroWilk_EachPlayerStrategy(base,players):
    #["Player",column_tag["regionCode"],"Champion/Function","Year","Month","Week","WeekParts","pick_rate","Wins","win_rate"]
    AllPlayersResults = []; i = 0; startTime = datetime.datetime.now()
    for player in players:
        PlayerDirectory = directory+"TaxasDosJogadores\\"+player+"\\"
        playerData = base[base["Player"] == player]
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

                    playerAllResults.append(monthData)
                    playerAllResultsForMonth.append(pd.DataFrame({
                        "Player": [player], column_tag["regionCode"] : regionCode, "Champion/Function" : [tag], "Year": [year], "Month": [month],
                        "ShapiroStat_Parts": [round(part_stat,4)],
                        "ShapiroP_Parts" : [round(part_p,4)],
                        "ShapiroStat_Pick_Rate": [round(pick_rate_stat,4)],
                        "ShapiroP_Pick_Rate" : [round(pick_rate_p,4)],
                        "ShapiroStat_Wins": [round(win_stat,4)],
                        "ShapiroP_Wins" : [round(win_p,4)],
                        "ShapiroStat_Win_Rate": [round(win_rate_stat,4)],
                        "ShapiroP_Win_Rate" : [round(win_rate_p,4)]
                    }))
        playerAllResults:pd.DataFrame = pd.concat(playerAllResults,ignore_index=True)
        playerAllResults.to_csv(PlayerDirectory+"ShapiroWilk_EachPlayerStrategy.csv",encoding="utf-16")

        playerAllResultsForMonth:pd.DataFrame = pd.concat(playerAllResultsForMonth,ignore_index=True)
        AllPlayersResults.append(playerAllResultsForMonth)

        i+= 1; ProgressBar("Making ShapiroWilk_EachPlayerStrategy and Make csv ",i,len(players_all),startTime=startTime,end=True) #00:16:38
    startTime = datetime.datetime.now(); ProgressBar("Making all players Shapiro csv...",0,1,startTime=startTime)
    result:pd.DataFrame = pd.concat(AllPlayersResults,ignore_index=True)
    result = SetNormals(result)
    result.to_csv(stepBasePath+"ShapiroWilk_EachPlayerStrategy.csv",encoding="utf-16",index=False)
    ProgressBar("All ShapiroWilk_EachPlayerStrategy csv Maked",1,1,startTime=startTime,end=True) #00:00:010
    return

def ShapiroWilk_EachPlayersAllStrategy(base,players):

    allResultsArray = []; i = 0; startTime = datetime.datetime.now()
    for player in players:
        PlayerDirectory = directory+"TaxasDosJogadores\\"+player+"\\"
        playerData = base[base["Player"] == player]
        playerData = playerData[["Player",column_tag["regionCode"],"Champion/Function","Year","Month","Week","WeekParts","pick_rate","Wins","win_rate"]]
        tags = playerData["Champion/Function"].unique(); regionCode = playerData["regionCode"].unique()
        years = playerData["Year"].unique()
        playerResultArray = []
        for year in years:
            yearData = playerData[playerData["Year"] == year]
            months = yearData["Month"].unique()
            for month in months:
                monthData = yearData[yearData["Month"] == month]; tagNumber = len(monthData["Champion/Function"].unique())
                base_functions = monthData[monthData["Champion/Function"].isin(functions)].copy()
                base_champions = monthData[~monthData["Champion/Function"].isin(functions)].copy()

                playerResultArray.append(MakeSafeShapiro(player,regionCode,year,month,base_functions))
                playerResultArray.append(MakeSafeShapiro(player,regionCode,year,month,base_champions))

        PlayerResult = pd.concat(playerResultArray,ignore_index=True); allResultsArray.append(PlayerResult)
        i+= 1; ProgressBar("Making ShapiroWilk_EachPlayersAllStrategy and Make csv ",i,len(players_all),startTime=startTime,end=True)
    result = pd.concat(allResultsArray,ignore_index=True)
    result = SetNormals(result)
    result.to_csv(stepBasePath+"ShapiroWilk_EachPlayersAllStrategy.csv",encoding="utf-16",index=False)    
    return

def MakeSafeShapiro(player,regionCode,year,month,base):
    tagNumber = len(base["Champion/Function"].unique())
    
    part_stat, part_p = shapiro(base["WeekParts"]); pick_rate_stat, pick_rate_p = shapiro(base["pick_rate"])
    win_stat, win_p = shapiro(base["Wins"]); win_rate_stat, win_rate_p = shapiro(base["win_rate"])

    frame = pd.DataFrame({
        "Player": [player], column_tag["regionCode"] : regionCode, "Champion/Function Number" : [tagNumber], "Year": [year], "Month": [month],
        "ShapiroStat_Parts": [round(part_stat,4)],
        "ShapiroP_Parts" : [round(part_p,4)],
        "ShapiroStat_Pick_Rate": [round(pick_rate_stat,4)],
        "ShapiroP_Pick_Rate" : [round(pick_rate_p,4)],
        "ShapiroStat_Wins": [round(win_stat,4)],
        "ShapiroP_Wins" : [round(win_p,4)],
        "ShapiroStat_Win_Rate": [round(win_rate_stat,4)],
        "ShapiroP_Win_Rate" : [round(win_rate_p,4)]
    })
    return frame

def ShapiroWilk_AllPlayersStrategy(base):#Aqui vamos tirar o shapiro de todos os camps e func com relação a todos os jogadores.
    #["Player",column_tag["regionCode"],"Champion/Function","Year","Month","Week","WeekParts","pick_rate","Wins","win_rate"]
    tags = base["Champion/Function"].unique()
    allResults = []; i = 0; startTime = datetime.datetime.now()
    for tag in tags:
        tagAllResults = []
        tagBase = base[base["Champion/Function"] == tag]
        years = tagBase["Year"].unique()
        for year in years:
            yearBase = tagBase[tagBase["Year"] == year]
            months = yearBase["Month"].unique()
            for month in months:
                monthBase = yearBase[yearBase["Month"] == month]
                player_number = len(monthBase["Player"].unique())
                part_stat, part_p = shapiro(monthBase["WeekParts"]); pick_rate_stat, pick_rate_p = shapiro(monthBase["pick_rate"])
                win_stat, win_p = shapiro(monthBase["Wins"]); win_rate_stat, win_rate_p = shapiro(monthBase["win_rate"])

                tagAllResults.append(pd.DataFrame({
                        "Champion/Function" : [tag], "Year": [year], "Month": [month], "PlayerNumber": [player_number],
                        "ShapiroStat_Parts": [round(part_stat,4)],
                        "ShapiroP_Parts" : [round(part_p,4)],
                        "ShapiroStat_Pick_Rate": [round(pick_rate_stat,4)],
                        "ShapiroP_Pick_Rate" : [round(pick_rate_p,4)],
                        "ShapiroStat_Wins": [round(win_stat,4)],
                        "ShapiroP_Wins" : [round(win_p,4)],
                        "ShapiroStat_Win_Rate": [round(win_rate_stat,4)],
                        "ShapiroP_Win_Rate" : [round(win_rate_p,4)]
                    }))
        tagResult = pd.concat(tagAllResults,ignore_index=True); allResults.append(tagResult)
        i+= 1; ProgressBar("Making ShapiroWilk_AllPlayersStrategy and Make csv ",i,len(tags),startTime=startTime,end=True)
    result:pd.DataFrame = pd.concat(allResults,ignore_index=True)
    result = SetNormals(result)
    result.to_csv(stepBasePath+"ShapiroWilk_AllPlayersStrategy.csv",encoding="utf-16",index=False)        
    return

def SetNormals(base:pd.DataFrame):
    base["normal_parts"] = np.where(base["ShapiroP_Parts"] > 0.05,True,False)
    base["normal_pickRate"] =  np.where(base["ShapiroP_Pick_Rate"] > 0.05,True,False)
    base["normal_wins"] = np.where(base["ShapiroP_Wins"] > 0.05,True,False)
    base["normal_winRate"] = np.where(base["ShapiroP_Win_Rate"] > 0.05,True,False)
    return base

def MakeSpearmanEachPlayerStrategy(base:pd.DataFrame,players):
    allPlayersResults = []; i = 0; startTime = datetime.datetime.now()
    for player in players:
        allTagsResults = []
        PlayerDirectory = directory+"TaxasDosJogadores\\"+player+"\\"
        playerData = base[base["Player"] == player]
        tags = playerData["Champion/Function"].unique(); regionCode = playerData["regionCode"].unique()
        for tag in tags:
            allMonthResults = []
            tagData = playerData[playerData["Champion/Function"] == tag]
            years = tagData["Year"].unique()
            for year in years:
                yearData = tagData[tagData["Year"] == year]
                months = yearData["Month"].unique()
                for month in months:
                    monthData = yearData[yearData["Month"] == month]
                    #SafeCorrelation(data,column1,column2,method="spearman"):
                    pickRateForWinRate = round(SafeCorrelation(monthData,"pick_rate","win_rate"),4)
                    pickRateForWin = round(SafeCorrelation(monthData,"pick_rate","Wins"),4)
                    partsForWinRate = round(SafeCorrelation(monthData,"WeekParts","win_rate"),4)
                    partsForWin = round(SafeCorrelation(monthData,"WeekParts","Wins"),4)
                    allMonthResults.append(pd.DataFrame({
                        "Player": [player], "regionCode": regionCode, "Champion/Function" : [tag], "Year": [year], "Month": [month],
                        "PickRate/WinRate": [pickRateForWinRate],
                        "PickRate/Win" : [pickRateForWin],
                        "Parts/WinRate": [partsForWinRate],
                        "Parts/Win" : [partsForWin],
                    }))
            allMonthResults = pd.concat(allMonthResults,ignore_index=True)
            allTagsResults.append(allMonthResults)
        allTagsResults = pd.concat(allTagsResults,ignore_index=True)
        allTagsResults.to_csv(PlayerDirectory+"SpearmanEachPlayerStrategy.csv",encoding="utf-16",index=True)
        allPlayersResults.append(allTagsResults)
        i+= 1; ProgressBar("Making SpearmanEachPlayerStrategy.csv ",i,len(players_all),startTime=startTime,end=True)
    allPlayersResults = pd.concat(allPlayersResults,ignore_index=True)
    allPlayersResults.to_csv(stepBasePath+"SpearmanEachPlayerStrategy.csv",encoding="utf-16",index=False)
    return

def MakeSpearmanEachPlayersAllStrategy(base:pd.DataFrame,players):
    allPlayersResults = []; i = 0; startTime = datetime.datetime.now()
    for player in players:
        allMonthResults = []
        playerData = base[base["Player"] == player]
        years = playerData["Year"].unique(); regionCode = playerData["regionCode"].unique()
        for year in years:
            yearData = playerData[playerData["Year"] == year]
            months = yearData["Month"].unique()
            for month in months:
                monthData = yearData[yearData["Month"] == month]
                base_functions = monthData[monthData["Champion/Function"].isin(functions)].copy()
                base_champions = monthData[~monthData["Champion/Function"].isin(functions)].copy()

                allMonthResults.append(MakeSafeCorrelation(player,regionCode,year,month,base_functions))
                allMonthResults.append(MakeSafeCorrelation(player,regionCode,year,month,base_champions))
                
        allMonthResults = pd.concat(allMonthResults,ignore_index=True)
        allPlayersResults.append(allMonthResults)
        i+= 1; ProgressBar("Making SpearmanEachPlayersAllStrategy.csv ",i,len(players_all),startTime=startTime,end=True)
    allPlayersResults = pd.concat(allPlayersResults,ignore_index=True)
    allPlayersResults.to_csv(stepBasePath+"SpearmanEachPlayersAllStrategy.csv",encoding="utf-16",index=False)
    return

def MakeSpearmanAllPlayersStrategy(base:pd.DataFrame):
    allPlayersResults = []; i = 0; startTime = datetime.datetime.now()
    tags = base["Champion/Function"].unique()
    for tag in tags:
        allMonthResults = []
        tagData = base[base["Champion/Function"] == tag]
        years = tagData["Year"].unique(); regionCode = tagData["regionCode"].unique()
        for year in years:
            yearData = tagData[tagData["Year"] == year]
            months = yearData["Month"].unique()
            for month in months:
                monthData = yearData[yearData["Month"] == month]
                #SafeCorrelation(data,column1,column2,method="spearman"):
                player_number = len(monthData["Player"].unique())
                pickRateForWinRate = round(SafeCorrelation(monthData,"pick_rate","win_rate"),4)
                pickRateForWin = round(SafeCorrelation(monthData,"pick_rate","Wins"),4)
                partsForWinRate = round(SafeCorrelation(monthData,"WeekParts","win_rate"),4)
                partsForWin = round(SafeCorrelation(monthData,"WeekParts","Wins"),4)
                allMonthResults.append(pd.DataFrame({
                    "Champion/Function" : [tag], "Year": [year], "Month": [month], "PlayerNumber" : [player_number],
                    "PickRate/WinRate": [pickRateForWinRate],
                    "PickRate/Win" : [pickRateForWin],
                    "Parts/WinRate": [partsForWinRate],
                    "Parts/Win" : [partsForWin],
                }))
        allMonthResults = pd.concat(allMonthResults,ignore_index=True)
        allPlayersResults.append(allMonthResults)
        i+= 1; ProgressBar("Making SpearmanAllPlayersStrategy csv ",i,len(tags),startTime=startTime,end=True)
    allPlayersResults = pd.concat(allPlayersResults,ignore_index=True)
    allPlayersResults.to_csv(stepBasePath+"SpearmanAllPlayersStrategy.csv",encoding="utf-16",index=False)
    return

def SafeCorrelation(data,column1,column2,method="spearman"):
    valid_data = data[[column1, column2]].dropna()

    if len(valid_data) < 2:
        return float("nan")

    if (valid_data[column1].nunique() < 2 or valid_data[column2].nunique() < 2):
        return float("nan")
    
    return data[column1].corr(data[column2],method=method)

def MakeSafeCorrelation(player,regionCode,year,month,base):
    tagNumber = len(base["Champion/Function"].unique())
    #SafeCorrelation(data,column1,column2,method="spearman"):
    pickRateForWinRate = round(SafeCorrelation(base,"pick_rate","win_rate"),4)
    pickRateForWin = round(SafeCorrelation(base,"pick_rate","Wins"),4)
    partsForWinRate = round(SafeCorrelation(base,"WeekParts","win_rate"),4)
    partsForWin = round(SafeCorrelation(base,"WeekParts","Wins"),4)
    frame = pd.DataFrame({
        "Player": [player], "regionCode": regionCode, "Champion/Function Numb" : [tagNumber], "Year": [year], "Month": [month],
        "PickRate/WinRate": [pickRateForWinRate],
        "PickRate/Win" : [pickRateForWin],
        "Parts/WinRate": [partsForWinRate],
        "Parts/Win" : [partsForWin],
    })
    return frame

players_all = filtredData[column_tag["playerIdentifier"]].unique()
champions_all = filtredData[column_tag["champion"]].unique()
functions_all = filtredData[column_tag["function"]].unique()

print("==============================================================")

print("Start Second Step.")

#players_base = GetAllPlayersBase(players_all)
unifiqued_csv = unifiqued_csv = MakeUnifiquedCsv(players_all) #00:02:24
os.makedirs(dataBasePath+"4º Step", exist_ok=True)
step_shapiro1 = True
if step_shapiro1:
    shap1 = ShapiroWilk_EachPlayerStrategy(unifiqued_csv,players_all) #00:19:38
step_shapiro2 = True
if step_shapiro2:
    shap2 = ShapiroWilk_EachPlayersAllStrategy(unifiqued_csv,players_all) #00:08:06 ~ 00:08:26
step_shapiro3 = True
if step_shapiro3:
    shap3 = ShapiroWilk_AllPlayersStrategy(unifiqued_csv) #00:00:08

step_MakeSpearman1 = True
if step_MakeSpearman1:
    MakeSpearmanEachPlayerStrategy(unifiqued_csv,players_all) #00:16:31 ~ 00:20:05
step_MakeSpearman2 = True
if step_MakeSpearman2:
    MakeSpearmanEachPlayersAllStrategy(unifiqued_csv,players_all) #00:08:20 ~ 00:08:26
step_MakeSpearman3 = True
if step_MakeSpearman3:
    MakeSpearmanAllPlayersStrategy(unifiqued_csv) #00:00:11

print("==============================================================")
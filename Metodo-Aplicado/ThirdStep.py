import os #Criar pastas
import csv
import datetime
import pandas as pd
import calendar
from pathlib import Path
#from sklearn.cluster import KMeans
import numpy as np

#contagem = df['categoria'].value_counts()
#df = df[df['categoria'].isin(contagem[contagem >= 3].index)]

#df = df[df["coluna"] == playerName]

#pd.to_datetime

#from sklearn.cluster import KMeans
#import numpy as np

#from sklearn.tree import DecisionTreeClassifier

directory = "C:\\Users\\marco\\Documents\\TCC\\Metodo-Aplicado\\"
dataBasePath = directory+"\\DataBase\\"

dataBaseFiltred = "LOL_2023_Filtred.csv"
filtredData = pd.read_csv(dataBasePath+dataBaseFiltred)
filtredData["gameEndTimestampToDate"] = pd.to_datetime(filtredData["gameEndTimestampToDate"])

updateCount = 0

column_tag = {
    "player" : "summonerName",
    "champion" : "championName",
    "function" : "individualPosition"
}

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

#This is a generic function created to make CSV for the Champions and Functions just change the values.
def CreateVectors(base,player_tag,dir):
    tags = base["Champion/Function"].unique()
    for tag in tags:
        tagData = base[base["Champion/Function"] == tag]
        years = tagData["Year"].unique()
        for year in years:
            yearData = tagData[tagData["Year"] == year]
            months = yearData["Month"].unique()
            for month in months:
                monthData = yearData[yearData["Month"] == month]

                partidas_totais = monthData["WeekParts"].sum()
                
                taxa_min_escolha = round(monthData["pick_rate"].min(),2)
                taxa_max_escolha = round(monthData["pick_rate"].max(),2)
                taxa_delta_vitoria = round(taxa_max_escolha - taxa_min_escolha,2)
                #["Player","Champion/Function","Year","Month","parts","rate_min","rate_max","rate_delta"]
                UpdateCSV(os.path.join(dir+"PlayerVector_Escolha.csv"),
                          [player_tag,        #Player
                           tag,               #Champion/Function
                           year,              #Year
                           month,             #Month
                           partidas_totais,   #parts
                           taxa_min_escolha,  #rate_min
                           taxa_max_escolha,  #rate_max
                           taxa_delta_vitoria #rate_delta
                           ],0,False)
                                
                taxa_min_vitoria = round(monthData["win_rate"].min(),2)
                taxa_max_vitoria = round(monthData["win_rate"].max(),2)
                taxa_delta_vitoria = round(taxa_max_vitoria - taxa_min_vitoria,2)
                #["Player","Champion/Function","Year","Month","parts","rate_min","rate_max","rate_delta"]
                UpdateCSV(os.path.join(dir+"PlayerVector_Win.csv"),
                          [player_tag,        #Player
                           tag,               #Champion/Function
                           year,              #Year
                           month,             #Month
                           partidas_totais,   #parts
                           taxa_min_vitoria,  #rate_min
                           taxa_max_vitoria,  #rate_max
                           taxa_delta_vitoria #rate_delta
                           ],0,False)
                #kmeans_escolha = KMeans(n_clusters=3,random_state=42)
                #kmeans_vitoria = KMeans(n_clusters=3,random_state=42)

#This Function is used for makin path and create all CSV about champions and functions of player.
def CreateVectorsForPlayers(player_name):

    playerDirectory = directory+"TaxasDosJogadores\\"+player_name+"\\"
    #print("Player Path: "+playerDirectory+"Player_Taxas.csv")
    #player = filtredData[filtredData["summonerName"] == player_name]
    player = pd.read_csv(playerDirectory+"Player_Taxas.csv",encoding="utf-16")

    os.makedirs(directory+"TaxasDosJogadores", exist_ok=True)
    os.makedirs(directory+"TaxasDosJogadores\\"+player_name,exist_ok=True)
    #C:\Users\marco\Documents\TCC\Metodo-Aplicado\\Player_4
    CreateCSV(os.path.join(playerDirectory,"PlayerVector_Escolha.csv"),["Player","Champion/Function","Year","Month","parts","rate_min","rate_max","rate_delta"])
    CreateCSV(os.path.join(playerDirectory,"PlayerVector_Win.csv"),["Player","Champion/Function","Year","Month","parts","rate_min","rate_max","rate_delta"])

    CreateVectors(player,player_name,playerDirectory)

players_all = filtredData["summonerName"].unique()

print("==============================================================")
print("Start Second Step.")
i = 0
for player in players_all:
    CreateVectorsForPlayers(player)
    i+= 1; ProgressBar("Analysis in ",i,len(players_all),end=True)
print("==============================================================")
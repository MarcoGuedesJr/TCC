import os #Criar pastas
import csv
import datetime
import pandas as pd
import calendar
from pathlib import Path
from sklearn.cluster import KMeans
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
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

def GetVectorForAllPlayers(players):

    first = True
    all_vector = { "escolha" : None, "win" : None}
    i = 0; startTime = datetime.datetime.now()

    CreateCSV(os.path.join(dataBasePath,"Players_Vector_Escolha.csv"),["Player","Champion/Function","Year","Month","parts","rate_min","rate_max","rate_delta"])
    CreateCSV(os.path.join(dataBasePath,"Players_Vector_Win.csv"),["Player","Champion/Function","Year","Month","parts","rate_min","rate_max","rate_delta"])
    for player in players:
        i += 1
        playerDirectory = directory+"TaxasDosJogadores\\"+player+"\\"
        targetVector_escolhas = pd.read_csv(playerDirectory+"PlayerVector_Escolha.csv",encoding="utf-16")
        targetVector_win = pd.read_csv(playerDirectory+"PlayerVector_Win.csv",encoding="utf-16")

        if first: all_vector["escolha"] = targetVector_escolhas; all_vector["win"] = targetVector_win; first = False; continue

        all_vector["escolha"] = pd.concat([all_vector["escolha"],targetVector_escolhas],ignore_index=True)
        all_vector["win"] = pd.concat([all_vector["win"],targetVector_win],ignore_index=True)

        ProgressBar("Making unifiqued vectors csv ",i,len(players_all),startTime=startTime,end=True)

    all_vector["escolha"].to_csv(dataBasePath+"Players_Vector_Escolha.csv", index=False)
    all_vector["win"].to_csv(dataBasePath+"Players_Vector_Win.csv", index=False)

    return all_vector

def ClusterKmeans(vectors):
    k = 3; kmeans = KMeans(n_clusters = k, random_state=42)

    min_parts = 2
    enable_vectors = vectors[vectors["parts"] >= min_parts].copy()
    disable_vectors = vectors[vectors["parts"] < min_parts].copy()

    distinct_vectors = len(enable_vectors[clustersColumns].drop_duplicates())
    month_enable = distinct_vectors >= k

    if month_enable:
        kmeans.fit(enable_vectors[clustersColumns])
        enable_vectors["cluster"] = kmeans.labels_
    else:
        enable_vectors["cluster"] = -1
    disable_vectors["cluster"] = -1

    if month_enable:
        clusters_med = {
            0: round(enable_vectors[enable_vectors["cluster"] == 0]["rate_max"].mean(), 2),
            1: round(enable_vectors[enable_vectors["cluster"] == 1]["rate_max"].mean(), 2),
            2: round(enable_vectors[enable_vectors["cluster"] == 2]["rate_max"].mean(), 2)}
        ordered_clusters = sorted(clusters_med,key=clusters_med.get)
        cluster_names = {
            ordered_clusters[0]: "Low",
            ordered_clusters[1]: "Average",
            ordered_clusters[2]: "High"}
        enable_vectors["clusterLabel"] = enable_vectors["cluster"].map(cluster_names)
    else:
        enable_vectors["clusterLabel"] = "Minimum Variation Not Reached"
        print("Vetor Disable:"); print(disable_vectors)
        print("Vetor Enable:"); print(enable_vectors); vectors = enable_vectors

    if len(disable_vectors) != 0:
        disable_vectors["clusterLabel"] = "Minimum Parts Not Reached"
        #print("Vetor Disable:"); print(disable_vectors)
        vectors = pd.concat([enable_vectors,disable_vectors],ignore_index=True)

    if month_enable != True: print("Vetor Complet:"); print(vectors)
    return vectors

def ClusterStep(players_vectors,players_all,champions_all,functions_all):
    vector_escolhas = players_vectors["escolha"]
    vector_wins = players_vectors["win"]

    all_tags = np.concatenate((champions_all,functions_all))

    first = True
    models_escolhas:pd.DataFrame = None; models_wins:pd.DataFrame = None
    i = 0; startTime = datetime.datetime.now()
    for tag in all_tags:
        i+= 1
        tagVector_escolhas = vector_escolhas[vector_escolhas["Champion/Function"] == tag]
        tagVector_wins = vector_wins[vector_wins["Champion/Function"] == tag]
        years = tagVector_escolhas["Year"].unique()
        for year in years:
            yearVector_escolhas = tagVector_escolhas[tagVector_escolhas["Year"] == year]
            yearVector_wins = tagVector_wins[tagVector_wins["Year"] == year]
            months = yearVector_escolhas["Month"].unique()
            for month in months:
                monthVector_escolhas = yearVector_escolhas[yearVector_escolhas["Month"] == month]
                monthVector_wins = yearVector_wins[yearVector_wins["Month"] == month]
                if first: models_escolhas = ClusterKmeans(monthVector_escolhas); models_wins = ClusterKmeans(monthVector_wins); first = False
                models_escolhas = pd.concat([models_escolhas,ClusterKmeans(monthVector_escolhas)],ignore_index=True)
                models_wins = pd.concat([models_wins,ClusterKmeans(monthVector_wins)],ignore_index=True)
        ProgressBar("Making Clusters is in ",i,len(all_tags),startTime=startTime,end=True)

    results = {
        "escolha" : models_escolhas,
        "win" : models_wins
    }
    models_escolhas.to_csv(dataBasePath+"Players_Vector_Escolha.csv", index=False)
    models_wins.to_csv(dataBasePath+"Players_Vector_Win.csv", index=False)
    return results

def RandomTree(vectors):
    tree = RandomForestClassifier(n_estimators=100,random_state=42)

    min_parts = 2
    enable_vectors = vectors[vectors["cluster"] != -1].copy() #Separa os vetores que de fato vamos utilizar.
    disable_vectors = vectors[vectors["cluster"] == -1].copy() #Separa os vetores que não passaram pela verificação do K-Means
                                                               #ou seja, foram "excluidos".

    distinct_vectors = enable_vectors[treeColumn].nunique()
    month_enable = distinct_vectors >= 3

    if month_enable:
        x = enable_vectors[clustersColumns]; y = enable_vectors[treeColumn]
        tree.fit(x,y)
        enable_vectors["classifierLabel"] = tree.predict(x)

    if len(disable_vectors) > 0:
        disable_vectors["classifierLabel"] = disable_vectors["clusterLabel"]
        vectors = pd.concat([enable_vectors,disable_vectors],ignore_index=True)

    if month_enable != True: print("Vetor Complet:"); print(vectors)
    return vectors

def TreeStep(players_vectors,players_all,champions_all,functions_all):
    vector_escolhas = players_vectors["escolha"]
    vector_wins = players_vectors["win"]

    all_tags = np.concatenate((champions_all,functions_all))

    first = True
    models_escolhas:pd.DataFrame = None; models_wins:pd.DataFrame = None
    i = 0; startTime = datetime.datetime.now()
    for tag in all_tags:
        i+= 1
        tagVector_escolhas = vector_escolhas[vector_escolhas["Champion/Function"] == tag]
        tagVector_wins = vector_wins[vector_wins["Champion/Function"] == tag]
        years = tagVector_escolhas["Year"].unique()
        for year in years:
            yearVector_escolhas = tagVector_escolhas[tagVector_escolhas["Year"] == year]
            yearVector_wins = tagVector_wins[tagVector_wins["Year"] == year]
            months = yearVector_escolhas["Month"].unique()
            for month in months:
                monthVector_escolhas = yearVector_escolhas[yearVector_escolhas["Month"] == month]
                monthVector_wins = yearVector_wins[yearVector_wins["Month"] == month]

                if first: models_escolhas = RandomTree(monthVector_escolhas); models_wins = RandomTree(monthVector_wins); first = False
                
                models_escolhas = pd.concat([models_escolhas,RandomTree(monthVector_escolhas)],ignore_index=True)
                models_wins = pd.concat([models_wins,RandomTree(monthVector_wins)],ignore_index=True)
        ProgressBar("Making Random Florest is in ",i,len(all_tags),startTime=startTime,end=True)

    results = {
        "escolha" : models_escolhas,
        "win" : models_wins
    }
    models_escolhas.to_csv(dataBasePath+"Players_Vector_Escolha.csv", index=False)
    models_wins.to_csv(dataBasePath+"Players_Vector_Win.csv", index=False)
    return results

players_all = filtredData[column_tag["playerIdentifier"]].unique()
champions_all = filtredData[column_tag["champion"]].unique()
functions_all = filtredData[column_tag["function"]].unique()

print("==============================================================")

print("Start Second Step.")
i = 0; startTime = datetime.datetime.now()
for player in players_all:
    #CreateVectorsForPlayers(player)
    i+= 1; ProgressBar("Analysis in ",i,len(players_all),startTime=startTime,end=True) #00:08:46 ~ 00:14:59

#players_vectors = GetVectorForAllPlayers(players_all) #00:06:17 ~ 00:08:03
players_vectors = { "escolha" : pd.read_csv(dataBasePath+"Players_Vector_Escolha.csv"), "win" : pd.read_csv(dataBasePath+"Players_Vector_Win.csv")}
players_vectors["escolha"] = players_vectors["escolha"][["Player","Champion/Function","Year","Month","parts","rate_min","rate_max","rate_delta"]]
players_vectors["win"] = players_vectors["win"][["Player","Champion/Function","Year","Month","parts","rate_min","rate_max","rate_delta"]]

#player_models = ClusterStep(players_vectors,players_all,champions_all,functions_all) #00:00:33 ~ 00:01:24
player_models = { "escolha" : pd.read_csv(dataBasePath+"Players_Vector_Escolha.csv"), "win" : pd.read_csv(dataBasePath+"Players_Vector_Win.csv")}
player_models["escolha"] = player_models["escolha"][["Player","Champion/Function","Year","Month","parts","rate_min","rate_max","rate_delta","cluster","clusterLabel"]]
player_models["win"] = player_models["win"][["Player","Champion/Function","Year","Month","parts","rate_min","rate_max","rate_delta","cluster","clusterLabel"]]

player_tree = TreeStep(player_models,players_all,champions_all,functions_all)

print("==============================================================")
import os #Criar pastas
import csv
import datetime
import pandas as pd
import calendar
from pathlib import Path
from sklearn.cluster import KMeans
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
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
stepBasePath = dataBasePath+"3º Step\\"

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

clustersColumns = ["parts","score_min","score_max","score_delta"]
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
def SaveVector(data,colum,player_tag,tag,year,month,partidas_totais,dir,name):
    score_min = round(data[colum].min(),2)
    score_max = round(data[colum].max(),2)
    score_delta = round(score_max - score_min,2)
    #["Player","Champion/Function","Year","Month","parts","rate_min","rate_max","rate_delta"]
    UpdateCSV(os.path.join(dir+name+".csv"),
              [player_tag,        #Player
               tag,               #Champion/Function
               year,              #Year
               month,             #Month
               partidas_totais,   #parts
               score_min,  #score_min
               score_max,  #score_max
               score_delta #score_delta
               ],0,False)
    return True
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

                #data,colum,player_tag,tag,year,month,partidas_totais,dir
                SaveVector(monthData,"pick_rate",player_tag,tag,year,month,partidas_totais,dir,"PlayerVector_Escolha") #Pick_Rate
                SaveVector(monthData,"win_rate",player_tag,tag,year,month,partidas_totais,dir,"PlayerVector_WinTaxa") #Win_Rate
                SaveVector(monthData,"Wins",player_tag,tag,year,month,partidas_totais,dir,"PlayerVector_WinValue") #Win Value

#This Function is used for makin path and create all CSV about champions and functions of player.
def CreateVectorsForPlayers(player_name):

    playerDirectory = directory+"TaxasDosJogadores\\"+player_name+"\\"
    player = pd.read_csv(playerDirectory+"Player_Taxas.csv",encoding="utf-16")

    os.makedirs(directory+"TaxasDosJogadores", exist_ok=True)
    os.makedirs(directory+"TaxasDosJogadores\\"+player_name,exist_ok=True)
    #C:\Users\marco\Documents\TCC\Metodo-Aplicado\\Player_4
    CreateCSV(os.path.join(playerDirectory,"PlayerVector_Escolha.csv"),["Player","Champion/Function","Year","Month","parts","score_min","score_max","score_delta"])
    CreateCSV(os.path.join(playerDirectory,"PlayerVector_WinTaxa.csv"),["Player","Champion/Function","Year","Month","parts","score_min","score_max","score_delta"])
    CreateCSV(os.path.join(playerDirectory,"PlayerVector_WinValue.csv"),["Player","Champion/Function","Year","Month","parts","score_min","score_max","score_delta"])

    CreateVectors(player,player_name,playerDirectory)

def GetVectorForAllPlayers(players):

    first = True
    all_vector = { "escolha" : None, "win" : None}
    i = 0; startTime = datetime.datetime.now()

    CreateCSV(os.path.join(stepBasePath,"Players_Vector_Escolha.csv"),["Player","Champion/Function","Year","Month","parts","score_min","score_max","score_delta"])
    CreateCSV(os.path.join(stepBasePath,"Players_Vector_WinTaxa.csv"),["Player","Champion/Function","Year","Month","parts","score_min","score_max","score_delta"])
    CreateCSV(os.path.join(stepBasePath,"Players_Vector_WinValue.csv"),["Player","Champion/Function","Year","Month","parts","score_min","score_max","score_delta"])

    for player in players:
        i += 1
        playerDirectory = directory+"TaxasDosJogadores\\"+player+"\\"
        targetVector_escolhas = pd.read_csv(playerDirectory+"PlayerVector_Escolha.csv",encoding="utf-16")
        targetVector_winTaxa = pd.read_csv(playerDirectory+"PlayerVector_WinTaxa.csv",encoding="utf-16")
        targetVector_winValue = pd.read_csv(playerDirectory+"PlayerVector_WinValue.csv",encoding="utf-16")

        if first: 
            all_vector["escolha"] = targetVector_escolhas; all_vector["winTaxa"] = targetVector_winTaxa; all_vector["winValue"] = targetVector_winValue
            first = False; continue

        all_vector["escolha"] = pd.concat([all_vector["escolha"],targetVector_escolhas],ignore_index=True)
        all_vector["winTaxa"] = pd.concat([all_vector["winTaxa"],targetVector_winTaxa],ignore_index=True)
        all_vector["winValue"] = pd.concat([all_vector["winValue"],targetVector_winValue],ignore_index=True)

        ProgressBar("Making unifiqued vectors csv ",i,len(players_all),startTime=startTime,end=True)

    all_vector["escolha"].to_csv(stepBasePath+"Players_Vector_Escolha.csv", index=False)
    all_vector["winTaxa"].to_csv(stepBasePath+"Players_Vector_WinTaxa.csv", index=False)
    all_vector["winValue"].to_csv(stepBasePath+"Players_Vector_WinValue.csv", index=False)

    return all_vector

def ClusterKmeans(vectors):
    k = 3; kmeans = KMeans(n_clusters = k, random_state=42)

    min_parts = 1
    enable_vectors = vectors[vectors["parts"] >= min_parts].copy()
    disable_vectors = vectors[vectors["parts"] < min_parts].copy()

    distinct_vectors = len(enable_vectors[clustersColumns].drop_duplicates())
    month_enable = distinct_vectors >= k

    if month_enable:
        kmeans.fit(enable_vectors[clustersColumns])
        enable_vectors["cluster"] = kmeans.labels_
        clusters_med = {
            0: round(enable_vectors[enable_vectors["cluster"] == 0]["score_max"].mean(), 2),
            1: round(enable_vectors[enable_vectors["cluster"] == 1]["score_max"].mean(), 2),
            2: round(enable_vectors[enable_vectors["cluster"] == 2]["score_max"].mean(), 2)}
        ordered_clusters = sorted(clusters_med,key=clusters_med.get)
        cluster_names = {
            ordered_clusters[0]: "Low",
            ordered_clusters[1]: "Average",
            ordered_clusters[2]: "High"}
        enable_vectors["clusterLabel"] = enable_vectors["cluster"].map(cluster_names)
    else:
        enable_vectors["cluster"] = -1
        enable_vectors["clusterLabel"] = "Minimum Variation Not Reached"
        #print("Vetor Disable:"); print(disable_vectors)
        #print("Vetor Enable:"); print(enable_vectors); vectors = enable_vectors


    if len(disable_vectors) != 0:
        disable_vectors["cluster"] = -1
        disable_vectors["clusterLabel"] = "Minimum Parts Not Reached"
        #print("Vetor Disable:"); print(disable_vectors)
        vectors = pd.concat([enable_vectors,disable_vectors],ignore_index=True)
    else:
        vectors = enable_vectors
    #if month_enable != True: print("Vetor Complet:"); print(vectors)
    return vectors

def ClusterStep(players_vectors,players_all,champions_all,functions_all):
    vector_escolhas = players_vectors["escolha"]
    vector_winsTaxa = players_vectors["winTaxa"]
    vector_winsValue = players_vectors["winValue"]

    all_tags = np.concatenate((champions_all,functions_all))

    first = True
    #models_escolhas:pd.DataFrame = None; models_wins:pd.DataFrame = None
    models_escolhas = []; models_winsTaxa = []; models_winsValue = [] 
    i = 0; startTime = datetime.datetime.now()
    for tag in all_tags:
        i+= 1
        tagVector_escolhas = vector_escolhas[vector_escolhas["Champion/Function"] == tag]
        tagVector_winsTaxa = vector_winsTaxa[vector_winsTaxa["Champion/Function"] == tag]
        tagVector_winsValue = vector_winsValue[vector_winsValue["Champion/Function"] == tag]
        years = sorted(tagVector_escolhas["Year"].unique())
        for year in years:
            yearVector_escolhas = tagVector_escolhas[tagVector_escolhas["Year"] == year]
            yearVector_winsTaxa = tagVector_winsTaxa[tagVector_winsTaxa["Year"] == year]
            yearVector_winsValue = tagVector_winsValue[tagVector_winsValue["Year"] == year]
            months = sorted(yearVector_escolhas["Month"].unique())
            for month in months:
                monthVector_escolhas = yearVector_escolhas[yearVector_escolhas["Month"] == month]
                monthVector_winsTaxa = yearVector_winsTaxa[yearVector_winsTaxa["Month"] == month]
                monthVector_winsValue = yearVector_winsValue[yearVector_winsValue["Month"] == month]
                
                #if first: models_escolhas = ClusterKmeans(monthVector_escolhas); models_wins = ClusterKmeans(monthVector_wins); first = False
                #models_escolhas = pd.concat([models_escolhas,ClusterKmeans(monthVector_escolhas)],ignore_index=True)
                #models_wins = pd.concat([models_wins,ClusterKmeans(monthVector_wins)],ignore_index=True)
                models_escolhas.append(ClusterKmeans(monthVector_escolhas))
                models_winsTaxa.append(ClusterKmeans(monthVector_winsTaxa))
                models_winsValue.append(ClusterKmeans(monthVector_winsValue))
        ProgressBar("Making Clusters is in ",i,len(all_tags),startTime=startTime,end=True)

    models_escolhas = pd.concat(models_escolhas,ignore_index=True)
    models_winsTaxa = pd.concat(models_winsTaxa,ignore_index=True)
    models_winsValue = pd.concat(models_winsValue,ignore_index=True)

    results = {
        "escolha" : models_escolhas,
        "winTaxas" : models_winsTaxa,
        "winValue" : models_winsValue
    }
    models_escolhas.to_csv(stepBasePath+"Players_Vector_Escolha.csv", index=False)
    models_winsTaxa.to_csv(stepBasePath+"Players_Vector_WinTaxa.csv", index=False)
    models_winsValue.to_csv(stepBasePath+"Players_Vector_WinValue.csv", index=False)
    return results

def RandomTree(allVectors,vectors):
    tree = RandomForestClassifier(n_estimators=100,random_state=42)

    enable_vectors = vectors[vectors["cluster"] != -1].copy() #Separa os vetores que de fato vamos utilizar.
    disable_vectors = vectors[vectors["cluster"] == -1].copy() #Separa os vetores que não passaram pela verificação do K-Means
                                                               #ou seja, foram "excluidos".

    distinct_vectors = enable_vectors[treeColumn].nunique()
    month_enable = distinct_vectors >= 3

    if month_enable:
        x = enable_vectors[clustersColumns]; y = enable_vectors[treeColumn]
        tree.fit(x,y)
        enable_vectors["classifierLabel"] = tree.predict(x)
        m = Ensemble(allVectors,enable_vectors)

        allVectors = m["all_vectors"]; enable_vectors = m["vectors"]

    if len(disable_vectors) > 0:
        disable_vectors["classifierLabel"] = disable_vectors["clusterLabel"]
        disable_vectors["ensemble"] = disable_vectors["clusterLabel"]
        vectors = pd.concat([enable_vectors,disable_vectors],ignore_index=True)
    else:
        vectors = enable_vectors

    #if month_enable != True: print("Vetor Complet:"); print(vectors)

    r = {"all_vectors" : allVectors, "vectors": vectors}
    return r

def Ensemble(allVectors,vectors):

    allVectors.append(vectors)
    training = pd.concat(allVectors,ignore_index=True)

    x = training[clustersColumns]
    y = training["classifierLabel"]


    randomFlorest = RandomForestClassifier(random_state=42)
    decisionTree = DecisionTreeClassifier(random_state=42)
    logisticRegression = LogisticRegression(max_iter=1000)

    model = VotingClassifier(estimators=[("randomFlorest",randomFlorest),
                                         ("decisionTree",decisionTree),
                                         ("logisticRegression",logisticRegression)],voting="hard")

    model.fit(x,y)

    vectors["ensemble"] = model.predict(vectors[clustersColumns])

    m = { "all_vectors": allVectors, "vectors": vectors }
    return m

def TreeStep(players_vectors,players_all,champions_all,functions_all):
    vector_escolhas = players_vectors["escolha"]
    vector_winTaxa = players_vectors["winTaxa"]
    vector_winValue = players_vectors["winValue"]

    all_tags = np.concatenate((champions_all,functions_all))
    models_escolhas = []; models_winTaxa = []; models_winValue = []
    i = 0; startTime = datetime.datetime.now()
    for tag in all_tags:
        i+= 1; allVectors_escolha = []; allVectors_winTaxa = []; allVectors_winValue = []
        tagVector_escolhas = vector_escolhas[vector_escolhas["Champion/Function"] == tag]
        tagVector_winTaxa = vector_winTaxa[vector_winTaxa["Champion/Function"] == tag]
        tagVector_winValue = vector_winValue[vector_winValue["Champion/Function"] == tag]
        years = sorted(tagVector_escolhas["Year"].unique())
        for year in years:
            yearVector_escolhas = tagVector_escolhas[tagVector_escolhas["Year"] == year]
            yearVector_winTaxa = tagVector_winTaxa[tagVector_winTaxa["Year"] == year]
            yearVector_winValue = tagVector_winValue[tagVector_winValue["Year"] == year]
            months = sorted(yearVector_escolhas["Month"].unique())
            for month in months:
                monthVector_escolhas = yearVector_escolhas[yearVector_escolhas["Month"] == month]
                monthVector_winTaxa = yearVector_winTaxa[yearVector_winTaxa["Month"] == month]
                monthVector_winValue = yearVector_winValue[yearVector_winValue["Month"] == month]

                duplicates = monthVector_escolhas[monthVector_escolhas.duplicated(subset=["Player","Champion/Function","Year","Month"],keep=False)]
                if not duplicates.empty:print("Duplicates:");print(duplicates)

                dup_vector_escolhas = monthVector_escolhas[monthVector_escolhas.duplicated(keep=False)]
                if not dup_vector_escolhas.empty:print("Duplicates Escolha Vector:");print(dup_vector_escolhas)

                dup_vector_winTaxa = monthVector_winTaxa[monthVector_winTaxa.duplicated(keep=False)]
                if not dup_vector_winTaxa.empty: print("Duplicates Win Vector:"); print(dup_vector_winTaxa)

                dup_vector_winValue = monthVector_winValue[monthVector_winValue.duplicated(keep=False)]
                if not dup_vector_winValue.empty: print("Duplicates Win Vector:"); print(dup_vector_winValue)

                m1 = RandomTree(allVectors_escolha,monthVector_escolhas)
                m2 = RandomTree(allVectors_winTaxa,monthVector_winTaxa)
                m3 = RandomTree(allVectors_winValue,monthVector_winValue)

                for name, df in [("m1 Escolha", m1["vectors"]),("m2 WinTaxa", m2["vectors"]),("m3 WinValue", m3["vectors"])]:
                    duplicates = df[df.duplicated(subset=["Player", "Champion/Function", "Year", "Month"],keep=False)]
                    if not duplicates.empty:
                        print(f"\nDUPLICATAS DEPOIS DO RandomTree: {name}")
                        print(duplicates)

                allVectors_escolha = m1["all_vectors"]; allVectors_winTaxa = m2["all_vectors"]; allVectors_winValue = m3["all_vectors"]
                models_escolhas.append(m1["vectors"]); models_winTaxa.append(m2["vectors"]); models_winValue.append(m3["vectors"])
        ProgressBar("Making Random Florest is in ",i,len(all_tags),startTime=startTime,end=True)
    
    models_escolhas = pd.concat(models_escolhas,ignore_index=True)
    models_winTaxa = pd.concat(models_winTaxa,ignore_index=True)
    models_winValue = pd.concat(models_winValue,ignore_index=True)

    results = {
        "escolha" : models_escolhas,
        "winTaxas" : models_winTaxa,
        "winValue" : models_winValue
    }
    models_escolhas.to_csv(stepBasePath+"Players_Vector_Escolha.csv",index=False)
    models_winTaxa.to_csv(stepBasePath+"Players_Vector_WinTaxa.csv",index=False)
    models_winValue.to_csv(stepBasePath+"Players_Vector_WinValue.csv",index=False)
    return results

players_all = filtredData[column_tag["playerIdentifier"]].unique()
champions_all = filtredData[column_tag["champion"]].unique()
functions_all = filtredData[column_tag["function"]].unique()

print("==============================================================")

print("Start Second Step.")
i = 0; startTime = datetime.datetime.now()
os.makedirs(dataBasePath+"3º Step", exist_ok=True)

step_mak_vectors = True
if step_mak_vectors:
    for player in players_all:
        CreateVectorsForPlayers(player) #00:12:07 ~ 00:14:59
        i+= 1; ProgressBar("Analysis in ",i,len(players_all),startTime=startTime,end=True)

step_allVectors = True
if step_allVectors:
    GetVectorForAllPlayers(players_all) #00:06:17 ~ 00:17:46

step_cluster = True
if step_cluster:
    players_vectors = { 
        "escolha" : pd.read_csv(stepBasePath+"Players_Vector_Escolha.csv"),
        "winTaxa" : pd.read_csv(stepBasePath+"Players_Vector_WinTaxa.csv"),
        "winValue" : pd.read_csv(stepBasePath+"Players_Vector_WinValue.csv")}
    players_vectors["escolha"] = players_vectors["escolha"][["Player","Champion/Function","Year","Month","parts","score_min","score_max","score_delta"]]
    players_vectors["winTaxa"] = players_vectors["winTaxa"][["Player","Champion/Function","Year","Month","parts","score_min","score_max","score_delta"]]
    players_vectors["winValue"] = players_vectors["winValue"][["Player","Champion/Function","Year","Month","parts","score_min","score_max","score_delta"]]

    player_models = ClusterStep(players_vectors,players_all,champions_all,functions_all) #00:00:33 ~ 00:01:24

step_tree = True
if step_tree:
    player_models = {
        "escolha" : pd.read_csv(stepBasePath+"Players_Vector_Escolha.csv"),
        "winTaxa" : pd.read_csv(stepBasePath+"Players_Vector_WinTaxa.csv"),
        "winValue" : pd.read_csv(stepBasePath+"Players_Vector_WinValue.csv")}
    player_models["escolha"] = player_models["escolha"][["Player","Champion/Function","Year","Month","parts","score_min","score_max","score_delta","cluster","clusterLabel"]]
    player_models["winTaxa"] = player_models["winTaxa"][["Player","Champion/Function","Year","Month","parts","score_min","score_max","score_delta","cluster","clusterLabel"]]
    player_models["winValue"] = player_models["winValue"][["Player","Champion/Function","Year","Month","parts","score_min","score_max","score_delta","cluster","clusterLabel"]]
    player_tree = TreeStep(player_models,players_all,champions_all,functions_all) #00:16:06 ~ 00:19:17
#player_tree = { "escolha" : pd.read_csv(dataBasePath+"Players_Vector_Escolha.csv"), "win" : pd.read_csv(dataBasePath+"Players_Vector_Win.csv")}
#player_tree["escolha"] = player_tree["escolha"][
#    ["Player","Champion/Function","Year","Month","parts","rate_min","rate_max","rate_delta","cluster","clusterLabel","classifierLabel"]]
#player_tree["win"] = player_tree["win"][
#    ["Player","Champion/Function","Year","Month","parts","rate_min","rate_max","rate_delta","cluster","clusterLabel","classifierLabel"]]

#player_commitment = PlayersCommitment(player_models,players_all,champions_all,functions_all)

print("==============================================================")
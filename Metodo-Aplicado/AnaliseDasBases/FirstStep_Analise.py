import os
import csv
import datetime
import calendar
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

textMode = False
limit_percent = 1

#Set why columns name is able to use.

directory = "C:\\Users\\marco\\Documents\\TCC\\Metodo-Aplicado\\"
dataBasePath = directory+"DataBase\\"
analysPath = directory+"Analysis\\"

dataBaseName = "Dataset_LeagueOfLegends_2023.csv"
filtredName = "LOL_2023_Filtred.csv"

dataBaseAnaliseName = "AnalysisDataBase.csv"
filtredBaseAnaliseName = "AnalysisFiltredBase.csv"

column_tag = {
    "player" : "summonerName",
    "region" : "region",
    "regionCode" : "regionCode",
    "champion" : "championName",
    "function" : "individualPosition",
    "win" : "win"
}

monthTag = {"1" : "Janeiro","2" : "Fevereiro","3" : "Março","4" : "Abril","5" : "Maio",
            "6" : "Junho","7" : "Julho","8" : "Agosto","9" : "Setembro","10" : "Outubro",
            "11": "Novembro","12" : "Dezembro"}

base_csv = pd.read_csv(dataBasePath+dataBaseName)
baseFiltred_csv = pd.read_csv(dataBasePath+filtredName)

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
    print("Create CSV.")
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

def AdjustTimeStamp(base):
    r:pd.DataFrame = base
    r["gameEndTimestampToDate"] = pd.to_datetime(r["gameEndTimestampToDate"])
    r["year"] = r["gameEndTimestampToDate"].dt.year
    r["month"] = r["gameEndTimestampToDate"].dt.month
    r["week"] = ((r["gameEndTimestampToDate"].dt.day -1) // 7) + 1
    return r

def CreateAnalisedCSV(fileName):
    CreateCSV(os.path.join(directory+"Analysis",fileName),["ValueTag",
                                                "Mínimo - Escolha", "Player Mínimo - Escolha",
                                                "Máximo - Escolha", "Player Máximo - Escolha",
                                                "Média - Escolha", "Player Média - Escolha",
                                                "Desvio Padrão - Escolha",
                                                "Mínimo - Vitoria","Player Mínimo - Vitoria",
                                                "Máximo - Vitoria", "Player Máximo - Vitoria",
                                                "Média - Vitoria", "Player Média - Vitoria",
                                                "Desvio Padrão - Vitoria",
                                                "Mínimo - Derrota", "Player Mínimo - Derrota",
                                                "Máximo - Derrota", "Player Máximo - Derrota",
                                                "Média - Derrota", "Player Média - Derrota",
                                                "Desvio Padrão - Derrota",
                                                "Distribuição"])

def Analise(base,columnTag,fileName):

    tags = base[columnTag].unique()
    i = 0; startTime = datetime.datetime.now()
    for tag in tags:
        i += 1
        tagBase = base[base[columnTag] == tag]
        winBase = tagBase[tagBase["win"] == True]
        loseBase = tagBase[tagBase["win"] == False]

        tagCount = tagBase[column_tag["player"]].value_counts()
        tagWin = winBase[column_tag["player"]].value_counts()
        tagLose = loseBase[column_tag["player"]].value_counts()

        value_tag = tag

        min_escolha = tagCount.min();  player_min_escolha = tagCount.idxmin()
        max_escolha = tagCount.max();  player_max_escolha = tagCount.idxmax()
        med_escolha = round(tagCount.mean(),2); player_med_escolha = (tagCount - tagCount.mean()).abs().idxmin()
        des_escolha = round(tagCount.std(),2)

        min_win = tagWin.min();  player_min_win = tagWin.idxmin()
        max_win = tagWin.max();  player_max_win = tagWin.idxmax()
        med_win = round(tagWin.mean(),2); player_med_win = (tagWin - tagWin.mean()).abs().idxmin()
        des_win = round(tagWin.std(),2)

        min_lose = tagLose.min();  player_min_lose = tagLose.idxmin()
        max_lose = tagLose.max();  player_max_lose = tagLose.idxmax()
        med_lose = round(tagLose.mean(),2); player_med_lose = (tagLose - tagLose.mean()).abs().idxmin()
        des_lose = round(tagLose.std(),2)

        dist = tagCount.sum()

        UpdateCSV(os.path.join(directory+"Analysis",fileName),[value_tag,
                                                    min_escolha, player_min_escolha,
                                                    max_escolha,player_max_escolha,
                                                    med_escolha,player_med_escolha,
                                                    des_escolha,
                                                    min_win,player_min_win,
                                                    max_win,player_max_win,
                                                    med_win,player_med_win,
                                                    des_win,
                                                    min_lose,player_min_lose,
                                                    max_lose,player_max_lose,
                                                    med_lose,player_med_lose,
                                                    des_lose,
                                                    dist],0,False)
        ProgressBar("Analysis in ",i,len(tags),startTime=startTime,end=True)

def BoxPlot(dados,title,label,saveName,path,labelNumbers=0):
    print("BoxPlot : "+title+".")

    if labelNumbers != 0: 
        i = 0; while_called = 0
        dadosLimited1 = []
        dadosLimited2 = []
        for data1,data2 in zip(dados[0],dados[1]):
            i+=1
            dadosLimited1.append(data1)
            dadosLimited2.append(data2)
            if i == labelNumbers:
                i=0; while_called+=1; BoxPlot([dadosLimited1,dadosLimited2],title+str(while_called),label,saveName+str(while_called),path)
                dadosLimited1 = []; dadosLimited2 = []
        if i != 0:
            i=0; while_called+=1; BoxPlot([dadosLimited1,dadosLimited2],title+str(while_called),label,saveName+str(while_called),path)
            dadosLimited1 = []; dadosLimited2 = []
        return
    
    boxplot = plt.boxplot(dados[0],tick_labels=dados[1])

    plt.title(title)
    plt.boxplot(dados[0],tick_labels=dados[1])
    plt.ylabel(label)

    outliers = boxplot["fliers"][0].get_ydata()
        
    
    #plt.show()
    plt.savefig(path+".png",dpi=300,bbox_inches="tight")
    plt.close()

def MakeBoxPlot(base,baseName):

    os.makedirs(directory+"Analysis\\BoxPlot\\"+baseName,exist_ok=True)
    dados1_escolha = []; dados2_escolha = []; dados1_win = []; dados2_win = []

    dados_players = [
            base[column_tag["player"]].value_counts(),
            base[column_tag["player"]].unique()
        ]
    
    champions = base[column_tag["champion"]].unique()
    for champion in champions:

        champion_data = base[base[column_tag["champion"]] == champion]
        partidas_por_player = champion_data[column_tag["player"]].value_counts()
        wins_por_player = champion_data.groupby(column_tag["player"])[column_tag["win"]].sum()
        
        dados1_escolha.append(partidas_por_player.values)
        dados2_escolha.append(champion)
        dados1_win.append(wins_por_player.values)
        dados2_win.append(champion)

    dados_champions_escolha = [dados1_escolha,dados2_escolha]
    dados_champions_win = [dados1_win,dados2_win]

    dados1_escolha = []; dados2_escolha = []; dados1_win = []; dados2_win = []
    functions = base[column_tag["function"]].unique()
    for function in functions:

        function_data = base[base[column_tag["function"]] == function]
        partidas_por_player = function_data[column_tag["player"]].value_counts()
        wins_por_player = function_data.groupby(column_tag["player"])[column_tag["win"]].sum()
        dados1_escolha.append(partidas_por_player.values)
        dados2_escolha.append(function)
        dados1_win.append(wins_por_player.values)
        dados2_win.append(function)

    dados_functions_escolha = [dados1_escolha,dados2_escolha]
    dados_functions_win = [dados1_win,dados2_win]

    #BoxPlot(base,column_tag["player"],"Box Plot "+baseName+": Maximo De Partidas P/ Player","Partidas Jogadas",baseName+"_Players")

    #dados,title,label,saveName,path,labelNumbers=0
    BoxPlot(dados=dados_champions_escolha,
            title="Box Plot "+baseName+": Escolhas P/ Campeão",
            label="Vezes Escolhidas P/ Player",
            path=baseName,
            labelNumbers=5)
    BoxPlot(dados=dados_champions_win,
            title="Box Plot "+baseName+": Vitorias P/ Campeão",
            label="Vitorias P/ Player",
            path=baseName,
            labelNumbers=5)
    
    BoxPlot(dados=dados_functions_escolha,
            title="Box Plot "+baseName+": Escolhas P/ Função",
            label="Vezes Escolhidas P/ Player",
            path=baseName)
    BoxPlot(dados=dados_functions_win,
            title="Box Plot "+baseName+": Vitorias P/ Função",
            label="Vitorias P/ Player",
            path=baseName)

def MakeAnalysisDirs():
    os.makedirs(directory+"Analysis", exist_ok=True)
    os.makedirs(directory+"Analysis\\BoxPlot",exist_ok=True)

def AnaliseDataBase():
    MakeAnalysisDirs()

    CreateAnalisedCSV(dataBaseAnaliseName)
    Analise(base_csv,column_tag["champion"],dataBaseAnaliseName)
    Analise(base_csv,column_tag["function"],dataBaseAnaliseName)

    MakeBoxPlot(base_csv,"Base")

def AnaliseFiltredDataBase():
    MakeAnalysisDirs()

    CreateAnalisedCSV(filtredBaseAnaliseName)
    Analise(baseFiltred_csv,column_tag["champion"],filtredBaseAnaliseName)
    Analise(baseFiltred_csv,column_tag["function"],filtredBaseAnaliseName)

    MakeBoxPlot(baseFiltred_csv,"Filtred")

def MonthMorePlayed(base:pd.DataFrame,base_tag:str):
    os.makedirs(analysPath+base_tag+"\\PartsForMonth\\",exist_ok=True)
    years = base["year"].unique()

    i = 0; startTime1 = datetime.datetime.now()
    for year in years:
        i += 1; yearPath = analysPath+base_tag+"\\PartsForMonth\\"+str(year); yearBase: pd.DataFrame = base[base["year"] == year]
        CreateCSV(os.path.join(yearPath+".csv"),["Month","min_played_for_players","max_played_for_players","med_played_for_players","all_parts"])
        months = yearBase["month"].unique()
        o = 0; startTime2 = datetime.datetime.now()
        for month in months:
            o+= 1
            monthBase = yearBase[yearBase["month"] == month]
            players = monthBase[column_tag["player"]].value_counts()
            min_played = players.min()
            max_played = players.max()
            med_played = round(players.mean())
            all_parts = players.sum()
            UpdateCSV(os.path.join(yearPath+".csv"),[month,min_played,max_played,med_played,all_parts],0,False)
            ProgressBar("Month Analysis is in ",o,len(months),startTime=startTime2,end=True)

        graficBase = pd.read_csv(yearPath+".csv",encoding="utf-16")

        plt.figure(figsize=(10, 6))

        plt.bar(graficBase["Month"],graficBase["all_parts"])

        plt.title("Partidas Jogadas p/ Mês")
        plt.xlabel("Mês")
        plt.ylabel("Partidas")

        plt.xticks(graficBase["Month"],graficBase["Month"].astype(str).map(monthTag))
        plt.tight_layout()

        plt.savefig(yearPath+".png",dpi=300)
        plt.close()

        ProgressBar("Year Analysis is in ",i,len(years),startTime=startTime1,end=True)
    return True

def ChampionsAndFunctionsPlayedByPlayers(base:pd.DataFrame,base_tag:str):
    os.makedirs(analysPath+base_tag+"\\ChampionsAndFunctionsPlayedByPlayers\\",exist_ok=True)
    dir = analysPath+base_tag+"\\ChampionsAndFunctionsPlayedByPlayers\\"
    players = base[column_tag["player"]].unique()
    CreateCSV(os.path.join(dir+"ChampionsAndFunctionsPlayedByPlayers.csv"),["Tag","champ_versatility","func_versatility"])
    
    i = 0; startTime = datetime.datetime.now()
    for player in players:
        i += 1
        playerBase: pd.DataFrame = base[base[column_tag["player"]] == player]
    
        tag = player
        champ_versatility = playerBase[column_tag["champion"]].nunique()
        func_versatility = playerBase[column_tag["function"]].nunique()
        #print([tag,champ_versatility,func_versatility])
    
        UpdateCSV(os.path.join(dir+"ChampionsAndFunctionsPlayedByPlayers.csv"),[tag,champ_versatility,func_versatility],0,False)
        ProgressBar("Players Versatility Analysis is in ",i,len(players),startTime=startTime,end=True)

    graficBase = pd.read_csv(dir+"ChampionsAndFunctionsPlayedByPlayers.csv",encoding="utf-16")

    versatility_count = graficBase["champ_versatility"].value_counts().sort_index()
    plt.figure(figsize=(10, 6))

    plt.bar(versatility_count.index,versatility_count.values)

    #plt.bar(bins =(0,0))

    plt.title("Versatilidade Dos Jogadores")
    plt.xlabel("Nível de Versatilidade")
    plt.ylabel("Quantidade de jogadores")

    plt.xticks(versatility_count.index,rotation=-90,ha="right")
    plt.tight_layout(pad=2)

    plt.savefig(dir+"ChampionsVersatilityByPlayers.png",dpi=300)
    plt.close()

    versatility_count = graficBase["func_versatility"].value_counts().sort_index()
    plt.figure(figsize=(10, 6))
    
    plt.bar(versatility_count.index,versatility_count.values)
    
    plt.title("Versatilidade Dos Jogadores")
    plt.xlabel("Nível de Versatilidade")
    plt.ylabel("Quantidade de jogadores")
    
    plt.xticks(versatility_count.index,rotation=0)
    plt.tight_layout()
    
    plt.savefig(dir+"FunctionsVersatilityByPlayers.png",dpi=300)
    plt.close()

    return

def PlayersForServers(base:pd.DataFrame,base_tag:str):
    os.makedirs(analysPath+base_tag+"\\PlayersForServers\\",exist_ok=True)
    dir = analysPath+base_tag+"\\PlayersForServers\\"
    regionCodes = base[column_tag["regionCode"]].unique()
    for region in regionCodes:
        CreateCSV(os.path.join(dir+region+"PlayerBase.csv"),[])
        #print("Region:"+region)
        #print("Columtag:"+column_tag["regionCode"])
        regionBase = base[base[column_tag["regionCode"]] == region]
        regionBase.to_csv(dir+region+"PlayerBase.csv")

    graficBase = base

    players_in_regions = (graficBase.groupby(column_tag["regionCode"])[column_tag["player"]].nunique().sort_index())

    plt.figure(figsize=(10, 6))

    plt.bar(players_in_regions.index,players_in_regions.values)

    plt.title("Quantidade de Jogadores por Região")
    plt.xlabel("Região")
    plt.ylabel("Quantidade de jogadores")

    plt.xticks(players_in_regions.index)

    plt.tight_layout()
    plt.savefig(dir+"PlayersForServers.png", dpi=300)
    plt.close()

    games_in_regions = graficBase[column_tag["regionCode"]].value_counts().sort_index()

    plt.figure(figsize=(10, 6))

    plt.bar(games_in_regions.index,games_in_regions.values)

    plt.title("Quantidade de Partidas por Região")
    plt.xlabel("Região")
    plt.ylabel("Quantidade de partidas")

    plt.xticks(games_in_regions.index)

    plt.tight_layout()
    plt.savefig(dir+"GamesForServers.png", dpi=300)
    plt.close()
    
    return

def FunctionsForChampions(base:pd.DataFrame,base_tag:str):
    os.makedirs(analysPath+base_tag+"\\FunctionsForChampions\\",exist_ok=True)
    dir = analysPath+base_tag+"\\FunctionsForChampions\\"
    champions = base[column_tag["champion"]].unique()

    i = 0; startTIme = datetime.datetime.now()
    for champion in champions:
        CreateCSV(os.path.join(dir+champion+"FunctionsPlayed.csv"),["Function", "Played"])
        championCsv = pd.read_csv(dir+champion+"FunctionsPlayed.csv",encoding="utf-16")
        championBase = base[base[column_tag["champion"]] == champion]

        FunctionsNumberPlayed = championBase[column_tag["function"]].value_counts()

        championCsv = pd.DataFrame({
            "Function": FunctionsNumberPlayed.index,
            "Played": FunctionsNumberPlayed.values})

        championCsv.to_csv(dir+champion+"FunctionsPlayed.csv",index=False,encoding="utf-16")

        plt.figure(figsize=(10, 6))

        plt.bar(championCsv["Function"],championCsv["Played"])

        plt.title("Distribuição de Funções para "+champion)
        plt.xlabel("Funções")
        plt.ylabel("Partidas")

        plt.xticks(championCsv["Function"]) #graficBase["Month"].astype(str).map(monthTag)
        plt.tight_layout()

        plt.savefig(dir+champion+"FunctionsPlayed.png",dpi=300)
        plt.close()

        i += 1
        ProgressBar("Function for Champion Analysis is in ",i,len(champions),startTime=startTIme,end=True)
    return

def RegionForPlayers(base:pd.DataFrame,base_tag:str):
    os.makedirs(analysPath+base_tag+"\\MultiRegionPlayers\\",exist_ok=True)
    CreateCSV(os.path.join(analysPath+base_tag+"\\MultiRegionPlayers\\MultiRegionPlayers.csv"),["Player","region","region_code"])
    regionsByPlayer = (base.groupby(column_tag["player"])[column_tag["regionCode"]].nunique().sort_values(ascending=False))

    playersMultipleRegions = regionsByPlayer[regionsByPlayer > 1]

    if (regionsByPlayer > 1).any():
        print("Existem jogadores presentes em mais de uma região.")
        multipleRegionsBase = base[base[column_tag["player"]].isin(playersMultipleRegions.index)]
        multipleRegionsBase = multipleRegionsBase[[column_tag["player"],column_tag["regionCode"],column_tag["region"]]]
        multipleRegionsBase = multipleRegionsBase.drop_duplicates()
        multipleRegionsBase = multipleRegionsBase.groupby(column_tag["player"])
        multipleRegionsBase = multipleRegionsBase.agg({column_tag["regionCode"]: lambda x: "/".join(x),column_tag["region"]: lambda x: "/".join(x)})
        multipleRegionsBase = multipleRegionsBase.reset_index()
        multipleRegionsBase["variation"] = (multipleRegionsBase[column_tag["regionCode"]].str.count("/") + 1)
        multipleRegionsBase.to_csv(analysPath+base_tag+"\\MultiRegionPlayers\\MultiRegionPlayers.csv",index=False,encoding="utf-16")
        print(playersMultipleRegions)
    else:
        print("Nenhum jogador aparece em mais de uma região.")

    graficBase = pd.read_csv(analysPath+base_tag+"\\MultiRegionPlayers\\MultiRegionPlayers.csv",encoding="utf-16")

    variationCount = (graficBase["variation"].value_counts().sort_index())

    plt.figure(figsize=(10, 6))
    
    plt.bar(variationCount.index,variationCount.values)

    plt.title("Variação de jogadores em mais de uma região")
    plt.xlabel("Quantidade de regiões jogadas")
    plt.ylabel("Número de jogadores")

    plt.xticks(variationCount.index) #graficBase["Month"].astype(str).map(monthTag)
    plt.tight_layout()

    plt.savefig(analysPath+base_tag+"\\MultiRegionPlayers\\MultiRegionPlayers.png",dpi=300)
    plt.close()
    
    return

def PuuidAndAccountIdTest(base:pd.DataFrame,base_tag:str):
    os.makedirs(analysPath+base_tag+"\\PuuidAndAccountIdTest\\",exist_ok=True)
    CreateCSV(os.path.join(analysPath+base_tag+"\\PuuidAndAccountIdTest\\PuuidAndAccountIdTest.csv"),["puuid","accountId","region","region_code"])
    playerNames = base[column_tag["player"]].unique()
    puuid = base["puuid"].unique()
    accountId = base["accountId"].unique()
    print("PlayerNameLeng :" + str(len(playerNames)) + " | PuuidLeng :" + str(len(puuid)) + " | AccountIdLeng :"+ str(len(accountId)))

    puuidAnalysis = base.groupby("puuid")
    puuidAnalysis = puuidAnalysis.agg(
        names=(column_tag["player"], "nunique"),
        accountIds=("accountId", "nunique"),
        regions=(column_tag["regionCode"], "nunique"))
    puuidAnalysis = puuidAnalysis.reset_index()

    puuidAnalysis.to_csv(analysPath+base_tag+"\\PuuidAndAccountIdTest\\PuuidAndAccountIdTest.csv",index=False,encoding="utf-16")

    puuidAnalysis = puuidAnalysis[puuidAnalysis["puuid"] != "Player Not Found"]

    graficBase = puuidAnalysis
    
    variationCount = (graficBase["names"].value_counts().sort_index())
    
    plt.figure(figsize=(10, 6))
        
    bars = plt.bar(variationCount.index,variationCount.values)
    plt.bar_label(bars)
    
    plt.title("Player Names For Unique Puuid")
    plt.xlabel("Player Name Variation")
    plt.ylabel("Number Of Puuids")
    
    plt.xticks(variationCount.index) #graficBase["Month"].astype(str).map(monthTag)
    plt.tight_layout()
    
    plt.savefig(analysPath+base_tag+"\\PuuidAndAccountIdTest\\PuuidAndAccountIdTest.png",dpi=300)
    plt.close()
    return

def PlayerLevel(base:pd.DataFrame,base_tag:str):
    os.makedirs(analysPath+base_tag+"\\PlayerLevel\\",exist_ok=True)
    #CreateCSV(os.path.join(analysPath+base_tag+"\\PlayerLevel\\PlayerLevel.csv"),["puuid","accountId","region","region_code"])
    
    graficBase = base
        
    variationCount = graficBase["summonerLevel"].unique()
        
    plt.figure(figsize=(10, 6))
            
    bars = plt.bar(variationCount.index,variationCount.values)

    

    return

def PlayerPuuidAdjust(base:pd.DataFrame,base_tag:str):
    os.makedirs(analysPath+base_tag+"\\PlayerPuuidAdjust\\",exist_ok=True)
    otherCsv = base[base["puuid"] != "Player Not Found"].copy()
    pnfCsv = base[base["puuid"] == "Player Not Found"].copy()
    otherCsv["playerIdRemaster"] = (otherCsv[column_tag["player"]] + otherCsv[column_tag["regionCode"]])
    pnfCsv["playerIdRemaster"] = (pnfCsv[column_tag["player"]] + pnfCsv[column_tag["regionCode"]])

    otherPlayers = otherCsv["playerIdRemaster"].unique()
    pnfPlayers = pnfCsv["playerIdRemaster"].unique()

    hasMatch = pnfPlayers[np.isin(pnfPlayers, otherPlayers)].size

    print("Pnf Players : "+str(len(pnfPlayers)))
    print("Double Players Searched : "+str(hasMatch))

    duplicatedPlayers = pnfCsv[pnfCsv["playerIdRemaster"].isin(otherCsv["playerIdRemaster"])].copy()
    notDuplicatedPlayers = pnfCsv[~pnfCsv["playerIdRemaster"].isin(otherCsv["playerIdRemaster"])].copy()

    duplicatedPlayers.to_csv(analysPath+base_tag+"\\PlayerPuuidAdjust\\DuplicatedPlayers.csv",index=False,encoding="utf-16")
    notDuplicatedPlayers.to_csv(analysPath+base_tag+"\\PlayerPuuidAdjust\\NotDuplicatedPlayers.csv",index=False,encoding="utf-16")

    return

print("==============================================================")
print("Start Analysis First Step.")
base_csv = AdjustTimeStamp(base_csv); baseFiltred_csv = AdjustTimeStamp(baseFiltred_csv)
AnaliseDataBase()
AnaliseFiltredDataBase()
MakeBoxPlot(baseFiltred_csv,"Filtred")

MonthMorePlayed(base_csv,"base")
MonthMorePlayed(baseFiltred_csv,"filtred")

#ChampionsAndFunctionsPlayedByPlayers(base_csv,"base") #Bem demorado, umas 7h/8h.
ChampionsAndFunctionsPlayedByPlayers(baseFiltred_csv,"filtred")

PlayersForServers(base_csv,"base")
PlayersForServers(baseFiltred_csv,"filtred")

FunctionsForChampions(base_csv,"base")
FunctionsForChampions(baseFiltred_csv,"filtred")

RegionForPlayers(base_csv,"base")
RegionForPlayers(baseFiltred_csv,"filtred")

PuuidAndAccountIdTest(base_csv,"base")
PuuidAndAccountIdTest(baseFiltred_csv,"filtred")

PlayerPuuidAdjust(base_csv,"base")
PlayerPuuidAdjust(baseFiltred_csv,"filtred")

print("==============================================================")



    
import os
import csv
import datetime
import pandas as pd
import matplotlib.pyplot as plt

textMode = False
limit_percent = 1

#Set why columns name is able to use.

directory = r"C:\Users\marco\Documents\TCC\Metodo-Aplicado\\"
dataBasePath = directory+"\\DataBase\\"

dataBaseName = "Dataset_LeagueOfLegends_2023.csv"
filtredName = "LOL_2023_Filtred.csv"

dataBaseAnaliseName = "AnalysisDataBase.csv"
filtredBaseAnaliseName = "AnalysisFiltredBase.csv"

column_tag = {
    "player" : "summonerName",
    "champion" : "championName",
    "function" : "individualPosition",
    "win" : "win"
}

base_csv = pd.read_csv(dataBasePath+dataBaseName)
baseFiltred_csv = pd.read_csv(dataBasePath+filtredName)

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
    i = 0
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
        med_escolha = round(tagCount.mean()); player_med_escolha = (tagCount - tagCount.mean()).abs().idxmin()
        des_escolha = round(tagCount.std())

        min_win = tagWin.min();  player_min_win = tagWin.idxmin()
        max_win = tagWin.max();  player_max_win = tagWin.idxmax()
        med_win = round(tagWin.mean()); player_med_win = (tagWin - tagWin.mean()).abs().idxmin()
        des_win = round(tagWin.std())

        min_lose = tagLose.min();  player_min_lose = tagLose.idxmin()
        max_lose = tagLose.max();  player_max_lose = tagLose.idxmax()
        med_lose = round(tagLose.mean()); player_med_lose = (tagLose - tagLose.mean()).abs().idxmin()
        des_lose = round(tagLose.std())

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
        ProgressBar("Analysis in ",i,len(tags),end=True)

def BoxPlot(dados,title,label,saveName,baseName,labelNumbers=0):
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
                i=0; while_called+=1; BoxPlot([dadosLimited1,dadosLimited2],title+str(while_called),label,saveName+str(while_called),baseName)
                dadosLimited1 = []; dadosLimited2 = []
        if i != 0:
            i=0; while_called+=1; BoxPlot([dadosLimited1,dadosLimited2],title+str(while_called),label,saveName+str(while_called),baseName)
            dadosLimited1 = []; dadosLimited2 = []
        return
    
    boxplot = plt.boxplot(dados[0],tick_labels=dados[1])

    plt.title(title)
    plt.boxplot(dados[0],tick_labels=dados[1])
    plt.ylabel(label)

    outliers = boxplot["fliers"][0].get_ydata()
        
    
    #plt.show()
    plt.savefig(directory+"Analysis\\BoxPlot\\"+baseName+"\\"+saveName+".png",dpi=300,bbox_inches="tight")
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

    BoxPlot(dados_champions_escolha,"Box Plot "+baseName+": Escolhas P/ Campeão","Vezes Escolhidas P/ Player",baseName+"_Champions",baseName,labelNumbers=5)
    BoxPlot(dados_champions_win,"Box Plot "+baseName+": Vitorias P/ Campeão","Vitorias P/ Player",baseName+"_ChampionsWin",baseName,labelNumbers=5)
    
    BoxPlot(dados_functions_escolha,"Box Plot "+baseName+": Escolhas P/ Função","Vezes Escolhidas P/ Player",baseName+"_Functions",baseName)
    BoxPlot(dados_functions_win,"Box Plot "+baseName+": Vitorias P/ Função","Vitorias P/ Player",baseName+"_FunctionsWin",baseName)

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

print("==============================================================")
print("Start Analysis First Step.")
#AnaliseDataBase()
#AnaliseFiltredDataBase()
MakeBoxPlot(baseFiltred_csv,"Filtred")
print("==============================================================")



    
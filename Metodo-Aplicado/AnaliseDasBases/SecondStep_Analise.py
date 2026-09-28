import os
import csv
import datetime
import pandas as pd
import matplotlib.pyplot as plt

textMode = False
limit_percent = 1

#Set why columns name is able to use.

directory = "C:\\Users\\marco\\Documents\\TCC\\Metodo-Aplicado\\"
dataBasePath = directory+"DataBase\\"
playersPath = directory+"TaxasDosJogadores\\"

filtredName = "LOL_2023_Filtred.csv"
taxasAnaliseName = "AnalysisTaxas.csv"

column_tag = {
    "player" : "summonerName",
    "playerIdentifier": "playerIdRemaster",
    "regionCode" : "regionCode",
    "champion" : "championName",
    "function" : "individualPosition"
}

#pick_rate e win_rate, "Player_Taxas.csv"
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

def Analise(base,columnTag,fileName,dir=directory+"Analysis",writePlayer=True):

    tags = base[columnTag].unique()
    i = 0; startTime = datetime.datetime.now()
    for tag in tags:
        i += 1
        tagBase = base[base[columnTag] == tag]
        winRate = tagBase["win_rate"]
        pickRate = tagBase["pick_rate"]

        tagCount = tagBase["Player"].value_counts()

        value_tag = tag
        player_tag = tagBase["Player"].unique()[0]

        min_winRate = winRate.min()
        max_winRate = winRate.max()
        med_winRate = round(winRate.mean(),2)
        des_winRate = winRate.std()

        if pd.isna(des_winRate):
            des_winRate = "NaN"
        else:
            des_winRate = round(des_winRate,2)

        min_pickRate = pickRate.min()
        max_pickRate = pickRate.max()
        med_pickRate = round(pickRate.mean(),2)
        des_pickRate = pickRate.std()
        if pd.isna(des_pickRate):
            des_pickRate = "NaN"
        else:
            des_pickRate = round(des_winRate,2)

        dist = tagCount.sum()

        if writePlayer: UpdateCSV(os.path.join(dir,fileName),[value_tag, player_tag,
                                                              min_winRate, max_winRate, med_winRate,
                                                              des_winRate,
                                                              min_pickRate, max_pickRate, med_pickRate,
                                                              des_pickRate,
                                                              dist],0,False)
        else: UpdateCSV(os.path.join(dir,fileName),[value_tag,
                                                    min_winRate, max_winRate, med_winRate,
                                                    des_winRate,
                                                    min_pickRate, max_pickRate, med_pickRate,
                                                    des_pickRate,
                                                    dist],0,False)
        #ProgressBar("Analysis in ",i,len(tags),startTime=startTime,end=True)

def BoxPlot(dados,title,label,path,saveNameAcress="",labelNumbers=0):
    #print("BoxPlot : "+title+".")

    if labelNumbers != 0: 
        i = 0; while_called = 0
        dadosLimited1 = []
        dadosLimited2 = []
        for data1,data2 in zip(dados[0],dados[1]):
            i+=1
            dadosLimited1.append(data1)
            dadosLimited2.append(data2)
            if i == labelNumbers:
                i=0; while_called+=1; BoxPlot([dadosLimited1,dadosLimited2],title+str(while_called),label,path,saveNameAcress=str(while_called))
                dadosLimited1 = []; dadosLimited2 = []
        if i != 0:
            i=0; while_called+=1; BoxPlot([dadosLimited1,dadosLimited2],title+str(while_called),label,path,saveNameAcress=str(while_called))
            dadosLimited1 = []; dadosLimited2 = []
        return
    
    boxplot = plt.boxplot(dados[0],tick_labels=dados[1])

    plt.title(title)
    plt.boxplot(dados[0],tick_labels=dados[1])
    plt.ylabel(label)

    outliers = boxplot["fliers"][0].get_ydata()
        
    
    #plt.show()
    plt.savefig(path+saveNameAcress+".png",dpi=300,bbox_inches="tight")
    plt.close()

def MakeBoxPlot(base,dir=directory+"Analysis"):
    champions = baseFiltred_csv[column_tag["champion"]]
    functions = baseFiltred_csv[column_tag["function"]]

    baseChampion = base[base["Champion/Function"].isin(champions)]
    baseFunctions = base[base["Champion/Function"].isin(functions)]

    #os.makedirs(directory+"Analysis\\BoxPlot\\"+baseName,exist_ok=True)

    dados1_escolha = []; dados2_escolha = []; dados1_win = []; dados2_win = []
    champions = baseChampion["Champion/Function"].unique()
    for champion in champions:
        champion_data = baseChampion[baseChampion["Champion/Function"] == champion]
        pickRate_por_player = champion_data.groupby("Player")["pick_rate"].mean()
        winsRate_por_player = champion_data.groupby("Player")["win_rate"].mean()
        dados1_escolha.append(pickRate_por_player.values)
        dados2_escolha.append(champion)
        dados1_win.append(winsRate_por_player.values)
        dados2_win.append(champion)

    dados_champions_win = [dados1_win,dados2_win]
    dados_champions_escolha = [dados1_escolha,dados2_escolha]

    dados1_escolha = []; dados2_escolha = []; dados1_win = []; dados2_win = []
    functions = baseFunctions["Champion/Function"].unique()
    for function in functions:
        function_data = baseFunctions[baseFunctions["Champion/Function"] == function]
        pickRate_por_player = function_data.groupby("Player")["pick_rate"].mean()
        winsRate_por_player = function_data.groupby("Player")["win_rate"].mean()
        dados1_escolha.append(pickRate_por_player.values)
        dados2_escolha.append(function)
        dados1_win.append(winsRate_por_player.values)
        dados2_win.append(function)

    dados_functions_win = [dados1_win,dados2_win]
    dados_functions_escolha = [dados1_escolha,dados2_escolha]

    #BoxPlot(base,"Player","Box Plot "+baseName+": Maximo De Partidas P/ Player","Partidas Jogadas",baseName+"_Players.png",dir=dir)
    
    #dados,title,label,path,labelNumbers=0
    BoxPlot(dados=dados_champions_win,
            title="Champions Win Rate Box Plot",
            label="Win Rate",
            path=dir+"\\Champions_WinRate",
            labelNumbers=5,)
    
    BoxPlot(dados=dados_champions_escolha,
            title="Champions Pick Rate Box Plot",
            label="Pick Rate",
            path=dir+"\\Champions_PickRate",
            labelNumbers=5)

    BoxPlot(dados=dados_functions_win,
            title="Functions Win Rate Box Plot",
            label="Win Rate",
            path=dir+"\\Functions_WinRate")
    
    BoxPlot(dados=dados_functions_escolha,
            title="Functions Pick Rate Box Plot",
            label="Pick Rate",
            path=dir+"\\Functions_PickRate")

def CreateAnalisedCSV(fileName,dir=directory+"\\Analysis\\filtred"):
    CreateCSV(os.path.join(dir,fileName),["ValueTag", "Player",
                                                "Mínimo - Taxa Vitoria",
                                                "Máximo - Taxa Vitoria",
                                                "Média - Taxa Vitoria",
                                                "Desvio Padrão - Taxa Vitoria",
                                                "Mínimo - Taxa Escolha",
                                                "Máximo - Taxa Escolha",
                                                "Média - Taxa Escolha",
                                                "Desvio Padrão - Taxa Escolha",
                                                "Distribuição"])

def StartAnalise():
    os.makedirs(directory+"\\Analysis\\filtred", exist_ok=True)
    os.makedirs(directory+"\\Analysis\\filtred\\SecondStepAnalysis",exist_ok=True)

    players = baseFiltred_csv[column_tag["playerIdentifier"]].unique()

    dir = directory+"\\Analysis\\filtred"
    first = True
    taxasBase = None
    i = 0; startTime = datetime.datetime.now()
    for player in players:
        i+=1
        playerDir = playersPath+player
        taxasTarget = pd.read_csv(playerDir+"\\Player_Taxas.csv",encoding="utf-16")

        os.makedirs(playerDir+"\\SecondStepAnalysis",exist_ok=True)
        
        CreateCSV(os.path.join(playerDir+"\\SecondStepAnalysis",taxasAnaliseName),["ValueTag", "Player",
                                                        "Mínimo - Taxa Vitoria",
                                                        "Máximo - Taxa Vitoria",
                                                        "Média - Taxa Vitoria",
                                                        "Desvio Padrão - Taxa Vitoria",
                                                        "Mínimo - Taxa Escolha",
                                                        "Máximo - Taxa Escolha",
                                                        "Média - Taxa Escolha",
                                                        "Desvio Padrão - Taxa Escolha",
                                                        "Distribuição"])
        #base,columnTag,fileName,dir=directory+"Analysis"
        Analise(taxasTarget,"Champion/Function",taxasAnaliseName,playerDir+"\\SecondStepAnalysis")
        #base,dir=directory+"Analysis"
        #MakeBoxPlot(taxasTarget,playerDir+"\\SecondStepAnalysis")
        if first:
            first = False; taxasBase = taxasTarget
            continue
        taxasBase = pd.concat([taxasBase,taxasTarget],ignore_index=True)
        ProgressBar("Make Taxas Base Unifiqued in ",i,len(players),startTime=startTime,end=True) #00:08:47 ~ 00:09:24

    CreateCSV(os.path.join(dir+"\\SecondStepAnalysis",taxasAnaliseName),["ValueTag",
                                                            "Mínimo - Taxa Vitoria",
                                                            "Máximo - Taxa Vitoria",
                                                            "Média - Taxa Vitoria",
                                                            "Desvio Padrão - Taxa Vitoria",
                                                            "Mínimo - Taxa Escolha",
                                                            "Máximo - Taxa Escolha",
                                                            "Média - Taxa Escolha",
                                                            "Desvio Padrão - Taxa Escolha",
                                                            "Distribuição"])
    Analise(taxasBase,"Champion/Function",taxasAnaliseName,dir=dir+"\\SecondStepAnalysis",writePlayer=False) #00:00:04

    MakeBoxPlot(taxasBase,dir+"\\SecondStepAnalysis")

print("==============================================================")
print("Start Analysis Second Step")
StartAnalise()
print("==============================================================")




    
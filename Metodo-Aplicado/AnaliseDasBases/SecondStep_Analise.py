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
    "champion" : "championName",
    "function" : "individualPosition"
}

#pick_rate e win_rate, "Player_Taxas.csv"
baseFiltred_csv = pd.read_csv(dataBasePath+filtredName)


#Use this to show your progress in terminal.
def ProgressBar(message1,value,maxValue,message2 = "%.",end = False, startTime=None):
    progress = (value / maxValue)
    progress = progress*100
    progress = round(progress)
    progress_str = str(progress)

    timePass = ""
    if startTime != None:
        time = datetime.datetime.now()-startTime; seconds = int(time.total_seconds())
        hours = seconds // 3600; minutes = (seconds % 3600) // 60; seconds = seconds % 60
        timePass = f" | {hours:02}:{minutes:02}:{seconds:02}"

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

def CreateAnalisedCSV(fileName,dir=directory+"Analysis"):
    CreateCSV(os.path.join(dir,fileName),["ValueTag", "Player"
                                                "Mínimo - Taxa Vitoria",
                                                "Máximo - Taxa Vitoria",
                                                "Média - Taxa Vitoria",
                                                "Desvio Padrão - Taxa Vitoria",
                                                "Mínimo - Taxa Escolha",
                                                "Máximo - Taxa Escolha",
                                                "Média - Taxa Escolha",
                                                "Desvio Padrão - Taxa Escolha",
                                                "Distribuição"])

def Analise(base,columnTag,fileName,dir = directory+"Analysis"):

    tags = base[columnTag].unique()
    i = 0
    for tag in tags:
        i += 1
        tagBase = base[base[columnTag] == tag]
        winRate = tagBase["win_rate"]
        pickRate = tagBase["pick_rate"]

        tagCount = tagBase["Player"].value_counts()

        value_tag = tag
        player_tag = winRate.idxmin()

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

        UpdateCSV(os.path.join(dir,fileName),[value_tag, player_tag,
                                                    min_winRate, max_winRate, med_winRate,
                                                    des_winRate,
                                                    min_pickRate, max_pickRate, med_pickRate,
                                                    des_pickRate,
                                                    dist],0,False)
        ProgressBar("Analysis in ",i,len(tags),end=True)

def BoxPlot(dados,columnTag,title,label,saveName,labelNumbers=0,dir=directory+"Analysis"):
    print("BoxPlot : "+columnTag+".")

    if labelNumbers != 0: 
            i = 0; while_called = 0
            dadosLimited1 = []
            dadosLimited2 = []
            for data1,data2 in zip(dados[0],dados[1]):
                i+=1
                dadosLimited1.append(data1)
                dadosLimited2.append(data2)
                if i == labelNumbers:
                    i=0; while_called+=1; BoxPlot([dadosLimited1,dadosLimited2],title+str(while_called),label,saveName+str(while_called),dir=dir)
                    dadosLimited1 = []; dadosLimited2 = []
            if i != 0:
                i=0; while_called+=1; BoxPlot([dadosLimited1,dadosLimited2],title+str(while_called),label,saveName+str(while_called),dir=dir)
                dadosLimited1 = []; dadosLimited2 = []
            return
    
    boxplot = plt.boxplot(dados)

    plt.title(title)
    plt.boxplot(dados)
    plt.ylabel(label)

    outliers = boxplot["fliers"][0].get_ydata()

    print("Outliers")
    max_it = 100
    it = 0
    for outlier in outliers:
        it += 1
        if(it > max_it): print("Max Iteration = True."); print("Iteration Falue ="+str(len(outliers)-max_it)); break

        for tag,value in dados.items():
            if value == outlier:
                print(tag+" : "+str(value)+".")
                break
        
    
    #plt.show(boxplot)
    plt.savefig(dir+"\\BoxPlot\\"+saveName,dpi=300,bbox_inches="tight")
    plt.close()

def MakeBoxPlot(base,baseName,dir=directory+"Analysis",toPlayer=True,toChampion=True,toFunction=True):
    champions = baseFiltred_csv[column_tag["champion"]]
    function = baseFiltred_csv[column_tag["function"]]
    baseChampion = base[base["Champion/Function"].isin(champions)]
    baseFunctions = base[base["Champion/Function"].isin(function)]

    if toPlayer: BoxPlot(base,"Player","Box Plot "+baseName+": Maximo De Partidas P/ Player","Partidas Jogadas",baseName+"_Players.png",dir=dir)
    if toChampion: BoxPlot(baseChampion,"Champion/Function","Box Plot "+baseName+": Maximo De Escolhas P/ Campeão","Vezes Escolhidas",baseName+"_Champions.png",dir=dir)
    if toFunction: BoxPlot(baseFunctions,"Champion/Function","Box Plot "+baseName+": Maximo De Escolhas P/ Função","Vezes Escolhidas",baseName+"_Functions.png",dir=dir)

def MakeAnalysisDirs(dir = directory+"Analysis"):
    os.makedirs(dir, exist_ok=True)
    os.makedirs(dir+"\\BoxPlot",exist_ok=True)

def StartAnalise():
    MakeAnalysisDirs()

    players = baseFiltred_csv[column_tag["player"]].unique()

    first = True
    taxasBase = None
    i = 0
    for player in players:
        i+=1
        playerDir = playersPath+player
        taxasTarget = pd.read_csv(playerDir+"\\Player_Taxas.csv",encoding="utf-16")
        MakeAnalysisDirs(dir=playerDir)
        CreateAnalisedCSV(taxasAnaliseName,dir=playerDir)
        Analise(taxasTarget,"Champion/Function",taxasAnaliseName,playerDir)
        MakeBoxPlot(taxasTarget,"Taxas",dir=playerDir,toPlayer=False)
        if first:
            first = False; taxasBase = taxasTarget
            continue
        taxasBase = pd.concat([taxasBase,taxasTarget],ignore_index=True)
        ProgressBar("Make Taxas Base Unifiqued in ",i,len(players),end=True)


    CreateAnalisedCSV(taxasAnaliseName)
    Analise(taxasBase,"Champion/Function",taxasAnaliseName)

    MakeBoxPlot(baseFiltred_csv,"Taxas")

print("==============================================================")
print("Start Analysis Second Step")
StartAnalise()
print("==============================================================")




    
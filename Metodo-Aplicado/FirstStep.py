import os
import csv
import datetime
import pandas as pd
import os

textMode = False
limit_percent = 1

#Set why columns name is able to use.
usedColumns = ["region","regionCode","gameEndTimestampToDate","championName","gameEndedInEarlySurrender","gameEndedInSurrender",
               "individualPosition","lane","role","summonerName","win"]
cutPlayersParameter = 5

directory = r"C:\Users\marco\Documents\TCC\Metodo-Aplicado\\"
dataBasePath = directory+"\\DataBase\\"

dataBaseName = "Dataset_LeagueOfLegends_2023.csv"
filtredName = "LOL_2023_Filtred.csv"

base_csv = pd.read_csv(dataBasePath+dataBaseName)

#This Function create CSV file if this don't is created before.
def CreateCSV(filePath,fieldnames): 
    print("Create CSV.")
    with open(filePath, mode="w",encoding="utf-16", newline="") as csvfile: 
        writer = csv.writer(csvfile)
        writer.writerow(fieldnames)

#This Function save all elements of local CSV in the file CSV.
def SaveCSV(baseCSV,otherCSVPath):
    baseCSV.to_csv(otherCSVPath,index=False)
    return 

#This Function is used to filter all things about the CSV.
def FilterData(playersIdentifierColumn:str,earlySurrenderIdentifier:str) -> bool:
    CreateCSV(os.path.join(dataBasePath,filtredName),usedColumns)

    filtred_csv = pd.read_csv(dataBasePath+filtredName,encoding = "utf-16")

    contagem = base_csv[playersIdentifierColumn].value_counts()
    filtred_csv = base_csv[base_csv[playersIdentifierColumn].isin(contagem[contagem.values > cutPlayersParameter].index)]
    filtred_csv = filtred_csv[usedColumns]
    filtred_csv = filtred_csv[filtred_csv[earlySurrenderIdentifier] != True]

    SaveCSV(filtred_csv,dataBasePath+filtredName)

    CreateCSV(os.path.join(directory,"Player_List.csv"),["Player_Id","Game_Count","Remove"])

    player_list = pd.DataFrame({
        "Player_Id": contagem.index,
        "Game_Count": contagem.values,
        "Remove": contagem > cutPlayersParameter
    })
    SaveCSV(player_list,directory+"Player_List.csv")
    return True

print("Start Process.")
FilterData("summonerName","gameEndedInEarlySurrender")
print("End Process.")
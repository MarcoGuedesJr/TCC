import os
import csv
import datetime
import pandas as pd
import os

textMode = False
limit_percent = 1

#Set why columns name is able to use.
usedColumns = ["region","regionCode","puuid","accountId","gameEndTimestampToDate","championName","gameEndedInEarlySurrender","gameEndedInSurrender",
               "individualPosition","lane","role","summonerName","win","playerIdRemaster"]

column_tag = {
    "player" : "summonerName",
    "playerIdentifier": "playerIdRemaster",
    "regionCode" : "regionCode",
    "champion" : "championName",
    "function" : "individualPosition"
}

cutPlayersParameter = 5

directory = r"C:\Users\marco\Documents\TCC\Metodo-Aplicado\\"
dataBasePath = directory+"\\DataBase\\"

dataBaseName = "Dataset_LeagueOfLegends_2023.csv"
filtredName = "LOL_2023_Filtred.csv"

base_csv = pd.read_csv(dataBasePath+dataBaseName)

def MakeTimePassString(startTime,endTime):
    time = endTime-startTime; seconds = int(time.total_seconds())
    hours = seconds // 3600; minutes = (seconds % 3600) // 60; seconds = seconds % 60
    timePass = f" | {hours:02}:{minutes:02}:{seconds:02}"
    return timePass

#This Function create CSV file if this don't is created before.
def CreateCSV(filePath,fieldnames): 
    print("Create CSV.")
    with open(filePath, mode="w",encoding="utf-16", newline="") as csvfile: 
        writer = csv.writer(csvfile)
        writer.writerow(fieldnames)

#This Function is used to filter all things about the CSV.
def FilterData(playersIdentifierColumn:str,earlySurrenderIdentifier:str) -> bool:
    CreateCSV(os.path.join(dataBasePath,filtredName),usedColumns)

    filtred_csv = pd.read_csv(dataBasePath+filtredName,encoding = "utf-16")

    base_csv["playerIdRemaster"] = (base_csv[column_tag["player"]] + base_csv[column_tag["regionCode"]])
    base_csv.to_csv(dataBasePath+"Dataset_LeagueOfLegends_2023.csv",index=False)

    filtred_csv = base_csv[base_csv[earlySurrenderIdentifier] != True]
    contagem = filtred_csv[playersIdentifierColumn].value_counts()
    filtred_csv = filtred_csv[filtred_csv[playersIdentifierColumn].isin(contagem[contagem.values > cutPlayersParameter].index)]
    filtred_csv = filtred_csv[usedColumns]
    filtred_csv.to_csv(dataBasePath+filtredName,index=False)

    CreateCSV(os.path.join(directory,"Player_List.csv"),["Player_Id","Game_Count","Remove"])

    player_list = pd.DataFrame({
        "Player_Id": contagem.index,
        "Game_Count": contagem.values,
        "Remove": contagem > cutPlayersParameter
    })
    player_list.to_csv(directory+"Player_List.csv",index=False)
    return True

print("==============================================================")
startTime = datetime.datetime.now()
print("Start Process. ")
FilterData(column_tag["playerIdentifier"],"gameEndedInEarlySurrender") #00:00:27
endTime = datetime.datetime.now()
print("End Process. "+MakeTimePassString(startTime,endTime))
print("==============================================================")
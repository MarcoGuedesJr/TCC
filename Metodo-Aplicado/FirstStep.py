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
dataBaseName = "Dataset_LeagueOfLegends_2023.csv"
filtredName = "LOL_2023_Filtred.csv"

base_csv = pd.read_csv(directory+dataBaseName)

def ProgressBar(message1,percentage,message2 = "%.",end = False):
    print(f"\r                                                                                                              ",
          end="", flush=True)
    print(f"\r"+message1+str(percentage)+message2, end="", flush=True)
    if(end): print("")

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

#This Function copy all elements in target columns from CSV file to other CSV file.
def CopyCSVColumnsToOtherCSV(baseCSV,otherCSV):
    columns_filtred = baseCSV[usedColumns]
    columns_filtred.to_csv(otherCSV,index=False)
    return 

#This Function is used to remove all columns don't used.
def RemoveColumns() -> bool:
    updateCount = 0

    print("###################################################################")
    print("Start Remove Columns Step.")
    print("###################################################################")
    CreateCSV(os.path.join(directory,filtredName),usedColumns)

    print("Copy Columns To Other CSV file.")
    CopyCSVColumnsToOtherCSV(base_csv,filtredName)

    print("Step Finish.")
    print("###################################################################")
    return True

def RemovePlayers(playersIdentifierColumn:str) -> bool:
    print("###################################################################")
    print("Start Remove Players Step.")
    print("###################################################################")

    print("Get Players in Columns.")
    players = base_csv[playersIdentifierColumn]

    print("Making Players List.")
    players_list = {}
    search_count = 0
    percentage = 0
    percentage_caller_number = 0.1
    percentage_old_called = -1 
    for player in players:
        if(textMode and limit_percent <= percentage): break
        search_count += 1
        percentage = 100*search_count/players.count()
        if(percentage >= percentage_old_called + percentage_caller_number):
            ProgressBar("Player List ",percentage,"%.")
            percentage_old_called = percentage
        search = False
        for target in players_list:
            if(player == target):
                players_list[player] = players_list[player]+1
                search = True
                break
        if(search == False):
            players_list[player] = 1
    ProgressBar("Player List ",100,"%.",True)
    
    print("Making Remove List.")
    players_remove_list = {}
    search_count = 0
    percentage = 0
    percentage_old_called = -1
    for player,count in players_list.items():
        if(textMode and limit_percent <= percentage): break
        search_count += 1
        percentage = 100*search_count/len(players_list)
        if(percentage >= percentage_old_called + percentage_caller_number):
            ProgressBar("Player Remove List ",percentage,"%.")
        players_remove_list[player] = count <= cutPlayersParameter
    ProgressBar("Player Remove List ",100,"%.",True)

    print("Remove Players From List.")
    modify_list = pd.read_csv(directory+filtredName)
    modify_list = modify_list[~modify_list["summonerName"].isin(player for player,remov in players_remove_list.items()
                                                                if remov == True)]
    CopyCSVColumnsToOtherCSV(modify_list,filtredName)

    print("Making CSV Player_List.")
    updateCount = 0
    search_count = 0
    percentage = 0
    percentage_old_called = -1
    CreateCSV(os.path.join(directory,"Player_List.csv"),["Player_Id","Game_Count","Remove"])
    for player,count in players_list.items():
        if(textMode and limit_percent <= percentage): break
        search_count += 1
        percentage = 100*search_count/len(players_list)
        remove = players_remove_list[player]
        updateCount = UpdateCSV(os.path.join(directory,"Player_List.csv"),[player,count,remove],updateCount,False)
        if(percentage >= percentage_old_called + percentage_caller_number):
                    ProgressBar("CSV Player_List ",percentage,"%. Update CSV Count : "+str(updateCount)+".")
    ProgressBar("CSV Player_List ",100,"%. "+ "Update CSV Count : "+str(updateCount),True)
    print("###################################################################")
    return True

def RemoveParts(earlySurrenderIdentifier: str) -> bool:
    print("###################################################################")
    print("Start Remove Parts Step.")
    print("###################################################################")

    print("Remove Parts From List.")
    modify_list = pd.read_csv(directory+filtredName)
    modify_list = modify_list[modify_list[earlySurrenderIdentifier] != True]
    CopyCSVColumnsToOtherCSV(modify_list,filtredName)

    print("###################################################################")
    return True

RemoveColumns()
RemovePlayers("summonerName")
RemoveParts("gameEndedInEarlySurrender")
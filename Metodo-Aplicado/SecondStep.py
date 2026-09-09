import os #Criar pastas
import csv
import datetime
import pandas as pd
import calendar
from pathlib import Path

#contagem = df['categoria'].value_counts()
#df = df[df['categoria'].isin(contagem[contagem >= 3].index)]

#df = df[df["coluna"] == playerName]

#pd.to_datetime

#from sklearn.cluster import KMeans
#import numpy as np

#from sklearn.tree import DecisionTreeClassifier

directory = r"C:\Users\marco\Documents\TCC\Metodo-Aplicado\\"
dataBaseFiltred = "LOL_2023_Filtred.csv"

WeekEnum = {1 : "Domingo", 2 : "Segunda-Feira",3 : "Terça-Feira", 4 : "Quarta-Feira",
    5 : "Quinta-Feira", 6 : "Sexta-Feira", 7 : "Sabado"}

MonthEnum = {1: "Janeiro", 2: "Fevereiro", 3: "Marco", 4: "Abril", 5: "Maio", 6: "Junho",
             7: "Julho", 8: "Agosto", 9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"}
MonthMaxDays = {1:31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}

startData = "aaaa/mm/dd"
whatYearsHave = 1
startYear = 2019
startMonth = MonthEnum[2]
startWeekDay = WeekEnum[1]
calendar_list = [ # Array of Years
            [ # Array of Months
             [ # Array of Week
                 ]]]

def Media(valoresA):
    soma = 0
    total = 0
    media = 0
    for valor in valoresA:
        soma += valor
        total += 1
    media = soma/total
    return media

def CreateTaxaForPlayer(player_name):
    filtredData = pd.read_csv(directory+dataBaseFiltred)
    filtredData["gameEndTimestampToDate"] = pd.to_datetime(filtredData["gameEndTimestampToDate"])
    filtredData["win"] = filtredData["gameEndTimestampToDate"].dt.year
    filtredData["year"] = filtredData["gameEndTimestampToDate"].dt.year
    filtredData["month"] = filtredData["gameEndTimestampToDate"].dt.month
    filtredData["week"] = ((filtredData["gameEndTimestampToDate"].dt.day -1) // 7) + 1

    player = filtredData[filtredData["summonerName"] == player_name]
    #player_parts = player.groupby(["year", "month", "week", "win"])
    player_champions = player.groupby(["championName"])

    os.makedirs(directory+"TaxasDosJogadores", exist_ok=True)
    os.makedirs(directory+"TaxasDosJogadores\\"+player_name,exist_ok=True)

    for champion in player_champions:
        championData = filtredData[filtredData["championName"] == champion]
        
        old_week = -1
        old_month = -1
        week_win_total = 0
        week_part_total = 0

        CreateCSV(os.path.join(directory+"TaxasDosJogadores\\"+player_name+"\\",champion+".csv"),["Year","Month","Week","pick_rate","win_rate"])

        years = championData["year"].unique()
        for year in years:
            yearData = championData[championData["year"] == year]
            months = yearData["month"].unique()
            for month in months:
                monthData = yearData[yearData["month"] == month]
                weeks = monthData["week"].unique()
                for week in weeks:
                    weekData = monthData[monthData["week" == week]]
                    week_part_total = (weekData["win"]).sum()
                    week_pick_rate = 
                    week_win_total = (weekData["win"] == win).sum()
                    UpdateCSV(os.path.join(directory+"TaxasDosJogadores\\"+player_name+"\\",champion+".csv"),
                              )

        for (year, month, week, win), parts in player_parts:
            if(old_month != month):
                 old_month = month
            if(old_week != week):
                old_week = week
                week_win_total = 0
                week_part_total = 0
            week_part_total += 1
            if win:
                week_win_total += 1

        print(parts)
        print(f"{year}/{month} - Semana {week}")

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

def CreateCalendar(startData,):
    pasta = Path(directory+"\\Calendaries")
    pasta.mkdir(parents=True, exist_ok=True)
    week_day = WeekEnum(startWeekDay)
    for i in range(startYear,startYear+whatYearsHave):
        pasta = Path(directory+"\\Calendaries\\"+str(i))
        pasta.mkdir(parents=True, exist_ok=True)
        for o in range(1,12):
            pasta = Path(directory+"\\Calendaries\\"+str(i)+"\\"+MonthEnum(o))
            pasta.mkdir(parents=True, exist_ok=True)
    a = calendar.Calendar.yeardatescalendar(startData)
    calendar_list.append(a)
    print(a)
    print("#####################################################################################")
    print(calendar_list)
    print("#####################################################################################")
    d = datetime.date.year
    print((d))

CreateTaxaForPlayer()
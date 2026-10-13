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
ThirdStepPath = dataBasePath+"3º Step\\"
FourthStepPath = dataBasePath+"4º Step\\"

base = {
    "baseFiltred":  pd.read_csv(dataBasePath+filtredName),
    "commitment" : pd.read_csv(ThirdStepPath+"Players_Vector_WinValue.csv"),
    "playerForce": pd.read_csv(FourthStepPath+"SpearmanEachPlayersAllStrategy.csv",encoding="utf-16"),
    "strategyForce": pd.read_csv(FourthStepPath+"SpearmanAllPlayersStrategy.csv",encoding="utf-16"),
    "playerStrategyForce": pd.read_csv(FourthStepPath+"SpearmanEachPlayerStrategy.csv",encoding="utf-16")
}


column_tag = {
    "player" : "summonerName",
    "playerIdentifier": "playerIdRemaster",
    "regionCode" : "regionCode",
    "champion" : "championName",
    "function" : "individualPosition"
}

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

def MakePlayerProfile(player,strategy,year,month,partidas_totais,
                      partidas,vitorias,fcr_player,fcr_strategy,fcr_player_strategy,
                      taxa_escolha,taxa_vitoria,fcr_playertx,fcr_strategytx,fcr_player_strategytx,
                      commit):
    profile = pd.DataFrame({
        "Player" : [player],
        "Strategy" : [strategy],
        "Year" : [year],
        "Month" : [month],
        "Partidas_Totais" : [partidas_totais],
        "Partidas" : [partidas],
        "Vitorias" : [vitorias],
        "Fcr_Player" : [fcr_player],
        "Fcr_Strategy" : [fcr_strategy],
        "Fcr_Player_strategy" : [fcr_player_strategy],
        "Taxa_Escolha" : [taxa_escolha],
        "Taxa_Vitoria" : [taxa_vitoria],
        "Fcr_PlayerTx" : [fcr_playertx],
        "Fcr_StrategyTx" : [fcr_strategytx],
        "Fcr_Player_strategyTx" : [fcr_player_strategytx],
        "Commit" : [commit]
    })
    return profile

def MakeAllPlayerProfile():
    #Criar 1 perfil mensal do jogador com 
    players = base["baseFiltred"][column_tag["playerIdentifier"]].unique()

    filtredBase = base["baseFiltred"]; commitmentBase = base["commitment"]
    playerFcrBase = base["playerForce"]; strategyFcrBase = base["strategyForce"]; playerStrategyFcrBase = base["playerStrategyForce"]

    allPlayersArray = []; i = 0; startTime = datetime.datetime.now()
    for player in players: 
        playerPath = playersPath+player+"\\"
        playerBase = filtredBase[filtredBase[column_tag["playerIdentifier"]] == player]; playerArray = []
        commitmentBaseP = commitmentBase[commitmentBase["Player"] == player]
        playerFcrBaseP = playerFcrBase[playerFcrBase["Player"] == player]
        playerStrategyFcrBaseP = playerStrategyFcrBase[playerStrategyFcrBase["Player"] == player]


        strategys = pd.unique(playerBase[[column_tag["champion"], column_tag["function"]]].to_numpy().flatten())
        strategys = strategys[pd.notna(strategys)]
        for strategy in strategys:
            strategyBase = playerBase[(playerBase[column_tag["champion"]] == strategy)|(playerBase[column_tag["function"]] == strategy)]
            commitmentBaseS = commitmentBaseP[commitmentBaseP["Champion/Function"] == strategy]
            strategyFcrBaseS = strategyFcrBase[strategyFcrBase["Champion/Function"] == strategy]
            playerStrategyFcrBaseS = playerStrategyFcrBaseP[playerStrategyFcrBaseP["Champion/Function"] == strategy]

            years = strategyBase["Year"].unique()
            for year in years:
                yearBase = strategyBase[strategyBase["Year"] == year]
                playerBaseYear = playerBase[playerBase["Year"] == year]
                commitmentBaseYear = commitmentBaseS[commitmentBaseS["Year"] == year]
                playerFcrBaseYear = playerFcrBaseP[playerFcrBaseP["Year"] == year]
                strategyFcrBaseYear = strategyFcrBaseS[strategyFcrBaseS["Year"] == year]
                playerStrategyFcrBaseYear = playerStrategyFcrBaseS[playerStrategyFcrBaseS["Year"] == year]

                months = yearBase["Month"].unique()
                for month in months:
                    monthBase = yearBase[yearBase["Month"] == month]
                    playerBaseMonth = playerBaseYear[playerBaseYear["Month"] == month]
                    commitmentBaseMonth = commitmentBaseYear[commitmentBaseYear["Month"] == month]
                    playerFcrBaseMonth = playerFcrBaseYear[playerFcrBaseYear["Month"] == month]
                    strategyFcrBaseMonth = strategyFcrBaseYear[strategyFcrBaseYear["Month"] == month]
                    playerStrategyFcrBaseMonth = playerStrategyFcrBaseYear[playerStrategyFcrBaseYear["Month"] == month]

                    baseStrategy = monthBase
                    basePlayer = playerBaseMonth
                    baseCommitment = commitmentBaseMonth
                    basePlayerFcr = playerFcrBaseMonth
                    baseStrategyFcr = strategyFcrBaseMonth
                    basePlayerStrategyFcr = playerStrategyFcrBaseMonth

                    part_strategy = len(baseStrategy["win"])
                    part_player = len(basePlayer["win"])

                    partidas_totais = part_player
                    partidas = part_strategy
                    vitorias = baseStrategy["win"].sum()

                    fcr_column = { "taxa/taxa" : "PickRate/WinRate", "part/win" : "Parts/Win"}
                    fcr_player = basePlayerFcr[fcr_column["taxa/taxa"]].iloc[0]
                    fcr_strategy = baseStrategyFcr[fcr_column["taxa/taxa"]].iloc[0]
                    fcr_player_strategy = basePlayerStrategyFcr[fcr_column["taxa/taxa"]].iloc[0]

                    taxa_escolha = round(part_strategy/part_player,2)
                    taxa_vitoria = round(vitorias/part_strategy,2)

                    fcr_playertx = basePlayerFcr[fcr_column["part/win"]].iloc[0]
                    fcr_strategytx = baseStrategyFcr[fcr_column["part/win"]].iloc[0]
                    fcr_player_strategytx = basePlayerStrategyFcr[fcr_column["part/win"]].iloc[0]

                    commit = baseCommitment["ensemble"].iloc[0]

                    #                                 player,strategy,year,month,partidas_totais,partidas,vitorias,fcr_player,fcr_strategy,fcr_player_strategy,taxa_escolha,taxa_vitoria,fcr_playertx,fcr_strategytx,fcr_player_strategytx,commit
                    playerProfile = MakePlayerProfile(player,strategy,year,month,partidas_totais,partidas,vitorias,fcr_player,fcr_strategy,fcr_player_strategy,taxa_escolha,taxa_vitoria,fcr_playertx,fcr_strategytx,fcr_player_strategytx,commit)
                    playerArray.append(playerProfile)
        playerArray= pd.concat(playerArray,ignore_index=True)
        allPlayersArray.append(playerArray)
        playerArray.to_csv(playerPath+"PlayerProfile.csv",index=False)
        i+= 1; ProgressBar("Making AllPlayerProfile and Make csv ",i,len(players),startTime=startTime,end=True)
    allPlayersArray = pd.concat(allPlayersArray,ignore_index=True)
    allPlayersArray.to_csv(dataBasePath+"PlayersProfile.csv",index=False)
    return

def MakePlayerCommitmentGrafic():
    playersProfile = pd.read_csv(dataBasePath+"PlayersProfile.csv")
    players = playersProfile["Player"].unique()

    i = 0; startTime = datetime.datetime.now()
    for player in players:
        playerPath = playersPath+player+"\\"
        playerProfile = playersProfile[playersProfile["Player"] == player]
        strategys = playerProfile["Strategy"].unique()
        for strategy in strategys:
            os.makedirs(playerPath+"CommitmentForYears",exist_ok=True)
            strategyProfile = playerProfile[playerProfile["Strategy"] == strategy]
            years = strategyProfile["Year"].unique()
            for year in years:
                os.makedirs(playerPath+"CommitmentForYears\\"+str(year),exist_ok=True)
                playerProfileYear = strategyProfile[strategyProfile["Year"] == year]
                # Cada ponto representa uma aparição da string em determinado mês

                label_order = ["Low", "Average", "High"]
                label_to_y = {label: i for i, label in enumerate(label_order)}

                playerProfileYear = playerProfileYear.sort_values("Month")

                y = playerProfileYear["Commit"].map(label_to_y)
                x = playerProfileYear["Month"]

                # Linha conectando os pontos
                plt.plot(x, y, linestyle="-", color="gray", alpha=0.7)

                # Pontos sobre a linha
                plt.scatter(x, y)

                plt.xlabel("Mês")
                plt.ylabel("Comprometimento")
                plt.title("Comprometimento Com A Estrategia por Mês.")

                plt.yticks(range(len(label_order)), label_order)
                plt.xticks(range(1, 13))
                plt.grid(axis="x", alpha=0.3)

                save_path = f"{playerPath}CommitmentForYears\\{str(year)}\\{strategy}_in_{year}.png"
                plt.savefig(save_path, dpi=300, bbox_inches="tight")
                plt.close()
                ProgressBar("Making PlayerCommitmentGrafic, "+str(i)+" de len(players) : ",i,len(players),startTime=startTime,end=True)
        i+= 1; 
    return

def MakePlayerCommitmentGraficTwo():
    playersProfile = pd.read_csv(dataBasePath + "PlayersProfile.csv")
    players = playersProfile["Player"].unique()

    label_order = ["Low", "Average", "High"]
    label_to_y = {label: i for i, label in enumerate(label_order)}
    label_positions = range(len(label_order))

    i = 0
    startTime = datetime.datetime.now()

    # Agrupa os dados uma única vez, preservando a ordem de aparição
    groupedPlayers = playersProfile.groupby("Player", sort=False)

    for player, playerProfile in groupedPlayers:
        playerPath = playersPath + player + "\\"
        commitmentPath = playerPath + "CommitmentForYears\\"

        os.makedirs(commitmentPath, exist_ok=True)

        # Agrupa as estratégias do jogador
        groupedStrategies = playerProfile.groupby("Strategy", sort=False)

        for strategy, strategyProfile in groupedStrategies:
            # Agrupa os anos da estratégia
            groupedYears = strategyProfile.groupby("Year", sort=False)

            for year, playerProfileYear in groupedYears:
                yearPath = commitmentPath + str(year) + "\\"
                os.makedirs(yearPath, exist_ok=True)

                # Ignorar estratégias com menos de 2 aparições no ano
                if playerProfileYear["Month"].nunique() < 2:
                    continue

                # Mantém a ordenação mensal original
                playerProfileYear = playerProfileYear.sort_values("Month")

                x = playerProfileYear["Month"]
                y = playerProfileYear["Commit"].map(label_to_y)

                # Cria uma figura independente para cada gráfico
                fig, ax = plt.subplots()

                # Linha conectando os pontos
                ax.plot(x, y, linestyle="-", color="gray", alpha=0.7)

                # Pontos sobre a linha
                ax.scatter(x, y)

                ax.set_xlabel("Mês")
                ax.set_ylabel("Comprometimento")
                ax.set_title("Comprometimento Com A Estrategia por Mês.")

                ax.set_yticks(label_positions, label_order)
                ax.set_xticks(range(1, 13))
                ax.grid(axis="x", alpha=0.3)

                save_path = (f"{yearPath}{strategy}_in_{year}.png")

                fig.savefig(save_path,dpi=300,bbox_inches="tight")
                plt.close(fig)

        ProgressBar("Making PlayerCommitmentGrafic, "+ str(i)+ " de "+ str(len(players))+ " : ",i,len(players),startTime=startTime,end=True)
        i += 1
    return

def ClassifyCorrelation(value):
    if pd.isna(value):
        return None
    
    if value < -1 or value > 1:
        return None
    
    force = abs(value)

    if force < 0.1:
        return "Neutro"

    if force < 0.3:
        strength = "Fraca"
    elif force < 0.6:
        strength = "Moderada"
    elif force < 0.9:
        strength = "Forte"
    else:
        strength = "Muito Forte"

    if value > 0:
        return f"Pos {strength}"
    else:
        return f"Neg {strength}"

def MakePlayerForceGrafic():
    playersProfile = pd.read_csv(dataBasePath + "PlayersProfile.csv")
    players = playersProfile["Player"].unique()

    label_order = ["Pos Muito Forte", "Pos Forte", "Pos Moderada", "Pos Fraca",
                   "Neutro",
                   "Neg Fraca", "Neg Moderada", "Neg Forte", "Neg Muito Forte"]
    label_to_y = {label: i for i, label in enumerate(label_order)}
    label_positions = range(len(label_order))

    i = 0; startTime = datetime.datetime.now()

    groupedPlayers = playersProfile.groupby("Player", sort=False)

    for player, playerProfile in groupedPlayers:
        playerPath = playersPath + player + "\\"
        forcePath = playerPath + "ForceForYears\\"

        os.makedirs(forcePath, exist_ok=True)

        groupedYears = playerProfile.groupby("Year", sort=False)

        correlationColumn = "i"
        playersProfile["ForceLabel"] = playersProfile[correlationColumn].apply(ClassifyCorrelation)

        for year, playerProfileYear in groupedYears:
            yearPath = forcePath + str(year) + "\\"
            os.makedirs(yearPath, exist_ok=True)

            if playerProfileYear["Month"].nunique() < 2:
                continue

            playerProfileYear = playerProfileYear.sort_values("Month")

            x = playerProfileYear["Month"]
            y = playerProfileYear["Commit"].map(label_to_y)

            fig, ax = plt.subplots()

            ax.plot(x, y, linestyle="-", color="gray", alpha=0.7)

            ax.scatter(x, y)

            ax.set_xlabel("Mês")
            ax.set_ylabel("Força Da Relação")
            ax.set_title("Adaptação Estrategica do Jogador Por Mês.")

            ax.set_yticks(label_positions, label_order)
            ax.set_xticks(range(1, 13))
            ax.grid(axis="x", alpha=0.3)

            save_path = (f"{yearPath}PlayerForce_in_{year}.png")

            fig.savefig(save_path,dpi=300,bbox_inches="tight")
            plt.close(fig)

        ProgressBar("Making MakePlayerForceGrafic, "+ str(i)+ " de "+ str(len(players))+ " : ",i,len(players),startTime=startTime,end=True)
        i += 1
    return

print("==============================================================")
print("Start Analysis Final Step")
baseFiltred = base["baseFiltred"]
baseFiltred["gameEndTimestampToDate"] = pd.to_datetime(baseFiltred["gameEndTimestampToDate"])
baseFiltred["Year"] = baseFiltred["gameEndTimestampToDate"].dt.year
baseFiltred["Month"] = baseFiltred["gameEndTimestampToDate"].dt.month
baseFiltred["Week"] = ((baseFiltred["gameEndTimestampToDate"].dt.day -1) // 7) + 1
base["baseFiltred"] = baseFiltred

MakeAllPlayerProfile() #00:26:32
#MakePlayerCommitmentGraficTwo() #03:24:05

print("==============================================================")




    
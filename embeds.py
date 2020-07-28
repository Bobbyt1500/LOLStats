import discord
import datetime
import riot_api_interface as rai

def create_user_embed(username):
    new_embed = discord.Embed(title="User",color=discord.Color.green(),description="Username="+username)
    return new_embed

def create_runes_embed(statistics, runes_data):
    new_embed = discord.Embed(title="Mains",color=discord.Color.purple())

    # Make embed field for each rune
    for i in range(6):
        info = rai.get_rune_information(statistics[0][0]["perk" + str(i)],statistics[0][0]["perk" + str(i) + "Var1"],statistics[0][0]["perk" + str(i) + "Var2"],statistics[0][0]["perk" + str(i) + "Var3"],runes_data)
        formatted_description = ""
        for desc in info[1]:
            formatted_description +=  desc + "\n"
        new_embed.add_field(name=info[0], value=formatted_description)

    
    return new_embed

def create_game_preview_embed(matchRef, match,champion_data,queue_data,statistics,username):
    new_embed = discord.Embed(title="Game",color=discord.Color.red(),description="Matchid="+str(matchRef["gameId"])+",Username="+username)

    champion_name = "No Data"

    # Get champion
    for champion in champion_data:
        if champion_data[champion]["key"] == str(matchRef["champion"]):
            champion_name = champion

    # Get time
    time = datetime.datetime.utcfromtimestamp(int(str(match["gameCreation"])[:-3])).strftime('%Y-%m-%d %H:%M:%S UTC')

    queue_type = "No Data"

    # Get queue type
    for queue in queue_data:
        if queue["queueId"] == matchRef["queue"]:
            queue_type = queue["description"] 
    
    # Get winloss
    if statistics["win"]:
        win_value = "Win"
    else:
        win_value = "Loss"

    new_embed.add_field(name="Outcome", value=win_value)
    new_embed.add_field(name="Queuetype", value=queue_type)
    new_embed.add_field(name="Role", value=matchRef["role"])
    new_embed.add_field(name="Lane", value=matchRef["lane"])
    new_embed.add_field(name="Champion", value=champion_name)
    new_embed.add_field(name="Date", value=time)
    new_embed.add_field(name="Normal Stats", value="✅")
    new_embed.add_field(name="Runes", value="♦️")
    return new_embed

def create_main_embed(statistics,single=False):
    new_embed = discord.Embed(title="Mains",color=discord.Color.dark_blue())
    if not single:
        new_embed.add_field(name="Number Of Valid Games", value=len(statistics[0]))
    if single:
        if statistics[0][0]["win"]:
            winloss = "Win"
        else:
            winloss = "Loss"
        new_embed.add_field(name="Outcome", value=winloss)
        new_embed.add_field(name="Matchid", value=statistics[5][0]["gameId"])
    new_embed.add_field(name="Kills",value=rai.get_average_stat(statistics[0], "kills"))
    new_embed.add_field(name="Deaths",value=rai.get_average_stat(statistics[0], "deaths"))
    new_embed.add_field(name="Assists",value=rai.get_average_stat(statistics[0], "assists"))
    if not single:
        new_embed.add_field(name="Win Rate",value=rai.get_wr(statistics[0]))
    return new_embed

def create_item_embed(item_data):
    new_embed = discord.Embed(title=item_data["name"],color=discord.Color.dark_blue())
    new_embed.set_image(url="https://ddragon.leagueoflegends.com/cdn/10.14.1/img/item/"+item_data["image"]["full"])
    new_embed.add_field(name="Usage", value=item_data["plaintext"])


    description = item_data["description"]

    if "</stats>" in description:
        stats = description.split("</stats>")[0]
    else:
        stats = "Not Applicable"
    


    new_embed.add_field(name="Stats", value=re.sub("<.*?>", "", stats))
    new_embed.add_field(name="Full Description", value=re.sub("<.*?>", " ", description))
    new_embed.add_field(name="Price", value=item_data["gold"]["total"])
    new_embed.add_field(name="Sell Value", value=item_data["gold"]["sell"])
    return new_embed

def create_damages_embed(statistics):
    new_embed = discord.Embed(title="Damages Dealt", color=discord.Color.dark_blue())
    new_embed.add_field(name="Total Damage To Champions", value=rai.get_average_stat(statistics[0], "totalDamageDealtToChampions"))
    new_embed.add_field(name="Total Physical Damage To Champions", value=rai.get_average_stat(statistics[0], "physicalDamageDealtToChampions"))
    new_embed.add_field(name="Total Magic Damage To Champions", value=rai.get_average_stat(statistics[0], "magicDamageDealtToChampions"))
    new_embed.add_field(name="Total True Damage To Champions", value=rai.get_average_stat(statistics[0], "trueDamageDealtToChampions"))
    new_embed.add_field(name="Total Damage Dealt", value=rai.get_average_stat(statistics[0], "totalDamageDealt"))
    new_embed.add_field(name="Total Physical Damage Dealt", value=rai.get_average_stat(statistics[0], "physicalDamageDealt"))
    new_embed.add_field(name="Total Magic Damage Dealt", value=rai.get_average_stat(statistics[0], "magicDamageDealt"))
    new_embed.add_field(name="Total True Damage Dealt", value=rai.get_average_stat(statistics[0], "trueDamageDealt"))
    new_embed.add_field(name="Total Damage To Objectives", value=rai.get_average_stat(statistics[0], "damageDealtToObjectives"))
    return new_embed

def create_tanked_embed(statistics):
    new_embed = discord.Embed(title="Damages Taken", color=discord.Color.dark_blue())
    new_embed.add_field(name="Total Damage Taken", value=rai.get_average_stat(statistics[0], "totalDamageTaken"))
    new_embed.add_field(name="Total Physical Damage Taken", value=rai.get_average_stat(statistics[0], "physicalDamageTaken"))
    new_embed.add_field(name="Total Magic Damage Taken", value=rai.get_average_stat(statistics[0], "magicalDamageTaken"))
    new_embed.add_field(name="Total True Damage Taken", value=rai.get_average_stat(statistics[0], "trueDamageTaken"))
    return new_embed

def create_vision_embed(statistics):
    new_embed = discord.Embed(title="Vision Statistics",color=discord.Color.dark_blue())
    new_embed.add_field(name="Vision Score", value=rai.get_average_stat(statistics[0], "visionScore"))
    new_embed.add_field(name="Wards Placed", value=rai.get_average_stat(statistics[0], "wardsPlaced"))
    new_embed.add_field(name="Wards Killed", value=rai.get_average_stat(statistics[0], "wardsKilled"))
    new_embed.add_field(name="Vision Wards Bought", value=rai.get_average_stat(statistics[0], "visionWardsBoughtInGame"))
    return new_embed

def create_jungle_embed(statistics):
    new_embed = discord.Embed(title="Jungle Statistics",color=discord.Color.dark_blue())
    new_embed.add_field(name="Monster Kills", value=rai.get_average_stat(statistics[0], "neutralMinionsKilled"))
    new_embed.add_field(name="Monster Kills Team Side", value=rai.get_average_stat(statistics[0], "neutralMinionsKilledTeamJungle"))
    new_embed.add_field(name="Monster Kills Enemy Side", value=rai.get_average_stat(statistics[0], "neutralMinionsKilledEnemyJungle"))
    return new_embed

def create_diffs_embed(statistics):
    new_embed = discord.Embed(title="Differences In Lane",color=discord.Color.dark_blue())
    new_embed.add_field(name="CS Difference 0-10", value=rai.get_average_delta(statistics[3], "csDiffPerMinDeltas", "0-10"))
    new_embed.add_field(name="CS Difference 10-20", value=rai.get_average_delta(statistics[3], "csDiffPerMinDeltas", "10-20"))
    new_embed.add_field(name="CS Difference 20-30", value=rai.get_average_delta(statistics[3], "csDiffPerMinDeltas", "20-30"))
    new_embed.add_field(name="Damage Taken Difference 0-10", value=rai.get_average_delta(statistics[3], "damageTakenDiffPerMinDeltas", "0-10"))
    new_embed.add_field(name="Damage Taken Difference 10-20", value=rai.get_average_delta(statistics[3], "damageTakenDiffPerMinDeltas", "10-20"))
    new_embed.add_field(name="Damage Taken Difference 20-30", value=rai.get_average_delta(statistics[3], "damageTakenDiffPerMinDeltas", "20-30"))
    new_embed.add_field(name="XP Difference 0-10", value=rai.get_average_delta(statistics[3], "xpDiffPerMinDeltas", "0-10"))
    new_embed.add_field(name="XP Difference 10-20", value=rai.get_average_delta(statistics[3], "xpDiffPerMinDeltas", "10-20"))
    new_embed.add_field(name="XP Difference 20-30", value=rai.get_average_delta(statistics[3], "xpDiffPerMinDeltas", "20-30"))
    return new_embed

def create_per_min_embed(statistics):
    new_embed = discord.Embed(title="Values Per Min",color=discord.Color.dark_blue())
    new_embed.add_field(name="CS Per Min 0-10", value=rai.get_average_delta(statistics[3], "creepsPerMinDeltas", "0-10"))
    new_embed.add_field(name="CS Per Min 10-20", value=rai.get_average_delta(statistics[3], "creepsPerMinDeltas", "10-20"))
    new_embed.add_field(name="CS Per Min 20-30", value=rai.get_average_delta(statistics[3], "creepsPerMinDeltas", "20-30"))
    new_embed.add_field(name="Gold Per Min 0-10", value=rai.get_average_delta(statistics[3], "goldPerMinDeltas", "0-10"))
    new_embed.add_field(name="Gold Per Min 10-20", value=rai.get_average_delta(statistics[3], "goldPerMinDeltas", "10-20"))
    new_embed.add_field(name="Gold Per Min 20-30", value=rai.get_average_delta(statistics[3], "goldPerMinDeltas", "20-30"))
    new_embed.add_field(name="XP Per Min 0-10", value=rai.get_average_delta(statistics[3], "xpPerMinDeltas", "0-10"))
    new_embed.add_field(name="XP Per Min 10-20", value=rai.get_average_delta(statistics[3], "xpPerMinDeltas", "10-20"))
    new_embed.add_field(name="XP Per Min 20-30", value=rai.get_average_delta(statistics[3], "xpPerMinDeltas", "20-30"))
    new_embed.add_field(name="Damage Taken Per Min 0-10", value=rai.get_average_delta(statistics[3], "damageTakenPerMinDeltas", "0-10"))
    new_embed.add_field(name="Damage Taken Per Min 10-20", value=rai.get_average_delta(statistics[3], "damageTakenPerMinDeltas", "10-20"))
    new_embed.add_field(name="Damage Taken Per Min 20-30", value=rai.get_average_delta(statistics[3], "damageTakenPerMinDeltas", "20-30"))
    return new_embed

def create_team_values_embed(statistics,single=False,champion_data=None):
    new_embed = discord.Embed(title="Team Statistics", color=discord.Color.dark_blue())
    new_embed.add_field(name="Tower Kills", value=rai.get_average_stat(statistics[4], "towerKills"))
    new_embed.add_field(name="Inhibitor Kills", value=rai.get_average_stat(statistics[4], "inhibitorKills"))
    new_embed.add_field(name="Dragon Kills", value=rai.get_average_stat(statistics[4], "dragonKills"))
    new_embed.add_field(name="Rift Herald Kills", value=rai.get_average_stat(statistics[4], "riftHeraldKills"))
    new_embed.add_field(name="Baron Kills", value=rai.get_average_stat(statistics[4], "baronKills"))
    if single:
        # Get bans from champ data
        bans = []
        for i in range(len(statistics[4][0]["bans"])):
            key = statistics[4][0]["bans"][i]["championId"]
            for champ in champion_data:
                if champion_data[champ]["key"] == str(key):
                    bans.append(champ)
        if len(bans) == 0:
            new_embed.add_field(name="Bans",value="No Data")
        else:
            new_embed.add_field(name="Bans",value=(", ".join(bans)))

    return new_embed

def create_build_embed(statistics,item_data):
    new_embed = discord.Embed(title="Build",color=discord.Color.dark_blue())
    for i in range(6):
        itemId = str(statistics[0][0]["item"+str(i)])
        if itemId == "0":
            new_embed.add_field(name="Item" + str(i), value="None")
        else:
            new_embed.add_field(name="Item" + str(i), value=item_data[itemId]["name"])
    

    return new_embed

def create_misc_embed(statistics):
    new_embed = discord.Embed(title="Miscellaneous",color=discord.Color.dark_blue())
    new_embed.add_field(name="Gold Earned",value=rai.get_average_stat(statistics[0], "goldEarned"))
    new_embed.add_field(name="Gold Spent",value=rai.get_average_stat(statistics[0], "goldSpent"))
    new_embed.add_field(name="Champion Level",value=rai.get_average_stat(statistics[0], "champLevel"))
    new_embed.add_field(name="Inhibitor Kills",value=rai.get_average_stat(statistics[0], "inhibitorKills"))
    new_embed.add_field(name="Turret Kills",value=rai.get_average_stat(statistics[0], "turretKills"))
    new_embed.add_field(name="Turret Damage",value=rai.get_average_stat(statistics[0], "damageDealtToTurrets"))
    new_embed.add_field(name="Total Healing",value=rai.get_average_stat(statistics[0], "totalHeal"))
    new_embed.add_field(name="Time CCing Others",value=rai.get_average_stat(statistics[0], "timeCCingOthers"))
    new_embed.add_field(name="Largest Multi Kill",value=rai.get_average_stat(statistics[0], "largestMultiKill"))
    return new_embed

def create_champs_embed(statistics,champion_data):
    new_embed = discord.Embed(title="Champions Played", color=discord.Color.dark_blue())

    # Create embed field for each champion
    for champion_key in statistics[6]:

        # Get champion name
        for champion in champion_data:
            if champion_data[champion]["key"] == str(champion_key):
                champion_name = champion
                break
        
        total_amount = statistics[6][champion_key]
        if total_amount > 1:
            new_embed.add_field(name=champion_name, value=str(total_amount) + " Games")
        else:
            new_embed.add_field(name=champion_name, value=str(total_amount) + " Game")

    return new_embed
import riot_api_interface as rai
import json
import discord
import datetime
import re

class Bot(discord.Client):
    async def on_ready(self):
        self.api = rai.RiotApi("Insert Key", "na1")
        self.accepted_list = ["Insert User IDs"]
        with open("item.json") as json_file:
            self.item_data = json.load(json_file)
        with open("champion.json") as json_file:
            self.champion_data = json.load(json_file)
        with open("queues.json") as json_file:
            self.queue_data = json.load(json_file)
        with open("perks.json") as json_file:
            self.runes_data = json.load(json_file)

    async def on_message(self, message):
        user = message.author
        # Check if accepted user
        if user.id in self.accepted_list:
            
            # Split message into arguments
            split_message = message.content.split(" ")

            # Request Command
            if split_message[0] == "request":
                if len(split_message) < 4:
                    await message.channel.send("Wrong parameters")
                    return
                # Get username from op.gg or just input
                if "op.gg" in split_message[1]:
                    username = split_message[1].split("userName=")[1].replace("+", " ")
                else:
                    username = split_message[1].replace("_", " ")
                
                if split_message[2] == "avg":

                    # Get match history and check if there was an error
                    if len(split_message) >= 5:

                        # If champion requested
                        if split_message[4] in self.champion_data["data"]:
                            champion_key = self.champion_data["data"][split_message[4]]["key"]
                            match_history = self.api.get_match_history(split_message[3], username, champion=champion_key)
                        else:
                            await message.channel.send("Not a correct champion name. Make sure the first letter is capitalized and it is spelled correctly")
                            await message.channel.send("If the champion name has a space/,/'/. dont include it. Example: Twisted Fate is just TwistedFate  Dr.Mundo is DrMundo    Rek'Sai is RekSai    Nunu is also just Nunu")
                            return
                    else:     
                        match_history = self.api.get_match_history(split_message[3], username)

                    if not match_history:
                        await message.channel.send("Something went wrong. Most likely too much data was requested from the riot API. Try again later")
                        return

                    # Get statistics
                    statistics = rai.get_player_statistics(match_history[0], match_history[1], extras=True)

                    if not statistics:
                        await message.channel.send("Something went wrong.")
                        return
                    
                    # Create Embeds for Stats
                    main_embed = create_main_embed(statistics)

                    await message.channel.send(embed=main_embed)

                    champs_embed = create_champs_embed(statistics, self.champion_data["data"])

                    await message.channel.send(embed=champs_embed)

                    damages_embed = create_damages_embed(statistics)
                    
                    await message.channel.send(embed=damages_embed)

                    tanked_embed = create_tanked_embed(statistics)

                    await message.channel.send(embed=tanked_embed)

                    vision_embed = create_vision_embed(statistics)

                    await message.channel.send(embed=vision_embed)

                    jungle_embed = create_jungle_embed(statistics)
                    
                    await message.channel.send(embed=jungle_embed)

                    diffs_embed = create_diffs_embed(statistics)

                    await message.channel.send(embed=diffs_embed)

                    per_min_embed = create_per_min_embed(statistics)

                    await message.channel.send(embed=per_min_embed)

                    misc_embed = create_misc_embed(statistics)

                    await message.channel.send(embed=misc_embed)

                if split_message[2] == "rankedavg":

                    # Get match history and check if there was an error
                    if len(split_message) >= 5:

                        # If champion requested
                        if split_message[4] in self.champion_data["data"]:
                            champion_key = self.champion_data["data"][split_message[4]]["key"]
                            match_history = self.api.get_match_history(split_message[3], username, champion=champion_key,ranked=True)
                        else:
                            await message.channel.send("Not a correct champion name. Make sure the first letter is capitalized and it is spelled correctly")
                            await message.channel.send("If the champion name has a space/,/'/. dont include it. Example: Twisted Fate is just TwistedFate  Dr.Mundo is DrMundo    Rek'Sai is RekSai    Nunu is also just Nunu")
                            return
                    else:     
                        match_history = self.api.get_match_history(split_message[3], username,ranked=True)

                    if not match_history:
                        await message.channel.send("Something went wrong. Most likely too much data was requested from the riot API. Try again later")
                        return

                    # Get statistics
                    statistics = rai.get_player_statistics(match_history[0], match_history[1], extras=True)

                    if not statistics:
                        await message.channel.send("Something went wrong.")
                        return
                    
                    # Create Embeds for Stats
                    main_embed = create_main_embed(statistics)

                    await message.channel.send(embed=main_embed)

                    champs_embed = create_champs_embed(statistics, self.champion_data["data"])

                    await message.channel.send(embed=champs_embed)

                    damages_embed = create_damages_embed(statistics)
                    
                    await message.channel.send(embed=damages_embed)

                    tanked_embed = create_tanked_embed(statistics)

                    await message.channel.send(embed=tanked_embed)

                    vision_embed = create_vision_embed(statistics)

                    await message.channel.send(embed=vision_embed)

                    jungle_embed = create_jungle_embed(statistics)
                    
                    await message.channel.send(embed=jungle_embed)

                    diffs_embed = create_diffs_embed(statistics)

                    await message.channel.send(embed=diffs_embed)

                    per_min_embed = create_per_min_embed(statistics)

                    await message.channel.send(embed=per_min_embed)

                    misc_embed = create_misc_embed(statistics)

                    await message.channel.send(embed=misc_embed)

                if split_message[2] == "games":



                    if len(split_message) >= 5:

                        # If champion requested
                        if split_message[4] in self.champion_data["data"]:
                            champion_key = self.champion_data["data"][split_message[4]]["key"]
                            match_history = self.api.get_match_history(split_message[3], username, champion=champion_key, orginals=True)
                        else:
                            await message.channel.send("Not a correct champion name. Make sure the first letter is capitalized and it is spelled correctly")
                            await message.channel.send("If the champion name has a space/,/'/. dont include it. Example: Twisted Fate is just TwistedFate  Dr.Mundo is DrMundo    Rek'Sai is RekSai    Nunu & Willump is also just Nunu")
                            return
                    else:     
                        match_history = self.api.get_match_history(split_message[3], username, orginals=True)


                    # Check if request went through
                    if not match_history:
                        await message.channel.send("Something went wrong. Most likely too much data was requested from the riot API. Try again later")
                        return

                    match_history[0].reverse()
                    match_history[1].reverse()

                    # Get statistics
                    statistics = rai.get_player_statistics(match_history[0], match_history[2], game_mode_exclusion=False)

                    if not statistics:
                        await message.channel.send("Something went wrong.")
                        return

                    for i in range(len(match_history[1])):
                        sent = await message.channel.send(embed=create_game_preview_embed(match_history[1][i], match_history[0][i],self.champion_data["data"],self.queue_data,statistics[0][i],username))
                        await sent.add_reaction("✅")
                        await sent.add_reaction("♦️")

            # Match Request Command
            if split_message[0] == "matchrequest":
                if len(split_message) == 3:

                    # Get champion key
                    if split_message[2] in self.champion_data["data"]:
                        champion_key = self.champion_data["data"][split_message[2]]["key"]
                    else:
                        await message.channel.send("Not a correct champion name. Make sure the first letter is capitalized and it is spelled correctly")
                        await message.channel.send("If the champion name has a space/,/'/. dont include it. Example: Twisted Fate is just TwistedFate  Dr.Mundo is DrMundo    Rek'Sai is RekSai    Nunu is also just Nunu")
                        return
                    
                    statistics = self.api.get_single_match(split_message[1], champion_key)

                    await message.channel.send(embed=create_main_embed(statistics,single=True))
                    await message.channel.send(embed=create_damages_embed(statistics))
                    await message.channel.send(embed=create_tanked_embed(statistics))
                    await message.channel.send(embed=create_vision_embed(statistics))
                    await message.channel.send(embed=create_jungle_embed(statistics))
                    await message.channel.send(embed=create_diffs_embed(statistics))
                    await message.channel.send(embed=create_per_min_embed(statistics))
                    await message.channel.send(embed=create_team_values_embed(statistics,single=True,champion_data=self.champion_data["data"]))
                    await message.channel.send(embed=create_build_embed(statistics,self.item_data["data"]))
                    await message.channel.send(embed=create_misc_embed(statistics))
            
            # Help Command
            if split_message[0] == "help":
                new_embed = discord.Embed(title="Help",color=discord.Color.green())
                #new_embed.add_field(name="Request Averages",value="request {username/op.gg (replace spaces with _)} avg {number of games} {optional-Name of champion (replace spaces with _)}",inline=True)
                #new_embed.add_field(name="Request Games",value="request {username/op.gg (replace spaces with _)} games {number of games} {optional-Name of champion (replace spaces with _)}")
                #new_embed._field(name="Request Custom Game/Match",value="matchrequest {matchid} {Name of champion played (replace spaces with _)}")
                #new_embed.add_field(name="Request Item",value="item {Name of item (replace spaces with _)/list - to see all my }")
                new_embed.insert_field_at(index=1,name="Request Averages",value="request {username/op.gg (replace spaces with underscores)} avg {number of games} {optional-Name of champion (replace spaces with underscores)}")
                await message.channel.send(embed=new_embed)
                new_embed.clear_fields()
                new_embed.insert_field_at(index=1,name="Request Ranked Averages",value="request {username/op.gg (replace spaces with underscores)} rankedavg {number of games} {optional-Name of champion (replace spaces with underscores)}")
                await message.channel.send(embed=new_embed)
                new_embed.clear_fields()
                new_embed.insert_field_at(index=1,name="Request Games",value="request {username/op.gg (replace spaces with underscores)} games {number of games} {optional-Name of champion (replace spaces with underscores)}")
                await message.channel.send(embed=new_embed)
                new_embed.clear_fields()
                new_embed.insert_field_at(index=1,name="Request Custom Game/Match",value="matchrequest {matchid} {Name of champion played (replace spaces with underscores)}")
                await message.channel.send(embed=new_embed)
                new_embed.clear_fields()
                new_embed.insert_field_at(index=1,name="Request Item",value="item {Name of item (replace spaces with underscores)/list - to see all items }")
                await message.channel.send(embed=new_embed)

            # Item Command
            if split_message[0] == "item":
                
                # List Items
                if split_message[1] == "list":
                    data = self.item_data["data"]
                    item_list = ""
                    for item in data:
                        if len(item_list + (", " + data[item]["name"])) >= 2000:
                            await message.channel.send(item_list)
                            item_list = ""
                        item_list += (", " + data[item]["name"])
                    await message.channel.send(item_list)
                    return
                        

                # Check parameters
                if len(split_message) > 2:
                    await message.channel.send("Too many parameters. Make sure spaces are replaced with _")
                    return

                # Get Data on item and send it
                data = self.item_data["data"]
                query = split_message[1].replace("_", " ")
                for item in data:
                    if data[item]["name"] == query:
                        item_data = data[item]
                        item_embed = create_item_embed(item_data)
                        await message.channel.send(embed=item_embed)
                        return

                # If item isnt found, tell user
                await message.channel.send("Item not found. Make sure it is spelled correctly, has proper capitalization, and spaces are replaced with -")
                    
    async def on_reaction_add(self, reaction, user):
        if reaction.count > 1:
            if user.id in self.accepted_list:
                message = reaction.message
                embed = message.embeds[0]
                description = embed.description
                # Get data
                if "Matchid=" in description and "Username=" in description:
                    split = description.split(",")
                    matchid = split[0].replace("Matchid=", "")
                    username = split[1].replace("Username=", "")
                    accoundId = self.api.make_request("/lol/summoner/v4/summoners/by-name/" + username)["accountId"]
                    match = self.api.make_request("/lol/match/v4/matches/" + matchid)

                    if not match or not accoundId:
                        await message.channel.send("Something went wrong. Most likely too much data was requested from the riot API. Try again later")
                        return

                    # Get stats
                    statistics = rai.get_player_statistics([match], accoundId, extras=True, game_mode_exclusion=False)

                    if not statistics:
                        await message.channel.send("Error getting statistics")
                        return

                    if reaction.emoji == "♦️":
                        await message.channel.send(embed=create_runes_embed(statistics,self.runes_data))

                    if reaction.emoji == "✅":
                        # Send normal statistics
                        await message.channel.send(embed=create_main_embed(statistics,single=True))
                        await message.channel.send(embed=create_damages_embed(statistics))
                        await message.channel.send(embed=create_tanked_embed(statistics))
                        await message.channel.send(embed=create_vision_embed(statistics))
                        await message.channel.send(embed=create_jungle_embed(statistics))
                        await message.channel.send(embed=create_diffs_embed(statistics))
                        await message.channel.send(embed=create_per_min_embed(statistics))
                        await message.channel.send(embed=create_team_values_embed(statistics,single=True,champion_data=self.champion_data["data"]))
                        await message.channel.send(embed=create_build_embed(statistics,self.item_data["data"]))
                        await message.channel.send(embed=create_misc_embed(statistics))
                
                
def create_runes_embed(statistics, runes_data):
    new_embed = discord.Embed(title="Runes",color=discord.Color.purple())

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

client = Bot()
client.run("Insert bot token")


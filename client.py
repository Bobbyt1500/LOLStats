import riot_api_interface as rai
import json
import discord
import re
import os
from embeds import *

class Bot(discord.Client):
    async def on_ready(self):
        self.api = rai.RiotApi(os.environ["API-KEY"], "na1")
        self.accepted_list = [200689481496526850,299314753220640778,149869170291507201]
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

            if split_message[0] == "cr":
                self.api.region = split_message[1].lower()
                await message.channel.send("Region changed")

            if split_message[0] == "region":
                await message.channel.send(self.api.region)

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
            
            # Multi Request Command
            if split_message[0] == "multirequest":
                if "op.gg" in split_message[1]:
                    usernames = split_message[1].split("query=")[1].split("%2C")
                    for user in usernames:
                        sent = await message.channel.send(embed=create_user_embed(user));
                        await sent.add_reaction("✅")
                    

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
                elif "Username=" in description:
                    username = description.split("Username=")[1]
                    match_history = self.api.get_match_history(15, username,ranked=True)

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

client = Bot()
client.run(os.environ["API-KEY"])


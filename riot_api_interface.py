import requests

class RiotApi:
    def __init__(self, api_key, region):
        self.api_key = api_key
        self.region = region
    
    def make_request(self, link, parameters=None):
        # Create a request url
        if parameters:
            request_url = "https://" + self.region + ".api.riotgames.com" + link + "?api_key=" + self.api_key + "&" + parameters
        else:
            request_url = "https://" + self.region + ".api.riotgames.com" + link + "?api_key=" + self.api_key


        # Make the request
        response = requests.get(request_url)

        # Returns false if the response did not work
        if not response.status_code == 200:
            return False
        return response.json()

    def change_region(self, region):
        self.region = region
    
    def get_match_history(self, n, username, champion = False, orginals=False, ranked = False):

        # Request account id and return false if failure
        request = self.make_request("/lol/summoner/v4/summoners/by-name/" + username)
        if not request:
            return False
        account_id = request["accountId"]

        # Request matchlist and return false if failure
        if champion:
            # Request for specific champ if given
            if ranked:
                request = self.make_request("/lol/match/v4/matchlists/by-account/"+account_id, parameters="endIndex=" + str(n) + "&queue=420&champion=" + champion)
            else:
                request = self.make_request("/lol/match/v4/matchlists/by-account/"+account_id, parameters="endIndex=" + str(n) + "&champion=" + champion)
        else:
            if ranked:
                request = self.make_request("/lol/match/v4/matchlists/by-account/"+account_id, parameters="endIndex=" + str(n) + "&queue=420")
            else:
                request = self.make_request("/lol/match/v4/matchlists/by-account/"+account_id, parameters="endIndex=" + str(n))
        if not request:
            return False
        match_history = request["matches"]
        
        # Add all matchs to a list
        matches = []
        for match in match_history:
            # Request match and return false if failure
            request = self.make_request("/lol/match/v4/matches/"+str(match["gameId"]))
            if not request:
                return False
            
            matches.append(request)

        # If original match dictionaries are requested, return them
        if orginals:
            return (matches, match_history, account_id)

        # If no failures occured, return matches and account+id
        return (matches, account_id)

    def get_single_match(self, matchid, champion):
        match = self.make_request("/lol/match/v4/matches/" + matchid)
        if not match:
            return False
        for participant in match["participants"]:
            if str(participant["championId"]) == champion:
                teamid = participant["teamId"]
                for team in match["teams"]:
                    if team["teamId"] == teamid:
                        correct_team = team
                return ([participant["stats"]], None, [participant],[participant["timeline"]],[correct_team],[match])


def get_average_stat(statistics, stat):
    """
    Gets an average for a stat
    """
    summation = 0
    total = 0
    for s in statistics:
        if stat not in s.keys():
            continue
        summation += s[stat]
        total += 1
    
    if total == 0:
        return "No Data"

    return round(summation/len(statistics), 3)

def get_wr(statistics):
    """
    Gets winrate over the games given in stats
    """
    total_wins = 0
    total_games = 0
    for s in statistics:
        total_games += 1
        if s["win"]:
            total_wins += 1
    
    if total_games == 0:
        return "No Data"
    return round(total_wins/total_games, 3)

def get_average_delta(timelines, value, time_frame):
    """
    Gets average values for a delta with timeframe and value
    """
    summation = 0
    total = 0 
    for timeline in timelines:
        if value in timeline:
            delta = timeline[value]
            if time_frame in delta:
                summation += delta[time_frame]
                total += 1
    if total == 0:
        return "No Data"
    return round(summation/total, 3)

def get_player_statistics(match_history, account_id, extras = False, game_mode_exclusion=True):
    """
    Returns a list of player statistics dictionaries for each of the games
    """
    statistics = []
    timelines = []
    participantDatas = []
    teams = []
    games = []
    champions = {}
    amount = 0
    

    for match in match_history:
        # Check gamemode
        if game_mode_exclusion:
            if not match["gameMode"] == "CLASSIC":
                continue
        
        participant_id = None
        # Get participant id of username
        for identity in match["participantIdentities"]:
            player = identity["player"]
            if player["currentAccountId"] == account_id:
                participant_id = identity["participantId"]
                break
        
        if not participant_id:
            continue

        # Add all statistics on a player to the correct list
        for participant in match["participants"]:
            if participant["participantId"] == participant_id:
                amount += 1
                # Statistics data
                statistics.append(participant["stats"])
                if extras:
                    # Game
                    games.append(match)
                    # Participantdata
                    participantDatas.append(participant)
                    # Teamdata
                    teamid = participant["teamId"]
                    for team in match["teams"]:
                        if team["teamId"] == teamid:
                            teams.append(team)
                    # Timelinedata
                    timelines.append(participant["timeline"])
                    # Champion data
                    champ = participant["championId"]
                    if champ not in champions.keys():
                        champions[champ] = 1
                    else:
                        champions[champ] += 1
                break

    if extras:
        return (statistics, amount, participantDatas, timelines, teams, games, champions)
    else:
        return (statistics, amount)

def get_rune_information(rune, runevar1, runevar2, runevar3, runes_data):
    name = "Not Found"
    descriptions = "Descriptions Not Found"

    # Check in rune data for the rune
    for rune_info in runes_data:
        if rune_info["id"] == rune:

            # Get the name and descriptions
            name = rune_info["name"]
            descriptions = rune_info["endOfGameStatDescs"]

            # Update descriptions with rune vars
            for i in range(len(descriptions)):
                if "@eogvar1@" in descriptions[i]:
                    descriptions[i] = descriptions[i].replace("@eogvar1@", str(runevar1))
                if "@eogvar2@" in descriptions[i]:
                    descriptions[i] = descriptions[i].replace("@eogvar2@", str(runevar2))
                if "@eogvar3@" in descriptions[i]:
                    descriptions[i] = descriptions[i].replace("@eogvar3@", str(runevar3))

                
    return (name, descriptions)
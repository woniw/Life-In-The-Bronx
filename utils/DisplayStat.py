from utils.variables import player_stats
from utils.Allitems import weapons

def showItemDescription(requested_item_description: str):
    if requested_item_description in weapons:
        item_description = weapons[requested_item_description]["description"]

        return item_description
    elif requested_item_description not in weapons:
        return "Item Doesnt exist"



def showStat(requested_stat: str, user_id: str, data: dict):
    if requested_stat in player_stats:
        print("")
        print("| --- LOG --- |")
        print("   Stat is being displayed!")
        print("")

        if requested_stat == "equipped":
            equipped_item = data["USERS"][user_id]["equipped"]["name"]
            return equipped_item
        
        elif requested_stat == "class":
            user_stat = data["USERS"][user_id][requested_stat]
            return user_stat
        
        elif requested_stat != "class":
            user_stat = data["USERS"][user_id][requested_stat]
            return user_stat
        
    elif requested_stat not in player_stats:
        print("| --- LOG --- |")
        print("   Returning: 'Invalid Request'")
        return "Invalid Request"
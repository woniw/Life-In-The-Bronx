from utils.variables import player_stats
from utils.Allitems import all_items

def showItemDescription(requested_item_description: str):
    if requested_item_description in all_items:
        print("-- ITEM WAS FOUND --")
        item_description = all_items[requested_item_description]["description"]
        item_type = all_items[requested_item_description]["type"]

        print("")
        print("| --- ITEM LOG --- |")
        print(f"    Item Name: {requested_item_description}")
        print(f"    Item description: {item_description}")
        print(f"    Item type: {item_type}")
        return item_description, item_type
    
    elif requested_item_description not in all_items:
        print("-- ITEM WAS NOT FOUND --")
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
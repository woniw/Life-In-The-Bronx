from utils.Allitems import all_items
from utils.variables import default_health
from utils.variables import tank_health


def CheckJoinedUser(data: dict, user_id: str):
    if user_id in data["USERS"]:
        print("USER IS ALREADY ADDED")
        return True
    elif user_id not in data["USERS"]:
        print("USER IS NOT ADDED")
        return False

def AddUser(data: dict, user_id: str, generated_handedness: str, generated_class: str):
    if generated_class == "Tank":
        print(f"TANK CLASS HAS BEEN GIVEN TO {user_id}")
        print(f"{tank_health} HAS BEEN GIVEN TO {user_id}")
        data["USERS"][user_id] = {
            "class": generated_class,
            "health": tank_health,
            "balance": 0,
            "handedness": generated_handedness,
            "equipped": all_items["fists"]["name"],
            "damage": all_items["fists"]["damage"],
            "inventory": []
        }
    else:
        print(f"{generated_class} CLASS HAS BEEN GIVEN TO {user_id}")
        data["USERS"][user_id] = {
            "class": generated_class,
            "health": default_health,
            "balance": 0,
            "handedness": generated_handedness,
            "equipped": all_items["fists"],
            "damage": all_items["fists"]["damage"],
            "inventory": []
        }

def checkUserStat(data: dict, user_id: str, stat):
    user_stat_result = data["USERS"][user_id][stat]
    return user_stat_result



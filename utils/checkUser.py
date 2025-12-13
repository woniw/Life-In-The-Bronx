from utils.Allitems import all_items
from utils.variables import default_health
from utils.variables import tank_health


def CheckJoinedUser(data: dict, user_id: str):
    if user_id in data["USERS"]:
        print("USER IS ALREADY ADDED")
        return True
    elif user_id not in data["USERS"]:
        return False

def AddUser(data: dict, user_id: str, generated_handedness: str, generated_class: str):
    if user_id == "710208977614536725":
        generated_class = "Fatty"
        print(f"THE fatty has joined")
        data["USERS"][user_id] = {
            "class": generated_class,
            "health": 100,
            "balance": 0,
            "handedness": generated_handedness,
            "equipped": "Fists",
            "damage": 5,
            "durability": 999999999,
            "inventory": [],
            "title": "THE fatty",
            "titles": ["THE fatty"],

            "record": {
                "dumpster_diving_count": 0,
                "jump_count": 0,
                "beg_count": 0
            }

        }
    elif generated_class == "Tank":
        print(f"TANK CLASS HAS BEEN GIVEN TO {user_id}")
        print(f"{tank_health} HAS BEEN GIVEN TO {user_id}")
        data["USERS"][user_id] = {
            "class": generated_class,
            "health": tank_health,
            "balance": 0,
            "handedness": generated_handedness,
            "equipped": "Fists",
            "damage": 5,
            "durability": 999999999,
            "inventory": [],
            "title": "none",
            "titles": [],

            "record": {
                "dumpster_diving_count": 0,
                "jump_count": 0,
                "beg_count": 0
            }
            
        }
    else:
        print(f"{generated_class} CLASS HAS BEEN GIVEN TO {user_id}")
        data["USERS"][user_id] = {
            "class": generated_class,
            "health": default_health,
            "balance": 0,
            "handedness": generated_handedness,
            "equipped": "Fists",
            "damage": 5,
            "durability": 999999999,
            "inventory": [],
            "title": "none",
            "titles": [],

            "record": {
                "dumpster_diving_count": 0,
                "jump_count": 0,
                "beg_count": 0
            }
        }

def checkUserStat(data: dict, user_id: str, stat):
    user_stat_result = data["USERS"][user_id][stat]
    return user_stat_result



from utils.GenerateStats import generateHandedness
from utils.GenerateStats import generateClass
from utils.variables import default_health
from utils.Allitems import weapons

handedness_result = generateHandedness()
class_result = generateClass()

def CheckJoinedUser(data: dict, user_id: str):
    if user_id in data:
        print("USER IS ALREADY ADDED")
        return True
    elif user_id not in data:
        print("USER IS NOT ADDED")
        return False

def AddUser(data: dict, user_id: str):
    if class_result == "Tank":
        data["USERS"][user_id] = {
            "health": default_health + 15,
            "balance": 0,
            "handedness": handedness_result,
            "equipped": weapons["fists"]["name"],
            "damage": weapons["fists"]["damage"],
            "inventory": []
        }
    else:
        data["USERS"][user_id] = {
            "health": default_health,
            "balance": 0,
            "handedness": handedness_result,
            "equipped": weapons["fists"],
            "damage": weapons["fists"]["damage"],
            "inventory": []
        }


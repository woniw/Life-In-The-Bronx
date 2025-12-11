from utils.variables import admin_ids
from utils.checkUser import CheckJoinedUser
from utils.variables import player_classes

def addMoney(data: dict, user_id: str, amount: int, target: str):
    target_joined_result = CheckJoinedUser(data=data, user_id=target)
    target_balance = data["USERS"][target]["balance"]

    if target_joined_result:
        if user_id not in admin_ids:
            return "Invalid Permissions"
        elif user_id in admin_ids:
            print("")
            print("| --- LOG --- |")
            print(f"   User balance before adding money: {data['USERS'][target]['balance']}")
            print(f"   adding: {amount}")
            new_target_balance = data["USERS"][target]["balance"] = data["USERS"][target]["balance"] + amount
            print("   **Money has been added**")
            print(f"   User balance after adding money: {new_target_balance}")
            print("")

            return "Successfull Transaction", new_target_balance, target_balance
    else:
        return "Invalid Target"


def setMoney(data: dict, user_id: str, amount: int, target: str):
    target_joined_result = CheckJoinedUser(data=data, user_id=target)
    target_balance = data["USERS"][target]["balance"]

    if target_joined_result:
        if user_id not in admin_ids:
            return "Invalid Permissions"
        elif user_id in admin_ids:
            print("")
            print("| --- LOG --- |")
            print(f"   User balance before setting money: {data['USERS'][target]['balance']}")
            print(f"   seting to: {amount}")
            new_target_balance = data["USERS"][target]["balance"] = data["USERS"][target]["balance"] - data["USERS"][target]["balance"]
            new_target_balance = data["USERS"][target]["balance"] = new_target_balance + amount
            print("   **Money has been added**")
            print(f"   User balance after setting money: {new_target_balance}")
            print("")

            return "Successfull Transaction", new_target_balance, target_balance
    else:
        return "Invalid Target"
    

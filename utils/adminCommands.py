from utils.variables import admin_ids
from utils.checkUser import CheckJoinedUser

def addMoney(data: dict, user_id: str, amount: int, target: str):
    target_joined_result = CheckJoinedUser(data=data, user_id=target)
    target_balance = data["USERS"][user_id]["balance"]

    if target_joined_result:
        if target not in admin_ids:
            return "Invalid Permissions"
        elif target in admin_ids:
            data["USERS"][user_id]["balance"] += amount
            print("")
            print("| --- LOG --- |")
            print("   Money has been added")
            print(f"   User Balance: {target_balance}")
            print("")

            return "Successfull Transaction"
    else:
        return "Invalid Target"

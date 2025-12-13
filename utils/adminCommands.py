from utils.variables import admin_ids
from utils.checkUser import CheckJoinedUser

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
    
def giveMoney(data: dict, user_id: str, amount: int, target: str):
    print('Running give money function')
    user_id = str(user_id)
    target_joined_result = CheckJoinedUser(data=data, user_id=target)
    target_balance = int(data["USERS"][target]["balance"])

    print(f"amount: {amount}")
    print(f'user balance: {data["USERS"][user_id]["balance"]}')
    print(f"target balance: {target_balance}")

    if target_joined_result:
        print("target has joined")
        if amount > data["USERS"][user_id]["balance"]:
            print('INVALID BALANCE')
            return "Invalid Balance"
        elif amount <= data["USERS"][user_id]["balance"]:
            print("GIVING MONEY")
            data["USERS"][target]["balance"] = data["USERS"][target]["balance"] + amount
            data["USERS"][user_id]["balance"] = data["USERS"][user_id]["balance"] - amount
            return "Successfull Transaction"
        else:
            print("FATAL ERROR")
            return "something else"
    else:
        print('target hasnt joined')
        return "Invalid Target"
    
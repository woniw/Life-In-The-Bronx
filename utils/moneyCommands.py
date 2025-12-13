import random
from utils.variables import dumpster_dive_item_chances
from utils.variables import title_money_rewards

def checkItemType(item: str):
    print(f"- ITEM: {item}")
    new_item = item[0]
    if new_item in  dumpster_dive_item_chances:
        if dumpster_dive_item_chances[new_item]["type"] == "nothing":
            new_message = "You found nothing, better luck next time!"
            return new_message
        elif dumpster_dive_item_chances[new_item]["type"] == "money":
            new_message = f"You found ${new_item}"
            return new_message
        elif dumpster_dive_item_chances[new_item]["type"] == "item":
            new_message = f"You found a {new_item}"
            return new_message

    else:
        print("ITEM WAS NOT FOUND || FATAL ERROR")
def addItemToInventory(user_id: str, item: str, data: dict):
    new_item = item[0]
    if dumpster_dive_item_chances[new_item]["type"] == "money":
        data["USERS"][user_id]['balance'] = data["USERS"][user_id]['balance'] + int(new_item)
    elif dumpster_dive_item_chances[new_item]["type"] == "nothing":  
        print("adding nothing")
        pass 
    else:
        print(f"ADDING ITEM: {new_item}")
        data["USERS"][user_id]["inventory"].append(new_item)
        print(f"USER INVENTORY: {data['USERS'][user_id]['inventory']}")

def addTitleToList(user_id: str, title_name: str, data: dict):
    print(f"ADDING ITEM: {title_name}")
    data["USERS"][user_id]["titles"].append(title_name)
    print(f"USER INVENTORY: {data['USERS'][user_id]['titles']}")
    
def dumpsterDive(user_id: str, data: dict):
    population = list(dumpster_dive_item_chances.keys())
    weights = [info["weight"] for info in dumpster_dive_item_chances.values()]  

    random_reward = random.choices(
        population=population,
        weights=weights,
        k=1
    )
    data["USERS"][user_id]['record']["dumpster_diving_count"] = data["USERS"][user_id]['record']["dumpster_diving_count"] + 1

    if data["USERS"][user_id]['record']["dumpster_diving_count"] == 10:
        #money rewards
        money_reward = title_money_rewards["Amateur diver"]

        data["USERS"][user_id]["balance"] = data["USERS"][user_id]["balance"] + money_reward
        addItemToInventory(user_id=user_id, item=random_reward, data=data)
        addTitleToList(user_id=user_id, title_name="Amateur diver", data=data)

        message = checkItemType(item=random_reward)
        return message, 'New Title Unlocked "Amateur diver"'
    

    elif data["USERS"][user_id]['record']["dumpster_diving_count"] == 50:
        money_reward = title_money_rewards["Intermediate diver"]

        data["USERS"][user_id]["balance"] = data["USERS"][user_id]["balance"] + money_reward
        addItemToInventory(user_id=user_id, item=random_reward, data=data)
        addTitleToList(user_id=user_id, title_name="Intermediate diver", data=data)

        message = checkItemType(item=random_reward)
        return message, 'New Title Unlocked "Intermediate diver"'
    
    elif data["USERS"][user_id]['record']["dumpster_diving_count"] == 100:
        addItemToInventory(user_id=user_id, item=random_reward, data=data)
        addTitleToList(user_id=user_id, title_name="King Diver", data=data)
        return random_reward, 'New Title Unlocked "King Diver"'
    else:
        print(f"FOUND: {random_reward}")
        addItemToInventory(user_id=user_id, item=random_reward, data=data)
        message = checkItemType(item=random_reward)
            #because no title was given
        return message, ""
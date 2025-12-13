from utils.Allitems import all_items

def equipWeapon(data: dict, weapon: str, user_id: str):
    print("Checking if item exists")
    print(f'User inventory: {data["USERS"][user_id]["inventory"]}')
    if weapon in all_items:
        print("** ITEM WAS FOUND IN ITEMS LIST **")

        weapon_damage = all_items[weapon]["damage"]
        weapon_durability = all_items[weapon]["durability"]

        
        print(f"USER INVENTORY: {data['USERS'][user_id]['inventory']}")
        if weapon in data["USERS"][user_id]["inventory"]:
            data["USERS"][user_id]["inventory"].remove(weapon)
            data["USERS"][user_id]["equipped"] = f"{weapon}"
            data["USERS"][user_id]["damage"] = weapon_damage
            data["USERS"][user_id]["durability"] = weapon_durability

            return "Weapon Has Been Equipped", weapon_damage
        else:
            print("USER CANT EQUIP AN ITEM THEY DONT HAVE")
            return "You Can't Equip A Weapon You Don't Have", ""
    else:
        print("ITEM DOES NOT EXIST")
        return "Weapon does not exist", ""


def eatConsumable(data: dict, item: str, user_id: str):
    print("Checking if item exists")
    print(f'User inventory: {data["USERS"][user_id]["inventory"]}')
    if item in all_items:
        print("** ITEM WAS FOUND IN ITEMS LIST **")

        item_heal = all_items[item]["heals"]
        user_class = data["USERS"][user_id]["class"]
        user_health = data["USERS"][user_id]["health"]

        print("| --- Logs --- |")
        print(f"   item heal: {item_heal}")
        print(f"   user class: {user_class}")
        print(f"   user health : {user_health}")

        print(f"USER INVENTORY: {data['USERS'][user_id]['inventory']}")
        if item in data["USERS"][user_id]["inventory"]:
            print('ITEM IS IN INVENTORY')
            data["USERS"][user_id]["inventory"].remove(item)
            health_after_consumed = user_health + item_heal
            print(f"health after consumed: {health_after_consumed}")

            if user_class == "Tank":
                print("user is a tank")
                if health_after_consumed > 115 or health_after_consumed == 115:
                    user_health = data["USERS"][user_id]["health"] = 115
                    return "Item Has Been Eaten", user_health
                else:
                    user_health = data["USERS"][user_id]["health"] = health_after_consumed
                    return "Item Has Been Eaten", user_health
            elif user_class != "Tank":
                print("user is not a tank")
                if health_after_consumed > 100 or health_after_consumed == 100:
                    user_health = data["USERS"][user_id]["health"] = 100
                    return "Item Has Been Eaten", user_health
                
                else:
                    user_health = data["USERS"][user_id]["health"] = health_after_consumed
                    return "Item Has Been Eaten", health_after_consumed
            else:
                print("something is wrong")
                return "Something is wrong"
        else:
            print("USER CANT EQUIP AN ITEM THEY DONT HAVE")
            return "You Can't Consume An Item You Don't Have"
    else:
        print("ITEM DOES NOT EXIST")
        return "Item does not exist"
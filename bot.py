import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from json_functions import save_json
from json_functions import load_json

from utils.checkUser import CheckJoinedUser
from utils.checkUser import AddUser

from utils.DisplayStat import showStat
from utils.DisplayStat import showItemDescription

from utils.adminCommands import addMoney
from utils.adminCommands import setMoney

from utils.adminCommands import giveMoney

from utils.GenerateStats import generatedClass
from utils.GenerateStats import generatedHandedness

from utils.moneyCommands import dumpsterDive

from utils.useItems import equipWeapon
from utils.useItems import eatConsumable

data = load_json("data.json")

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="$", intents=intents)


@bot.event
async def on_ready():
    await bot.wait_until_ready()
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")  # type: ignore
    try:
        await bot.tree.sync()
        print("Slash commands synced!")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

@bot.tree.error
async def on_app_command_error(interaction, error):
    if isinstance(error, commands.CommandOnCooldown):
        await interaction.response.send_message(
            f"The Bronx is telling you to wait {error.retry_after:.1f}s",
            ephemeral=True
        )

@bot.tree.command(name="join", description="Join The bronx!")
async def join(interaction: discord.Interaction):
    print("JOIN COMMAND HAS BEEN USED")
    handedness_result = generatedHandedness()
    class_result = generatedClass()

    user_id = str(interaction.user.id)
    User_Result = CheckJoinedUser(data=data, user_id=user_id)
    if User_Result:
        join_embed = discord.Embed(
            title="The Bronx",
            description=f"You Have Already Joined {interaction.user.mention}!",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=join_embed)
    else:
        if user_id == "710208977614536725":
            print("THE FATTY HAS BEEN CHOSEN")
            joining_embed = discord.Embed(
                title="The Bronx",
                description=f'The Bronx have chosen you to be "THE fatty" {interaction.user.mention} \n (Title unlocked)',
                color=discord.Color.gold()
            )
            AddUser(data=data, user_id=user_id, generated_handedness=handedness_result, generated_class=class_result)
            save_json(data, "data.json")
            await interaction.response.send_message(embed=joining_embed)
        else:
            joining_embed = discord.Embed(
                title="The Bronx",
                description=f"Welcome to the bronx {interaction.user.mention}",
                color=discord.Color.green()
            )
            AddUser(data=data, user_id=user_id, generated_handedness=handedness_result, generated_class=class_result)
            save_json(data, "data.json")
            await interaction.response.send_message(embed=joining_embed)

@bot.tree.command(name="check_stat", description="Check a stat!")
async def check_stat(interaction: discord.Interaction, stat: str):
    user_id = str(interaction.user.id)
    User_Result = CheckJoinedUser(data=data, user_id=user_id)

    if User_Result:
        response = showStat(requested_stat=stat, user_id=user_id, data=data)

        print(f"DISPLAYING STAT: {response}")
        print("| --- LOG --- |")
        print(f" USER: {user_id}")
        print(f" USER STAT: {response}")
        if response != "Invalid Request":
            stat_embed = discord.Embed(
                title="Stat",
                description=f"Your {stat}: {response}",
                color=discord.Color.green()
            )

            await interaction.response.send_message(embed=stat_embed)
        elif response == "Invalid Request":
            invalid_stat_embed = discord.Embed(
                title="Invalid Stat",
                description="**Hmm... I couldnt find that stat, instead try one of these:**\n - class \n - health \n - balance \n - handedness \n - damage \n - equipped",
                color=discord.Color.dark_green(),
            )
            await interaction.response.send_message(embed=invalid_stat_embed)
    else:
        await interaction.response.send_message(f"You Have Not Joined The Bronx, Please use /join")

@bot.tree.command(name="check_description", description="See the description of a certain item")
async def check_description(interaction: discord.Interaction, item: str):
    response_phrase = showItemDescription(requested_item_description=item)

    if response_phrase == "Item Doesnt exist":
        await interaction.response.send_message("https://tenor.com/view/shrug-shoulders-spongebob-gif-19763306")
    else:
        response_phrase, item_type = showItemDescription(requested_item_description=item)
        item_desciption_embed = discord.Embed(
            title="Item",
            description=f"Item name: **{item}** \n Description: {response_phrase} \n Type: {item_type}",
            color=discord.Color.blue()
        )

        await interaction.response.send_message(embed=item_desciption_embed)


#economy
@bot.tree.command(name="dive", description="Go dumpster diving!")
@commands.cooldown(1, 5, commands.BucketType.user)
async def dive(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    User_Result = CheckJoinedUser(data=data, user_id=user_id)

    if User_Result:
        reward, message = dumpsterDive(user_id=user_id, data=data)
        save_json(data, "data.json")
        result_embed = discord.Embed(
            title="Dumpster Diving",
            description=f"{message} {reward}",
            color=discord.Color.dark_embed()
        )
        await interaction.response.send_message(embed=result_embed)
    else:
        await interaction.response.send_message(f"You Have Not Joined The Bronx, Please use /join")

@bot.tree.command(name="give_money", description="bless up other members of the bronx with some of your own money")
async def give_money(interaction: discord.Interaction, value: int, target: discord.Member):
    user_id = str(interaction.user.id)
    target_id = str(target.id)
                                                #data: dict, user_id: str, amount: int, target: str
    result = giveMoney(data=data, user_id=user_id, amount=value, target=target_id)    

    print("")
    print("| --- LOG --- |")
    print(f"   USER ID: {user_id}")
    print(f"   TARGET ID: {target_id}")
    
    print(f"- ADD MONEY FUNCTION, RETURNED: {result}")

    if result == "Invalid Target":
        await interaction.response.send_message("Target Hasn't Joined The Bronx💔")
    elif result == "Invalid Balance":
        await interaction.response.send_message("You dont have enough money, get your money up not your funny up")
    elif result == "Successfull Transaction":
        save_json(data, "data.json")
        add_money_embed = discord.Embed(
            title="**🤑 Cha-ching, Money Given! 🤑**",
            description=f"💸{target} has been given ${value} from {interaction.user.mention}💸",
            color=discord.Color.green(),
        )
        await interaction.response.send_message(embed=add_money_embed)

@bot.tree.command(name="equip", description="Equip any weapon in your inventory")
async def equip(interaction: discord.Interaction, weapon_name: str):
    user_id = str(interaction.user.id)
    User_Result = CheckJoinedUser(data=data, user_id=user_id)

    if User_Result:
        message, weapon_damage = equipWeapon(data=data, weapon=weapon_name, user_id=user_id)
        save_json(data, "data.json")

        if message == "Weapon does not exist":
            response_embed = discord.Embed(
                title="The Bronx",
                description=f"{message}",
                color=discord.Color.dark_gold()
            )
            await interaction.response.send_message(embed=response_embed)
        elif message == "Weapon Has Been Equipped":
            response_embed = discord.Embed(
                title="The Bronx",
                description=f"{message} \n New Damage: {weapon_damage}",
                color=discord.Color.dark_gold()
            )
            await interaction.response.send_message(embed=response_embed)
    else:
        await interaction.response.send_message(f"You Have Not Joined The Bronx, Please use /join")


@bot.tree.command(name="eat", description="Eat to restore health")
async def equip(interaction: discord.Interaction, item: str):
    user_id = str(interaction.user.id)
    User_Result = CheckJoinedUser(data=data, user_id=user_id)

    if User_Result:
        message, new_health = eatConsumable(data=data, item=item, user_id=user_id)
        save_json(data, "data.json")

        if message == "Item does not exist":
            response_embed = discord.Embed(
                title="The Bronx",
                description=f"{message}",
                color=discord.Color.dark_gold()
            )
            await interaction.response.send_message(embed=response_embed)
        elif message == "Item Has Been Eaten":
            response_embed = discord.Embed(
                title="The Bronx",
                description=f"{message} \n New Health: {new_health}",
                color=discord.Color.dark_gold()
            )
            await interaction.response.send_message(embed=response_embed)
    else:
        await interaction.response.send_message(f"You Have Not Joined The Bronx, Please use /join")

#! admin commands
@bot.tree.command(name="add_money", description="add money to a users balance (admin only)")
async def add_money(interaction: discord.Interaction, value: int, target: discord.Member):
    user_id = str(interaction.user.id)
    target_id = str(target.id)

    print("")
    print("| --- LOG --- |")
    print(f"   USER ID: {user_id}")
    print(f"   TARGET ID: {target_id}")
    
    result, new_target_balance, target_balance = addMoney(data=data, user_id=user_id, amount=value, target=target_id)
    print(f"- ADD MONEY FUNCTION, RETURNED: {result}")
    print(f"- ADD MONEY FUNCTION, RETURNED: {new_target_balance}")
    print(f"- ADD MONEY FUNCTION, RETURNED: {target_balance}")

    if result == "Invalid Target":
        await interaction.response.send_message("Target Hasn't Joined The Bronx💔")
    elif result == "Invalid Permissions":
        await interaction.response.send_message("You dont have permissions to use this command")

    elif result == "Successfull Transaction":
        save_json(data, "data.json")
        add_money_embed = discord.Embed(
            title="**🤑 Cha-ching, Money added! 🤑**",
            description=f"💸{target} has been given ${value} from {interaction.user.mention}💸",
            color=discord.Color.green(),
        )

        await interaction.response.send_message(embed=add_money_embed)

@bot.tree.command(name="set_money", description="set a users balance to something (admin only)")
async def add_money(interaction: discord.Interaction, value: int, target: discord.Member):
    user_id = str(interaction.user.id)
    target_id = str(target.id)

    print("")
    print("| --- LOG --- |")
    print(f"   USER ID: {user_id}")
    print(f"   TARGET ID: {target_id}")
    
    result, new_target_balance, target_balance = setMoney(data=data, user_id=user_id, amount=value, target=target_id)
    print(f"- SET MONEY FUNCTION, RETURNED: {result}")
    print(f"- SET MONEY FUNCTION, RETURNED: {new_target_balance}")
    print(f"- SET MONEY FUNCTION, RETURNED: {target_balance}")

    if result == "Invalid Target":
        await interaction.response.send_message("Target Hasn't Joined The Bronx💔")
    elif result == "Invalid Permissions":
        await interaction.response.send_message("You dont have permissions to use this command")

    elif result == "Successfull Transaction":
        save_json(data, "data.json")
        set_money_embed = discord.Embed(
            title="**🤑 Money has been set 🤑**",
            description=f"💸{target} has been set to ${value}💸",
            color=discord.Color.green(),
        )

        await interaction.response.send_message(embed=set_money_embed)


if __name__ == "__main__":
    if TOKEN is None:
        print("Error: DISCORD_TOKEN not found.")
    else:
        bot.run(TOKEN)

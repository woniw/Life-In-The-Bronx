import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from json_functions import save_json
from json_functions import load_json

from utils.checkUser import CheckJoinedUser
from utils.checkUser import AddUser
from utils.DisplayStat import showStat

from utils.adminCommands import addMoney
from utils.adminCommands import setMoney
from utils.adminCommands import setClass


from utils.GenerateStats import generatedClass
from utils.GenerateStats import generatedHandedness

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


@bot.tree.command(name="join", description="Join The bronx!")
async def join(interaction: discord.Interaction):
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
        joining_embed = discord.Embed(
            title="The Bronx",
            description=f"Welcome to the bronx {interaction.user.mention}",
            color=discord.Color.green()
        )
        AddUser(data=data, user_id=user_id, generated_handedness=handedness_result, generated_class=class_result)
        save_json(data, "data.json")
        await interaction.response.send_message(embed=joining_embed)

@bot.tree.command(name="check_stat", description="Check a stat!")
async def check(interaction: discord.Interaction, stat: str):
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
        await interaction.response.send_message(f"You Have Not Joined The Bronx, Please us /join")

#@bot.tree.command(name="check_description", description="check a certain items description")
#async def check_description(requested_item: str):

#setMoney


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

@bot.tree.command(name="set_class", description="change a users class (admin only)")
async def set_class(interaction: discord.Interaction, setting_class: str, target: discord.Member):
    user_id = str(interaction.user.id)
    target_id = str(target.id)

    print("")
    print("| --- LOG --- |")
    print(f"   USER ID: {user_id}")
    print(f"   TARGET ID: {target_id}")
    
    result, new_target_class, target_class = setClass(data=data, user_id=user_id, setting_class=setting_class, target=target_id)
    print(f"- SET CLASS FUNCTION, RETURNED: {result}")
    print(f"- SET CLASS FUNCTION, RETURNED: {new_target_class}")
    print(f"- SET CLASS FUNCTION, RETURNED: {target_class}")

    if result == "Invalid Target":
        await interaction.response.send_message("Target Hasn't Joined The Bronx💔")
    elif result == "Invalid Permissions":
        await interaction.response.send_message("You dont have permissions to use this command")
    elif result == "Invalid Class":
        await interaction.response.send_message("That class does NOT exist💔")
    elif result == "Successfull Transaction":
        save_json(data, "data.json")
        set_class_embed = discord.Embed(
            title="**Class has been set**",
            description=f"💸{target}s class has been set to {setting_class}",
            color=discord.Color.green(),
        )

        await interaction.response.send_message(embed=set_class_embed)

if __name__ == "__main__":
    if TOKEN is None:
        print("Error: DISCORD_TOKEN not found.")
    else:
        bot.run(TOKEN)

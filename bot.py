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



#! admin commands
@bot.tree.command(name="add_money", description="add money to a users balance (admin only)")
async def add_money(interaction: discord.Interaction, value: int, target: discord.Member):
    user_id = interaction.user.id

    result = addMoney(data=data, user_id=user_id, amount=value, target=target)
    save_json(data, "data.json")

    if result == "Invalid Target":
        await interaction.response.send_message("Target Hasn't Joined The Bronx💔")
    elif result == "Invalid Permissions":
        await interaction.response.send_message("You dont have permissions to use this command")
    elif result == "Successfull Transaction":
        add_money_embed = discord.Embed(
            title="**🤑 Cha-ching, Money added! 🤑**",
            description=f"💸{target.mention} has been given ${value} from {interaction.user.mention}💸",
            color=discord.Color.green(),
        )
        await interaction.response.send_message(embed=add_money_embed)

if __name__ == "__main__":
    if TOKEN is None:
        print("Error: DISCORD_TOKEN not found.")
    else:
        bot.run(TOKEN)

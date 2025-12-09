import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from json_functions import save_json
from json_functions import load_json

from utils.checkUser import CheckJoinedUser
from utils.checkUser import AddUser

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
    user_id = str(interaction.user.id)

    User_Result = CheckJoinedUser(data=data, user_id=user_id)

    if User_Result:
        #! if its true
        await interaction.response.send_message("You Have Already Joined")
    else:
        AddUser(data=data, user_id=user_id)
        save_json(data, "data.json")
        await interaction.response.send_message(f"Welcome to the bronx {interaction.user.mention}")


if __name__ == "__main__":
    if TOKEN is None:
        print("Error: DISCORD_TOKEN not found.")
    else:
        bot.run(TOKEN)

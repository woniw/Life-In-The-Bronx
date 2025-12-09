import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from json_functions import save_json
from json_functions import load_json

data = load_json("data.json")

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    await bot.wait_until_ready()
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")  # type: ignore
    try:
        await bot.tree.sync()
        print("Slash commands synced!")
    except Exception as e:
        print(f"Failed to sync commands: {e}")


@bot.command()
async def ping(ctx):
    print("Log: !ping command activated")
    await ctx.send("Pong!")


@bot.tree.command(name="hello", description="Say hello!")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("Hello, world!")


if __name__ == "__main__":
    if TOKEN is None:
        print("Error: DISCORD_TOKEN not found.")
    else:
        bot.run(TOKEN)

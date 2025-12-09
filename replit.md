# Ultimate League RP Discord Bot

## Overview
This is a Discord bot for the Ultimate League RP game. It allows users to join the game and manages user data including health, balance, handedness, weapons, and inventory.

## Project Structure
- `bot.py` - Main bot entry point with Discord slash commands
- `json_functions.py` - JSON file save/load utilities
- `data.json` - User data storage
- `utils/` - Utility modules
  - `checkUser.py` - User join/add functions
  - `GenerateStats.py` - Random stat generation (class, handedness)
  - `Allitems.py` - Weapon definitions
  - `variables.py` - Game constants

## Commands
- `/join` - Join the game (creates a new user profile with random class and handedness)

## Running the Bot
The bot requires a `DISCORD_TOKEN` environment variable set with a valid Discord bot token.

Run with: `python bot.py`

## Dependencies
- discord.py
- python-dotenv

## Recent Changes
- Dec 9, 2025: Initial Replit setup with workflow configuration

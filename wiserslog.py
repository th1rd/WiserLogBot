import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Google Sheets Setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Wisers Log").sheet1  # Open first sheet

# Discord Bot Setup
intents = discord.Intents.default()
intents.members = True  
intents.message_content = True  # if bot reads messages

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.channel.name == "wisers-status":
        content = message.content.lower()
        if "logging in" in content or "logging out" in content:
            status = "Login" if "logging in" in content else "Logout"
            username = str(message.author)
            timestamp = message.created_at.strftime("%Y-%m-%d %H:%M:%S")

            # Save to Google Sheet
            sheet.append_row([username, status, timestamp])
            print(f"Logged: {username} - {status} at {timestamp}")

bot.run(TOKEN)

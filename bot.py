import os
import discord
import requests
from discord.ext import commands
from dotenv import load_dotenv

# Load .env locally
load_dotenv()

# Environment variables
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GROK_API_KEY = os.getenv("GROK_API_KEY")

# Grok API endpoint
GROK_URL = "https://api.x.ai/v1/chat/completions"

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ================================================================
# FUNCTION TO CALL GROK-2
# ================================================================
def grok_chat(user_message):
    headers = {
        "Authorization": f"Bearer {GROK_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "grok-2",
        "messages": [
            {"role": "system", "content": "You are Galaxy's AI."},
            {"role": "user", "content": user_message}
        ]
    }

    response = requests.post(GROK_URL, json=payload, headers=headers)

    if response.status_code != 200:
        print("Grok API error:", response.text)
        return None

    data = response.json()
    return data["choices"][0]["message"]["content"]

# ================================================================
# READY EVENT
# ================================================================
@bot.event
async def on_ready():
    print(f"🟢 Connected as {bot.user}")

# ================================================================
# AUTO-REPLY WHEN MENTIONED
# ================================================================
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if bot.user in message.mentions:
        reply = grok_chat(message.content)
        if reply:
            await message.reply(reply)
        else:
            await message.reply("❌ Something went wrong with Grok.")

    await bot.process_commands(message)

# ================================================================
# /ask COMMAND — GROK-2
# ================================================================
@bot.command()
async def ask(ctx, *, prompt: str):
    reply = grok_chat(prompt)
    if reply:
        await ctx.reply(reply)
    else:
        await ctx.reply("❌ Something went wrong with Grok.")

# Run bot
bot.run(DISCORD_TOKEN)

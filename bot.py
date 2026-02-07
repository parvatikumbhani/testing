import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from openai import OpenAI

# Load .env locally
load_dotenv()

# Environment variables
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GROK_API_KEY = os.getenv("GROK_API_KEY")

# Grok client (xAI)
client_ai = OpenAI(
    api_key=GROK_API_KEY,
    base_url="https://api.x.ai/v1"
)

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ================================================================
# READY EVENT
# ================================================================
@bot.event
async def on_ready():
    print(f"🟢 Connected as {bot.user}")

# ================================================================
# MENTION RESPONSE (AI auto-reply)
# ================================================================
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if bot.user in message.mentions:
        try:
            response = client_ai.chat.completions.create(
                model="grok-2",
                messages=[
                    {"role": "system", "content": "You are Galaxy's AI."},
                    {"role": "user", "content": message.content}
                ]
            )

            ai_reply = response.choices[0].message["content"]
            await message.reply(ai_reply)

        except Exception as e:
            print("Grok error:", e)
            await message.reply("❌ Something went wrong with Grok.")

    await bot.process_commands(message)

# ================================================================
# /ask COMMAND
# ================================================================
@bot.command()
async def ask(ctx, *, prompt: str):
    try:
        response = client_ai.chat.completions.create(
            model="grok-2",
            messages=[
                {"role": "system", "content": "You are Galaxy's AI."},
                {"role": "user", "content": prompt}
            ]
        )

        ai_reply = response.choices[0].message["content"]
        await ctx.reply(ai_reply)

    except Exception as e:
        print("Grok error:", e)
        await ctx.reply("❌ Something went wrong with Grok.")

# Run bot
bot.run(DISCORD_TOKEN)

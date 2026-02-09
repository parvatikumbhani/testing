import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from openai import OpenAI

# Load .env locally
load_dotenv()

# Environment variables
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
QWEN_API_KEY = os.getenv("QWEN_API_KEY")

# Qwen client (Alibaba Cloud)
client_ai = OpenAI(
    api_key=QWEN_API_KEY,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
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
# AUTO-REPLY WHEN MENTIONED
# ================================================================
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if bot.user in message.mentions:
        try:
            response = client_ai.chat.completions.create(
                model="qwen-max",
                messages=[
                    {"role": "system", "content": "You are Galaxy's AI."},
                    {"role": "user", "content": message.content}
                ]
            )

            ai_reply = response.choices[0].message["content"]
            await message.reply(ai_reply)

        except Exception as e:
            print("Qwen error:", e)
            await message.reply("❌ Something went wrong with Qwen.")

    await bot.process_commands(message)

# ================================================================
# /ask COMMAND — QWEN
# ================================================================
@bot.command()
async def ask(ctx, *, prompt: str):
    try:
        response = client_ai.chat.completions.create(
            model="qwen-max",
            messages=[
                {"role": "system", "content": "You are Galaxy's AI."},
                {"role": "user", "content": prompt}
            ]
        )

        ai_reply = response.choices[0].message["content"]
        await ctx.reply(ai_reply)

    except Exception as e:
        print("Qwen error:", e)
        await ctx.reply("❌ Something went wrong with Qwen.")

# Run bot
bot.run(DISCORD_TOKEN)

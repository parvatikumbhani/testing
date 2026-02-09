import os
import discord
import requests
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
HF_API_KEY = os.getenv("HF_API_KEY")

HF_URL = "https://api-inference.huggingface.co/models/Qwen/Qwen2.5-7B-Instruct"

def hf_chat(prompt):
    headers = {
        "Authorization": f"Bearer {HF_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 200}
    }

    r = requests.post(HF_URL, json=payload, headers=headers)
    if r.status_code != 200:
        print("HF error:", r.text)
        return None

    data = r.json()
    return data[0]["generated_text"]

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Connected as {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if bot.user in message.mentions:
        reply = hf_chat(message.content)
        await message.reply(reply or "Something went wrong with HuggingFace.")

    await bot.process_commands(message)

@bot.command()
async def ask(ctx, *, prompt: str):
    reply = hf_chat(prompt)
    await ctx.reply(reply or "Something went wrong with HuggingFace.")

bot.run(DISCORD_TOKEN)

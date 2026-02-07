import os
import discord
from discord.ext import commands
from discord import app_commands
from openai import OpenAI
from dotenv import load_dotenv

# Load .env locally (Render uses its own environment variables)
load_dotenv()

# Environment variables
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# OpenAI client
client_ai = OpenAI(api_key=OPENAI_API_KEY)

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix="!", intents=intents)


# ============================================================
#  READY EVENT (your original logic preserved)
# ============================================================
@bot.event
async def on_ready():
    print(f"🔌 Connected as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"📡 Synced {len(synced)} slash commands")
    except Exception as e:
        print(f"❌ Sync error: {e}")


# ============================================================
#  ORIGINAL /ask COMMAND (your exact logic)
# ============================================================
@bot.tree.command(name="ask", description="Ask OpenAI a question")
async def ask(interaction: discord.Interaction, prompt: str):
    await interaction.response.defer()

    try:
        response = client_ai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
        )
        reply = response.choices[0].message.content
        await interaction.followup.send(reply)

    except Exception as e:
        print("OpenAI Error:", e)
        await interaction.followup.send("❌ Something went wrong with OpenAI.")


# ============================================================
#  NEW: /info COMMAND (clean embed)
# ============================================================
@bot.tree.command(name="info", description="Bot information")
async def info(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🤖 AI Discord Bot",
        description="Powered by OpenAI and built by you.",
        color=0x3498DB
    )
    embed.add_field(name="Model", value="gpt-4o-mini", inline=False)
    embed.add_field(name="Commands", value="/ask, /info, /ping", inline=False)
    embed.set_footer(text="Online and ready to help")

    await interaction.response.send_message(embed=embed)


# ============================================================
#  NEW: /ping COMMAND
# ============================================================
@bot.tree.command(name="ping", description="Check bot latency")
async def ping(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)
    await interaction.response.send_message(f"🏓 Pong! `{latency}ms`")


# ============================================================
#  NEW: AUTO-REPLY WHEN BOT IS MENTIONED
# ============================================================
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if bot.user in message.mentions:
        try:
            response = client_ai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": message.content}],
            )
            reply = response.choices[0].message.content
            await message.reply(reply)

        except Exception as e:
            print("Auto-reply error:", e)
            await message.reply("❌ I couldn't generate a response.")

    await bot.process_commands(message)


# ============================================================
#  RUN BOT
# ============================================================
if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)

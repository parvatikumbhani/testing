import os
import discord
from discord import app_commands
from discord.ext import commands
from openai import OpenAI
from dotenv import load_dotenv

# Load .env locally (Render uses its own environment variables)
load_dotenv()

# Load environment variables
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Setup OpenAI client
client_ai = OpenAI(api_key=OPENAI_API_KEY)

# Setup Discord bot
intents = discord.Intents.default()
intents.message_content = True  # allows auto-reply and message reading
bot = commands.Bot(command_prefix="!", intents=intents)


# -----------------------------
#  BOT READY EVENT
# -----------------------------
@bot.event
async def on_ready():
    try:
        await bot.tree.sync()
        print(f"✅ Logged in as {bot.user}")
    except Exception as e:
        print(f"Error syncing commands: {e}")


# -----------------------------
#  SLASH COMMAND: /ask
#  (Your original command)
# -----------------------------
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


# -----------------------------
#  NEW FEATURE: /ping
# -----------------------------
@bot.tree.command(name="ping", description="Check if the bot is alive")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("🏓 Pong! I'm awake and running.")


# -----------------------------
#  NEW FEATURE: /help
# -----------------------------
@bot.tree.command(name="help_ai", description="Show all bot commands")
async def help_ai(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🤖 AI Bot Commands",
        description="Here’s what I can do:",
        color=0x5865F2
    )
    embed.add_field(name="/ask <prompt>", value="Ask the AI anything.", inline=False)
    embed.add_field(name="/ping", value="Check if the bot is online.", inline=False)
    embed.add_field(name="Mention the bot", value="I will auto‑reply using AI.", inline=False)

    await interaction.response.send_message(embed=embed)


# -----------------------------
#  NEW FEATURE:
#  Auto‑reply when mentioned
# -----------------------------
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # If someone mentions the bot, it replies using OpenAI
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
            await message.reply("❌ I couldn't think of a response.")

    await bot.process_commands(message)


# -----------------------------
#  RUN BOT
# -----------------------------
if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)

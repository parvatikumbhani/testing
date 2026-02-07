import os
import discord
from discord import app_commands
from discord.ext import commands
from openai import OpenAI

# Load environment variables from Render dashboard
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Setup OpenAI client
client_ai = OpenAI(api_key=OPENAI_API_KEY)

# Setup Discord bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Sync slash commands when bot is ready
@bot.event
async def on_ready():
    try:
        await bot.tree.sync()
        print(f"✅ Logged in as {bot.user}")
    except Exception as e:
        print(f"Error syncing commands: {e}")

# Slash command: /ask
@bot.tree.command(name="ask", description="Ask OpenAI a question")
async def ask(interaction: discord.Interaction, prompt: str):
    await interaction.response.defer()

    try:
        response = client_ai.chat.completions.create(
            model="gpt-4o-mini",  # fast + cheap
            messages=[{"role": "user", "content": prompt}],
        )
        reply = response.choices[0].message.content
        await interaction.followup.send(reply)

    except Exception as e:
        print(e)
        await interaction.followup.send("❌ Something went wrong with OpenAI.")

# Run bot
if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)

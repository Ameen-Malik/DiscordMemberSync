import discord
from discord.ext import commands
import csv
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

intents = discord.Intents.default()
intents.members = True  # Required to access server members
intents.guilds = True
intents.message_content = True  # Needed for responding to messages in some configurations

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.command(name='fetch_user_data')
async def fetch_user_data(ctx):
    guild = ctx.guild
    if guild is None:
        await ctx.send("❌ This command must be run in a server.")
        return

    msg = await ctx.send("⏳ Fetching member data...")

    print(f"[INFO] Fetching member data for: {guild.name} (ID: {guild.id})")
    await guild.chunk()
    print(f"[INFO] Member list chunked. Total members: {len(guild.members)}")

    filename = f'members_{guild.id}.csv'
    with open(filename, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Username#Discriminator', 'Display Name', 'ID'])  # Header row

        for i, member in enumerate(guild.members, start=1):
            writer.writerow([f'{member.name}#{member.discriminator}', member.display_name, member.id])
            if i % 50 == 0 or i == len(guild.members):  # Periodic log for progress
                print(f"[INFO] Processed {i}/{len(guild.members)} members...")

    await msg.edit(content=f"✅ Member data saved to `{filename}`")
    print(f"[SUCCESS] CSV file created: {filename}")

bot.run(TOKEN)

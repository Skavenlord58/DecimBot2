import json
import os
from ntpath import join
from typing import List
import aiohttp
import random
import asyncio
import datetime as dt
import requests

import disnake
from disnake import Message
from disnake.ext import commands

from dotenv import load_dotenv

import decimdictionary as decdi 

#TODO: logging
#TODO: make all stuff loadable modules

# preload all useful stuff
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
TEXT_SYNTH_TOKEN = os.getenv('TEXT_SYNTH_TOKEN')
PREFIX = os.getenv('BOT_PREFIX')

# add intents for bot and command prefix for classic command support
intents = disnake.Intents.all()
client = disnake.ext.commands.Bot(command_prefix=PREFIX, intents=intents)

# on_ready event - happens when bot connects to Discord API
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


# constants
HELP = decdi.HELP
WARCRAFTY_CZ = decdi.WARCRAFTY_CZ
GMOD_CZ = decdi.GMOD_CZ
MOT_HLASKY = decdi.MOT_HLASKY
LINUX_COPYPASTA = decdi.LINUX_COPYPASTA

# useful functions/methods
async def batch_react(m, reactions: List):
    for reaction in reactions:
        await m.add_reaction(reaction)
    pass

## Commands here ->
# Show all available commands
@client.command()
async def decimhelp(ctx):
    m = await ctx.send(HELP)
    await asyncio.sleep(10)
    # automoderation
    await ctx.message.delete()
    await m.delete()

# debug command/trolling
@client.command()
async def say(ctx, *args):
    if str(ctx.message.author) == 'SkavenLord58#0420':
        await ctx.message.delete()
        await ctx.send(f'{" ".join(args)}')
    else:
        print(f'{ctx.message.author} tried to use "say" command.')
        # await ctx.message.delete()

# poll creation, takes up to five arguments
@client.command()
async def poll(ctx, *args):
    poll_mess = f"Anketa: {args[0]}\n".replace("_", " ")
    m = await ctx.send("Creating poll... (If stuck, something failed horribly.)")
    try:
        poll_mess += f":one: = {args[1]}\n".replace("_", " ")
        await m.add_reaction("1️⃣")
        poll_mess += f":two: = {args[2]}\n".replace("_", " ")
        await m.add_reaction("2️⃣")
        poll_mess += f":three: = {args[3]}\n".replace("_", " ")
        await m.add_reaction("3️⃣")
        poll_mess += f":four: = {args[4]}\n".replace("_", " ")
        await m.add_reaction("4️⃣")
        poll_mess += f":five: = {args[5]}\n".replace("_", " ")
        await m.add_reaction("5️⃣")
    except Exception as exc:
        pass
    await m.edit(content=f"{poll_mess}")

# rolls a dice
@client.command()
async def roll(ctx, arg_range=None):
    range = None
    try:
        range = int(arg_range)
    except Exception as exc:
        pass

    if arg_range == "joint":
        await ctx.reply(f'https://youtu.be/LF6ok8IelJo?t=56')
    elif not range:
        await ctx.send(f'{random.randint(0, 100)} (Defaulted to 100d.)')
    elif type(range) is int and range > 0:
        await ctx.send(f'{random.randint(0, int(range))} (Used d{range}.)')
    else:
        await ctx.reply(f'Something\'s wrong. Check your syntax.')


# "twitter" functionality 
@client.slash_command(name = "tweet", description = "Posts a 'tweet' in #twitter-pero channel.", guild_ids=decdi.GIDS)
async def tweet(ctx, content: str, media: str = "null"):
    twitterpero = client.get_channel(decdi.TWITTERPERO)
    embed = disnake.Embed(
        title=f"{ctx.author.display_name} tweeted:",
        description=f"{content}",
        color=disnake.Colour.dark_purple()
    )
    embed.set_thumbnail(url=ctx.author.avatar)
    if media != "null":
        embed.set_image(url=media)
    embed.add_field(name=f"_", value=f"Sent from #{ctx.channel.name}", inline=True)
    # if ctx.author.mobile_status:
    #    embed.add_field(name=f"Sent from a mobile device 📱", value="_", inline=True)
    await ctx.response.send_message(content="Tweet posted! 👍", ephemeral=True)
    m = await twitterpero.send(embed=embed)
    await batch_react(m, ["💜", "🔁", "⬇️", "💭", "🔗"])

    

@client.command()
async def ping(ctx):
    m = await ctx.send(f'Ping?')
    ping = int(str(m.created_at - ctx.message.created_at).split(".")[1]) / 1000
    await m.edit(content=f'Pong! Latency is {ping}ms. API Latency is {round(client.latency * 1000)}ms.')
    pass


@client.command()
async def yesorno(ctx, *args):
    answers = ("Yes.", "No.", "Perhaps.", "Definitely yes.", "Definitely no.")
    await ctx.reply(f'{answers[random.randint(0, len(answers) - 1)]}')
    pass


@client.command()
async def warcraft(ctx, *args):
    # automoderation
    await ctx.message.delete()
    # send z templaty
    if args:
        m = await ctx.send(WARCRAFTY_CZ.replace('{0}', f' v cca {args[0]}'))
    else:
        m = await ctx.send(WARCRAFTY_CZ.replace('{0}', ''))
    # přidání reakcí
    await batch_react(m, ["✅", "❎", "🤔", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "❓"])
    pass


@client.command()
async def gmod(ctx, *args):
    # automoderation
    await ctx.message.delete()
    # send z templaty
    if args:
        m = await ctx.send(GMOD_CZ.replace('{0}', f' v cca {args[0]}'))
    else:
        m = await ctx.send(GMOD_CZ.replace('{0}', ''))
    # přidání reakcí
    await batch_react(m, ["✅", "❎", "🤔", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "❓"])
    pass

@client.command()
async def today(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://national-api-day.herokuapp.com/api/today') as response:
            payload = await response.json()
            holidays: List[str] = payload.get("holidays", [])
            await ctx.reply(f'Today are following holiday: {", ".join(holidays)}')
    pass

@client.command()
async def autostat(ctx):
    m = ctx.message
    await m.reply("OK;")

# sends an xkcd comics
@client.command()
async def xkcd(ctx, *args):
    if args:
        x = requests.get('https://xkcd.com/' + args[0] + '/info.0.json')
        if x.status_code == 200:
            await ctx.send(x.json()["img"])
        else:
            await ctx.send("No such xkcd comics with this ID found.")
    else:
        x = requests.get('https://xkcd.com/info.0.json')
        await ctx.send(x.json()["img"])


# on message eventy
@client.event
async def on_message(m: Message):
    if not m.content:
        pass
    elif m.content[0] == PREFIX:
        # nutnost aby jely commandy    
        await client.process_commands(m)
    elif str(m.author) != "DecimBOT 2.0#8467":
        if "negr" in m.content.lower():
            await m.add_reaction("🇳")
            # await m.add_reaction("🇪")
            # await m.add_reaction("🇬")
            # await m.add_reaction("🇷")
        if "linux" in m.content.lower() and not "gnu/linux" in m.content.lower():
            if random.randint(0, 64) == 4:
                await m.reply(LINUX_COPYPASTA)
        if "based" in m.content:
            await m.add_reaction("👌")
        if  m.content.lower().startswith("hodný bot") or "good bot" in m.content.lower():
            await m.add_reaction("🙂")
        if  m.content.lower().startswith("zlý bot") or "bad bot" in m.content.lower() or \
        "naser si bote" in m.content.lower() or "si naser bote" in m.content.lower():
            await m.add_reaction("😢")
        if "drip" in m.content.lower():
            await m.add_reaction("🥶")
            await m.add_reaction("💦")
        if "windows" in m.content.lower():
            await m.add_reaction("😔")
        if "debian" in m.content.lower():
            await m.add_reaction("💜")
        if "všechno nejlepší" in m.content.lower():
            await m.add_reaction("🥳")
            await m.add_reaction("🎉")
        if "co jsem to stvořil" in m.content.lower() and m.author == 'SkavenLord58#0420':
            await m.reply("https://media.tenor.com/QRTVgLglL6AAAAAd/thanos-avengers.gif")
        if "atpro" in m.content.lower():
            await m.add_reaction("😥")
            await m.reply("To mě mrzí.")
        if "in a nutshell" in m.content.lower():
            await m.add_reaction("🌰")
        if "hilfe" in m.content.lower() or "pomoc" in m.content.lower() and "pomocí" not in m.content.lower():
            await m.reply(f'''
            „{MOT_HLASKY[random.randint(0, len(MOT_HLASKY) - 1)]}“
                                                                                - Mistr Oogway, {random.randint(470,480)} př. n. l.
            ''')
        if "novinky.cz" in m.content.lower():
            await m.reply("Přestaň postovat cringe, bro.")
        if "drž hubu" in m.content.lower() and "996439005405126787" in m.mentions.values():
            print(m.mentions)
            await m.reply("Ne, ty. 😃")
        if "free primos" in m.content.lower() or "príma džemy" in m.content.lower():
            await m.reply(
                "Neklikejte na odkazy s názvem FREE PRIMOS. Obvykle toto bývá phishing scam. https://www.avast.com/cs-cz/c-phishing")
        if "jsem" in m.content.lower():
            if random.randint(0, 32) == 4:
                kdo = " ".join(m.content.split("jsem")[1].split(" ")[1:])
                await m.reply(f'Ahoj, {kdo}. Já jsem táta.')
        if m.content.lower() == "kdo":
            await m.channel.send(f'kdo se ptal?')
        if "zhongli" in m.content.lower():
            await m.reply(f'haha žongli :clown:')
        if "aneurysm" in m.content.lower():
            await m.reply(f'https://www.youtube.com/watch?v=kyg1uxOsAUY')
        if "decim je negr" in m.content.lower():
            await m.channel.send("nn, ty seš")

client.run(TOKEN)

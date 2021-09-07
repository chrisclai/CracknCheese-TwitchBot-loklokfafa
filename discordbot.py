# Location for all the main (and important) code
# Run the bot from this file!!!

# Import all the important dependencies
import discord
from discord.ext import commands
from discord.utils import find, get

import asyncio
import json
import time
import random

import threading
from _thread import *

# File Dependencies
import privinfo
from update_json import *
from sortleaderboard import *

# Initalize bot information
client = commands.Bot(command_prefix='!')
token = privinfo.authkey

def finduser(username, accounts, mode):
    location = 0
    
    if mode == "discordname":
        for x in range (len(accounts)):
            if username == accounts[str(x)]['discordname']:
                location = x
                break
    elif mode == "twitchname":
        for x in range (len(accounts)):
            if username.lower() == accounts[str(x)]['username']:
                location = x
                break
    return location

def winroute(userlocation, accounts, username):
    winamount = round(random.randrange(1,500,1)/10000.0, 3)
    prevpoints = accounts[str(userlocation)]['points']
    endpoints = int(prevpoints * (1 + winamount))
    accounts[str(userlocation)]['points'] = endpoints
    accounts[str(userlocation)]['xp'] += 10
    
    update_json('accounts/accounts.json', accounts)

    return f"[🎲Risk Roll🎲] Congrats, {username}, you have beaten the computer! You have earned {endpoints - prevpoints}, or {round(winamount * 100, 3)}% extra points for your account, as well as 10xp! Thanks for playing!"


def loseroute(userlocation, accounts, username):
    loseamount = round(random.randrange(1,1000,1)/10000.0, 3)
    prevpoints = accounts[str(userlocation)]['points']
    endpoints = int(prevpoints - (prevpoints * loseamount))
    accounts[str(userlocation)]['points'] = endpoints
    accounts[str(userlocation)]['xp'] += 5

    update_json('accounts/accounts.json', accounts)

    return f"[🎲Risk Roll🎲] Unfortunately, the computer's number was higher, so {username} has lost. You lost {endpoints - prevpoints} points, or {round(loseamount * 100, 3)}% of your previous point total. As compensation, you have been rewarded 5xp. Thanks for playing!"

def rollgame():
    computernum = random.randrange(0,101,1)
    playernum = random.randrange(0,101,1)
    while playernum == computernum:
        playernum = random.randrange(0,101,1)

    if playernum > computernum:
        return True, computernum, playernum
    else:
        return False, computernum, playernum

@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    print(f"{message.author.name}: {message.content}")
    await client.process_commands(message)

@client.command(pass_context=True)
async def hi(ctx):
    await ctx.channel.send(f"Hi {ctx.author.nick}!")

@client.command(pass_context=True)
async def account(ctx):
    accounts = new_json()
    location = finduser(ctx.author.name, accounts, 'discordname')
    if not location:
        await ctx.channel.send(f"User not detected. Use !link to manually link your Twitch account to your discord account!")
    else:
        points = accounts[str(location)]['points']
        xp = accounts[str(location)]['xp']
        message = f"Welcome back {accounts[str(location)]['username']}! You have [{xp}] xp and a balance of [{points}] points. Hello from Twitch!"
        await ctx.channel.send(message)

@client.command(pass_context=True)
async def link(ctx):
    accounts = new_json()
    location = finduser(ctx.author.name, accounts, 'discordname')

    if not location:
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel
        discordname = ""
        try:
            await ctx.channel.send("Enter your Twitch Username:")
            msg = await client.wait_for("message", check=check, timeout=60)
            discordname = msg.content
        except asyncio.TimeoutError:
            await ctx.channel.send("Sorry, you didn't reply in time. Please try again.")

        if discordname:
            await ctx.channel.send("Searching for user..")
            time.sleep(1)
            location = finduser(discordname, accounts, 'twitchname')
            if not location:
                await ctx.channel.send("Username Invalid. Please Try Again!")
            else:
                await ctx.channel.send(f"Username Found. Your Discord and Twitch accounts have been successfully linked. Welcome back {accounts[str(location)]['username']}!")
                accounts[str(location)]['discordname'] = ctx.author.name
                update_json('accounts/accounts.json', accounts)
    else:
        await ctx.channel.send(f"Welcome back, {ctx.author.name}! Your account is already linked to your Twitch account, {accounts[str(location)]['username']}. Have a great day!")

@client.command(pass_context=True)
async def leaderboard(ctx):
    accounts = new_json()
    listnames, listxp = sortbyhigh(accounts)
    output = "__XP Leaderboard__\n"
    emojis = ["🔥", "🥇", "🥈", "🥉", "🏅", "🎖️", "🎖", "🔲"]
    for x in range(0, 8):
        output += f"> {emojis[x]}: [{listnames[x]}, {listxp[x]} xp]\n"
    await ctx.channel.send(output)

@client.command(pass_context=True)
async def roll(ctx):
    accounts = new_json()
    location = finduser(ctx.author.name, accounts, 'discordname')

    if not location:
        await ctx.channel.send("[🎲Risk Roll🎲] Unfortunately, it seems like you don't have an account! Use !link to connect your account with the Twitch account, or use !account during a stream to make a new one! Have a great day!")
    elif accounts[str(location)]['points'] > 100:
        result, computernum, playernum = rollgame()
        await ctx.channel.send(f"[🎲Risk Roll🎲] The computer rolled {computernum} while you rolled {playernum}.")
        time.sleep(1)
        if result:
            await ctx.channel.send(winroute(location, accounts, ctx.author.name))
        else:
            await ctx.channel.send(loseroute(location, accounts, ctx.author.name))
    else:
        await ctx.channel.send(f"[🎲Risk Roll🎲] Sorry, you do not have enough points to play this game! Come back when you have at least 100 points. Thank you!")

client.run(token)

# Location for all the main (and important) code
# Run the bot from this file!!!

# Import all the important dependencies
import discord
from discord.ext import commands
from discord.utils import get

import asyncio
import json
import time
import random

import threading
from _thread import *

# File Dependencies
import privinfo
from discordroll import rollgame
from update_json import *

# Initalize bot information
client = commands.Bot(command_prefix='!')
token = privinfo.authkey

def finduser(username, accounts):
    location = 0
    for x in range (len(accounts)):
        if username == accounts[str(x)]['username']:
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

def rollgame(ctx, username):
    accounts = new_json()
    userlocation = finduser(ctx.author.nick, accounts)
    username = accounts[str(userlocation)]['username']

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
    location = finduser(ctx.author.nick, accounts)
    if not location:
        await ctx.channel.send(f"Sorry, user not detected. Make sure you discord nickname is the same as your twitch username and try again!")
    else:
        points = accounts[str(location)]['points']
        xp = accounts[str(location)]['xp']
        message = f"Welcome back {accounts[str(location)]['username']}! You have [{xp}] xp and a balance of [{points}] points. Hello from Twitch!"
        await ctx.channel.send(message)

@client.command(pass_context=True)
async def roll(ctx):
    accounts = new_json()
    location = finduser(ctx.author.nick, accounts)

    if accounts[str(location)]['points'] > 100:
        result, computernum, playernum = rollgame(ctx, ctx.author.nick)
        await ctx.channel.send(f"[🎲Risk Roll🎲] The computer rolled {computernum} while you rolled {playernum}.")
        time.sleep(1)
        if result:
            await ctx.channel.send(winroute(location, accounts, ctx.author.nick))
        else:
            await ctx.channel.send(loseroute(location, accounts, ctx.author.nick))
    else:
        await ctx.channel.send(f"[🎲Risk Roll🎲] Sorry, you do not have enough points to play this game! Come back when you have at least 100 points. Thank you!")

client.run(token)

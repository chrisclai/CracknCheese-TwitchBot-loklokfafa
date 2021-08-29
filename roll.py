import random
import time
from update_json import update_json
from finduser import *

def winroute(self, c, userlocation, accounts, username):
    winamount = round(random.randrange(1,500,1)/10000.0, 3)
    prevpoints = accounts[str(userlocation)]['points']
    endpoints = int(prevpoints * (1 + winamount))
    accounts[str(userlocation)]['points'] = endpoints
    accounts[str(userlocation)]['xp'] += 10

    c.privmsg(self.channel, f"[🎲Risk Roll🎲] Congrats, {username}, you have beaten the computer! You have earned {endpoints - prevpoints}, or {round(winamount * 100, 3)}% extra points for your account, as well as 10xp! Thanks for playing!")

    update_json('accounts/accounts.json', accounts)


def loseroute(self, c, userlocation, accounts, username):
    loseamount = round(random.randrange(1,1000,1)/10000.0, 3)
    prevpoints = accounts[str(userlocation)]['points']
    endpoints = int(prevpoints - (prevpoints * loseamount))
    accounts[str(userlocation)]['points'] = endpoints
    accounts[str(userlocation)]['xp'] += 5

    c.privmsg(self.channel, f"[🎲Risk Roll🎲] Unfortunately, the computer's number was higher, so {username} has lost. You lost {endpoints - prevpoints} points, or {round(loseamount * 100, 3)}% of your previous point total. As compensation, you have been rewarded 5xp. Thanks for playing!")

    update_json('accounts/accounts.json', accounts)

def rollgame(self, c, e):
    accounts = new_json()
    userlocation = finduser(e, accounts)
    username = accounts[str(userlocation)]['username']
    c.privmsg(self.channel, f"[🎲Risk Roll🎲]: Starting Game with {username}! Highest number wins! Begin!")
    time.sleep(5)
    computernum = random.randrange(0,101,1)
    playernum = random.randrange(0,101,1)
    while playernum == computernum:
        playernum = random.randrange(0,101,1)
    c.privmsg(self.channel, f"[🎲Risk Roll🎲]: The computer has rolled {computernum}. Rolling {username}'s number...")
    time.sleep(3)
    c.privmsg(self.channel, f"[🎲Risk Roll🎲]: {username} has rolled {playernum}. Concluding results...")
    time.sleep(3)
    if playernum > computernum:
        winroute(self, c, userlocation, accounts, username)
    else:
        loseroute(self, c, userlocation, accounts, username)
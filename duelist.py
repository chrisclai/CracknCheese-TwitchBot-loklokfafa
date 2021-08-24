from update_json import *
import time
import random

class Duelist:
    def __init__(self, username):
        if not username:
            self.username = ""
            self.points = 0
            self.hasaccept = False
            self.location = 0
        else:
            self.username = username
            self.points = 0

            self.hasaccept = False

            self.winmin2 = False
            self.min2start = False

            accounts = new_json()
            self.location = 0
            for x in range(len(accounts)):
                if username == accounts[str(x)]['username']:
                    self.location = x
                    break

def playDuelist(self, c, player1, player2):
    pass

def minigame1(self, c, player1, player2, minigamenum):
    c.privmsg(self.channel, f"[Duelist] Minigame {minigamenum}: Dice Roll! A 100-sided die will be rolled for both players. Highest number wins!")
    time.sleep(1)

    player1roll = random.randrange(0,100,1)
    player2roll = random.randrange(0,100,1)

    while player2roll == player1roll:
        player2roll = random.randrange(0,100,1)

    c.privmsg(self.channel, f"[Duelist] {player1.username}, rolling rolling rolling...")
    time.sleep(2)
    c.privmsg(self.channel, f"[Duelist] {player1.username}, your dice landed on {player1roll}! {player2.username}, you're up next! Rolling rolling rolling...")
    time.sleep(2)
    c.privmsg(self.channel, f"[Duelist] {player2.username}, your dice landed on {player2roll}!")
    time.sleep(1)


    if player1roll > player2roll:
        c.privmsg(self.channel, f"[Duelist] {player1.username} wins! +1 point")
        player1.points += 1
    else:
        c.privmsg(self.channel, f"[Duelist] {player2.username} wins! +1 point")
        player1.points += 1

    time.sleep(1)
    c.privmsg(self.channel, f"[Duelist] The current scoreboard is: {player1.username} with {player1.points} points and {player2.username} with {player2.points} points!")

def minigame2(self, c, player1, player2, minigamenum):
    c.privmsg(self.channel, f"[Duelist] Minigame {minigamenum}: Speed! From the beginning of this message being sent, it will take anywhere from 4-20 seconds for a prompt message to show up. When that happens, the first player to type in \"!win\" will win the point!")
    time.sleep(random.randrange(4,20,1))
    c.privmsg(self.channel, f"[Duelist] First to type \"!win\" wins! Go!")


def minigame3():
    pass


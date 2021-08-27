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
            self.min2start = False
            self.winmin2 = False
            self.min3start = False
            self.mathanswer = -99999
        else:
            # Initialization of temp account
            self.username = username
            self.points = 0

            # Double checker for starting activation
            self.hasaccept = False

            # Game 2 Speed variables
            self.min2start = False
            self.winmin2 = False

            # Game 3 Math variables
            self.min3start = False
            self.mathanswer = -99999

            # Location identifier
            accounts = new_json()
            self.location = 0
            for x in range(len(accounts)):
                if username == accounts[str(x)]['username']:
                    self.location = x
                    break

def minigame1(self, c, player1, player2, minigamenum):
    c.privmsg(self.channel, f"[Duelist] Minigame {minigamenum}: Dice Roll! A 100-sided die will be rolled for both players. Highest number wins!")
    time.sleep(5)

    player1roll = random.randrange(0,100,1)
    player2roll = random.randrange(0,100,1)

    while player2roll == player1roll:
        player2roll = random.randrange(0,100,1)

    c.privmsg(self.channel, f"[Duelist] {player1.username}, rolling rolling rolling...")
    time.sleep(5)
    c.privmsg(self.channel, f"[Duelist] {player1.username}, your dice landed on {player1roll}! {player2.username}, you're up next! Rolling rolling rolling...")
    time.sleep(5)
    c.privmsg(self.channel, f"[Duelist] {player2.username}, your dice landed on {player2roll}!")
    time.sleep(5)

    if player1roll > player2roll:
        c.privmsg(self.channel, f"[Duelist] {player1.username} wins! +1 point")
        player1.points += 1
    else:
        c.privmsg(self.channel, f"[Duelist] {player2.username} wins! +1 point")
        player2.points += 1

    time.sleep(1)
    c.privmsg(self.channel, f"[Duelist] The current scoreboard is: {player1.username} with {player1.points} points and {player2.username} with {player2.points} points!")

def minigame2(self, c, player1, player2, minigamenum):
    c.privmsg(self.channel, f"[Duelist] Minigame {minigamenum}: Speed! From the beginning of this message being sent, it will take anywhere from 5-10 seconds for a prompt message to show up. When that happens, the first player to type in \"!win\" will win the point!")
    time.sleep(random.randrange(5,10,1))
    player1.min2start = True
    player2.min2start = True
    c.privmsg(self.channel, f"[Duelist] First to type \"!win\" wins! Go!")
    while True:
        if player1.winmin2:
            c.privmsg(self.channel, f"[Duelist] {player1.username} wins! +1 point")
            player1.points += 1
            player1.min2start = False
            player1.winmin2 = False
            break
        elif player2.winmin2:
            c.privmsg(self.channel, f"[Duelist] {player2.username} wins! +1 point")
            player2.points += 1
            player2.min2start = False
            player2.winmin2 = False
            break
    time.sleep(1)
    c.privmsg(self.channel, f"[Duelist] The current scoreboard is: {player1.username} with {player1.points} points and {player2.username} with {player2.points} points!")


def minigame3(self, c, player1, player2, minigamenum):
    c.privmsg(self.channel, f"[Duelist] Minigame {minigamenum}: Math! Answer the following randomly generated math problem faster than your opponent to win the round! Generating...")
    time.sleep(5)
    amountofnum = random.randrange(2,6)
    operationchoice = ["+", "-", "*"]
    listnum = []
    listoperation = []
    equation = ""
    answer = 0

    # Create random equation based on number of variables
    for x in range(amountofnum):
        op = operationchoice[random.randrange(0,3,1)]
        listoperation.append(op)
        if op == "*":
            listnum.append(random.randrange(2,6,1))
        else:
            listnum.append(random.randrange(5,10,1))
        equation += f"{str(listnum[x])} {listoperation[x]} "
    if listoperation[amountofnum-1] == "*":
        listnum.append(random.randrange(2,6,1))
    else:
        listnum.append(random.randrange(5,45,1))
    equation += str(listnum[amountofnum-1])
    answer = eval(equation)

    player1.min3start = True
    player2.min3start = True

    c.privmsg(self.channel, f"[Duelist] Equation generated. Solve the following problem using !math <answer> to win a point! || {equation}")
    while (True):
        if str(answer) == player1.mathanswer:
            c.privmsg(self.channel, f"[Duelist] {player1.username} wins! +1 point")
            player1.points += 1
            player1.mathanswer = -99999
            player1.min3start = False
            break
        elif str(answer) == player2.mathanswer:
            c.privmsg(self.channel, f"[Duelist] {player2.username} wins! +1 point")
            player2.points += 1
            player2.mathanswer = -99999
            player1.min3start = False
            break
     
def gameChooser(gamenumber, self, c, player1, player2, minigamenum):
    if gamenumber == 0:
        minigame1(self, c, player1, player2, minigamenum)
    elif gamenumber == 1:
        minigame2(self, c, player1, player2, minigamenum)
    elif gamenumber == 2:
        minigame3(self, c, player1, player2, minigamenum)

def riskreward(player1, player2, whowon):
    # Refresh accounts
    accounts = new_json()

    # If player 1 wins, +100xp player 1, -100 points player 2
    if whowon == player1.username:
        accounts[str(player1.location)]['xp'] += 100
        accounts[str(player2.location)]['points'] -= 100
    elif whowon == player2.username:
        accounts[str(player2.location)]['xp'] += 100
        accounts[str(player1.location)]['points'] -= 100

    # Update with new data
    update_json("accounts/accounts.json", accounts)

def playDuelist(self, c, player1, player2):
    gameorder = []
    for x in range(0,3):
        gameorder.append(random.randrange(0,3))
    c.privmsg(self.channel, f"[⚔️Duelist⚔️] Game order created! Let the games begin!")
    time.sleep(2)

    gameChooser(gameorder[0], self, c, player1, player2, "1")
    if player1.points > player2.points:
        c.privmsg(self.channel, f"[⚔️Duelist⚔️] Game 1 completed! {player1.username} is in the lead!")
    else:
        c.privmsg(self.channel, f"[⚔️Duelist⚔️] Game 1 completed! {player2.username} is in the lead!")
    time.sleep(2)

    gameChooser(gameorder[1], self, c, player1, player2, "2")
    if player1.points == player2.points:
        c.privmsg(self.channel, f"[⚔️Duelist⚔️] Game 2 completed! Both players are currently equal in points! Time for the deathmatch round!")
        time.sleep(2)

        gameChooser(gameorder[1], self, c, player1, player2, "3")
        if player1.points == 2:
            c.privmsg(self.channel, f"[⚔️Duelist⚔️] Game 3 completed! {player1.username} has won! Congratulations! [+100xp]")
            c.privmsg(self.channel, f"[⚔️Duelist⚔️] Unfortunately, {player2.username} has lost. Better luck next time! [-100 points]")
            riskreward(self, c, player1, player2, player1.username)
        elif player2.points == 2:
            c.privmsg(self.channel, f"[⚔️Duelist⚔️] Game 3 completed! {player2.username} has won! Congratulations! [+100xp]")
            c.privmsg(self.channel, f"[⚔️Duelist⚔️] Unfortunately, {player1.username} has lost. Better luck next time! [-100 points]")
            riskreward(player1, player2, player2.username)

    elif player1.points == 2:
        c.privmsg(self.channel, f"[⚔️Duelist⚔️] Game 2 completed! {player1.username} has won! Congratulations! [+100xp]")
        c.privmsg(self.channel, f"[⚔️Duelist⚔️] Unfortunately, {player2.username} has lost. Better luck next time! [-100 points]")
        riskreward(player1, player2, player1.username)
    elif player2.points == 2:
        c.privmsg(self.channel, f"[⚔️Duelist⚔️] Game 2 completed! {player2.username} has won! Congratulations! [+100xp]")
        c.privmsg(self.channel, f"[⚔️Duelist⚔️] Unfortunately, {player1.username} has lost. Better luck next time! [-100 points]")
        riskreward(player1, player2, player2.username)
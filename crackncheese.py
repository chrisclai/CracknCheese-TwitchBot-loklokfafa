from hashlib import new
from logging import exception
import irc.bot
import requests
import random
import time
from datetime import datetime

from requests.models import StreamConsumedError
import privinfo
from _thread import *
import threading
import tkinter as tk
from pygame import mixer

# Individual File Dependencies
from update_json import *
from checkrank import *
from info import *
from sortleaderboard import *
from tkleaderboard import *
from groupreward import *
from requestreward import checkreward
from duelist import *

class TwitchBot(irc.bot.SingleServerIRCBot):
    # GLOBAL VARIABLES
    global accounts
    accounts = {}
    accounts = refresh_json(accounts)

    # For wordcharade game only!
    global wordactive
    wordactive = False

    global currentwordlocation
    currentwordlocation = ""

    global numguesses
    numguesses = 0

    # For Duelist game only!
    global firstplayerenter
    firstplayerenter = False

    global secondplayerenter
    secondplayerenter = False

    global player1
    player1 = Duelist("")

    global player2
    player2 = Duelist("")

    def __init__(self, username, client_id, token, channel):
        self.client_id = client_id
        self.token = token
        self.channel = '#' + channel

        # Get the channel id, we will need this for v5 API calls
        url = 'https://api.twitch.tv/kraken/users?login=' + channel
        headers = {'Client-ID': client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
        r = requests.get(url, headers=headers).json()
        self.channel_id = r['users'][0]['_id']

        # Create IRC bot connection
        server = 'irc.chat.twitch.tv'
        port = 6667
        print ('Connecting to ' + server + ' on port ' + str(port) + '...')
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, 'oauth:'+token)], username, username)

    def on_welcome(self, c, e):
        print ('Joining ' + self.channel)

        def auto_msg(self, c):
            while True:
                try:
                    c.privmsg(self.channel, "Hi, I'm a bot created just for this twitch channel! To use me, just type in !help. Enjoy the stream!")
                    time.sleep(240)
                except KeyboardInterrupt:
                    break

        def check_bell(self, c):
            while True:
                time.sleep(1)
                message = checkreward()
                if message:
                    c.privmsg(self.channel, message)
                else:
                    pass
                
        thread_automsg = threading.Thread(target = auto_msg, args = (self, c))
        thread_automsg.start()

        thread_leaderboard = threading.Thread(target = tkleaderboard)
        thread_leaderboard.start()

        thread_checkbell = threading.Thread(target = check_bell, args = (self, c))
        thread_checkbell.start()

        # You must request specific capabilities before you can use them
        c.cap('REQ', ':twitch.tv/membership')
        c.cap('REQ', ':twitch.tv/tags')
        c.cap('REQ', ':twitch.tv/commands')
        c.join(self.channel)

    def on_pubmsg(self, c, e):
        # Global player1 and player 2 variables for math game
        global player1
        global player2
        
        # Update the Bong Bell (iterate by 1) when a message is sent by anyone
        msgup()

        # If a chat message starts with an exclamation point, try to run it as a command
        if e.arguments[0][:5] == '!math':
            try:
                ans = e.arguments[0].split(' ')[1]
                if player1.min3start and player2.min3start:
                    if e.source.nick == player1.username:
                        player1.mathanswer = ans
                    elif e.source.nick == player2.username:
                        player2.mathanswer = ans
                else:
                    c.privmsg(self.channel, "[Duelist] This command cannot be used outside of battle. Use !duelist to begin a match!")
            except:
                c.privmsg(self.channel, "[Duelist] Please enter an answer!")
        elif e.arguments[0][:10] == '!playsound':
            try:
                cmd = e.arguments[0].split(' ')[1]
                print('Recieved command: ' + cmd)
                self.playsound(e, cmd)
            except:
                c.privmsg(self.channel, "What would you like me to play?")
        elif e.arguments[0][:1] == '!':
            cmd = e.arguments[0].split(' ')[0][1:]
            print('Received command: ' + cmd)
            self.do_command(e, cmd)
            

        # Word charade game
        global wordactive
        global currentwordlocation
        global numguesses
        global accounts
        if e.arguments[0][:12] == '!wordcharade':
            try:
                guess = e.arguments[0].split(' ')[1]
                if guess == 'help':
                    c.privmsg(self.channel, wordcharadehelp())
                elif wordactive:
                    words = word_charade_get()
                    if guess.lower() != words[str(currentwordlocation)]['word']:
                        numguesses += 1
                        if numguesses >= 100:
                            correctword = words[str(currentwordlocation)]['word']
                            c.privmsg(self.channel, f"[Word Charade] Unfortunately, no one has gotten the word correct in 100 messages. The correct word was {correctword}. Thanks for playing, see you next time!")
                        else:
                            c.privmsg(self.channel, f"[Word Charade] Unfortunately, that guess is incorrect. You are currently at {numguesses} guesses. Try Again!")
                    else:
                        reward = words[str(currentwordlocation)]['reward']
                        if numguesses >= 0 and numguesses < 15:
                            reward *= 1
                        elif numguesses >= 15 and numguesses < 30:
                            reward *= 0.8
                        elif numguesses >= 30 and numguesses < 50:
                            reward *= 0.6
                        elif numguesses >= 50:
                            reward *= 0.4
                        c.privmsg(self.channel, f"[Word Charade] Congrats! That is the correct answer! You have been awarded {int(reward)} xp!")
                        accounts = new_json()
                        for x in range (len(accounts)):
                            if accounts[str(x)]['username'] == e.source.nick:
                                accounts[str(x)]['xp'] += int(reward)
                                break
                        update_json('accounts/accounts.json', accounts)
                        wordactive = False
                else:
                    c.privmsg(self.channel, "Game has not started yet! Please use !wordcharade to play the game!")
            except:
                words = word_charade_get()
                hint0 = words[str(currentwordlocation)]["hint0"]
                hint1 = words[str(currentwordlocation)]["hint1"]
                hint2 = words[str(currentwordlocation)]["hint2"]
                hint3 = words[str(currentwordlocation)]["hint3"]
                if numguesses >= 0 and numguesses < 15:
                    c.privmsg(self.channel, f"[Word Charade] The first hint is: [{hint0}]. Keep guessing to unlock more hints!")
                elif numguesses >= 15 and numguesses < 30:
                    c.privmsg(self.channel, f"[Word Charade] The second hint is: [{hint1}]. Keep guessing to unlock more hints!")
                elif numguesses >= 30 and numguesses < 50:
                    c.privmsg(self.channel, f"[Word Charade] The third hint is: [{hint2}]. Keep guessing to unlock more hints!")
                elif numguesses >= 50:
                    c.privmsg(self.channel, f"[Word Charade] The final hint is: [{hint3}]. Keep guessing to unlock more hints!")

        # Award points to the chatter for interaction (also awards xp)
        print(f"System has given {e.source.nick} 1 point and 1 xp!")
        accounts = refresh_json(accounts)
        accountlen = len(accounts)
        awardee = e.source.nick
        exist = False
        for x in range (accountlen):
            if accounts[str(x)]['username'] == awardee:
                accounts[str(x)]['points'] += 1
                accounts[str(x)]['xp'] += 1
                rank, _ = checkrank(accounts[str(x)]['xp'])
                accounts[str(x)]['rank'] = rank
                update_json('accounts/accounts.json',accounts)
                exist = True
                break
        if not exist:
            c.privmsg(self.channel, "You did not recieve xp for this message! Please use !account to save your progress, earn xp, and gain points!")

    def playsound(self, e, cmd):
        global accounts
        c = self.connection
        exist = False
        location = 0

        for x in range (len(accounts)):
            if accounts[str(x)]['username'] == e.source.nick:
                exist = True
                location = x
                break

        if exist and accounts[str(location)]['points'] > 50:
            mixer.init()
            if cmd == 'bong':
                accounts[str(location)]['points'] -= 50
                update_json('accounts/accounts.json', accounts)
                mixer.music.load('sounds/bong.mp3')
                c.privmsg(self.channel, f"Hey {e.source.nick}, you ran the command !playsound bong, which costs 50 points. You now have {accounts[str(location)]['points']} points remaining!")
            else:
                c.privmsg(self.channel, "Sorry, that sound doesn't exist (yet)! Please use !checkcooldown to view the current status of the cooldown.")
            mixer.music.play()
        else:
            c.privmsg(self.channel, f"Sorry, you do not have enough points! {50 - accounts[str(location)]['points']} points until you can use this command! Use !account to check how many points you have!")

    def do_command(self, e, cmd):
        c = self.connection

        # Just for accounts
        global accounts

        # Just for wordcharade game
        global wordactive
        global currentwordlocation
        global numguesses

        # Just for Duelist game
        global firstplayerenter
        global secondplayerenter
        global player1
        global player2

        # Poll the API to get current game.
        if cmd == "game":
            url = 'https://api.twitch.tv/kraken/channels/' + self.channel_id
            headers = {'Client-ID': self.client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
            r = requests.get(url, headers=headers).json()
            c.privmsg(self.channel, r['display_name'] + ' is currently playing ' + r['game'])

        # Poll the API the get the current status of the stream
        elif cmd == "title":
            url = 'https://api.twitch.tv/kraken/channels/' + self.channel_id
            headers = {'Client-ID': self.client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
            r = requests.get(url, headers=headers).json()
            c.privmsg(self.channel, r['display_name'] + ' channel title is currently streaming: ' + r['status'])

        # Provide the Discord Link
        elif cmd == "discord":
            message = "Join the Discord for more fun! [https://discord.gg/Teu3KF7sAk]"
            c.privmsg(self.channel, message)

        # Provide all the help commands
        elif cmd == "help":
            c.privmsg(self.channel, help())
            
        # Roll command
        elif cmd == "roll":
            randnum = random.randrange(0,100,1)
            message = str(randnum)
            c.privmsg(self.channel, message)

        # lurk command
        elif cmd == "lurk":
            message = e.source.nick + " is now lurking loklokfafa's channel. See you when you come back! 🎉🎉🎉"
            c.privmsg(self.channel, message)

        # list available sounds
        elif cmd == "listsounds":
            message = "Currently Available Sounds: bong || Use the !playsound <sound> command to play a sound on stream! Use !account to check your point total!"
            c.privmsg(self.channel, message)

        # Create a account for the loklokfafa channel
        elif cmd == "account":
            exist = False
            location = 0

            print("Accounts Refreshed!")
            accounts = refresh_json(accounts)
            accountlen = len(accounts)

            for x in range(accountlen):
                if e.source.nick == accounts[str(x)]['username']:
                    exist = True
                    location = x
                    break

            if not exist:
                tempdict = {}
                tempdict['username'] = e.source.nick
                tempdict['points'] = 0
                tempdict['xp'] = 0
                tempdict['rank'] = ""
                tempdict['lastjoined'] = ""
                accounts[str(accountlen)] = tempdict
                update_json("accounts/accounts.json",accounts)
                c.privmsg(self.channel, f"Thank you for creating a loklokfafa account, {e.source.nick}! Enjoy the stream!")
                print("Account created!")
                accountlen = len(accounts)
            else:
                points = accounts[str(location)]['points']
                xp = accounts[str(location)]['xp']
                rank, difference = checkrank(xp)
                message = f"Welcome back {e.source.nick}, you are currently in the [{rank}] rank! You have [{xp}] xp and a balance of [{points}] points. {difference} more xp to go until the next rank! Thanks for participating!"
                c.privmsg(self.channel, message)

        # Display Awards
        elif cmd == "redeem":
            c.privmsg(self.channel, redeem())

        # Display Leaderboard
        elif cmd == "leaderboard":
            accounts = refresh_json(accounts)
            listnames, listxp = sortbyhigh(accounts)
            output = "XP Leaderboard"
            emojis = ["🏆", "🥇", "🥈", "🥉", "🏅", "🎖️", "🎖", "🔲"]
            for x in range(0, 8):
                output += f" || {emojis[x]}: [{listnames[x]}, {listxp[x]} xp]"
            c.privmsg(self.channel, output)

        # Daily Reward
        elif cmd == "daily":
            exist = False
            location = 0
            accounts = refresh_json(accounts)
            for x in range (len(accounts)):
                if e.source.nick == accounts[str(x)]['username']:
                    exist = True
                    location = x
                    break
            if exist:
                now = datetime.now()
                pointamount = random.randrange(50, 100, 1)
                if now.strftime('%m/%d/%Y') != accounts[str(x)]['lastjoined']:
                    accounts[str(x)]['lastjoined'] = now.strftime('%m/%d/%Y')
                    accounts[str(x)]['points'] += pointamount
                    c.privmsg(self.channel, f"Thank you for tuning in today. Here is your daily reward! [+{pointamount} points]")
                else:
                    c.privmsg(self.channel, "Sorry, your daily reward was already collected. Come back tomorrow for another go!")
            else:
                c.privmsg(self.channel, "Sorry, you do not have an account yet. Please use !account to create an account.")
            update_json("accounts/accounts.json", accounts)

        # Displays Ranks
        elif cmd == "rankinfo":
            c.privmsg(self.channel, ranks())

        # Wordcharade Game
        elif cmd == "wordcharade":
            if not wordactive:
                wordactive = True
                c.privmsg(self.channel, "Word Charade Started, searching for word now!")
                words = word_charade_get()
                numguesses = 0
                currentwordlocation = random.randrange(0,len(words))
                randword = words[str(currentwordlocation)]["word"]
                time.sleep(3)
                c.privmsg(self.channel, f"Word Found! Start Guessing!")
                print(self.channel, f"Word Found! The word is {randword}")
            else:
               pass

        elif cmd == "duelist":
            if not firstplayerenter:
                player1 = Duelist(e.source.nick)
                accounts = new_json()
                if accounts[str(player1.location)]['points'] < 100:
                    c.privmsg(self.channel, "Sorry, the required point total to play [Duelist] is 100 points. Please come back when you have the required points!")
                    player1 = Duelist("")
                else:
                    firstplayerenter = True
                    c.privmsg(self.channel, f"Hello {e.source.nick}, waiting for another person to play [Duelist]!")
                    
                    def querySecondPlayer(self, c, e):
                        global firstplayerenter
                        global secondplayerenter
                        timecounter = 0
                        while(True):
                            print(secondplayerenter)
                            if not secondplayerenter:
                                time.sleep(30)
                                c.privmsg(self.channel, f"[Duelist] {e.source.nick} is currently waiting for another person to play Duelist. Use !duelist to begin the match!")
                                timecounter += 1
                            elif timecounter == 6:
                                firstplayerenter = True
                                c.privmsg(self.channel, f"[Duelist] Timeout occured at 5 minutes. Please re-type !duelist to enter queue again!")
                            else:
                                break

                    thread_query2 = threading.Thread(target = querySecondPlayer, args = (self, c, e))
                    thread_query2.start()
            elif not secondplayerenter:
                player2 = Duelist(e.source.nick)
                accounts = new_json()
                if accounts[str(player1.location)]['points'] < 100:
                    c.privmsg(self.channel, "Sorry, the required point total to play [Duelist] is 100 points. Please come back when you have the required points!")
                    player2 = Duelist("")
                else:
                    secondplayerenter = True
                    c.privmsg(self.channel, f"[Duelist] {e.source.nick} has entered the arena! Prepare for battle!")

                    def matchTimeout(self, c):
                        global firstplayerenter
                        global secondplayerenter
                        global player1
                        global player2

                        timecounter = 0

                        while True:
                            time.sleep(1)
                            timecounter += 1
                            if player1.hasaccept == True and player2.hasaccept == True:
                                playDuelist(self, c, player1, player2)
                                firstplayerenter = False
                                secondplayerenter = False
                                player1 = Duelist("")
                                player2 = Duelist("")
                                break
                                
                            elif timecounter > 60:
                                c.privmsg(self.channel, "[Duelist] Sorry, one of the players has not accepted the battle! (Use !accept). Queue has been reset to allow other players in. Thanks for participating!")
                                firstplayerenter = False
                                secondplayerenter = False
                                player1 = Duelist("")
                                player2 = Duelist("")
                                break

                    time.sleep(1)
                    c.privmsg(self.channel, f"[Duelist] {player1.username} and {player2.username}, please use !accept to start the game! You have 1 minute to do this before the system will reset!")

                    thread_startgame = threading.Thread(target = matchTimeout, args = (self, c))
                    thread_startgame.start()
            else:
                c.privmsg(self.channel, "[Duelist] A game has already started. Please wait for the current game to end before trying this command again!")

        elif cmd == "accept":
            if firstplayerenter and secondplayerenter:
                if e.source.nick == player1.username:
                    player1.hasaccept = True
                    c.privmsg(self.channel, f"[Duelist] {e.source.nick} is ready for battle!")
                elif e.source.nick == player2.username:
                    player2.hasaccept = True
                    c.privmsg(self.channel, f"[Duelist] {e.source.nick} is ready for battle!")
                else:
                    c.privmsg(self.channel, "[Duelist] Sorry, an ongoing game is occuring right now. Please wait until the current game is finished before starting a new one!")
            elif firstplayerenter:
                c.privmsg(self.channel, "[Duelist] Sorry, this command won't work unless a second player joins!")
            else:
                c.privmsg(self.channel, "[Duelist] Sorry, that command does not work yet. Please use !duelist to start a game!")

        elif cmd == "win":
            if player1.min2start and player2.min2start:
                if player1.username == e.source.nick:
                    player1.winmin2 = True
                elif player2.username == e.source.nick:
                    player2.winmin2 = True
            else:
                c.privmsg(self.channel, "[Duelist] Sorry, that command does not work but is part of the Duelist game. Use !duelist to begin a new game!")

        # If empty command is recieved
        elif not cmd:
            message = "no."
            c.privmsg(self.channel, message)

        # The command was not recognized
        else:
            c.privmsg(self.channel, "Did not understand command: " + cmd + " Please Use !help for all available commands.")

def main():
    username  = "crackncheesebot"
    client_id = privinfo.client_id
    token     = privinfo.token
    channel   = "loklokfafa"

    thread_groupreward = threading.Thread(target = groupreward)
    thread_groupreward.start()

    bot = TwitchBot(username, client_id, token, channel)
    bot.start()

if __name__ == "__main__":
    main()
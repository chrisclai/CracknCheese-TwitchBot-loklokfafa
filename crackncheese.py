import irc.bot
import requests
import random
import time
from datetime import datetime
import privinfo
from _thread import *
import threading
from pygame import mixer
from update_json import *
from checkrank import *
from info import *
from sortleaderboard import *
from tkleaderboard import *

class TwitchBot(irc.bot.SingleServerIRCBot):
    # GLOBAL VARIABLES
    global accounts
    accounts = {}
    accounts = refresh_json(accounts)
    
    global accountlen
    accountlen = len(accounts)

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

        thread_automsg = threading.Thread(target = auto_msg, args = (self, c))
        thread_automsg.start()

        thread_leaderboard = threading.Thread(target = tkleaderboard)
        thread_leaderboard.start()

        # You must request specific capabilities before you can use them
        c.cap('REQ', ':twitch.tv/membership')
        c.cap('REQ', ':twitch.tv/tags')
        c.cap('REQ', ':twitch.tv/commands')
        c.join(self.channel)

    def on_pubmsg(self, c, e):

        # If a chat message starts with an exclamation point, try to run it as a command
        if e.arguments[0][:1] == '!' and e.arguments[0][:10] != '!playsound':
            cmd = e.arguments[0].split(' ')[0][1:]
            print('Received command: ' + cmd)
            self.do_command(e, cmd)
        elif e.arguments[0][:10] == '!playsound':
            try:
                cmd = e.arguments[0].split(' ')[1]
                print('Recieved command: ' + cmd)
                self.playsound(e, cmd)
            except:
                c.privmsg(self.channel, "What would you like me to play?")

        # Award points to the chatter for interaction (also awards xp)
        global accounts
        global accountlen
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

        global accounts
        global accountlen

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
            message = "No discord found! Stay tuned for more updates!"
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

    bot = TwitchBot(username, client_id, token, channel)
    bot.start()

if __name__ == "__main__":
    main()
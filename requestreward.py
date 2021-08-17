from irc.client import MessageTooLong
import requests
from update_json import *

global message 
message = ""

def distribute_rewards():
    global message

    # Refresh dictionary
    accounts = new_json()

    # Amount of points added (reward)
    points = 50

    # Get url, request information from it
    url = 'https://tmi.twitch.tv/group/user/loklokfafa/chatters'
    info = requests.get(url).json()
    
    # Create list with all current chatters
    viewers = []
    for x in range (len(info['chatters']['moderators'])):
        viewers.append(info['chatters']['moderators'][x])

    for x in range (len(info['chatters']['viewers'])):
        viewers.append(info['chatters']['viewers'][x])

    # Iterate through all elements of for loop in order to add the correct points
    # Filter out any members not in accounts.json and refresh dictionary afterwards
    trueviewers = []
    for i in range (len(viewers)):
        for j in range (len(accounts)):
            if viewers[i] == accounts[str(j)]['username']:
                trueviewers.append(viewers[i])
                accounts[str(j)]['points'] += points
    update_json('accounts/accounts.json', accounts)

    # Create a string (display message) as to show who has recieved the points
    message = ""
    for x in range (0, len(trueviewers) - 1):
        message += trueviewers[x] + ", "
    message +=  " and " + trueviewers[len(trueviewers) - 1] + ", thank you for participating in the chat! You all have been awarded " + str(points) + " points for ringing the bong bell! GlitchLit"

def checkreward():
    global message
    tempmessage = message
    message = ""
    return tempmessage
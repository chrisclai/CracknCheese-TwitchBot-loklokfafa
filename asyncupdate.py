from update_json import *

def addkey():
    accounts = new_json()

    for x in range(len(accounts)):
        accounts[str(x)]['discordname'] = ""

    update_json('accounts/accounts.json', accounts)

def removekey():
    accounts = new_json()

    for x in range(len(accounts)):
        del accounts[str(x)]['discordname']

    update_json('accounts/accounts.json', accounts)

if __name__ == "__main__":
    addkey()
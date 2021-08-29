from update_json import new_json

def finduser(e, accounts):
    location = 0
    for x in range (len(accounts)):
        if e.source.nick == accounts[str(x)]['username']:
            location = x
            break
    return location
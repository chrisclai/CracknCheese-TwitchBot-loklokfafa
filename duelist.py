from update_json import *

class Duelist:
    def __init__(self, username):
        self.username = username
        self.points = 0

        accounts = new_json()
        self.location = 0
        for x in range(len(accounts)):
            if username == accounts[str(x)]['username']:
                self.location = x
                break

    def addPoint(self):
        self.points += 1


import json

def update_json(directory, dictionary):
    temp = open(directory, 'w')
    json.dump(dictionary, temp, indent = 4)
    temp.close()

def refresh_json(accounts):
    with open('accounts/accounts.json') as read_file:
            accounts = json.load(read_file)
            return accounts

def new_json():
    with open('accounts/accounts.json') as read_file:
            accounts = json.load(read_file)
            return accounts

def word_charade():
    with open('wordcharade.json') as read_file:
            return json.load(read_file)
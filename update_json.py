import json

def update_json(directory, dictionary):
    temp = open(directory, 'w')
    json.dump(dictionary, temp, indent = 4)
    temp.close()
    
def new_json():
    with open('accounts/accounts.json') as read_file:
            accounts = json.load(read_file)
            return accounts

def word_charade_get():
    with open('wordcharade.json') as read_file:
            return json.load(read_file)
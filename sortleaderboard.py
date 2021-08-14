def sortbyhigh(accounts):
    listnames = []
    listpoints = []
    for x in range (len(accounts)):
        listnames.append(accounts[str(x)]['username'])
        listpoints.append(accounts[str(x)]['xp'])
    for i in range(len(accounts)):
        for j in range(0, len(accounts) - i - 1):
            if listpoints[j] < listpoints[j + 1]:
                tempvar = listpoints[j]
                listpoints[j] = listpoints[j + 1]
                listpoints[j + 1] = tempvar
                tempvar = listnames[j]
                listnames[j] = listnames[j + 1]
                listnames[j + 1] = tempvar
    return listnames, listpoints
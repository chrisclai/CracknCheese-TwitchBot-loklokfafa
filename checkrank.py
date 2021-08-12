def checkrank(self, c, e, xp):
    rank = ""
    toplvl = 0
    
    if xp >= 0 and xp < 50:
        rank = "Starter"
        toplvl = 50
    elif xp >= 100 and xp < 150:
        rank = "Experienced"
        toplvl = 150
    elif xp >= 150 and xp < 300:
        rank = "Limestone"
        toplvl = 300
    elif xp >= 300 and xp < 500:
        rank = "Iron"
        toplvl = 500
    elif xp >= 500 and xp < 750:
        rank = "Bronze"
        toplvl = 750
    elif xp >= 750 and xp < 1250:
        rank = "Silver"
        toplvl = 1250
    elif xp >= 1250 and xp < 1750:
        rank = "Gold"
        toplvl = 1750
    elif xp >= 1750 and xp < 3000:
        rank = "Emerald"
        toplvl = 3000
    elif xp >= 3000 and xp < 5000:
        rank = "Sapphire"
        toplvl = 5000
    elif xp >= 5000 and xp < 10000:
        rank = "Ruby"
        toplvl = 10000
    elif xp >= 10000 and xp < 50000:
        rank = "Diamond"
        toplvl = 50000
    elif xp >= 50000 and xp < 100000:
        rank = "Obsidian"
        toplvl = 100000
    elif xp >= 100000:
        rank = "Immortal"
        toplvl = 2147483647

    difference = toplvl - xp
    return rank, difference

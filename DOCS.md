# Daily Updates and Documentation

This markdown file contains daily updates on progress that is made during a livestream. The corresponding label relates to the stream that the progress came from. Series title: Day ### of coding twitch chat perks until I get affiliate (or until I get a chat)

### August 12th, 2021 (Day 5)
- Created a new file called tkleaderboard to display a leaderboard in real time on stream such that chatters can see xp rise
- Spammers in chat stress tested the bot, bot did not fail (which is a good thing)
- Few chatters reached Grass -> Iron rank in the span of 50 minutes
- Added the requisite emojis into the window, will improve on design at another time

---

### August 11th, 2021 (Day 4)
- Documentation of progress made from previous streams (day by day)
- Created **README.md**, **LICENCE** and **DOCS.md** files for publication
- Created **.gitignore** file to prevent private information from being on the repository

---

### August 8th, 2021 (Day 3)
- Created xp system similar to the points system except it negates depeletion due to rewards
- Created ranking system based on the total cumulative xp earned by chatters
- Created multiple assistive files (dependencies) to minimize code
    * **checkrank.py** Contains function to take in parameter xp value, return correct rank and difference to next rank for display purposes
    * **info.py** Contains function in which its core purpose is to return a long string that contains information on instructions for several commmands, such as **!help**, **!rankinfo**, and **!redeem**
- Edited **!account** command to display points, xp, and rank information, as well as the difference calculated in **checkrank.py**
- Changed leaderboard from ranking points to ranking xp due to consistency

---

### August 7th, 2021 (Day 2)
- Created an interactive leaderboard that displays who has the most points at any given time (top 8)
    * Split the dictionary into two lists containing the entire **username** key and **points** key
    * Used a sorting algorithm (bubble sort) to organize the points list from highest to lowest
    * For the same swapping sequence used in the **points** list, apply the same to the **username** list so both user and point total match
    * Display top 8 using for loop, with iterator variable taking from both lists at the same time
- Created a third list containg emojis with degrading quality to display who is in first -> last place

---

### August 6th, 2021 (Day 1)
- Decided on how to track users through chatlog
    * Initially wanted to track users through time watched like you can with affiliate bonuses, but due to Twitch's bylaws on third party applications, this was a privacy concern (denied)
    * To mitigate this, we narrowed the scope and focused on what we currently have, which is the function that records every message sent in chat (on_pubmsg())
    * 1 point = 1 message sent
- Created logic to integrate the sending system in on_pubmsg() with the accounts.json data
    * Add 1 if message sent, update/refresh dictionary
- Utilized dependency **update_json.py** to both insert file and extract information
- Optimized **update_json.py** to contain two functions that continuously update a dictionary **accounts**
    * **update_json(directory, dictionary)**: Open the .json file in specified directory, dump contents of dictionary into file with indentation level of 4, close file
    * **refresh_json(accounts)**: Open the .json file in a read_only state, load contents of the data file into the **accounts** dictionary, return **accounts** dictionary

---

### August 5th, 2021 (Day 0)
- Basic framework of a twitch bot using IRC
- Description of startup protocol, \_init\_, main() functions, TwitchBot class initialization
- on_pubmsg() function and closed loop feedback using reactive Twitch chat, automated process
- do_command() function, **c**, **e**, and **self** parameters for each message sent
- Described basic commands, such as discord, game, title, roll, lurk, etc.
- Basic points system created using individual messages sent through chat (group effort)
- Basic rewards system creating using pygame mp3 sounds sent through streamer's computer
- Began creating accounts.json, individualized user accounts for all chat participants
- Separate username and point keys in dictionary accessed through
- Created an asynchronous threaded function **auto_msg()** to send a message to the chat to allow new viewers to interact with the bot and know of its existence

# Daily Updates and Documentation

This markdown file contains daily updates on progress that is made during a livestream. The corresponding label relates to the stream that the progress came from. Series title: Day ### of coding twitch chat perks until I get affiliate (or until I get a chat)

### August 18th, 2021 (Day 11)
- Completed implementation of word charade game, including doing clues for words
    * Added a point system, points are based on difficulty of word and gradually decrease as more hints are revealed
    * Provides xp upon the singular person guessing
    * Group effort to reveal more hints (global variable to keep track of number of guesses)
- Completed field testing of bot and fixed bugs. Functioned properly with minimal issues (minor typos/bugs)
- Connected variables through global references from on_pubmsg() to do_command()
- Allowed chat to begin guessing the word "calculus" utilizing contents of **wordcharade.json** 

---

### August 17th, 2021 (Day 10)
- Documented all file paths and dependency requirements inside **Systems.drawio** as a flowchart
- Began simple skeleton code system for designing a game that can be played by twitch chat (word charade)

---

### August 16th, 2021 (Day 9)
- Created a variable called threshold that is linked to all systems that control position and maximum total for the progress bar. Max messages linked
- Created a thread for the completion of the progress bar as to not interfere with the rest of the recursive **updatedata** function
- Create a global toggle variable called trackactivate to track the state of the global variable messages throughout the threaded function
- Changed colors such that green = complete, and ship will restart after the bongs have been completed
- Implemented a rewards system using Twitch API to give all current viewers that are inside of the accounts.json file 50 free points once the bell has rung
    * Take entire info file from API using **requests** library
    * Extract all moderators and current viewers (including the bots)
    * Put all viewers into a list
    * Filter the true viewers from regular viewers using O(n^2) algorithm comparison checker
    * Provide points to only the true viewers and update the accounts.json file
    * Create global variable called message and use a toggling system to feed the message that needs to be sent back into chat through the main .py file
    * In the main file, create a thread with an infinite loop segmented by time.sleep(1) that will check the function inside **requestreward.py** for any new messages
- Current threshold = 250 messages (xp) and current reward is 50 points (pts)

---

### August 15th, 2021 (Day 8)
- Added a label that tracks the percentage of goal reached
- Used the recursive update function inside tk function in order to track group progress over time based on messages sent from on_pubmsg() from main script
- Came up with increment function that calculates the relative x position based on % of messages sent
- Developed a reward system that provides bong noises once the ship reaches the bell and rings it 5 times over a period of 15 seconds

---

### August 14th, 2021 (Day 7)
- Added a new file called **groupreward.py** in which the twitch chat's cumulative effort will go into a group reward
- Created a tkinter window and drew a line, imported images, designed title in preparation for tomorrow in which we will make the rocketship move

---

### August 13th, 2021 (Day 6)
- Added a key into the accounts.json dictionary file called "lastjoin" that contains the last date that a chatter runs the command !daily
- Added a command called !daily that proves the chatter with a random amount of points between 50-100 (one bong guarenteed)
- Constrained the usage of !daily to once a day using the **datetime** module (Find today, put in dictionary, use to compare values)
- Completed implementation of a basic leaderboard system using the module **tkleaderboard** to create a seperate screen that live updates the value of xp that one gains
- Updated SLOBS (stream lab obs) in order to specifically display that screen on opening
- Integrated file into main **crackncheese.py** script so that the tk window can open upon starting script

---

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

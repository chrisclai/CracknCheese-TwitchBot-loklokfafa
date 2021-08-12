# CracknCheese TwitchBot (loklokfafa)

This Github repository outlines a basic twitch chatbot script that can be activated through a Python file.

Developed and released open-source by loklokfafa: twitch.tv/loklokfafa

## Personal Files

For privacy purposes, the following files were hidden through the use of .gitignore. To mitigate this issue when a user activates the file, create the following folders/files with the correct information:

1. Create a **privinfo.py** file in the main directory, highest level. In it, place the client_id and auth token values taken from the bot's Twitch account as such:
    
    ```
    client_id = ""
    token = ""
    ```

2. Create an **accounts** folder in the main directory, highest level. In it, create a blank .json file named **accounts.json**. You may or may not want to preload the dictionary with an initial definition, listed below:

    ```
    {
        "0": {
            "username": "sample",
            "points": 0,
            "xp": 0,
            "rank": "sample"
        }
    }
    ```

3. Create a **sounds** folder in the main dictionary, highest level. In it, place any .mp3 files you may want to play through the computer's audio. Make sure to edit the main .py file such that the correct file is referenced. 

4. All paths in the main .py file are relative paths. Make sure you are running the file from the correct directory.
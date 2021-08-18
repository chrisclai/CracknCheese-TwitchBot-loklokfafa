from sortleaderboard import sortbyhigh
import tkinter as tk

# Individual File Dependencies
from update_json import *
from checkrank import *

def tkleaderboard():
    HEIGHT = 480
    WIDTH = 480
    BGCOLOR = 'black'
    TITLECOLOR = 'red'
    FONT = 'arial'
    REFRESH_RATE = 1000

    # Initialization
    root = tk.Tk()
    root.resizable(False, False)
    main_canv = tk.Canvas(root, height=HEIGHT, width=WIDTH, bg=BGCOLOR, highlightthickness=0)
    main_canv.pack()

    # Producing Labels and placing them in certain areas
    title = tk.Label(main_canv, text="XP Leaderboard", font=("courier new", 24, 'bold'), justify='left', bg=BGCOLOR, fg=TITLECOLOR)
    title.place(relx=0.5, rely=0.1, anchor='center')

    firstplace = tk.Label(main_canv, text="🏆", font=(FONT, 14, 'bold'), justify='left', bg=BGCOLOR, fg='yellow')
    firstplace.place(relx=0.08, rely = 0.25, anchor='w')

    secondplace = tk.Label(main_canv, text="🥇", font=(FONT, 14, 'bold'), justify='left', bg=BGCOLOR, fg='gold')
    secondplace.place(relx=0.08, rely = 0.4, anchor='w')

    thirdplace = tk.Label(main_canv, text="🥈", font=(FONT, 14, 'bold'), justify='left', bg=BGCOLOR, fg='silver')
    thirdplace.place(relx=0.08, rely = 0.55, anchor='w')

    fourthplace = tk.Label(main_canv, text="🥉", font=(FONT, 14, 'bold'), justify='left', bg=BGCOLOR, fg='brown')
    fourthplace.place(relx=0.08, rely = 0.7, anchor='w')

    fifthplace = tk.Label(main_canv, text="🏅", font=(FONT, 14, 'bold'), justify='left', bg=BGCOLOR, fg='white')
    fifthplace.place(relx=0.08, rely = 0.85, anchor='w')

    # Recursive loop to store new data every 1 second
    def updateData():
        accounts = new_json()
        listnames, listxp = sortbyhigh(accounts)

        firstplace['text'] = f"🏆: {listnames[0]} || Rank: {checkrank(listxp[0])[0]} || XP: {listxp[0]}"
        secondplace['text'] = f"🥇: {listnames[1]} || Rank: {checkrank(listxp[1])[0]} || XP: {listxp[1]}"
        thirdplace['text'] = f"🥈: {listnames[2]} || Rank: {checkrank(listxp[2])[0]} || XP: {listxp[2]}"
        fourthplace['text'] = f"🥉: {listnames[3]} || Rank: {checkrank(listxp[3])[0]} || XP: {listxp[3]}"
        fifthplace['text'] = f"🏅: {listnames[4]} || Rank: {checkrank(listxp[4])[0]} || XP: {listxp[4]}"
        
        root.after(REFRESH_RATE, updateData)

    root.after(REFRESH_RATE, updateData)

    root.mainloop()
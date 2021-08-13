import tkinter as tk
from tkinter.constants import CENTER

def tkleaderboard():
    HEIGHT = 600
    WIDTH = 480
    BGCOLOR = 'black'
    TITLECOLOR = 'red'
    FONT = 'helvetica'

    # Initialization
    root = tk.Tk()
    root.resizable(False, False)
    main_canv = tk.Canvas(root, height=HEIGHT, width=WIDTH, bg=BGCOLOR, highlightthickness=0)
    main_canv.pack()

    title = tk.Label(main_canv, text="XP Leaderboard", font=(FONT, 24, 'bold'), justify='center', bg=BGCOLOR, fg=TITLECOLOR)
    title.place(relx=0.5, rely=0.075, anchor='center')

    firstplace = tk.Label(main_canv, text="🏆", font=(FONT, 24, 'bold'), justify='center', bg=BGCOLOR, fg='yellow')
    firstplace.place(relx=0.5, rely = 0.25, anchor='center')

    secondplace = tk.Label(main_canv, text="🥇", font=(FONT, 24, 'bold'), justify='center', bg=BGCOLOR, fg='gold')
    secondplace.place(relx=0.5, rely = 0.4, anchor='center')

    thirdplace = tk.Label(main_canv, text="🥈", font=(FONT, 24, 'bold'), justify='center', bg=BGCOLOR, fg='silver')
    thirdplace.place(relx=0.5, rely = 0.55, anchor='center')

    fourthplace = tk.Label(main_canv, text="🥉", font=(FONT, 24, 'bold'), justify='center', bg=BGCOLOR, fg='brown')
    fourthplace.place(relx=0.5, rely = 0.7, anchor='center')

    fifthplace = tk.Label(main_canv, text="🏅", font=(FONT, 24, 'bold'), justify='center', bg=BGCOLOR, fg='white')
    fifthplace.place(relx=0.5, rely = 0.85, anchor='center')

    root.mainloop()

tkleaderboard()
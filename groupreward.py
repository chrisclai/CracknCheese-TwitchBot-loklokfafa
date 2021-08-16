import tkinter as tk
import time
from pygame import mixer

global messages
messages = 0

def msgup():
    global messages
    messages += 1

def groupreward():
    # Global Variables
    global messages

    # Local Variables
    HEIGHT = 250
    WIDTH = 2000
    BGCOLOR = 'black'
    TITLECOLOR = 'orange'
    REFRESH_RATE = 1000

    # Initialization
    root = tk.Tk()
    root.resizable(False, False)
    main_canv = tk.Canvas(root, height=HEIGHT, width=WIDTH, bg=BGCOLOR, highlightthickness=0)
    main_canv.pack()

    # Declare Images
    bell_icon = tk.PhotoImage(file='images/bell.png')
    rocket_icon = tk.PhotoImage(file='images/rocket.png')

    # Title
    title = tk.Label(main_canv, text="Bong Bell", font=("garamond", 24, 'bold'), justify='left', bg=BGCOLOR, fg=TITLECOLOR)
    title.place(relx=0.5, rely=0.15, anchor='center')

    # Progress Line
    main_canv.create_line(100, 125, 1900, 125, fill='white', width=5)

    # Assets
    bell_canv = tk.Canvas(main_canv, width=60, height=60, highlightthickness=0, bg='black')
    bell_canv.place(relx=0.95, rely=0.5, anchor='center')
    bell_canv.create_image(0,0,anchor='nw', image=bell_icon)

    rocket_canv = tk.Canvas(main_canv, width=62, height=60, highlightthickness=0, bg='black')
    rocket_canv.place(relx=0.05, rely=0.5, anchor='center')
    rocket_canv.create_image(0,0,anchor='nw', image=rocket_icon)

    rocket_label = tk.Label(main_canv, text="0 xp", font=("garamond", 18, 'bold'), justify='center', bg=BGCOLOR, fg='white')
    rocket_label.place(relx=0.05,rely=0.65,anchor='center')

    rocket_percent = tk.Label(main_canv, text="0.00%", font=("garamond", 18, 'bold'), justify='center', bg=BGCOLOR, fg='yellow')
    rocket_percent.place(relx=0.05,rely=0.8,anchor='center')

    bell_label = tk.Label(main_canv, text="250 xp", font=("garamond", 18, 'bold'), justify='center', bg=BGCOLOR, fg='white')
    bell_label.place(relx=0.95,rely=0.3,anchor='center')

    def findPos(msg):
        # Find location of ship relative to x axis
        increment = (0.95 - 0.05)/250
        return 0.05 + increment * msg

    def updateData():
        # If messages reach goal 250 proc reward
        global messages
        if messages == 250:
            rocket_label['fg'] = 'green'
            mixer.init()
            mixer.music.load('sounds/bong.mp3')
            for x in range(0,5):
                mixer.music.play()
                time.sleep(3)
            messages = 0

        # Check the value of messages every 1 second and update label
        rocket_label['text'] = f"{messages} xp"
        rocket_percent['text'] = f"{round(messages/250.0 * 100, 2)}%"

        # Placing the rocket depending on its relative position given % to goal
        xpos = findPos(messages)
        rocket_canv.place(relx=xpos, rely=0.5, anchor='center')
        rocket_label.place(relx=xpos, rely=0.65, anchor='center')
        rocket_percent.place(relx=xpos, rely=0.8, anchor='center')

        root.after(REFRESH_RATE, updateData)

    root.after(REFRESH_RATE, updateData)

    root.mainloop()
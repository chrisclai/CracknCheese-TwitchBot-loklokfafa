import tkinter as tk
from tkinter.constants import ANCHOR
from PIL import Image, ImageTk

def groupreward():
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

    title = tk.Label(main_canv, text="Bong Bell", font=("garamond", 24, 'bold'), justify='left', bg=BGCOLOR, fg=TITLECOLOR)
    title.place(relx=0.5, rely=0.15, anchor='center')

    main_canv.create_line(100, 125, 1900, 125, fill='white', width=5)

    bell_canv = tk.Canvas(main_canv, width=60, height=60, highlightthickness=0, bg='black')
    bell_canv.place(relx=0.95, rely=0.5, anchor='center')
    bell_canv.create_image(0,0,anchor='nw', image=bell_icon)

    rocket_canv = tk.Canvas(main_canv, width=62, height=60, highlightthickness=0, bg='black')
    rocket_canv.place(relx=0.075, rely=0.5, anchor='center')
    rocket_canv.create_image(0,0,anchor='nw', image=rocket_icon)

    def updateData():
        root.after(REFRESH_RATE, updateData)

    root.after(REFRESH_RATE, updateData)

    root.mainloop()

groupreward()
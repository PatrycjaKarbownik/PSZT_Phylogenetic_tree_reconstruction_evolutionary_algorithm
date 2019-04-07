from tkinter import *
from nodes import *


def run_graphics(tree):
    root = Tk()
    root.title("Phylogenetic tree")
    root.geometry('800x600')

    canvas = Canvas(root, width=800, height=600)
    canvas.configure(bg="white")
    canvas.pack()

    w = Label(root, text = "Hello Tkinter!")
    w.place(x=10, y=90)
    w = Scale(root, from_=0, to=200, orient=HORIZONTAL)
    w.place(x=12, y=40)

    canvas.create_line(13, 14, 166, 166)

    root.mainloop()

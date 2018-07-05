from tkinter import *
import random




def run(width = 500, height = 500):
	root = Tk()
	canvas = Canvas(root, width = width, height = height)
	canvas.pack()
	root.mainloop()

run()
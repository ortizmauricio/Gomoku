from tkinter import *
import random

board =[]

class boardPlace:
	def __init__(self, x, y):
		self.x =0
		self.y = 0
		self.value = 0


def run(width = 500, height = 500):
	root = Tk()
	canvas = Canvas(root, width = width, height = height)
	canvas.pack()
	root.mainloop()

run()
from tkinter import *
import random

board =[]

class boardPlace:
	def __init__(self, x, y, canvas):
		self.x =0
		self.y = 0
		self.value = 0
		 
def createBoard(canvas):
	for row in range(19):
		for col in range(19):
			print(row, col)

def run(width = 500, height = 500):
	def createBoardWrapper(canvas):
		createBoard(canvas)

	root = Tk()
	canvas = Canvas(root, width = width, height = height)
	canvas.pack()

	createBoardWrapper(canvas)

	root.mainloop()

run()
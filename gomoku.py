from tkinter import *
import random

board =[]

class boardPlace:
	def __init__(self, x, y, canvas):
		self.x = x
		self.y = y
		self.value = 0
		self.visual = canvas.create_rectangle(self.x, self.y, self.x+30, self.y+30, fill = "grey", outline = "black", width = "1")
		 
def createBoard(canvas, x = 10, y = 40):
	for row in range(19):
		x = 10
		y+=30
		board.append([])
		for col in range(19):
			x+=30
			board[row].append(boardPlace(x, y, canvas))

def run(width = 650, height = 700):
	def createBoardWrapper(canvas):
		createBoard(canvas)
		canvas.update()

	root = Tk()
	canvas = Canvas(root, width = width, height = height)
	canvas.pack()

	createBoardWrapper(canvas)

	root.mainloop()

run()
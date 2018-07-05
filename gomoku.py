from tkinter import *
import random

board =[]

class Game:
	def __init__(self):
		self.player = 1
		self.width = 650
		self.height = 700

session = Game()


class boardPlace:
	def __init__(self, x, y, canvas):
		self.x = x
		self.y = y
		self.value = 0
		self.visual = canvas.create_rectangle(self.x, self.y, self.x+30, self.y+30, fill = "grey", outline = "black", width = "1")

def createBoard(canvas, x = ((session.width - 570)/2), y = 40):
	for row in range(19):
		x = 10
		y+=30
		board.append([])
		for col in range(19):
			x+=30
			board[row].append(boardPlace(x, y, canvas))

def run(width = session.width, height = session.height):
	def createBoardWrapper(canvas):
		createBoard(canvas)
		canvas.update()

	root = Tk()
	canvas = Canvas(root, width = width, height = height)
	canvas.pack()

	createBoardWrapper(canvas)

	root.mainloop()

run()
from tkinter import *
import random

board =[]

class Game:
	def __init__(self):
		self.play = True
		self.player = 1
		self.width = 650
		self.height = 700

session = Game()


class boardPlace:
	def __init__(self, x, y, canvas, index):
		self.x = x
		self.y = y
		self.value = 0
		self.index = index
		self.visual = canvas.create_rectangle(self.x, self.y, self.x + 30, self.y + 30, fill = "grey", outline = "black", width = "1")

		canvas.tag_bind(self.visual, '<Button-1>', lambda event: placePiece(event, self, canvas))

def placePiece(event, self, canvas):
	if session.play:
		if self.value == 0:
			if session.player == 1:
				session.player = 2
				self.value = 1
				self.mark = canvas.create_oval(self.x + 2, self.y + 2, self.x + 28, self.y + 28, fill = "red")
			else:
				session.player = 1
				self.value = 2
				self.mark = canvas.create_oval(self.x + 2, self.y + 2, self.x + 28, self.y + 28, fill = "blue")
			canvas.update()
			if checkWin(self.index, self.value):
				print("Player ", self.value, " wins!")
				session.play = False

def createBoard(canvas, x = ((session.width - 570)/2), y = 40):
	for row in range(19):
		x = 10
		y+=30
		board.append([])
		for col in range(19):
			x+=30
			board[row].append(boardPlace(x, y, canvas, (row, col)))

def checkWin(index, piece):
	#Check horizontal
	for i in range(4,-1,-1):
		occupied = 0
		for j in range(0,5):
			if index[1] - i + j>= 0 and index[1] - i + j < 19:
				if board[index[0]][index[1] - i + j].value == piece:
					occupied +=1
		if occupied == 5:
			return True

	#Check vertical
	for i in range(4,-1,-1):
		occupied = 0
		for j in range(0,5):
			if index[0] - i + j >= 0 and index[0] - i + j < 19:
				if board[index[0] - i + j][index[1]].value == piece:
					occupied +=1
		if occupied == 5:
			return True

	#Check right diagonal
	for i in range(4,-1,-1):
		occupied = 0
		for j in range(0,5):
			if index[0] - i + j >= 0 and index[0] - i + j < 19 and index[1] - i + j >= 0 and index[1] - i + j < 19:
				if board[index[0] - i + j][index[1] - i + j].value == piece:
					occupied +=1
		if occupied == 5:
			return True

	#Check left diagonal
	for i in range(4,-1,-1):
		occupied = 0
		for j in range(0,5):
			if index[0] - i + j >= 0 and index[0] - i + j < 19 and index[1] + i - j >= 0 and index[1] + i - j < 19:
				if board[index[0] - i + j][index[1] + i - j].value == piece:
					occupied +=1
		if occupied == 5:
			return True

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
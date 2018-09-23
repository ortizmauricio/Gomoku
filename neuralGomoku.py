#Program starts running at run() function
from tkinter import *
import random, math
random.seed()

#All board objects
board =[]

#Monomials from human and computer
computer_monomials = []
opponent_monomials = []


#Contains and controls variables important for game session
class Game:
	def __init__(self):
		self.play = True
		self.player = 1
		self.width = 670
		self.height = 700
		self.computerFirst = 0
		self.lastComputerPosition = 0
		self.title = 0
		self.humanFirst = True

	def hardReset(self):
		self.play = True
		self.player = 1
		self.width = 650
		self.height = 700
		self.computerFirst = 0
		self.lastComputerPosition = 0
		self.title = 0
		self.humanFirst = True	

session = Game()


class Monomial:
	def __init__(self):
		self.score = 1;
		self.boardPoints =[]
		self.isAlive = True

	def changePointValues(self):
		return
	def updateMonomial(self):
		return


#Board place object that calls place piece on click
class boardPlace:
	def __init__(self, x, y, canvas, index):
		self.x = x
		self.y = y
		self.index = index

		self.score = 0

		self.visual = canvas.create_rectangle(self.x, self.y, self.x + 30, self.y + 30, fill = "grey", outline = "grey", width = "1", activeoutline = "blue")

		canvas.tag_bind(self.visual, '<Button-1>', lambda event: placePiece(event, self, canvas))


def updateMonomials(index):
	if session.player == 1:
		for monomial in opponent_monomials:
			if monomial.isAlive:
				if index in monomial.boardPoints:
					monomial.score *= 2
					monomial.boardPoints.remove(index)

		for monomial in computer_monomials:
			if index in monomial.boardPoints:
				monomial.isAlive = False




def placePiece(event, self, canvas):
	if session.play:
		if session.player == 1:
			self.mark = canvas.create_oval(self.x + 2, self.y + 2, self.x + 28, self.y + 28, fill = "white")
			updateMonomials(self.index)
			for monomial in opponent_monomials:
				if len(monomial.boardPoints) == session.size:
					print(monomial.boardPoints)

			session.player = 2
			print(session.player)
		else:
			self.mark = canvas.create_oval(self.x + 2, self.y + 2, self.x + 28, self.y + 28, fill = "black")
			session.player = 1
			print(session.player)


	canvas.update()


#Initializes board place scores based on monomials
def setIntialBoardPlaceScores(board):
	for row in range(19):
		for col in range(19):
			for point in opponent_monomials:
				if board[row][col].index in point.boardPoints:
					board[row][col].score += 1

#Populates master_monomials with monomial objects
def createMasterMonomials(monomials):
	noDuplicates = []

	for monomial in monomials:
		if monomial not in noDuplicates:
			noDuplicates.append(monomial)

	for monomial in noDuplicates:
		tmpMonomial = Monomial()
		tmpMonomial2 = Monomial()
		tmpMonomial.boardPoints = monomial
		tmpMonomial2.boardPoints = monomial
		computer_monomials.append(tmpMonomial)
		opponent_monomials.append(tmpMonomial2)
	print(len(computer_monomials))
	print(len(opponent_monomials))


#Generates monomials for specified point (tuple)
def generateMonomials(index):
	monomials = []
	#Calculate horizontal monomials
	for i in range(4,-1,-1):
		tmpMonomial = []
		for j in range(0,5):
			if index[1] - i + j>= 0 and index[1] - i + j < 19:
				tmpMonomial.append((index[0],  index[1] - i + j))
		if len(tmpMonomial) == 5:
			monomials.append(tmpMonomial)

	#Calculate vertifcal monomials
	for i in range(4,-1,-1):
		tmpMonomial = []
		for j in range(0,5):
			if index[0] - i + j >= 0 and index[0] - i + j < 19:
				tmpMonomial.append((index[0] - i + j, index[1]))
		if len(tmpMonomial) == 5:
			monomials.append(tmpMonomial)

	#Calculate right diagonal monomials
	for i in range(4,-1,-1):
		tmpMonomial = []
		for j in range(0,5):
			if index[0] - i + j >= 0 and index[0] - i + j < 19 and index[1] - i + j >= 0 and index[1] - i + j < 19:
				tmpMonomial.append((index[0] - i + j,index[1] - i + j))
		if len(tmpMonomial) == 5:
			monomials.append(tmpMonomial)

	#Calculate left diagonal monomials
	for i in range(4,-1,-1):
		tmpMonomial = []
		for j in range(0,5):
			if index[0] - i + j >= 0 and index[0] - i + j < 19 and index[1] + i - j >= 0 and index[1] + i - j < 19:
				tmpMonomial.append((index[0] - i + j, index[1] + i - j))
		if len(tmpMonomial) == 5:
			monomials.append(tmpMonomial)

	return monomials
 

#Board is created, each board place is an object, default title is also placed
#Globoal variable is set to determine whether human or computer goes first
def createBoard(canvas, option, x = ((session.width - 570)/2), y = 40):
	session.humanFirst = option
	monomials =[]
	for row in range(19):
		x = 10
		y+=31

		board.append([])
		for col in range(19):
			x+=30

			monomials = generateMonomials((row, col)) + monomials

			#First layer creation
			board[row].append(boardPlace(x, y, canvas, (row, col)))
			x+=1
				
		canvas.create_line(55, y + 15, 615, y + 15,fill = "black", width = 1)

	x = 10
	for col in range(19):
		x+=31
		canvas.create_line(x + 15, 85, x + 15, 645, fill = "black", width = 1)
	session.title = canvas.create_text(session.width/2, 40, text="Gomoku", fill="white", font="Helvetica 40 bold ")

	createMasterMonomials(monomials)
	setIntialBoardPlaceScores(board)


#Resets all data structures storing data and the canvas
def resetData(canvas):
	canvas.delete(ALL)
	board.clear()
	computer_monomials.clear()
	opponent_monomials.clear()


'''
First function that runs, creates menu and calls function to create
the board, functions are called with different value depending on whether
a human or computer is starting the game first, this can be altered, by 
changing the game mode
'''
def run(width = session.width, height = session.height):
	def createBoardWrapper(canvas, first):
		session.hardReset()
		resetData(canvas)
		if first == 1:
			createBoard(canvas, True)
		else:
			createBoard(canvas, False)
		canvas.update()

	root = Tk()
	canvas = Canvas(root, width = width, height = height, background = "grey")
	canvas.pack()

	createBoardWrapper(canvas, 1)

	menubar = Menu(root)

	optionmenu = Menu(menubar, tearoff=0)
	optionmenu.add_command(label="Human First", command = lambda: createBoardWrapper(canvas, 1))
	optionmenu.add_command(label="Computer First", command = lambda: createBoardWrapper(canvas, 2) )
	optionmenu.add_command(label="Exit", command=root.quit)
	menubar.add_cascade(label="Options", menu=optionmenu)
	root.config(menu = menubar)
	root.mainloop()

run()
#Program starts running at run() function
from tkinter import *
import random, math
random.seed()

#All board objects
board =[]

#Monomials from human and computer
master_monomials = []


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

		#canvas.tag_bind(self.visual, '<Button-1>', lambda event: placePiece(event, self, canvas))


#Populates master_monomials with monomial objects
def createMasterMonomials(monomials):
	noDuplicates = []

	for monomial in monomials:
		if monomial not in noDuplicates:
			noDuplicates.append(monomial)

	for monomial in noDuplicates:
		tmpMonomial = Monomial()
		tmpMonomial.boardPoints = monomial
		master_monomials.append(tmpMonomial)


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


#Resets all data structures storing data and the canvas
def resetData(canvas):
	canvas.delete(ALL)
	board.clear()
	master_monomials.clear()


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
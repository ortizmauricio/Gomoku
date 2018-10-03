#Program starts running at run() function
from tkinter import *
import random, math, copy
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
		self.size = 5

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

	def kill(self):
		self.isAlive = False

	def increment(self):
		self.score *= 2
		if session.player == 1:
			for row in range(19):
				for col in range(19):
					if board[row][col].index in self.boardPoints:
						board[row][col].oppScoreIncrement(self.score)			
		else:
			for row in range(19):
				for col in range(19):
					if board[row][col].index in self.boardPoints:
						board[row][col].comScoreIncrement(self.score)
	
	def decrement(self):
		if session.player == 1:
			for row in range(19):
				for col in range(19):
					if board[row][col].index in self.boardPoints:
						board[row][col].comScoreDecrement(self.score)
		else:
			for row in range(19):
				for col in range(19):
					if board[row][col].index in self.boardPoints:
						board[row][col].oppScoreDecrement(self.score)

#Board place object that calls place piece on click
class boardPlace:
	def __init__(self, x, y, canvas, index):
		self.x = x
		self.y = y
		self.index = index
		self.occupied = False;
		self.comScore = 0
		self.oppScore = 0

		self.visual = canvas.create_rectangle(self.x, self.y, self.x + 30, self.y + 30, fill = "grey", outline = "grey", width = "1", activeoutline = "blue")

		canvas.tag_bind(self.visual, '<Button-1>', lambda event: placePiece(event, self, canvas))


	def oppScoreIncrement(self, score):
		self.oppScore += (score) - (score/2)

	def comScoreIncrement(self, score):
		self.comScore += (score) - (score/2)

	def oppScoreDecrement(self, score):
		self.oppScore -= score

	def comScoreDecrement(self, score):
		self.comScore -= score


def updateMonomials(index):
	if session.player == 1:
		print("Incrementing opponent and decrementing computer")
		for monomial in opponent_monomials:
			if monomial.isAlive:
				if index in monomial.boardPoints:
					monomial.boardPoints.remove(index)
					monomial.increment()
		for monomial in computer_monomials:
			if(len(monomial.boardPoints) < 5):
				print(monomial.boardPoints)
			if index in monomial.boardPoints:
				monomial.kill()
				monomial.decrement()
		session.size -=1
	else:
		print("Incrementing computer and decrementing opponent")
		for monomial in computer_monomials:
			if monomial.isAlive:
				if index in monomial.boardPoints:
					monomial.boardPoints.remove(index)
					monomial.increment()
		for monomial in opponent_monomials:
			if index in monomial.boardPoints:
				monomial.kill()
				monomial.decrement()


def openThree():
	urgentMonomials = []
	for monomial in opponent_monomials:
		if monomial.isAlive:
			if len(monomial.boardPoints) == 2:
				urgentMonomials.append(monomial)
	return urgentMonomials

def closedFour():
	urgentMonomials = []
	for monomial in opponent_monomials:
		if monomial.isAlive:
			if len(monomial.boardPoints) == 1:
				print("This closed four monomial is alive", monomial.boardPoints)
				urgentMonomials.append(monomial)
	return urgentMonomials

def firstLayerReflexive():
	urgentMonomials = []
	urgentMonomials = closedFour()

	if not urgentMonomials:
		print("We are checking for an open three")
		urgentMonomials = openThree()

	print("These are the urgent monomials ")
	for monomial in urgentMonomials:
		print(monomial.boardPoints, monomial.isAlive)
	return urgentMonomials	

def boardAnalysis():

	openThreeOrClosedFour = firstLayerReflexive()
	rankedPoints = []
	topScoring = []

	if not openThreeOrClosedFour:
		for monomial in computer_monomials:
			if monomial.isAlive == True:
				for point in monomial.boardPoints:
					if (board[point[0]][point[1]].comScore, point) not in rankedPoints:
						rankedPoints.append((board[point[0]][point[1]].comScore, point))
	else:
		for monomial in openThreeOrClosedFour:
			for point in monomial.boardPoints:
					if (board[point[0]][point[1]].oppScore, point) not in rankedPoints:
						rankedPoints.append((board[point[0]][point[1]].oppScore, point))
		print(rankedPoints)

	rankedPoints.sort(reverse = True)

	maxScore = rankedPoints[0][0]
	for point in rankedPoints:
		if point[0] == maxScore:
			topScoring.append(point)

	choice = random.randint(0, (len(topScoring) - 1))
	return topScoring[choice][1]

def computerNearOpponent(self):
	initialMoves = []
	for row in range(2):
		for col in range(2):
			if (self.index[0] + 1 - row) < 19 and (self.index[0] + 1 - row) >= 0  and (self.index[1] + 1 - col) < 19 and (self.index[1] + 1 - col) >= 0:
				if not self.index == (self.index[0] + 1 - row, self.index[1] + 1 - col):
					initialMoves.append((self.index[0] + 1 - row, self.index[1] + 1 - col))

	choice = random.randint(0, (len(initialMoves) - 1))
	print(initialMoves)
	return initialMoves[choice]

def computerInitialMove(canvas):
	session.player = 2
	calculatedPoint = boardAnalysis()
	print("The chosen point is ", calculatedPoint )
	event = 0
	placePiece(event, board[calculatedPoint[0]][calculatedPoint[1]], canvas)


def placePiece(event, self, canvas):
	if session.play:
		print("We entered the function")
		if session.player == 1 and self.occupied == False:
			self.mark = canvas.create_oval(self.x + 2, self.y + 2, self.x + 28, self.y + 28, fill = "white")
			self.occupied = True

			updateMonomials(self.index)
			print("Point placed at ", self.index)
			if checkWin(canvas):
				session.play = False
				return

			session.player = 2				
			if session.humanFirst:
				session.humanFirst = False
				calculatedPoint = computerNearOpponent(self)
			else:
				calculatedPoint = boardAnalysis()

			print("point is ", calculatedPoint)
			point = board[calculatedPoint[0]][calculatedPoint[1]]
			point.mark = canvas.create_oval(point.x + 2, point.y + 2, point.x + 28, point.y + 28, fill = "black")
			point.occupied = True
			updateMonomials(point.index)
			if checkWin(canvas):
				session.play = False
				return

			session.player = 1
		else:
			print("We entered this part of the function")
			self.mark = canvas.create_oval(self.x + 2, self.y + 2, self.x + 28, self.y + 28, fill = "black")
			self.occupied = True
			updateMonomials(self.index)
			session.player = 1
	canvas.update()


#Checks for win and displays message
def checkWin(canvas):
	win = False
	if session.player == 1:
		for monomial in opponent_monomials:
			if len(monomial.boardPoints) == 0:
				win = True
				break
	else:
		for monomial in computer_monomials:
			if len(monomial.boardPoints) == 0:
				win = True
				break

	if win:
		canvas.delete(session.title)
		if session.player == 1:
			session.title = canvas.create_text(session.width/2, 40, text="Human Wins!", fill="white", font="Helvetica 40 bold ")
		else:
			session.title = canvas.create_text(session.width/2, 40, text="Computer Wins!", fill="white", font="Helvetica 40 bold ")
	canvas.update()
	return win
#Initializes board place scores based on monomials
def setIntialBoardPlaceScores(board):
	for row in range(19):
		for col in range(19):
			for point in opponent_monomials:
				if board[row][col].index in point.boardPoints:
					board[row][col].comScore += 1
					board[row][col].oppScore += 1

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
		tmpMonomial2.boardPoints = copy.deepcopy(monomial)
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
			computerInitialMove(canvas)
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
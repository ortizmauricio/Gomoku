#Program starts running at run() function
from tkinter import *
import random, math, copy
random.seed()

#All board objects
board =[]

#Monomials from human and computer, accesible by original boardpoints
master_monomials = []
computer_monomials = []
opponent_monomials = []

#Moves in chronological order
moves = []

#Contains and controls variables important for game session
class Game:
	def __init__(self):
		self.play = True
		self.player = 1
		self.width = 670
		self.height = 700
		self.computerFirst = False
		self.lastComputerPosition = 0
		self.title = 0
		self.humanFirst = True
		self.humanTurn = True

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
		self.comScore = 1;
		self.oppScore = 1;

		self.originalPoints =[]
		self.comBoardPoints =[]
		self.oppBoardPoints =[]

		self.isComAlive = True
		self.isOppAlive = True

	def setPoints(self, points):
		self.originalPoints = copy.deepcopy(points)
		self.comBoardPoints = copy.deepcopy(points)
		self.oppBoardPoints = copy.deepcopy(points)

	def killCom(self):
		self.isComAlive = False

	def killOpp(self):
		self.isOppAlive = False

	def update(self, index):
		if session.humanTurn:
			self.oppScore *= 2
			self.killCom()
			self.oppBoardPoints.remove(index)
			self.comBoardPoints.remove(index)
			for point in self.oppBoardPoints:
				board[point[0]][point[1]].oppScoreIncrement(self.oppScore)
				board[point[0]][point[1]].comScoreDecrement(self.comScore)
		else:
			self.comScore *= 2
			self.killOpp()
			self.oppBoardPoints.remove(index)
			self.comBoardPoints.remove(index)
			for point in self.comBoardPoints:
				board[point[0]][point[1]].oppScoreDecrement(self.oppScore)
				board[point[0]][point[1]].comScoreIncrement(self.comScore)

		self.checkWin()


	def undo(self, index):
		if session.humanTurn:
			self.comScore /= 2
			for point in self.comBoardPoints:
				board[point[0]][point[1]].undoOppIncrement(self.oppScore)
				board[point[0]][point[1]].comScoreDecrement(self.comScore)
		else:
			self.oppScore /= 2
			for point in self.oppBoardPoints:
				board[point[0]][point[1]].oppScoreDecrement(self.oppScore)
				board[point[0]][point[1]].undoComIncrement(self.comScore)

		self.oppBoardPoints.append(index)
		self.comBoardPoints.append(index)

	def checkWin(self):
		if not self.comBoardPoints or not self.oppBoardPoints:
			if self.isOppAlive and not self.isComAlive:
				session.play = False
			elif self.isComAlive and not self.isOppAlive:
				session.play = False
			
#Board place object that calls place piece on click
class boardPlace:
	def __init__(self, x, y, canvas, mylist, index):
		self.x = x
		self.y = y
		self.index = index
		self.occupied = False;
		self.comScore = 0
		self.oppScore = 0
		self.monomials = []

		self.visual = canvas.create_rectangle(self.x, self.y, self.x + 30, self.y + 30, fill = "grey", outline = "grey", width = "1", activeoutline = "blue")

		canvas.tag_bind(self.visual, '<Button-1>', lambda event: self.placePiece(canvas, mylist))


	def oppScoreIncrement(self, score):
		self.oppScore += (score) - (score/2)

	def comScoreIncrement(self, score):
		self.comScore += (score) - (score/2)

	def oppScoreDecrement(self, score):
		self.oppScore -= score

	def comScoreDecrement(self, score):
		self.comScore -= score

	def undoOppIncrement(self, score):
		self.oppScore += score

	def undoComIncrement(self, score):
		self.comScore += score

	def alternatePlayer(self):
		if session.humanTurn:
			session.humanTurn = False
		else:
			session.humanTurn = True

	def updateMonomials(self):
		if session.humanTurn:
			print("Incrementing opponent and decrementing computer")
			for monomial in self.monomials:
				monomial.update(self.index)
		else:
			print("Incrementing computer and decrementing opponent")
			for monomial in self.monomials:
				monomial.update(self.index)

	def undoMonomial(self):
		for monomial in self.monomials:
			monomial.undo(self.index)

	def updateList(self, mylist):
		if session.humanTurn:
			message = "Human placed at " + str(self.index)
		else:
			message = "Computer placed at " + str(self.index)
		mylist.insert(END, message)
		moves.append(self.index)

	def placePiece(self, canvas, mylist):
		if session.play:
			if not self.occupied:
				if session.humanTurn:
					print("Oppenent placed point at ", self.index, " \n")
					self.mark = canvas.create_oval(self.x + 2, self.y + 2, self.x + 28, self.y + 28, fill = "white")
				else:
					print("Computer placed point at ", self.index, " \n")
					self.mark = canvas.create_oval(self.x + 2, self.y + 2, self.x + 28, self.y + 28, fill = "black")
			
			self.updateMonomials()
			self.updateList(mylist)
			if not session.play:
				changeTitle(canvas)

			self.alternatePlayer()
			self.occupied = True
			
			canvas.update()

			if not session.humanTurn and session.play:
				computerMove(self.index, canvas, mylist)

	def undo(self, canvas):
		canvas.delete(self.mark)
		canvas.update()
		self.occupied = False 
		self.undoMonomial()
		self.alternatePlayer()

#Check for open three scenarios, starts by prioiritizing open threes
#where all pieces are next to each other
def openThreeOffensive():
	urgentMonomials = []
	obviousWin = []
	for monomial in master_monomials:
		if monomial.isComAlive:
			if len(monomial.comBoardPoints) == 2:
				urgentMonomials.append(monomial)

	for monomial in urgentMonomials:
		print((monomial.comBoardPoints[1][0], monomial.comBoardPoints[0][0]))
		if monomial.comBoardPoints[1][0] - monomial.comBoardPoints[0][0] == 4 or monomial.comBoardPoints[1][1] - monomial.comBoardPoints[0][1] == 4:
			print(monomial.comBoardPoints, monomial.originalPoints, monomial.isOppAlive, monomial.isComAlive, " was appended to obvious win")
			obviousWin.append(monomial)

	if not obviousWin:
		return urgentMonomials
	else:
		return obviousWin

#Check one move away wins for computer
def openFourOffensive():
	urgentMonomials = []
	for monomial in master_monomials:
		if monomial.isComAlive:
			if len(monomial.comBoardPoints) == 1:
				urgentMonomials.append(monomial)
	return urgentMonomials

#Check for any open three scenario from opponent perspective
def openThree():
	urgentMonomials = []
	for monomial in master_monomials:
		if monomial.isOppAlive:
			if len(monomial.oppBoardPoints) <= 2:
				urgentMonomials.append(monomial)
	return urgentMonomials

#Check for closed four from opponent perspective
def closedFour():
	urgentMonomials = []
	for monomial in master_monomials:
		if monomial.isOppAlive:
			if len(monomial.oppBoardPoints) == 1:
				print("This closed four monomial is alive", monomial.oppBoardPoints, monomial.originalPoints)
				urgentMonomials.append(monomial)
	return urgentMonomials

def firstLayerReflexiveOffensive():
	urgentMonomials = []
	urgentMonomials = openFourOffensive()
	
	if not urgentMonomials:
		print("We are checking for an offensive open three")
		urgentMonomials = openThreeOffensive()

	print("These are the urgent monomials offensive ")
	for monomial in urgentMonomials:
		print(monomial.comBoardPoints, monomial.isComAlive)
	return urgentMonomials	


def firstLayerReflexive():
	urgentMonomials = []
	urgentMonomials = closedFour()
	
	if not urgentMonomials:
		print("We are checking for an open three")
		urgentMonomials = openThree()

	print("These are the urgent monomials defensive ")
	for monomial in urgentMonomials:
		print(monomial.oppBoardPoints, monomial.isOppAlive)
	return urgentMonomials	

def boardAnalysis():
	openThreeOrOpenFourOffensive = firstLayerReflexiveOffensive()
	openThreeOrClosedFour = firstLayerReflexive()
	rankedPoints = []
	topScoring = []

	if openThreeOrOpenFourOffensive:
		for monomial in openThreeOrOpenFourOffensive:
			for point in monomial.comBoardPoints:
					if (board[point[0]][point[1]].comScore, point) not in rankedPoints:
						rankedPoints.append((board[point[0]][point[1]].oppScore, point))
	elif not openThreeOrClosedFour:
		for monomial in master_monomials:
			if monomial.isComAlive:
				for point in monomial.comBoardPoints:
					if (board[point[0]][point[1]].comScore, point) not in rankedPoints:
						rankedPoints.append((board[point[0]][point[1]].comScore, point))
	else:
		for monomial in openThreeOrClosedFour:
			for point in monomial.oppBoardPoints:
					if (board[point[0]][point[1]].oppScore, point) not in rankedPoints:
						rankedPoints.append((board[point[0]][point[1]].oppScore, point))

	print("The length of ranked points is ", len(rankedPoints))
	rankedPoints.sort(reverse = True)

	maxScore = rankedPoints[0][0]
	for point in rankedPoints:
		if point[0] == maxScore:
			topScoring.append(point)

	choice = random.randint(0, (len(topScoring) - 1))
	print("Top scoring choice is ", topScoring[choice][1])
	return topScoring[choice][1]


def computerMove(index, canvas, mylist):
	if session.play:
		if session.humanFirst:
			session.humanFirst = False
			calculatedPoint = computerNearOpponent(index)
		else:
			calculatedPoint = boardAnalysis()

		row = calculatedPoint[0]
		col = calculatedPoint[1]
		board[row][col].placePiece(canvas, mylist)


def computerNearOpponent(index):
	initialMoves = []
	for row in range(2):
		for col in range(2):
			if (index[0] + 1 - row) < 19 and (index[0] + 1 - row) >= 0  and (index[1] + 1 - col) < 19 and (index[1] + 1 - col) >= 0:
				if not index == (index[0] + 1 - row, index[1] + 1 - col):
					initialMoves.append((index[0] + 1 - row, index[1] + 1 - col))

	choice = random.randint(0, (len(initialMoves) - 1))
	print(initialMoves)
	return initialMoves[choice]

def computerInitialMove(canvas, mylist):
	session.player = 2
	calculatedPoint = boardAnalysis()
	print("The chosen point is ", calculatedPoint )
	event = 0
	placePiece(event, board[calculatedPoint[0]][calculatedPoint[1]], canvas, mylist)


#Initializes board place scores based on monomials
def setIntialBoardPlaceScores(board):
	for row in range(19):
		for col in range(19):
			for monomial in master_monomials:
				if board[row][col].index in monomial.originalPoints:
					board[row][col].comScore += 1
					board[row][col].oppScore += 1
					board[row][col].monomials.append(monomial)

#Populates master_monomials with monomial objects
def createMasterMonomials(monomials):
	noDuplicates = []

	for monomial in monomials:
		if monomial not in noDuplicates:
			noDuplicates.append(monomial)

	for monomial in noDuplicates:
		tmpMonomial = Monomial()
		tmpMonomial.setPoints(copy.deepcopy(monomial))
		master_monomials.append(tmpMonomial)

	print(len(master_monomials))
	
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
def createBoard(canvas, mylist, option, x = ((session.width - 570 )/2), y = 40):
	session.humanFirst = option

	if not session.humanFirst:
		session.computerFirst = True
		session.humanTurn = False
	monomials =[]

	for row in range(19):
		x = 10
		y+=31

		board.append([])
		for col in range(19):
			x+=30

			monomials = generateMonomials((row, col)) + monomials

			#First layer creation
			board[row].append(boardPlace(x, y, canvas, mylist, (row, col)))
			x+=1
				
		canvas.create_line(55, y + 15, 615, y + 15,fill = "black", width = 1)

	x = 10
	for col in range(19):
		x+=31
		canvas.create_line(x + 15, 85, x + 15, 645, fill = "black", width = 1)
	session.title = canvas.create_text(session.width/2, 40, text="Gomoku", fill="white", font="Helvetica 40 bold ")
	createMasterMonomials(monomials)
	setIntialBoardPlaceScores(board)

#Undo previous move
def undo(canvas,mylist):
	if session.play:
		if moves:
			lastPosition = moves[-1]
			moves.pop()
			message = "Undo: " + str(lastPosition)
			mylist.insert(END, message)
			board[lastPosition[0]][lastPosition[1]].undo(canvas)

			if not moves and not session.computerFirst:
				session.humanFirst = True
			elif not moves and session.computerFirst:
				computerMove((0,0), canvas, mylist)
	else:
		session.play = True
		resetTitle(canvas)

def resetTitle(canvas):
	canvas.delete(session.title)
	session.title = canvas.create_text(session.width/2, 40, text="Gomoku", fill="white", font="Helvetica 40 bold ")
	canvas.update()

def changeTitle(canvas):
	canvas.delete(session.title)
	if session.humanTurn:
		session.title = canvas.create_text(session.width/2, 40, text="Human Wins!", fill="white", font="Helvetica 40 bold ")
	else:
		session.title = canvas.create_text(session.width/2, 40, text="Computer Wins!", fill="white", font="Helvetica 40 bold ")


#Resets all data structures storing data and the canvas
def resetData(canvas, mylist):
	canvas.delete(ALL)
	mylist.delete(0, END)
	board.clear()
	master_monomials.clear()


'''
First function that runs, creates menu and calls function to create
the board, functions are called with different value depending on whether
a human or computer is starting the game first, this can be altered, by 
changing the game mode
'''
def run(width = session.width, height = session.height):
	def createBoardWrapper(canvas, mylist, first):
		session.hardReset()
		resetData(canvas, mylist)
		if first == 1:
			createBoard(canvas, mylist, True)
		else:
			createBoard(canvas, mylist, False)
			computerMove((0,0), canvas, mylist)
		canvas.update()

	root = Tk()
	scrollbar = Scrollbar(root)
	scrollbar.pack( side = LEFT, fill = Y )

	mylist = Listbox(root, yscrollcommand = scrollbar.set )
	
	mylist.pack( side = LEFT, fill = BOTH )
	scrollbar.config( command = mylist.yview )

	canvas = Canvas(root, width = width, height = height, background = "grey")
	canvas.pack()


	createBoardWrapper(canvas, mylist, 1)

	button = Button(root,text = "Undo", command =  lambda: undo(canvas, mylist))
	button1 = Button(root,text = "Computer", command =  lambda: computerMove((0,0), canvas, mylist))
	button.pack()
	button1.pack()


	menubar = Menu(root)

	optionmenu = Menu(menubar, tearoff=0)
	optionmenu.add_command(label="Human First", command = lambda: createBoardWrapper(canvas, mylist, 1))
	optionmenu.add_command(label="Computer First", command = lambda: createBoardWrapper(canvas, mylist, 2) )
	optionmenu.add_command(label="Exit", command=root.quit)
	menubar.add_cascade(label="Options", menu=optionmenu)
	root.config(menu = menubar)
	root.mainloop()

run()
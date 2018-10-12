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
		self.computerFirst = 0
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
		self.boardPoints =[]

		self.isComAlive = True
		self.isOppAlive = True

	def update(self, index):
		if session.humanTurn:
			if self.isOppAlive:
				self.oppScore *= 2
				self.isComAlive = False
				self.boardPoints.remove(index)
				for point in self.boardPoints:
					board[point[0]][point[1]].oppScoreIncrement(self.oppScore)
					board[point[0]][point[1]].comScoreDecrement(self.comScore)

				
		else:
			if self.isComAlive:
				self.comScore *= 2
				self.isOppAlive = False
				self.boardPoints.remove(index)
				for point in self.boardPoints:
					board[point[0]][point[1]].oppScoreDecrement(self.oppScore)
					board[point[0]][point[1]].comScoreIncrement(self.comcore)

				

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

		canvas.tag_bind(self.visual, '<Button-1>', lambda event: self.placePiece(canvas))


	def oppScoreIncrement(self, score):
		self.oppScore += (score) - (score/2)

	def comScoreIncrement(self, score):
		self.comScore += (score) - (score/2)

	def oppScoreDecrement(self, score):
		self.oppScore -= score

	def comScoreDecrement(self, score):
		self.comScore -= score

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


	def placePiece(self, canvas):
		if session.play:
			if not self.occupied:
				if session.humanTurn:
					self.mark = canvas.create_oval(self.x + 2, self.y + 2, self.x + 28, self.y + 28, fill = "white")
				else:
					self.mark = canvas.create_oval(self.x + 2, self.y + 2, self.x + 28, self.y + 28, fill = "black")
			
			self.updateMonomials()
			self.alternatePlayer()
			self.occupied = True
			canvas.update()


			for row in range(19):
				for col in range(19):
					print(board[row][col].index)
					print( "   oppScore: ", board[row][col].oppScore, " comScore", board[row][col].comScore)

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


def openThreeOffensive():
	urgentMonomials = []
	obviousWin = []
	for monomial in computer_monomials:
		if monomial.isAlive:
			if len(monomial.boardPoints) == 2:
				urgentMonomials.append(monomial)

	for monomial in urgentMonomials:
		print((monomial.boardPoints[1][0], monomial.boardPoints[0][0]))
		if monomial.boardPoints[1][0] - monomial.boardPoints[0][0] == 4 or monomial.boardPoints[1][1] - monomial.boardPoints[0][1] == 4:
			print(monomial.boardPoints, "was appended to obvious win")
			obviousWin.append(monomial)

	if not obviousWin:
		return urgentMonomials
	else:
		return obviousWin

def openFourOffensive():
	urgentMonomials = []
	for monomial in computer_monomials:
		if monomial.isAlive:
			if len(monomial.boardPoints) == 1:
				urgentMonomials.append(monomial)
	return urgentMonomials

def openThree():
	urgentMonomials = []
	for monomial in opponent_monomials:
		if monomial.isAlive:
			if len(monomial.boardPoints) <= 2:
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

def firstLayerReflexiveOffensive():
	urgentMonomials = []
	urgentMonomials = openFourOffensive()
	
	if not urgentMonomials:
		print("We are checking for an offensive open three")
		urgentMonomials = openThreeOffensive()

	print("These are the urgent monomials ")
	for monomial in urgentMonomials:
		print(monomial.boardPoints, monomial.isAlive)
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
	openThreeOrOpenFourOffensive = firstLayerReflexiveOffensive()
	openThreeOrClosedFour = firstLayerReflexive()
	rankedPoints = []
	topScoring = []

	if openThreeOrOpenFourOffensive:
		for monomial in openThreeOrOpenFourOffensive:
			for point in monomial.boardPoints:
					if (board[point[0]][point[1]].comScore, point) not in rankedPoints:
						rankedPoints.append((board[point[0]][point[1]].oppScore, point))
	elif not openThreeOrClosedFour:
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

def computerInitialMove(canvas, mylist):
	session.player = 2
	calculatedPoint = boardAnalysis()
	print("The chosen point is ", calculatedPoint )
	event = 0
	placePiece(event, board[calculatedPoint[0]][calculatedPoint[1]], canvas, mylist)


def placePiece(event, self, canvas, mylist):
	if session.play:
		print("We entered the function")






		if session.player == 1 and self.occupied == False:
			self.mark = canvas.create_oval(self.x + 2, self.y + 2, self.x + 28, self.y + 28, fill = "white")
			self.occupied = True

			updateMonomials(self.index)
			print("Point placed at ", self.index)
			moves.append((self.index, session.player))
			updateList(session.player, mylist, moves[len(moves) - 1][0])
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
			moves.append((calculatedPoint, session.player))
			updateList(session.player, mylist, moves[len(moves) - 1][0])
			if checkWin(canvas):
				session.play = False
				return
			
			session.player = 1
		else:
			print("We entered this part of the function")
			self.mark = canvas.create_oval(self.x + 2, self.y + 2, self.x + 28, self.y + 28, fill = "black")
			self.occupied = True
			updateMonomials(self.index)
			moves.append((self.index, session.player))
			updateList(session.player, mylist, moves[len(moves) - 1][0])
			session.player = 1
	canvas.update()
	mylist.update()

def updateList(player, mylist, index):
	if player == 1:
		message = "Opponent: " + str(index)
		
	else:
		message = "Computer: " + str(index)
	mylist.insert(END, message)


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
			for monomial in master_monomials:
				if board[row][col].index in monomial.boardPoints:
					board[row][col].comScore += 1
					board[row][col].oppScore += 1
					board[row][col].monomials.append(monomial)

	for row in range(19):
				for col in range(19):
					print(board[row][col].index)
					print( "   oppScore: ", board[row][col].oppScore, " comScore", board[row][col].comScore)
#Populates master_monomials with monomial objects
def createMasterMonomials(monomials):
	noDuplicates = []

	for monomial in monomials:
		if monomial not in noDuplicates:
			noDuplicates.append(monomial)

	for monomial in noDuplicates:
		tmpMonomial = Monomial()
		tmpMonomial.boardPoints = copy.deepcopy(monomial)
		tmpMonomial.originalPoints = copy.deepcopy(monomial)
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
def createBoard(canvas, mylist, option, x = ((session.width - 570 )/2), y = 40):
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
	pass

		


#Resets all data structures storing data and the canvas
def resetData(canvas, mylist):
	canvas.delete(ALL)
	mylist.delete(0, END)
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
	def createBoardWrapper(canvas, mylist, first):
		session.hardReset()
		resetData(canvas, mylist)
		if first == 1:
			createBoard(canvas, mylist, True)
		else:
			createBoard(canvas, mylist, False)
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
	button.pack()

	menubar = Menu(root)

	optionmenu = Menu(menubar, tearoff=0)
	optionmenu.add_command(label="Human First", command = lambda: createBoardWrapper(canvas, mylist, 1))
	optionmenu.add_command(label="Computer First", command = lambda: createBoardWrapper(canvas, mylist, 2) )
	optionmenu.add_command(label="Exit", command=root.quit)
	menubar.add_cascade(label="Options", menu=optionmenu)
	root.config(menu = menubar)
	root.mainloop()

run()
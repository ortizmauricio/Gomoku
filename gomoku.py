#Program starts running at run() function
from tkinter import *
import random, math
random.seed()

#All board objects
board =[]

#Monomials from human and computer
master_monomials = []

#Stores computer board places and their current score
point_rank = {}

#Contains computer places along with their overall score and completion score
ranked_points = []

#All pieces placed by computer
placedPieces = []
topMonomials = []

#Stores human board places and their current score
opponent_rank = {}

#Contains computer places along with their overall score and completion score
opponent_points = []
opponentPieces = []

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

#Board place object that calls place piece on click
class boardPlace:
	def __init__(self, x, y, canvas, index):
		self.x = x
		self.y = y
		self.value = 0
		self.index = index
		self.visual = canvas.create_rectangle(self.x, self.y, self.x + 30, self.y + 30, fill = "grey", outline = "grey", width = "1", activeoutline = "blue")

		canvas.tag_bind(self.visual, '<Button-1>', lambda event: placePiece(event, self, canvas))

#Places piece on the board and carries out decision making
#for computer piece placing
def placePiece(event, self, canvas):
	#If someone hasn't won already
	if session.play:
		#If the computer is set to go first
		if not session.humanFirst:
			session.humanFirst = True
			session.player = 2
			shortest = (9,9)
			placePiece(event, board[shortest[0]][shortest[1]], canvas)
			session.lastComputerPosition = shortest
			placedPieces.append(session.lastComputerPosition)
			generateMonomials(session.lastComputerPosition)
			rankPoints()
		#If board place is empty
		elif self.value == 0:
			#If it's human turn, visually places piece, 
			#sets session values for opponent, generates move
			#for computer
			if session.player == 1:
				session.player = 2
				if session.humanFirst:
					self.value = 1
					self.mark = canvas.create_oval(self.x + 2, self.y + 2, self.x + 28, self.y + 28, fill = "white")
					generateMonomials(self.index)
					rankPoints()
					#Checks if someone has won and displays winning message
					if checkWin(self.index, self.value):
						canvas.delete(session.title)
						if self.value == 2:
							session.title = canvas.create_text(session.width/2, 40, text="Computer Wins!", fill="white", font="Helvetica 40 bold ")
						else:
							session.title = canvas.create_text(session.width/2, 40, text="Human Wins!", fill="white", font="Helvetica 40 bold ")
						session.play = False

				#Computer's turn
				if session.computerFirst == 0:
					session.computerFirst = 1

					#Calculate point that is closest to the center from generated monomials
					if session.humanFirst:
						shortestDistance = math.sqrt(math.pow((self.index[0]-9),2) + math.pow(self.index[1] - 9,2))
						shortest = self.index
						tmpShortest = []
						if shortest == (9,9) or board[9][9].value != 0:
							shortest = (9,8)
						for m in master_monomials:
							for p in m:
								if p == self.index or p==(9,9):
									continue
								tmpShort = math.sqrt(math.pow((p[1]-9),2) + math.pow((p[0] - 9),2))
									
								if tmpShort < shortestDistance:
									shortest = p
								elif tmpShort == shortestDistance:
									if p not in tmpShortest:
										tmpShortest.append(p)

					else:
						shortest = (9,9)
					#Chooses random point if there are several with the same distance from (9,9)
					
					if len(tmpShortest) != 0:
						while True:
							short = random.randint(0, (len(tmpShortest)-1))
							shortest = tmpShortest[short]
							if board[shortest[0]][shortest[1]].value == 0:
								break
					
					#Piece is placed, stored for future reference
					#Generates monomials for placed piece and ranks monomials
					# or next move
					print(shortest)
					placePiece(event, board[shortest[0]][shortest[1]], canvas)
					session.lastComputerPosition = shortest
					placedPieces.append(session.lastComputerPosition)
					generateMonomials(session.lastComputerPosition)
					rankPoints()

				elif session.play:

					#Go by distance

					#Check if I have open three or open four
					#Prioritize completition
					
					#Prioritize adjacency by calculating distance
					#from previous point to top scoring points
					#and altering score 
					topScore = ranked_points[0][0]
					tmpTop = []

					for i in ranked_points:
						if i[0] == topScore:
							tmpTop.append(i)
					for i in tmpTop:
						distance = math.sqrt(math.pow((session.lastComputerPosition[0]-i[1][0]),2) + math.pow((session.lastComputerPosition[1] - i[1][1]),2))
						i[0]+=(4 - distance)
					tmpTop.sort(reverse = True)
			
					#Check on opponent to block move if necessary
					oppTop = []
					for m in opponent_points:
				
						if m[2] >= 12:
							oppTop.append(m)
					#If opponnent has no advantage or one move away from winning
					if len(oppTop) == 0 or point_rank[tmpTop[0][1]][1]>=78:
						nextPiece = tmpTop[0][1]
					else:
						for p in oppTop:
							print(p)
							if p[1] in point_rank:
								print(point_rank[p[1]][0])
								p[0]+=point_rank[p[1]][0]
						oppTop.sort(reverse = True)
						nextPiece = oppTop[0][1]
					print("oppTop")
					print(oppTop)
					print("tmpTop")
					print(tmpTop)

					#Piece is placed, stored for future reference
					#Generates monomials for placed piece and ranks monomials
					# or next move
					print(nextPiece)
					placePiece(event, board[nextPiece[0]][nextPiece[1]], canvas )
					session.lastComputerPosition = nextPiece

					placedPieces.append(session.lastComputerPosition)

					generateMonomials(session.lastComputerPosition)
					rankPoints()
					print("Ranked Points")
					print(ranked_points)
					print("opponent_points")
					print(opponent_points)
					
			else:
				#Visually places piece, sets session values for opponent
				session.player = 1
				self.value = 2
				self.mark = canvas.create_oval(self.x + 2, self.y + 2, self.x + 28, self.y + 28, fill = "black")
			canvas.update()
			#Checks if someone has won and displays winning message
			if checkWin(self.index, self.value):
				canvas.delete(session.title)
				if self.value == 2:
					session.title = canvas.create_text(session.width/2, 40, text="Computer Wins!", fill="white", font="Helvetica 40 bold ")
				else:
					session.title = canvas.create_text(session.width/2, 40, text="Human Wins!", fill="white", font="Helvetica 40 bold ")
				session.play = False
			canvas.update()

#Board is created, each board place is an object, default title is also placed
#Globoal variable is set to determine whether human or computer goes first
def createBoard(canvas, option, x = ((session.width - 570)/2), y = 40):
	session.humanFirst = option
	for row in range(19):
		x = 10
		y+=31

		board.append([])
		for col in range(19):
			x+=30
			board[row].append(boardPlace(x, y, canvas, (row, col)))
			x+=1
				
		canvas.create_line(55, y + 15, 615, y + 15,fill = "black", width = 1)

	x = 10
	for col in range(19):
		x+=31
		canvas.create_line(x + 15, 85, x + 15, 645, fill = "black", width = 1)
	session.title = canvas.create_text(session.width/2, 40, text="Gomoku", fill="white", font="Helvetica 40 bold ")

#Checks is a winning monomial has been created
#Called from placePiece
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

#Generates monomials for specified point (tuple)
def generateMonomials(index):

	#Calculate horizontal monomials
	for i in range(4,-1,-1):
		tmpMonomial = []
		for j in range(0,5):
			if index[1] - i + j>= 0 and index[1] - i + j < 19:
				tmpMonomial.append((index[0],  index[1] - i + j))
		if len(tmpMonomial) == 5:
			master_monomials.append(tmpMonomial)

	#Calculate vertifcal monomials
	for i in range(4,-1,-1):
		tmpMonomial = []
		for j in range(0,5):
			if index[0] - i + j >= 0 and index[0] - i + j < 19:
				tmpMonomial.append((index[0] - i + j, index[1]))
		if len(tmpMonomial) == 5:
			master_monomials.append(tmpMonomial)

	#Calculate right diagonal monomials
	for i in range(4,-1,-1):
		tmpMonomial = []
		for j in range(0,5):
			if index[0] - i + j >= 0 and index[0] - i + j < 19 and index[1] - i + j >= 0 and index[1] - i + j < 19:
				tmpMonomial.append((index[0] - i + j,index[1] - i + j))
		if len(tmpMonomial) == 5:
			master_monomials.append(tmpMonomial)

	#Calculate left diagonal monomials
	for i in range(4,-1,-1):
		tmpMonomial = []
		for j in range(0,5):
			if index[0] - i + j >= 0 and index[0] - i + j < 19 and index[1] + i - j >= 0 and index[1] + i - j < 19:
				tmpMonomial.append((index[0] - i + j, index[1] + i - j))
		if len(tmpMonomial) == 5:
			master_monomials.append(tmpMonomial)

'''
Helper function for rankPoints
Determines whether a monomial is alive 
based on whether any opposing pieces are present
within
'''
def monomialDead(m, v):
	for p in m:
		if board[p[0]][p[1]].value == v:
			return True
	return False

'''
Helper function for rankPoints
Determines the completion score of monomial,
score increases at a larger rate depending on
how many pieces are complete within the monomial
'''
def completionScore(m, v):
	score = 1
	
	for p in m:
		if board[p[0]][p[1]].value == v:
			score+=score
	return (score - 2) 

'''
This function calculates the points for the computer
and human monomials, from master_monomial list. Values
are then transferred from dictionary to seperate lists and
sorted for further use in placePiece
'''
def rankPoints():

	#Clear list to update all monomials
	point_rank.clear()
	opponent_rank.clear()
	#Go through all monomials for recalculation
	for m in master_monomials:

		#Check that monomial is not dead
		if not monomialDead(m, 1):
			#Calculate completion score and add it to corresponding
			#areas of dictionary
			completion = completionScore(m, 2)
			for p in m:
				if board[p[0]][p[1]].value == 0:
					
					if p not in point_rank:
						point_rank[p] = [1, 0]
					else:
						point_rank[p][0]+=1
					point_rank[p][0]+=completion
					point_rank[p][1]+=completion

		if not monomialDead(m, 2):
			completion = completionScore(m, 1)
			for p in m:
				if board[p[0]][p[1]].value == 0:
					
					if p not in opponent_rank:
						opponent_rank[p] = [1, 0]
					else:
						opponent_rank[p][0]+=1
					opponent_rank[p][0]+=completion
					opponent_rank[p][1]+=completion
	

	#Add to list for sorting
	ranked_points.clear()
	opponent_points.clear()

	for key in point_rank:
		ranked_points.append([point_rank[key][0], key, point_rank[key][1]])

	for key in opponent_rank:
		opponent_points.append([opponent_rank[key][0], key, opponent_rank[key][1]])

	#Sort from greatest to least
	ranked_points.sort(reverse = True)
	opponent_points.sort(reverse = True)

#Resets all data structures storing data and the canvas
def resetData(canvas):
	canvas.delete(ALL)
	board.clear()
	master_monomials.clear()
	point_rank.clear()
	ranked_points.clear()
	placedPieces.clear()
	topMonomials.clear()

	opponent_rank.clear()
	opponent_points.clear()
	opponentPieces.clear()

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
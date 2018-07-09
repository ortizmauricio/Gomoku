from tkinter import *
import random, math

board =[]
master_monomials = []
point_rank = {}
ranked_points = []
placedPieces = []
topMonomials = []

opponent_rank = {}
opponent_points = []
opponentPieces = []

class Game:
	def __init__(self):
		self.play = True
		self.player = 1
		self.width = 650
		self.height = 700
		self.computerFirst = 0
		self.lastComputerPosition = 0
		self.title = 0

session = Game()


class boardPlace:
	def __init__(self, x, y, canvas, index):
		self.x = x
		self.y = y
		self.value = 0
		self.index = index
		self.visual = canvas.create_rectangle(self.x, self.y, self.x + 30, self.y + 30, fill = "grey", outline = "grey", width = "1")

		canvas.tag_bind(self.visual, '<Button-1>', lambda event: placePiece(event, self, canvas))

def placePiece(event, self, canvas):
	if session.play:
		if self.value == 0:
			if session.player == 1:
				session.player = 2
				self.value = 1
				self.mark = canvas.create_oval(self.x + 2, self.y + 2, self.x + 28, self.y + 28, fill = "white")
				generateMonomials(self.index)
				rankPoints()
				#Computer's turn
				if checkWin(self.index, self.value):
					canvas.delete(session.title)
					if self.value == 2:
						session.title = canvas.create_text(session.width/2, 40, text="Computer Wins!", fill="white", font="Helvetica 40 bold ")
					else:
						session.title = canvas.create_text(session.width/2, 40, text="Human Wins!", fill="white", font="Helvetica 40 bold ")
					session.play = False

				if session.computerFirst == 0:
					session.computerFirst = 1

					#Calculate point that is closest to the center from generated monomials
					print("Initial starting point")
					print(master_monomials)
					shortestDistance = math.sqrt(math.pow((self.index[0]-9),2) + math.pow(self.index[1] - 9,2))
					shortest = self.index
					for m in master_monomials:
						for p in m:
							tmpShort = math.sqrt(math.pow((p[1]-9),2) + math.pow((p[0] - 9),2))
								
							if tmpShort < shortestDistance:
								shortest = p
								
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
				session.player = 1
				self.value = 2
				self.mark = canvas.create_oval(self.x + 2, self.y + 2, self.x + 28, self.y + 28, fill = "black")
			canvas.update()
			if checkWin(self.index, self.value):
				canvas.delete(session.title)
				if self.value == 2:
					session.title = canvas.create_text(session.width/2, 40, text="Computer Wins!", fill="white", font="Helvetica 40 bold ")
				else:
					session.title = canvas.create_text(session.width/2, 40, text="Human Wins!", fill="white", font="Helvetica 40 bold ")
				session.play = False
			canvas.update()

def createBoard(canvas, x = ((session.width - 570)/2), y = 40):
	for row in range(19):
		x = 10
		y+=30

		board.append([])
		for col in range(19):
			x+=30
			board[row].append(boardPlace(x, y, canvas, (row, col)))
				
		canvas.create_line(55, y + 15, 595, y + 15,fill = "black", width = 1)

	x = 10
	for col in range(19):
		x+=30
		canvas.create_line(x + 15, 85, x + 15, 626, fill = "black", width = 1)
	session.title = canvas.create_text(session.width/2, 40, text="Gomoku", fill="white", font="Helvetica 40 bold ")

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

def monomialDead(m, v):
	for p in m:
		if board[p[0]][p[1]].value == v:
			return True
	return False

def completionScore(m, v):
	score = 1
	
	for p in m:
		if board[p[0]][p[1]].value == v:
			score+=score
	return (score - 2) 

def rankPoints():

	#Clear list to update all monomials
	point_rank.clear()
	opponent_rank.clear()
	#Go through all monomials for recalculation
	for m in master_monomials:

		#Check that monomial is not dead
		if not monomialDead(m, 1):
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

	ranked_points.sort(reverse = True)
	opponent_points.sort(reverse = True)

	
def run(width = session.width, height = session.height):
	def createBoardWrapper(canvas):
		createBoard(canvas)
		canvas.update()

	root = Tk()
	canvas = Canvas(root, width = width, height = height, background = "grey")
	canvas.pack()

	createBoardWrapper(canvas)

	root.mainloop()

run()
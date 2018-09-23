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



#Board place object that calls place piece on click
class boardPlace:
	def __init__(self, x, y, canvas, index):
		self.x = x
		self.y = y
		self.value = 0
		self.index = index
		self.visual = canvas.create_rectangle(self.x, self.y, self.x + 30, self.y + 30, fill = "grey", outline = "grey", width = "1", activeoutline = "blue")

		#canvas.tag_bind(self.visual, '<Button-1>', lambda event: placePiece(event, self, canvas))

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
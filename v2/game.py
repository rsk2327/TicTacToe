
from agents import *
from string import *
from random import *
import util

grid3List=[[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]


grid3CheckList=[[[1,2],[3,6],[4,8]],
				[[0,2],[4,7]],
				[[0,1],[5,8],[4,6]],
				[[4,5],[0,6]],
				[[3,5],[1,7],[0,8],[2,6]],
				[[3,4],[2,8]],
				[[7,8],[0,3],[2,4]],
				[[6,8],[1,4]],
				[[6,7],[2,5],[0,4]]]

grid4List2 = [[0,1,2,3],[4,5,6,7],[8,9,10,11],[12,13,14,15],
			 [0,4,8,12],[1,5,9,13],[2,6,10,14],[3,7,11,15],
			 [0,5,10,15],[3,6,9,12]]

grid4List = [[0,1,2,3],[4,5,6,7],[8,9,10,11],[12,13,14,15],
			 [0,4,8,12],[1,5,9,13],[2,6,10,14],[3,7,11,15],
			 [0,5,10,15],[3,6,9,12]]

grid4CheckList=[]

def run4list():

	for i in range(16):
		checkList=[]

		for j in grid4List2:
			if i in j:
				k = j
				k.remove(i)
				checkList.append(k)

		grid4CheckList.append(checkList)
		checkList=[]

	return

class Game():

	def __init__(self,gridSize=3):

		print "gridSize :" + str(gridSize)
		self.player1 = RandomAction(gridSize)
		self.player2 = ApproxQLearningAgent(gridSize) #the type of agent that you are training
		self.gridSize = gridSize
		self.valuesEntered=0
		self.isActive=True
		self.verbose=0

		run4list()
		

		self.player1Wins=0
		self.player2Wins=0


		self.gridValues=[]
		for i in range(self.gridSize**2):
			self.gridValues.append('-')

		self.currentPlayer=1


	def gameWon(self):
		"""Returns whether the game has been won or the game has ended in a draw"""

		if self.gridSize==3:

			for i in range(len(grid3List)):
				checkList = grid3List[i]
				val1,val2,val3 = self.gridValues[checkList[0]],self.gridValues[checkList[1]],self.gridValues[checkList[2]]
				if (val1==val2 and val2==val3 and val1!="-"):
					self.isActive=False		
					return "W"

			if self.valuesEntered==self.gridSize**2:
				self.isActive=False
				return "D"
			else:
				return "L"
		elif self.gridSize==4:

			for i in range(len(grid4List)):
				checkList = grid4List[i]
				
				val1,val2,val3,val4 = self.gridValues[checkList[0]],self.gridValues[checkList[1]],self.gridValues[checkList[2]],self.gridValues[checkList[3]]
				if (val1==val2 and val2==val3 and val3==val4 and val1!="-"):
					self.isActive=False		
					return "W"

			if self.valuesEntered==self.gridSize**2:
				self.isActive=False
				return "D"
			else:
				return "L"


	def gameReset(self):
		""" Resets the game to original state """

		self.valuesEntered=0
		self.isActive=True
		self.currentPlayer=1
		for i in range(self.gridSize**2):
			self.gridValues[i]='-'

		self.player2.previousState=""
		self.player2.previousAction=-1

		return None

	def prettyPrint(self,state):
		""" Prints the current state in an easy to understand form
			Useful while debugging"""

		for i in range(self.gridSize):
			print(state[i*self.gridSize:(i+1)*self.gridSize])

		return None


	def train(self):
		""" Runs one iteration of a tic-tac-toe game"""

		
		while self.isActive==True:

			state = "".join(self.gridValues)
			player1Action = self.player1.getAction(state)
			self.gridValues[player1Action]="X"
			self.valuesEntered+=1
			newState = "".join(self.gridValues)
			winner=0   #winner = 0 means match was a draw

			if self.verbose==1:
				print "action player 1 : " + str(player1Action)
				self.prettyPrint(newState)
				print "***************"
			if self.gameWon()=="W":
				self.player1Wins+=1
				self.player1.update("W",newState,100)
				self.player2.update("L",state,-150)
				winner=1
			elif self.gameWon()=="D":
				self.player1.update("D",newState,60)
				self.player2.update("D",state,60)
			else:

				self.player2.update("C",state,30)

				state = newState
				player2Action = self.player2.getAction(state)
				self.gridValues[player2Action]="O"
				self.valuesEntered+=1
				newState = "".join(self.gridValues)

				if self.verbose==1:
					print "action player 2 : " + str(player2Action)
					self.prettyPrint(newState)
					print "***************"

				if self.gameWon()=="W":
					self.player2Wins+=1
					self.player1.update("L",state,-150)
					self.player2.update("W",newState,100)
					winner=2
				elif self.gameWon()=="D":
					self.player1.update("D",state,60)
					self.player2.update("D",newState,60)
				else:
					self.player1.update("C",state,30)

		self.gameReset()

		return winner





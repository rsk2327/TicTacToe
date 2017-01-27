
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


class Game():

	def __init__(self,gridSize=3):

		self.player1 = RandomAction(3)
		self.player2 = QLearningAgent(3)
		self.gridSize = gridSize
		self.valuesEntered=0
		self.isActive=True

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


	def gameReset(self):
		""" Resets the game to original state """

		self.valuesEntered=0
		self.isActive=True
		self.currentPlayer=1
		for i in range(self.gridSize**2):
			self.gridValues[i]='-'


		return None

	


	def train(self):

		while self.isActive==True:

			state = "".join(self.gridValues)
			player1Action = self.player1.getAction(state)
			self.gridValues[player1Action]="X"
			self.valuesEntered+=1
			newState = "".join(self.gridValues)
			winner=0   #winner = 0 means match was a draw

			if self.gameWon()=="W":
				self.player1Wins+=1
				self.player1.update("W",newState,100)
				self.player2.update("L",state,-150)
				winner=1
			elif self.gameWon()=="D":
				self.player1.update("D",newState,60)
				self.player2.update("D",state,60)
			else:

				self.player1.update("C",newState,30)

				state = newState
				player2Action = self.player2.getAction(state)
				self.gridValues[player2Action]="0"
				self.valuesEntered+=1
				newState = "".join(self.gridValues)

				if self.gameWon()=="W":
					self.player2Wins+=1
					self.player1.update("L",state,-150)
					self.player2.update("W",newState,100)
					winner=2
				elif self.gameWon()=="D":
					self.player1.update("D",state,60)
					self.player2.update("D",newState,60)
				else:
					self.player2.update("C",newState,30)

		self.gameReset()

		return winner





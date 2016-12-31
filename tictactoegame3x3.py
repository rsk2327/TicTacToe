
from random import *
import util
from string import *

grid3List=[[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]

class tictactoe():
	""" Base class """

	def __init__(self,gridSize=3):

		self.gridSize=gridSize
		self.valuesEntered=0
		self.isActive=True

		self.gridValues=[]
		for i in range(self.gridSize**2):
			self.gridValues.append('-')



		self.currentPlayer = 1





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
				return "C"


	def gameReset(self):
		""" Resets the game to original state """

		self.valuesEntered=0
		self.isActive=True
		self.currentPlayer=1
		for i in range(self.gridSize**2):
			self.gridValues[i]='-'

		return None

	def getAvailableActions(self,state):

		if self.isActive==True:
			possibleActions=[]

			for i in range(self.gridSize**2):
				if self.gridValues[i]=='-':
					possibleActions.append(i)
			return possibleActions
		else:
			return []


class RandomAction(tictactoe):

	def __init__(self,gridSize=3):
		tictactoe.__init__(self,gridSize)

		


	def takeAction(self):

		possibleActions = self.getAvailableActions()
		randomAction = randint(0,len(possibleActions)-1)

		return possibleActions[randomAction]


class QLearningAgent(tictactoe):

	def __init__(self,gridSize=3):
		tictactoe.__init__(self,gridSize)
		self.qvalues = util.Counter()
		self.epsilon = 0.1
		self.discount = 0.1
		self.alpha =0.01

		self.previousState=""
		self.previousAction=-1

		self.play1Wins=0
		self.play2Wins=0


	def getQValue(self,state,action):

		if self.qvalues.has_key((state,action))==True:
			return self.qvalues[(state,action)]
		else:
			return -999.0

	def computeValueFromQValues(self,state):

		possibleActions = self.getAvailableActions(state)

		if possibleActions==[]:
			return 0.0
		else:
			maxVal=-9999
			maxAction=""

			for action in possibleActions:
				if self.qvalues[(state,action)]>maxVal:
					maxVal = self.qvalues[(state,action)]
					maxAction = maxAction

			return maxVal

	def computeActionFromQValues(self,state):

		possibleActions = self.getAvailableActions(state)

		if possibleActions==[]:
			return None
		else:
			maxVal=-999
			maxAction=""

			for action in possibleActions:
				# if self.qvalues.has_key((state,action))==False:
					# continue

				if self.qvalues[(state,action)]>maxVal:
					maxVal = self.qvalues[(state,action)]
					maxAction = action

			return maxAction


	def getAction(self,state):

		legalActions = self.getAvailableActions(state)
		action=None

		if legalActions==[]:
			return None



		chooseRandomAction = util.flipCoin(self.epsilon)

		if chooseRandomAction == True:
			
			action = choice(legalActions)
		else:
			
			action = self.computeActionFromQValues(state)

		#updating previousAction
		self.previousAction=action 
		self.previousState = "".join(self.gridValues)
		
		return action 

	def update(self,state,action,nextState,reward):

		new_value =(1-self.alpha)*self.qvalues[(state,action)] + self.alpha*( reward + self.discount*self.computeValueFromQValues(nextState) )

		self.qvalues[(state,action)] = new_value

		return None

	def getPolicy(self,state):
		return self.computeActionFromQValues(state)

	def getValue(self,state):
		return self.computeValueFromQValues(state)
        
	def train(self,numIterations=10):

		for i in range(numIterations):
			while self.isActive==True:
				possibleActions = self.getAvailableActions([])
				player1Action = randint(0,len(possibleActions)-1)
				
				self.gridValues[player1Action]="X"
				self.valuesEntered+=1
				nextState = "".join(self.gridValues)

				if self.gameWon()=="W":
					self.play1Wins+=1
					self.update(self.previousState , self.previousAction, nextState,-100)

				elif self.gameWon()=="D":
					self.update(self.previousState, self.previousAction, nextState, 50)
				else:

					state = "".join(self.gridValues)
					action = self.getAction(state)

					self.gridValues[action]="O"
					self.valuesEntered+=1
					nextState = "".join(self.gridValues)

					if self.gameWon()=="W":
						self.update(state,action,nextState,100)
						self.play2Wins+=1
					elif self.gameWon()=="D":
						self.update(state,action,nextState,30)
					else:
						continue
			self.gameReset()

		print "After "+str(numIterations)+" rounds of training... "
		print "Player 1 wins : "+ str(self.play1Wins)
		print "Player 2 wins : "+ str(self.play2Wins)

		print "Player 2 win ratio : "+ str(float(self.play2Wins)/(float(self.play2Wins)+float(self.play1Wins)))
		

		self.play1Wins=0
		self.play2Wins=0



		# print self.qvalues

		return None


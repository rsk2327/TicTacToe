from random import *
import util
from string import *

class RandomAction():

	def __init__(self,gridSize=3):
		# tictactoe.__init__(self,gridSize)
		self.gridSize = gridSize
		
	def finishingMove(self,state):

		moves=[]

		for i in range(9):
			for action in grid3CheckList[i]:
				val1,val2 = action[0],action[1]
				if state[val1]==state[val2] and state[val1]=="X":
					moves.append(i)
					break

		if len(moves)>1:
			return choice(moves)
		elif len(moves)==1:
			return moves[0]
		else:
			return None

	def update(self,result,nextState,reward):
		return None

	def getAvailableActions(self,state):
		possibleActions=[]

		for i in range(self.gridSize**2):
			if state[i]=='-':
				possibleActions.append(i)
		return possibleActions
		

	def getAction(self,state):

		possibleActions = self.getAvailableActions(state)
		randomAction = randint(0,len(possibleActions)-1)

		return possibleActions[randomAction]





class QLearningAgent():

	def __init__(self,gridSize=3):
		# tictactoe.__init__(self,gridSize)
		self.gridSize=3
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
		self.previousState = state
		
		return action 
		
	def getAvailableActions(self,state):
		possibleActions=[]

		for i in range(self.gridSize**2):
			if state[i]=='-':
				possibleActions.append(i)
		return possibleActions

	def update(self,result,nextState,reward):

		if result == "W":
			state = self.previousState
			action = self.previousAction
			new_value =(1-self.alpha)*self.qvalues[(state,action)] + self.alpha*( reward + self.discount*self.computeValueFromQValues(nextState) )
			self.qvalues[(state,action)] = new_value
		elif result =="L":
			state = self.previousState
			action = self.previousAction
			new_value =(1-self.alpha)*self.qvalues[(state,action)] + self.alpha*( reward + self.discount*self.computeValueFromQValues(nextState) )
			self.qvalues[(state,action)] = new_value
		elif result == "D":
			state = self.previousState
			action = self.previousAction
			new_value =(1-self.alpha)*self.qvalues[(state,action)] + self.alpha*( reward + self.discount*self.computeValueFromQValues(nextState) )
			self.qvalues[(state,action)] = new_value
		else:
			state = self.previousState
			action = self.previousAction
			new_value =(1-self.alpha)*self.qvalues[(state,action)] + self.alpha*( reward + self.discount*self.computeValueFromQValues(nextState) )
			self.qvalues[(state,action)] = new_value


		return None

	def getPolicy(self,state):
		return self.computeActionFromQValues(state)

	def getValue(self,state):
		return self.computeValueFromQValues(state)

	def gameReset2(self):
		self.gameReset()

		self.previousAction=-1
		self.previousState=""
		self.rival.previousAction=-1
		self.rival.previousState=""
from random import *
from util import *
from string import *

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


grid4List = [[0,1,2,3],[4,5,6,7],[8,9,10,11],[12,13,14,15],
			 [0,4,8,12],[1,5,9,13],[2,6,10,14],[3,7,11,15],
			 [0,5,10,15],[3,6,9,12]]

grid4CheckList=[]

def run4list():

	for i in range(16):
		checkList=[]

		for j in grid4List:
			if i in j:
				k = j
				k.remove(i)
				checkList.append(k)

		grid4CheckList.append(checkList)
		checkList=[]

	return



class RandomAction():

	def __init__(self,gridSize=3):
		# tictactoe.__init__(self,gridSize)
		self.gridSize = gridSize
		run4list()
		
	def finishingMove(self,state):

		moves=[]

		for i in range(9):
			for action in grid3CheckList[i]:
				val1,val2 = action[0],action[1]
				if state[val1]==state[val2] and state[val1]=="X" and state[i]=="-":
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

		# if self.finishingMove(state)!=None:
		# 	return self.finishingMove(state)

		return choice(possibleActions)
		

class RandomAction2(RandomAction):

	def __init__(self,gridSize=3):
		RandomAction.__init__(self,gridSize)

	def getAction(self,state):
		possibleActions = self.getAvailableActions(state)
		randomAction = randint(0,len(possibleActions)-1)

		if self.finishingMove(state)!=None:
			return self.finishingMove(state)

		return choice(possibleActions)



class QLearningAgent():

	def __init__(self,gridSize=3):
		# tictactoe.__init__(self,gridSize)
		self.gridSize=gridSize
		
		self.qvalues = Counter()
		self.epsilon = 0.1
		self.discount = 0.1
		self.alpha =0.01

		run4list()
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



		chooseRandomAction = flipCoin(self.epsilon)

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





class QLearningAgent2():

	def __init__(self,gridSize=3):
		# tictactoe.__init__(self,gridSize)
		self.gridSize=gridSize
	
		self.qvalues = Counter()
		self.epsilon = 0.1
		self.discount = 0.1
		self.alpha =0.01
		run4list()

		self.previousState=""
		self.previousAction=-1

		self.playedStates=[]

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

		chooseRandomAction = flipCoin(self.epsilon)

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

		

		if result in ( "W","D","L"):
			state = self.previousState
			action = self.previousAction
			new_value =(1-self.alpha)*self.qvalues[(state,action)] + self.alpha*( reward + self.discount*self.computeValueFromQValues(nextState) )
			self.qvalues[(state,action)] = new_value

			for i in range(len(self.playedStates)):
				# print "------"
				# print "Step : "+str(i)
				# prettyPrint(self.playedStates[i][0])
				# print "Action : " + str(self.playedStates[i][1])
				# prettyPrint(self.playedStates[i][2])
				# print "------"
				totalSize= len(self.playedStates)
				state,action,nextState = self.playedStates[totalSize-i-1]
				self.qvalues[(state,action)] = self.qvalues[(state,action)] + 0.5**i*reward*self.alpha

			self.playedStates=[]
		elif result =="C":

			state = self.previousState
			action = self.previousAction
			new_value =(1-self.alpha)*self.qvalues[(state,action)] + self.alpha*( reward + self.discount*self.computeValueFromQValues(nextState) )
			self.qvalues[(state,action)] = new_value
			self.playedStates.append((state,action,nextState))

		# elif result == "D":
		# 	state = self.previousState
		# 	action = self.previousAction
		# 	new_value =(1-self.alpha)*self.qvalues[(state,action)] + self.alpha*( reward + self.discount*self.computeValueFromQValues(nextState) )
		# 	self.qvalues[(state,action)] = new_value
		# else:
		# 	state = self.previousState
		# 	action = self.previousAction
		# 	new_value =(1-self.alpha)*self.qvalues[(state,action)] + self.alpha*( reward + self.discount*self.computeValueFromQValues(nextState) )
		# 	self.qvalues[(state,action)] = new_value


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



def prettyPrint(state):
	print state[0:4]
	print state[4:8]
	print state[8:12]
	print state[12:16]

from random import *
import util
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
				if state[i]=='-':
					possibleActions.append(i)
			return possibleActions
		else:
			return []


class RandomAction(tictactoe):

	def __init__(self,gridSize=3):
		tictactoe.__init__(self,gridSize)

		
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

	def takeAction(self,state):

		possibleActions = self.getAvailableActions(state)
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

	def gameReset2(self):
		self.gameReset()

		self.previousAction=-1
		self.previousState=""
		self.rival.previousAction=-1
		self.rival.previousState=""

      

	def train(self,numIterations=10,agent="Random"):

		#initializing opponent
		self.rival = QLearningAgent(3)

		for i in range(numIterations):
			if agent=="Random":
				while self.isActive==True:
					state = "".join(self.gridValues)

					randomRival = RandomAction(3)
					
					player1Action = randomRival.takeAction(state)
					
					nextState = "".join(self.gridValues) #positioning of this line here or after line 197 matters
					self.gridValues[player1Action]="X"
					self.valuesEntered+=1
					

					if self.gameWon()=="W":
						self.play1Wins+=1
						self.update(self.previousState , self.previousAction, nextState,-150)

					elif self.gameWon()=="D":
						self.update(self.previousState, self.previousAction, nextState, 60)
					else:
						self.update(self.previousState, self.previousAction, nextState, 30) #living reward

						state = "".join(self.gridValues)
						action = self.getAction(state)

						self.gridValues[action]="O"
						self.valuesEntered+=1
						nextState = "".join(self.gridValues)

						if self.gameWon()=="W":
							self.update(state,action,nextState,100)
							self.play2Wins+=1
						elif self.gameWon()=="D":
							self.update(state,action,nextState,60)
						else:
							continue
				self.gameReset2()
			elif agent=="Random2":
				while self.isActive==True:
					state = "".join(self.gridValues)

					randomRival = RandomAction(3)
					player1Action = randomRival.takeAction(state)

					finishingMove = randomRival.finishingMove(state)
					if finishingMove!=None:
						player1Action = finishingMove
					
					nextState = "".join(self.gridValues) #positioning of this line here or after line 197 matters
					self.gridValues[player1Action]="X"
					self.valuesEntered+=1
					

					if self.gameWon()=="W":
						self.play1Wins+=1
						self.update(self.previousState , self.previousAction, nextState,-150)

					elif self.gameWon()=="D":
						self.update(self.previousState, self.previousAction, nextState, 60)
					else:
						self.update(self.previousState, self.previousAction, nextState, 30) #living reward

						state = "".join(self.gridValues)
						action = self.getAction(state)

						self.gridValues[action]="O"
						self.valuesEntered+=1
						nextState = "".join(self.gridValues)

						if self.gameWon()=="W":
							self.update(state,action,nextState,100)
							self.play2Wins+=1
						elif self.gameWon()=="D":
							self.update(state,action,nextState,60)
						else:
							continue
				self.gameReset2()

			else:
				while self.isActive==True:
					# print "reached"
					rivalState = "".join(self.gridValues)
					rivalAction = self.rival.getAction(rivalState)
					# print "rivalState :"
					# prettyPrint(rivalState)
					# print rivalAction

					nextState = "".join(self.gridValues)
					self.gridValues[rivalAction]="X"
					self.valuesEntered+=1
					rivalNextState = "".join(self.gridValues)

					# print "new rival state:"
					# prettyPrint(rivalNextState)
					# print "xxxxxxxxxxxxxxxxxxxxxxxx"

					if self.gameWon()=="W":
						#rival wins

						self.rival.update(rivalState,rivalAction,rivalNextState,100)
						self.update(self.previousState,self.previousAction,nextState,-150)
						self.play1Wins+=1
					elif self.gameWon()=="D":
						self.rival.update(rivalState,rivalAction,rivalNextState,60)
						self.update(self.previousState,self.previousAction,nextState,60)
					else:
						#players turn

						self.update(self.previousState, self.previousAction, nextState, 30) #living reward

						state = "".join(self.gridValues)
						action = self.getAction(state)
						# print "player2 turn"
						# print "player2 state:"
						# prettyPrint(state)
						# print action
						

						self.gridValues[action]="O"
						self.valuesEntered+=1
						nextState = "".join(self.gridValues)
						# print "player 2 new state"
						# prettyPrint(nextState)
						# print "_________________"
						if self.gameWon()=="W":
							self.update(state,action,nextState,100)
							self.play2Wins+=1
							self.rival.update(self.rival.previousState, self.previousAction,state,-150)
						elif self.gameWon()=="D":
							self.update(state,action,nextState,60)
							self.rival.update(self.rival.previousState, self.previousAction,state,60)
						else:
							self.rival.update(self.rival.previousState, self.previousAction,state,30) #living reward for rival
				self.gameReset2()





		print "After "+str(numIterations)+" rounds of training... "
		print "Player 1 wins : "+ str(self.play1Wins)
		print "Player 2 wins : "+ str(self.play2Wins)

		if self.play2Wins!=0:
			print "Player 2 win ratio : "+ str(float(self.play2Wins)/(float(self.play2Wins)+float(self.play1Wins)))
		

		self.play1Wins=0
		self.play2Wins=0



		# print self.qvalues

		return None


def prettyPrint(state):
	print state[0:3]
	print state[3:6]
	print state[6:9]
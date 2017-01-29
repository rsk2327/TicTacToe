try:
	import wx
except ImportError:
	raise ImportError, "The wxPython module is required to run this program"


from string import *
from game import *
from agents import *
import os 
import pickle

class tictactoeFrame(wx.Frame):

	def __init__(self,parent,title):
		super(tictactoeFrame,self).__init__(parent,title=title)

		self.game = Game(3)
		self.player1Wins=0
		self.player2Wins=0

		self.InitUI(3)
		self.Centre()
		self.Show()

	def InitUI(self,gridsize):

		panel = wx.Panel(self)
		self.gridSize=gridsize

		vbox = wx.BoxSizer(wx.VERTICAL)

		gameBox = wx.GridBagSizer(hgap=1,vgap=1)
		ctrlBox = wx.GridBagSizer(hgap=5,vgap=5)
		dispBox = wx.GridBagSizer(hgap=5,vgap=5)

		#ctrlBox widgets
		nextButton = wx.Button(panel,label="Next")
		nextButton.Bind(wx.EVT_BUTTON,self.nextButtonClick)
		resetButton = wx.Button(panel,label="Reset")	
		resetButton.Bind(wx.EVT_BUTTON,self.resetButtonClick)
		ctrlBox.Add(nextButton,(0,0),flag=wx.EXPAND)
		ctrlBox.Add(resetButton,(0,1),flag=wx.EXPAND)
		ctrlBox.AddGrowableCol(0)
		ctrlBox.AddGrowableCol(1)


	
		#gameBox widgets
		self.gameButtons=[]

		for i in range(self.gridSize):
			for j in range(self.gridSize):
				button = wx.Button(panel,(i*self.gridSize+j),label="-",name = str(i)+str(j),size=(160,160))
				button.Bind(wx.EVT_BUTTON,self.buttonClick)
				self.gameButtons.append(button)
				gameBox.Add(button,(i,j),(1,1),flag=wx.EXPAND,border=4)
			gameBox.AddGrowableCol(i)
			gameBox.AddGrowableRow(i)

		#dispBox widgets
		self.dispText = wx.StaticText(panel,-1,label="Player 1 turn",style=wx.CENTER)
		l1=wx.StaticLine(panel,-1,style=wx.LI_HORIZONTAL)
		l2=wx.StaticLine(panel,-1,style=wx.LI_HORIZONTAL)

		self.player1Stat = wx.StaticText(panel,-1,label="Player 1 : 0 ",style=wx.CENTER)
		self.player2Stat = wx.StaticText(panel,-1,label="Player 2 : 0 ",style=wx.RIGHT)

		#Save details
		self.saveFileName = wx.TextCtrl(panel,-1,value="Enter save file name",style = wx.CENTER|wx.EXPAND)
		saveButton = wx.Button(panel,label="Save",style=wx.CENTER|wx.EXPAND)
		saveButton.Bind(wx.EVT_BUTTON,self.saveButtonClick)
		loadButton = wx.Button(panel,label="Load",style=wx.CENTER|wx.EXPAND)
		loadButton.Bind(wx.EVT_BUTTON,self.loadButtonClick)

		#Train details
		trainLabel = wx.StaticText(panel,-1,label="TRAIN",style=wx.CENTER|wx.EXPAND)
		numIterLabel = wx.StaticText(panel,-1,label="No. of Iterations :",style=wx.LEFT)
		discountLabel = wx.StaticText(panel,-1,label="Discount :",style=wx.LEFT)
		alphaLabel = wx.StaticText(panel,-1,label="Alpha :",style=wx.LEFT)
		epsilonLabel = wx.StaticText(panel,-1,label="Epsilon :",style=wx.LEFT)
		# verboseLabel  = wx.StaticText(panel,-1,label="Label :",style=wx.LEFT)

		self.numIterEntry = wx.TextCtrl(panel,-1,value="1",style=wx.CENTER|wx.EXPAND)
		self.discountEntry = wx.TextCtrl(panel,-1,value="0.01",style=wx.CENTER|wx.EXPAND)
		self.alphaEntry = wx.TextCtrl(panel,-1,value="0.001",style=wx.CENTER|wx.EXPAND)
		self.epsilonEntry = wx.TextCtrl(panel,-1,value="0.6",style=wx.CENTER|wx.EXPAND)
		self.debugCheckbox = wx.CheckBox(panel,-1,label="Debug",style=wx.LEFT)

		trainOptions=["Random","Random2","QLearningAgent"]
		self.trainOptionBox = wx.ComboBox(panel,value="Random",choices=trainOptions,style = wx.CB_READONLY|wx.EXPAND)
		trainButton = wx.Button(panel,label="Train",style=wx.EXPAND|wx.CENTER)		
		trainButton.Bind(wx.EVT_BUTTON, self.trainButtonClick)


		#Adding widgets
		dispBox.Add(l1,(0,0),(1,4),flag=wx.EXPAND)
		dispBox.Add(self.dispText,(1,0),(2,2),flag=wx.EXPAND|wx.ALL|wx.ALIGN_CENTER)
		dispBox.Add(self.player1Stat,(1,2),(1,2),flag=wx.EXPAND|wx.ALL|wx.ALIGN_CENTER)
		dispBox.Add(self.player2Stat,(2,2),(1,2),flag=wx.EXPAND|wx.ALL|wx.ALIGN_CENTER)
		
		dispBox.Add(self.saveFileName,(4,0),(1,2),flag=wx.EXPAND|wx.ALL|wx.ALIGN_CENTER)
		dispBox.Add(saveButton,(4,2),(1,1),flag=wx.EXPAND|wx.ALL|wx.ALIGN_CENTER)
		dispBox.Add(loadButton,(4,3),(1,1),flag=wx.EXPAND|wx.ALL|wx.ALIGN_CENTER)
		dispBox.Add(l2,(5,0),(1,4),flag=wx.EXPAND)

		dispBox.Add(trainLabel,(6,0),(1,4),flag=wx.EXPAND|wx.CENTER)

		dispBox.Add(numIterLabel,(7,0),(1,1),flag=wx.EXPAND|wx.LEFT)
		dispBox.Add(self.numIterEntry,(7,1),(1,3),flag=wx.EXPAND|wx.CENTER)

		dispBox.Add(discountLabel,(8,0),(1,1),flag=wx.EXPAND|wx.LEFT)
		dispBox.Add(self.discountEntry,(8,1),(1,3),flag=wx.EXPAND|wx.CENTER)

		dispBox.Add(alphaLabel,(9,0),(1,1),flag=wx.EXPAND|wx.LEFT)
		dispBox.Add(self.alphaEntry,(9,1),(1,3),flag=wx.EXPAND|wx.CENTER)

		dispBox.Add(epsilonLabel,(10,0),(1,1),flag=wx.EXPAND|wx.LEFT)
		dispBox.Add(self.epsilonEntry,(10,1),(1,3),flag=wx.EXPAND|wx.CENTER)

		dispBox.Add(self.debugCheckbox,(11,3),(1,1),flag = wx.CENTER|wx.EXPAND)

		dispBox.Add(self.trainOptionBox,(12,1),(1,2),flag = wx.CENTER|wx.EXPAND)
		dispBox.Add(trainButton,(12,3),(1,1),flag = wx.CENTER|wx.EXPAND)




		dispBox.AddGrowableCol(0)
		dispBox.AddGrowableCol(1)
		dispBox.AddGrowableCol(2)
		dispBox.AddGrowableCol(3)




		vbox.Add(gameBox,4,wx.EXPAND|wx.ALL,5)
		vbox.Add(ctrlBox,0,wx.EXPAND|wx.ALL,5)
		vbox.Add(dispBox,0,flag=wx.EXPAND|wx.CENTER|wx.ALL,border=15)

		panel.SetSizer(vbox)
		vbox.Fit(self)



	def buttonClick(self,event):
		print "id is "+str(event.GetId())
		id = event.GetId()

		if event.GetEventObject().GetLabel()=="-" and self.game.isActive==True:
			if self.game.currentPlayer==1:
				event.GetEventObject().SetLabel("X")
				self.game.gridValues[id]="X"
				self.game.valuesEntered+=1
				
				if self.game.gameWon()=="W":
					self.dispText.SetLabel("Player 1 won")
					self.player1Wins+=1
					self.player1Stat.SetLabel("Player 1 : "+str(self.player1Wins))
				elif self.game.gameWon()=="D":
					self.dispText.SetLabel("Match Drawn")
				else:
					self.game.currentPlayer = self.changePlayer(self.game.currentPlayer)
					self.dispText.SetLabel("Player 2 turn")
			else:
				event.GetEventObject().SetLabel("O")
				self.game.gridValues[id]="O"
				self.game.valuesEntered+=1

				if self.game.gameWon()=="W":
					self.dispText.SetLabel("Player 2 won")
					self.player2Wins+=1
					self.player2Stat.SetLabel("Player 2 : "+str(self.player2Wins))
				elif self.game.gameWon()=="D":
					self.dispText.SetLabel("Match Drawn")
				else:
					self.game.currentPlayer = self.changePlayer(self.game.currentPlayer)
					self.dispText.SetLabel("Player 1 turn")
		else:
			print "invalid action"
			event.Skip()
	
	def trainButtonClick(self,event):

		numIter = int(self.numIterEntry.GetValue())
		alpha = float(self.alphaEntry.GetValue())
		discount = float(self.discountEntry.GetValue())
		epsilon = float(self.epsilonEntry.GetValue())

		if self.debugCheckbox.GetValue()==True and numIter<=5:
			self.game.verbose=1
		else:
			self.game.verbose=0

		self.game.player2.discount = discount
		self.game.player2.epsilon = epsilon
		trainOption = self.trainOptionBox.GetValue()

		if trainOption == "Random":
			self.game.player1 = RandomAction()
		elif trainOption == "Random2":
			self.game.player1 = RandomAction2()
		elif trainOption == "QLearningAgent":
			self.game.player1 = QLearningAgent()

		player1Wins=0
		player2Wins=0

		for i in range(numIter):
			winner=self.game.train()

			if winner==1:
				player1Wins+=1
			elif winner==2:
				player2Wins+=1

		print "After "+str(numIter)+" rounds of training... "
		print "Player 1 wins : "+ str(player1Wins)
		print "Player 2 wins : "+ str(player2Wins)

		if player2Wins!=0:
			print "Player 2 win ratio : "+ str(float(player2Wins)/(float(player2Wins)+float(player1Wins)))

		print len(self.game.player2.qvalues)

		return None


	def nextButtonClick(self,event):

		self.game.gameReset()
		for i in range(self.gridSize**2):
			self.gameButtons[i].SetLabel('-')
		self.dispText.SetLabel("Player 1 turn")

		return None

	def resetButtonClick(self,event):
		
		self.nextButtonClick(event)
		self.player1Wins=0
		self.player2Wins=0
		self.player1Stat.SetLabel("Player 1 : 0")
		self.player2Stat.SetLabel("Player 2 : 0")

		return None

	def loadButtonClick(self,event):
		filename = self.saveFileName.GetValue()
		qvalues = pickle.load(open(filename,"rb"))
		self.saveFileName.SetValue("")
		self.game.player2.qvalues = qvalues
		print qvalues

	def saveButtonClick(self,event):
		filename = self.saveFileName.GetValue()

		if self.game.player2.__class__.__name__=="ApproxQLearningAgent":
			pickle.dump(self.game.player2.weights,open(filename,"wb"))
		else:
			pickle.dump(self.game.player2.qvalues,open(filename,"wb"))

		print "File saved at "+os.getcwd()
		return None

	def changePlayer(self,player):
		if player==1:
			return 2
		else:
			return 1



class tictactoeFrameRandom(tictactoeFrame):

	def __init__(self,parent,title):
		tictactoeFrame.__init__(self,parent,title)

		self.game = RandomAction(3)

	def buttonClick(self,event):
		print "id is "+str(event.GetId())
		id = event.GetId()

		if event.GetEventObject().GetLabel()=="-" and self.game.isActive==True:
			if self.game.currentPlayer==1:
				event.GetEventObject().SetLabel("X")
				self.game.gridValues[id]="X"
				self.game.valuesEntered+=1
				
				if self.game.gameWon()=="W":
					self.dispText.SetLabel("Player 1 won")
					self.player1Wins+=1
					self.player1Stat.SetLabel("Player 1 : "+str(self.player1Wins))
				elif self.game.gameWon()=="D":
					self.dispText.SetLabel("Match Drawn")
				else:
					self.game.currentPlayer = self.changePlayer(self.game.currentPlayer)
					self.dispText.SetLabel("Player 2 turn")

					#player 2 takes action now
					action = self.game.takeAction()
					self.gameButtons[action].SetLabel("O")
					self.game.gridValues[action]="O"
					self.game.valuesEntered+=1

					if self.game.gameWon()=="W":
						self.dispText.SetLabel("Player 2 won")
						self.player2Wins+=1
						self.player2Stat.SetLabel("Player 2 : "+str(self.player2Wins))
					elif self.game.gameWon()=="D":
						self.dispText.SetLabel("Match Drawn")
					else:
						self.game.currentPlayer = self.changePlayer(self.game.currentPlayer)
						self.dispText.SetLabel("Player 1 turn")
		else:
			print "invalid action"
			event.Skip()

class tictactoeFrameQLearning(tictactoeFrame):

	def __init__(self,parent,title):
		tictactoeFrame.__init__(self,parent,title)

		

	def buttonClick(self,event):
		print "id is "+str(event.GetId())
		id = event.GetId()

		if event.GetEventObject().GetLabel()=="-" and self.game.isActive==True:
			print len(self.game.player2.qvalues)
			
			state = "".join(self.game.gridValues)	#positioning of this line here or after line 280 matters
			event.GetEventObject().SetLabel("X")
			self.game.gridValues[id]="X"
			self.game.valuesEntered+=1
			newState = "".join(self.game.gridValues)

			if self.game.gameWon()=="W":
				self.dispText.SetLabel("Player 1 won")
				self.player1Wins+=1
				self.player1Stat.SetLabel("Player 1 : "+str(self.player1Wins))
				self.stateValues(self.game.player2.previousState)
				self.game.player2.update("L",state, -150)

				self.prettyPrint(self.game.player2.previousState)
				self.prettyPrint(state)
				self.stateValues(self.game.player2.previousState)
				
				print self.game.player2.previousAction
				print self.game.player2.qvalues[(self.game.player2.previousState,self.game.player2.previousAction)]
				# print self.game.qvalues

			elif self.game.gameWon()=="D":
				self.game.player2.update("D",state, 60)
				self.dispText.SetLabel("Match Drawn")
				# print self.game.qvalues
			else:
				print "here"
				self.stateValues(self.game.player2.previousState)
				self.game.player2.update("C",state, 30) #living reward
				self.prettyPrint(self.game.player2.previousState)
				self.prettyPrint(state)
				print self.game.player2.previousAction
				print self.game.player2.qvalues[(self.game.player2.previousState,self.game.player2.previousAction)]

				self.game.currentPlayer = self.changePlayer(self.game.currentPlayer)
				self.dispText.SetLabel("Player 2 turn")

				state = "".join(self.game.gridValues)
				action = self.game.player2.getAction(state)

				self.gameButtons[action].SetLabel("O")
				self.game.gridValues[action]="O"
				self.game.valuesEntered+=1
				newState = "".join(self.game.gridValues)

				if self.game.gameWon()=="W":
					self.dispText.SetLabel("Player 2 won")
					self.game.player2.update("W",newState,100)
					self.player2Wins+=1
					self.player2Stat.SetLabel("Player 2 : "+str(self.player2Wins))
					# print self.game.qvalues

				elif self.game.gameWon()=="D":
					self.dispText.SetLabel("Match Drawn")
					self.game.player2.update("D",newState,60)
					# print self.game.qvalues

				else:
					self.game.currentPlayer = self.changePlayer(self.game.currentPlayer)
					self.dispText.SetLabel("Player 1 turn")
		else:
			print "invalid action"
			event.Skip()
	
	def prettyPrint(self,state):
		print state[0:3]
		print state[3:6]
		print state[6:9]

	def stateValues(self,state):
		for i in range(9):
			if self.game.player2.qvalues.has_key((state,i)):
				print "For action : "+str(i)+" QValue is : " + str(self.game.player2.qvalues[(state,i)])



class tictactoeFrameApproxQLearning(tictactoeFrame):

	def __init__(self,parent,title):
		tictactoeFrame.__init__(self,parent,title)

		

	def buttonClick(self,event):
		print "id is "+str(event.GetId())
		id = event.GetId()

		if event.GetEventObject().GetLabel()=="-" and self.game.isActive==True:
			print len(self.game.player2.qvalues)
			
			state = "".join(self.game.gridValues)	#positioning of this line here or after line 280 matters
			event.GetEventObject().SetLabel("X")
			self.game.gridValues[id]="X"
			self.game.valuesEntered+=1
			newState = "".join(self.game.gridValues)

			if self.game.gameWon()=="W":
				self.dispText.SetLabel("Player 1 won")
				self.player1Wins+=1
				self.player1Stat.SetLabel("Player 1 : "+str(self.player1Wins))
				
				self.game.player2.update("L",state, -150)

				

			elif self.game.gameWon()=="D":
				self.game.player2.update("D",state, 60)
				self.dispText.SetLabel("Match Drawn")
			else:

				currentWeights = self.game.player2.weights[:]

				self.game.player2.update("C",state, 30) #living reward
				
				
				# self.diffWeights(currentWeights)
				# self.printWeights2(currentWeights)
				# self.printWeights()
				# self.printFeatures(state)
				

				self.game.currentPlayer = self.changePlayer(self.game.currentPlayer)
				self.dispText.SetLabel("Player 2 turn")

				state = "".join(self.game.gridValues)
				action = self.game.player2.getAction(state)

				# self.printWeights()
				# self.printFeatures(state)
				
				# self.stateValues2(state)




				self.gameButtons[action].SetLabel("O")
				self.game.gridValues[action]="O"
				self.game.valuesEntered+=1
				newState = "".join(self.game.gridValues)

				if self.game.gameWon()=="W":
					self.dispText.SetLabel("Player 2 won")
					self.game.player2.update("W",newState,100)
					self.player2Wins+=1
					self.player2Stat.SetLabel("Player 2 : "+str(self.player2Wins))
					# self.diffWeights(currentWeights)
					# self.printWeights2(currentWeights)
					# self.printWeights()
					# self.printFeatures(state)
					

				elif self.game.gameWon()=="D":
					self.dispText.SetLabel("Match Drawn")
					self.game.player2.update("D",newState,60)
					# self.diffWeights(currentWeights)
					# self.printWeights2(currentWeights)
					# self.printWeights()
					# self.printFeatures(state)
					

				else:
					self.game.currentPlayer = self.changePlayer(self.game.currentPlayer)
					self.dispText.SetLabel("Player 1 turn")
					
		else:
			print "invalid action"
			event.Skip()
	
	def printFeatures(self,state):

		features = self.game.player2.getFeatures(state,self.game.player2.previousAction)

		print "################  Features ######################3"
		print "Singleton featuers"
		print features[0:9]
		# print "Winning position for player"
		# print features[9:18]
		# print "Winning position for opponent"
		# print features[18:27]
		# print "Winning move"
		# print features[27:29]
		# print "Winning position for player"
		# print features[29:38]
		# print "Winning position for opponent"
		# print features[38:47]


	def diffWeights(self,currentWeights):

		diff=[]

		print sum(self.game.player2.weights)
		print sum(currentWeights)
		for i in range(len(currentWeights)):
			diff.append(self.game.player2.weights[i] - currentWeights[i])

		print "################  DIFF in features ######################3"
		print "Singleton featuers"
		print [round(i,2) for i in diff[0:9]]
		# print "Winning position for player"
		# print [round(i,2) for i in diff[9:18]]
		# print "Winning position for opponent"
		# print [round(i,2) for i in diff[18:27]]
		# print "Winning move"
		# print [round(i,2) for i in diff[27:29]]
		# print "Winning position for player"
		# print [round(i,2) for i in diff[29:38]]
		# print "Winning position for opponent"
		# print [round(i,2) for i in diff[38:47]]

	def printWeights2(self,currentWeights):

		print "Singleton featuers"
		print [round(i,2) for i in currentWeights[0:9]]
		# print "Winning position for player"
		# print [round(i,2) for i in currentWeights[9:18]]
		# print "Winning position for opponent"
		# print [round(i,2) for i in currentWeights[18:27]]
		# print "Winning move"
		# print [round(i,2) for i in currentWeights[27:29]]
		# print "Winning position for player"
		# print [round(i,2) for i in currentWeights[29:38]]
		# print "Winning position for opponent"
		# print [round(i,2) for i in currentWeights[38:47]]

	def printWeights(self):

		print "################  Weights ######################3"
		print "Singleton featuers"
		print [round(i,2) for i in self.game.player2.weights[0:9]]
		# print "Winning position for player"
		# print [round(i,2) for i in self.game.player2.weights[9:18]]
		# print "Winning position for opponent"
		# print [round(i,2) for i in self.game.player2.weights[18:27]]
		# print "Winning move"
		# print [round(i,2) for i in self.game.player2.weights[27:29]]
		# print "Winning position for player"
		# print [round(i,2) for i in self.game.player2.weights[29:38]]
		# print "Winning position for opponent"
		# print [round(i,2) for i in self.game.player2.weights[38:47]]

	def prettyPrint(self):
		print self.game.gridValues[0:3]
		print self.game.gridValues[3:6]
		print self.game.gridValues[6:9]

	def stateValues2(self,state):
		for i in range(9):
			print "For action : "+str(i)+" QValue is : " + str(self.game.player2.getQValue(state,i))

	def stateValues(self,state):
		for i in range(9):
			if self.game.player2.qvalues.has_key((state,i)):
				print "For action : "+str(i)+" QValue is : " + str(self.game.player2.qvalues[(state,i)])

if __name__ == '__main__':
  
    app = wx.App()
    tictactoeFrameApproxQLearning(None, title='Tic Tac Toe')
    app.MainLoop()




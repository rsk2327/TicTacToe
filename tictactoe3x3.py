try:
	import wx
except ImportError:
	raise ImportError, "The wxPython module is required to run this program"

from tictactoegame3x3 import *
from string import *
import os 
import pickle

class tictactoeFrame(wx.Frame):

	def __init__(self,parent,title):
		super(tictactoeFrame,self).__init__(parent,title=title)

		self.game = tictactoe(3)
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

		self.numIterEntry = wx.TextCtrl(panel,-1,value="1",style=wx.CENTER|wx.EXPAND)
		self.discountEntry = wx.TextCtrl(panel,-1,value="0.01",style=wx.CENTER|wx.EXPAND)
		self.alphaEntry = wx.TextCtrl(panel,-1,value="0.001",style=wx.CENTER|wx.EXPAND)
		self.epsilonEntry = wx.TextCtrl(panel,-1,value="0.6",style=wx.CENTER|wx.EXPAND)

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

		dispBox.Add(self.trainOptionBox,(11,1),(1,2),flag = wx.CENTER|wx.EXPAND)
		dispBox.Add(trainButton,(11,3),(1,1),flag = wx.CENTER|wx.EXPAND)


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

		self.game.alpha = alpha
		self.game.discount = discount
		self.game.epsilon = epsilon
		trainOption = self.trainOptionBox.GetValue()

		self.game.train(numIter,trainOption)

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
		self.game.qvalues = qvalues
		print qvalues

	def saveButtonClick(self,event):
		filename = self.saveFileName.GetValue()
		pickle.dump(self.game.qvalues,open(filename,"wb"))
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

		self.game = QLearningAgent(3)

	def buttonClick(self,event):
		print "id is "+str(event.GetId())
		id = event.GetId()

		if event.GetEventObject().GetLabel()=="-" and self.game.isActive==True:
			print "Size of qvalues : " + str(len(self.game.qvalues))
			
			nextState = "".join(self.game.gridValues)	#positioning of this line here or after line 280 matters
			event.GetEventObject().SetLabel("X")
			self.game.gridValues[id]="X"
			self.game.valuesEntered+=1
						

			if self.game.gameWon()=="W":
				self.dispText.SetLabel("Player 1 won")
				self.player1Wins+=1
				self.player1Stat.SetLabel("Player 1 : "+str(self.player1Wins))
				self.stateValues(self.game.previousState)
				self.game.update(self.game.previousState, self.game.previousAction, nextState, -150)

				self.prettyPrint(self.game.previousState)
				self.prettyPrint(nextState)
				print self.game.previousAction
				print self.game.qvalues[(self.game.previousState,self.game.previousAction)]
				# print self.game.qvalues

			elif self.game.gameWon()=="D":
				self.game.update(self.game.previousState, self.game.previousAction, nextState, 60)
				self.dispText.SetLabel("Match Drawn")
				# print self.game.qvalues
			else:
				self.stateValues(self.game.previousState)
				self.game.update(self.game.previousState, self.game.previousAction, nextState, 30) #living reward
				self.prettyPrint(self.game.previousState)
				self.prettyPrint(nextState)
				print self.game.previousAction
				print self.game.qvalues[(self.game.previousState,self.game.previousAction)]

				self.game.currentPlayer = self.changePlayer(self.game.currentPlayer)
				self.dispText.SetLabel("Player 2 turn")

				state = "".join(self.game.gridValues)
				action = self.game.getAction(state)

				self.gameButtons[action].SetLabel("O")
				self.game.gridValues[action]="O"
				self.game.valuesEntered+=1
				nextState = "".join(self.game.gridValues)

				if self.game.gameWon()=="W":
					self.dispText.SetLabel("Player 2 won")
					self.game.update(state,action,nextState,100)
					self.player2Wins+=1
					self.player2Stat.SetLabel("Player 2 : "+str(self.player2Wins))
					# print self.game.qvalues

				elif self.game.gameWon()=="D":
					self.dispText.SetLabel("Match Drawn")
					self.game.update(state,action,nextState,0)
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
			if self.game.qvalues.has_key((state,i)):
				print "For action : "+str(i)+" QValue is : " + str(self.game.qvalues[(state,i)])

if __name__ == '__main__':
  
    app = wx.App()
    tictactoeFrameQLearning(None, title='Tic Tac Toe')
    app.MainLoop()




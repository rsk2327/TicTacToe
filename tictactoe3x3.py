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
				button = wx.Button(panel,(i*self.gridSize+j),label="-",name = str(i)+str(j),size=(100,100))
				button.Bind(wx.EVT_BUTTON,self.buttonClick)
				self.gameButtons.append(button)
				gameBox.Add(button,(i,j),(1,1),flag=wx.EXPAND,border=4)
			gameBox.AddGrowableCol(i)
			gameBox.AddGrowableRow(i)

		#dispBox widgets
		self.dispText = wx.StaticText(panel,-1,label="Player 1 turn",style=wx.CENTER)
		l1=wx.StaticLine(panel,-1,style=wx.LI_HORIZONTAL)

		self.player1Stat = wx.StaticText(panel,-1,label="Player 1 : 0 ",style=wx.CENTER)
		self.player2Stat = wx.StaticText(panel,-1,label="Player 2 : 0 ",style=wx.RIGHT)

		self.saveFileName = wx.TextCtrl(panel,-1,value="Enter save file name",style = wx.CENTER|wx.EXPAND)
		saveButton = wx.Button(panel,label="Save",style=wx.CENTER|wx.EXPAND)
		saveButton.Bind(wx.EVT_BUTTON,self.saveButtonClick)

		dispBox.Add(l1,(0,0),(1,2),flag=wx.EXPAND)
		dispBox.Add(self.dispText,(1,0),(2,2),flag=wx.EXPAND|wx.ALL|wx.ALIGN_CENTER)
		dispBox.Add(self.player1Stat,(1,2),(1,1),flag=wx.EXPAND|wx.ALL|wx.ALIGN_CENTER)
		dispBox.Add(self.player2Stat,(2,2),(1,1),flag=wx.EXPAND|wx.ALL|wx.ALIGN_CENTER)
		
		dispBox.Add(self.saveFileName,(4,0),(1,2),flag=wx.EXPAND|wx.ALL|wx.ALIGN_CENTER)
		dispBox.Add(saveButton,(4,2),(1,1),flag=wx.EXPAND|wx.ALL|wx.ALIGN_CENTER)

		dispBox.AddGrowableCol(0)
		dispBox.AddGrowableCol(1)




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

	def saveButtonClick(self,event):
		filename = self.saveFileName.GetValue()
		pickle.dump(self.game.qvalues,open(filename,"wb"))
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
			
			
			event.GetEventObject().SetLabel("X")
			self.game.gridValues[id]="X"
			self.game.valuesEntered+=1
			nextState = "".join(self.game.gridValues)				

			if self.game.gameWon()=="W":
				self.dispText.SetLabel("Player 1 won")
				self.player1Wins+=1
				self.player1Stat.SetLabel("Player 1 : "+str(self.player1Wins))
				self.game.update(self.game.previousState, self.game.previousAction, nextState, -100)
				print self.game.qvalues

			elif self.game.gameWon()=="D":
				self.game.update(self.game.previousState, self.game.previousAction, nextState, 50)
				self.dispText.SetLabel("Match Drawn")
				print self.game.qvalues
			else:
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
					print self.game.qvalues

				elif self.game.gameWon()=="D":
					self.dispText.SetLabel("Match Drawn")
					self.game.update(state,action,nextState,30)
					print self.game.qvalues

				else:
					self.game.currentPlayer = self.changePlayer(self.game.currentPlayer)
					self.dispText.SetLabel("Player 1 turn")
		else:
			print "invalid action"
			event.Skip()
    
if __name__ == '__main__':
  
    app = wx.App()
    tictactoeFrameQLearning(None, title='Tic Tac Toe')
    app.MainLoop()




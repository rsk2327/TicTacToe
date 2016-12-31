try:
	import wx
except ImportError:
	raise ImportError, "The wxPython module is required to run this program"

from tictactoegame2x2 import *

class tictactoeFrame(wx.Frame):

	def __init__(self,parent,title):
		super(tictactoeFrame,self).__init__(parent,title=title)

		self.game = tictactoe(2)
		self.player1Wins=0
		self.player2Wins=0

		self.InitUI(2)
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
				button = wx.Button(panel,(i*self.gridSize+j),label="",name = str(i)+str(j),size=(100,100))
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

		dispBox.Add(l1,(0,0),(1,1),flag=wx.EXPAND)
		dispBox.Add(self.dispText,(1,0),(2,1),flag=wx.EXPAND|wx.ALL|wx.ALIGN_CENTER)
		dispBox.Add(self.player1Stat,(1,1),(1,1),flag=wx.EXPAND|wx.ALL|wx.ALIGN_CENTER)
		dispBox.Add(self.player2Stat,(2,1),(1,1),flag=wx.EXPAND|wx.ALL|wx.ALIGN_CENTER)
		dispBox.AddGrowableCol(0)




		vbox.Add(gameBox,4,wx.EXPAND|wx.ALL,5)
		vbox.Add(ctrlBox,0,wx.EXPAND|wx.ALL,5)
		vbox.Add(dispBox,0,flag=wx.EXPAND|wx.CENTER|wx.ALL,border=15)

		panel.SetSizer(vbox)
		vbox.Fit(self)



	def buttonClick(self,event):
		print "id is "+str(event.GetId())
		id = event.GetId()

		if event.GetEventObject().GetLabel()=="" and self.game.isActive==True:
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
			self.gameButtons[i].SetLabel('')
		self.dispText.SetLabel("Player 1 turn")

		return None

	def resetButtonClick(self,event):
		
		self.nextButtonClick(event)

		return None


	def changePlayer(self,player):
		if player==1:
			return 2
		else:
			return 1






    
if __name__ == '__main__':
  
    app = wx.App()
    tictactoeFrame(None, title='Tic Tac Toe')
    app.MainLoop()




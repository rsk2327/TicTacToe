

grid3List=[[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
grid2List = [[0,1],[2,3],[0,2],[1,3],[0,3],[1,2]]

class tictactoe():

	def __init__(self,gridSize=3):

		self.gridSize=gridSize
		self.valuesEntered=0
		self.isActive=True

		self.gridValues=[]
		for i in range(self.gridSize**2):
			self.gridValues.append('')

		self.currentPlayer = 1





	def gameWon(self):
		"""Returns whether the game has been won or the game has ended in a draw"""

		if self.gridSize==3:

			for i in range(len(grid3List)):
				checkList = grid3List[i]
				val1,val2,val3 = self.gridValues[checkList[0]],self.gridValues[checkList[1]],self.gridValues[checkList[2]]
				if (val1==val2 and val2==val3 and val1!=""):
					self.isActive=False		
					return "W"

			if self.valuesEntered==self.gridSize**2:
				self.isActive=False
				return "D"
			else:
				return "C"
		elif self.gridSize==2:
			for i in range(len(grid2List)):
				checkList = grid2List[i]
				val1,val2 = self.gridValues[checkList[0]],self.gridValues[checkList[1]]
				if (val1==val2 and val1!=""):
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
			self.gridValues[i]=''

		return None




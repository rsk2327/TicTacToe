# TicTacToe
### Reinforcement Learning Agents for playing TicTacToe
------

In this project, I have developed a GUI for training and playing against different types of Reinforcement Learning agents. The training and "playing" phases can occur 
simulataneously thus allowing the user to play against the agent at various stages of training. The GUI was devevloped using **Tkinter** and at 
present supports 3x3 and 4x4 TicTacToe games.

#### **_Types of Agents_** :
* **QLearningAgent** - Standard Q-Learning agent with Q-values learned for all state,action pairs
* **QLearningAgent2** - Q-Learning agent with memory of moves made during the length of a game
* **ApproxQLearningAgent** - Approx Q-Learning agent with weights learned for various features defining the state


There are three major files that work in a top to bottom heirarchy :
1. [tictactoe3x3v2.py](https://github.com/rsk2327/TicTacToe/blob/master/v2/tictactoe3x3v2.py) - Defines the GUI structure. Also handles the interactive playing with the user
2. [game.py](https://github.com/rsk2327/TicTacToe/blob/master/v2/game.py) - Contains the Game class which defines functions handling the interaction between the GUI and the agents. Contains train() function.
3. [agents.py](https://github.com/rsk2327/TicTacToe/blob/master/v2/agents.py) - Defines the behaviour of the different types of agents

For a more detailed description, check out the [blog post](https://roshansanthosh.wordpress.com/2017/03/14/building-an-ai-bot/).

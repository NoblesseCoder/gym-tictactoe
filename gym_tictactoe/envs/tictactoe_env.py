import gym
import itertools
import copy

INIT_BOARD_STATE=[[' ',' ',' '],[' ',' ',' '],[' ',' ',' ']]
WIN_REWARD = 1.0 
LOSS_REWARD = -1.0
DRAW_REWARD = 0.0
NO_REWARD = 0.0

class TicTacToeEnv(gym.Env):
	'''Tic-Tac-Toe board environment for openai gym '''
	metadata={'render.modes':['human']}

	def __init__(self,player1_symbol,player2_symbol):
		'''Initialize Game parameters'''
		self.board_state=INIT_BOARD_STATE
		self.done=False
		self.player1_symbol=player1_symbol
		self.player2_symbol=player2_symbol
		#self.current_player_symbol=player1_symbol

	def _board_state_print(self):
		''' Displays board in proper format'''
		
		print('\n')
		print(self.board_state[0][0] + '|' + self.board_state[0][1] + '|' + self.board_state[0][2])
		print("-----")
		print(self.board_state[1][0] + '|' + self.board_state[1][1] + '|' + self.board_state[1][2])
		print("-----")
		print(self.board_state[2][0] + '|' + self.board_state[2][1] + '|' + self.board_state[2][2])
		print('\n')	

	def _get_obs(self):
		'''Returns Board State & current player's Symbol '''
		return(self.board_state)	


	def _check_game_status(self):
		'''Returns Game Status:(1:Player-1 wins,2:Player-2 Wins,-1:Draw)'''
		if((self.board_state[0][0] == self.board_state[0][1] == self.board_state[0][2] == self.player1_symbol)  or 
			(self.board_state[1][0] == self.board_state[1][1] == self.board_state[1][2] == self.player1_symbol) or
			(self.board_state[2][0] == self.board_state[2][1] == self.board_state[2][2] == self.player1_symbol) or
			(self.board_state[0][0] == self.board_state[1][0] == self.board_state[2][0] == self.player1_symbol) or
			(self.board_state[0][1] == self.board_state[1][1] == self.board_state[2][1] == self.player1_symbol) or
			(self.board_state[0][2] == self.board_state[1][2] == self.board_state[2][2] == self.player1_symbol) or
			(self.board_state[0][0] == self.board_state[1][1] == self.board_state[2][2] == self.player1_symbol) or
			(self.board_state[0][2] == self.board_state[1][1] == self.board_state[2][0] == self.player1_symbol) ): 
				return(1)
		elif((self.board_state[0][0] == self.board_state[0][1] == self.board_state[0][2] == self.player2_symbol)  or 
			(self.board_state[1][0] == self.board_state[1][1] == self.board_state[1][2] == self.player2_symbol) or
			(self.board_state[2][0] == self.board_state[2][1] == self.board_state[2][2] == self.player2_symbol) or
			(self.board_state[0][0] == self.board_state[1][0] == self.board_state[2][0] == self.player2_symbol) or
			(self.board_state[0][1] == self.board_state[1][1] == self.board_state[2][1] == self.player2_symbol) or
			(self.board_state[0][2] == self.board_state[1][2] == self.board_state[2][2] == self.player2_symbol) or
			(self.board_state[0][0] == self.board_state[1][1] == self.board_state[2][2] == self.player2_symbol) or
			(self.board_state[0][2] == self.board_state[1][1] == self.board_state[2][0] == self.player2_symbol) ): 
				return(2)					
		elif(' ' in list(itertools.chain.from_iterable(self.board_state))):
			return(-1)
		else:
			return(0)	
					
	def step(self,action,init_player_symbol,current_player_symbol):
		'''Execute one time step within the environment'''
		if self.done:
			return(self._get_obs(),0,True,None)
		
		self.board_state[action[0]][action[1]]=current_player_symbol
		reward=NO_REWARD
		status=self._check_game_status()
		
		if(status>=0):
			self.game_over=True
			if(init_player_symbol==self.player1_symbol):
				reward= WIN_REWARD if status==1 else LOSS_REWARD if status==2 else DRAW_REWARD
			elif(init_player_symbol==self.player2_symbol):
				reward= WIN_REWARD if status==2 else LOSS_REWARD if status==1 else DRAW_REWARD	
		
		#self.current_player_symbol=self._next_player_symbol()
		return(self._get_obs(),reward,self.game_over,None)	


	def reset(self):
		'''Reset the state of the environment to an initial state'''
		self.board_state=copy.deepcopy(INIT_BOARD_STATE)
		self.game_over=False
		#self.current_player_symbol=player_symbol
		return(self._get_obs())

	def render(self):
		'''Render the environment to the screen'''
		self._board_state_print()			

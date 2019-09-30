import random
import gym_tictactoe.envs.tictactoe_env as ttt
import copy
import itertools
import numpy as np
import csv
import pickle
class QLearningAgent:

	def __init__(self,player_symbol,alpha=0.1,gamma=0.9,q_init=0.6):
		self.player_symbol=player_symbol
		self.alpha=alpha # Learning rate
		self.gamma=gamma # Discounting factor
		self.q_init_val = q_init
		self.move_history = []
		self.q_table={}
		self.moves={0:[0,0],1:[0,1],2:[0,2],3:[1,0],4:[1,1],5:[1,2],6:[2,0],7:[2,1],8:[2,2]}

	def _choose_random_action(self,board_state):
		legal_moves=self.lookForLegalMoves(board_state)
		action=random.choice(legal_moves)
		return(action)

	def _is_legal_move(self,board_state,move):
		''' Returns a list of legal moves for a given board state.'''
		if(board_state[move[0]][move[1]]==' '):					
			return(True)
		else:
			return(False)	

	def _encrypt_board_state(self,board_state):
		bs=list(itertools.chain(*board_state))
		board_hash_val=''.join(bs)
		return(board_hash_val)

	def _decrypt_board_hash_val(self,board_hash_val):
		bs=list(board_hash_val)
		return(bs)
			 
	def _get_q_vals(self,board_state):
		board_hash_val=self._encrypt_board_state(board_state)
		if board_hash_val in self.q_table:
			q_vals=self.q_table[board_hash_val]
		else:
			#q_vals=np.full(9,self.q_init_val)
			q_vals=np.array([np.random.rand() for i in range(9)])
			self.q_table[board_hash_val]=q_vals
		return(q_vals)		

	def _update_q_table(self,game_history,action_history,rewards):			
		move_history=[self._encrypt_board_state(i) for i in game_history]
		action_history=[list(self.moves.keys())[list(self.moves.values()).index(i)] for i in action_history]
		move_history.reverse()
		action_history.reverse()
		rewards.reverse()
		print(rewards)
		next_max=-1.0
		for move in range(len(move_history)):
			q_vals=self._get_q_vals(move_history[move])
			if(next_max<0):
				q_vals[action_history[move]]=rewards[0]
			else:
				q_vals[action_history[move]]=((
					(1-self.alpha)*q_vals[action_history[move]])+(
					self.alpha*(rewards[move]+self.gamma*next_max)))
			next_max=max(q_vals)
		self.q_table[move_history[move]]=q_vals	
			
	def choose_action(self,board_state):
		board_hash_val=self._encrypt_board_state(board_state)
		q_vals=self._get_q_vals(board_hash_val)
		while True:
			m=np.argmax(q_vals)
			next_move=self.moves[m]
			if(self._is_legal_move(board_state,next_move)):
				action=[next_move[0],next_move[1]]
				return(action)
			else:
				q_vals[m]=-1.0

	def _write_q_values_to_file(self,filename='./data/qtables.csv'):
		rows=[]
		for i in self.q_table.keys():
			row=[i,self.q_table[i][0],self.q_table[i][1],self.q_table[i][2],self.q_table[i][3],
				self.q_table[i][4],self.q_table[i][5],self.q_table[i][6],self.q_table[i][7],self.q_table[i][8]]
			rows.append(row)	
		
		with open(filename,"w") as f:
			wr = csv.writer(f)
			wr.writerows(rows)		


	def _read_q_values_from_file(self,filename='./data/qtables.csv'):
		with open(filename,'r') as f:
			reader = csv.reader(f)
			temp_q_table=list(reader)
		q_table={}
		for i in temp_q_table:
			vals=[float(j) for j in i[1:]]
			q_table[i[0]]=[float(j) for j in i[1:]]					
		return(q_table)	
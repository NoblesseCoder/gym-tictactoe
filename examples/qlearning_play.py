import itertools
import gym_tictactoe.envs.tictactoe_env as ttt
from agents.q_learning_agent import QLearningAgent
from agents.base_agents import HumanAgent,RandomAgent
import copy
import matplotlib.pyplot as plt
import random

def train(max_episodes=20,p1='QLA',p2='RA'):
	episode=0
	player1_symbol,player2_symbol='X','O'
	env=ttt.TicTacToeEnv(player1_symbol,player2_symbol)
	if(p1=='QLA'):
		player1=QLearningAgent(player1_symbol) #Initialize agents
	elif(p1=='RA'):
		player1=RandomAgent(player2_symbol)
	if(p2=='QLA'):
		player2=QLearningAgent(player1_symbol) #Initialize agents
	elif(p2=='RA'):
		player2=RandomAgent(player2_symbol)

	p1_win_cnt,p2_win_cnt,draw_cnt=0,0,0
	while(episode<max_episodes):
		print("Episode:"+str(episode))
		game_history,action_history,rewards=[],[],[]
		
		board_state=env.reset()
		game_over=False
		if(episode%2==0):
			current_player_symbol=player1_symbol
			init_player_symbol=player1_symbol
		else:
			current_player_symbol=player2_symbol
			init_player_symbol=player2_symbol
		
		while(not game_over):
			if(current_player_symbol==player1_symbol):
				action=player1.choose_action(board_state)
			else:
				action=player2.choose_action(board_state)
			board_state,reward,game_over,info=env.step(action,init_player_symbol,current_player_symbol)
			current_player_symbol= player2_symbol if current_player_symbol==player1_symbol else player1_symbol
			game_history.append([list(itertools.chain(*board_state))])
			action_history.append(action)
			rewards.append(reward)
			env.render()

		if(episode%2==0):	
			player1._update_q_table(game_history,action_history,rewards)
			if(reward==1):
				p1_win_cnt=p1_win_cnt+1	#player-1 wins
			if(reward==-1):
				p2_win_cnt=p2_win_cnt+1	#player-2 wins
			elif(reward==0):
				draw_cnt=draw_cnt+1	#draw
		else:
			if(reward==1):
				p2_win_cnt=p2_win_cnt+1	#player-2 wins
			elif(reward==-1):
				p1_win_cnt=p1_win_cnt+1	#player-1 wins
			elif(reward==0):
				draw_cnt=draw_cnt+1	#draw	
			
		player1._write_q_values_to_file()	
		episode=episode+1

	env.close()
	return(p1_win_cnt,p2_win_cnt,draw_cnt)


def train_stochastic(max_episodes=2000,p1='QLA',p2='QLA'):
	episode=0
	player1_symbol,player2_symbol='X','O'
	env=ttt.TicTacToeEnv(player1_symbol,player2_symbol)
	if(p1=='QLA'):
		player1=QLearningAgent(player1_symbol) #Initialize agents
	elif(p1=='RA'):
		player1=RandomAgent(player2_symbol)
	if(p2=='QLA'):
		player2=QLearningAgent(player1_symbol) #Initialize agents
	elif(p2=='RA'):
		player2=RandomAgent(player2_symbol)

	p1_win_cnt,p2_win_cnt,draw_cnt=0,0,0
	while(episode<max_episodes):
		print("Episode:"+str(episode))
		game_history,action_history,rewards=[],[],[]
		
		board_state=env.reset()
		game_over=False
		if(episode%2==0):
			current_player_symbol=player1_symbol
			init_player_symbol=player1_symbol
		else:
			current_player_symbol=player2_symbol
			init_player_symbol=player2_symbol
		
		while(not game_over):
			player_choice=random.choices([1,2],weights=[0.8, 0.2])
			if(player_choice==1):
				action=player1.choose_action(board_state)
				current_player_symbol=player1_symbol
			else:
				action=player2.choose_action(board_state)
				current_player_symbol=player2_symbol
			board_state,reward,game_over,info=env.step(action,init_player_symbol,current_player_symbol)
			game_history.append([list(itertools.chain(*board_state))])
			action_history.append(action)
			rewards.append(reward)
			env.render()

		if(episode%2==0):	
			player1._update_q_table(game_history,action_history,rewards)
			if(reward==1):
				p1_win_cnt=p1_win_cnt+1	#player-1 wins
			if(reward==-1):
				p2_win_cnt=p2_win_cnt+1	#player-2 wins
			elif(reward==0):
				draw_cnt=draw_cnt+1	#draw
		else:
			if(reward==1):
				p2_win_cnt=p2_win_cnt+1	#player-2 wins
			elif(reward==-1):
				p1_win_cnt=p1_win_cnt+1	#player-1 wins
			elif(reward==0):
				draw_cnt=draw_cnt+1	#draw	
			
		player1._write_q_values_to_file()	
		episode=episode+1

	env.close()
	return(p1_win_cnt,p2_win_cnt,draw_cnt)	

def play_against_human(filename='qtables.csv'):
	flag=True
	episode=0
	player1_symbol,player2_symbol='X','O'
	env=ttt.TicTacToeEnv(player1_symbol,player2_symbol)
	player1=QLearningAgent(player1_symbol)
	player1.q_table=player1._read_q_values_from_file(filename)
	player2=HumanAgent(player2_symbol)
	
	while(flag):
		print("Episode:"+str(episode))
		board_state=env.reset()
		game_over=False
		game_history=[]
		
		if(episode%2==0):
			current_player_symbol=player1_symbol
			init_player_symbol=player1_symbol
		else:
			current_player_symbol=player2_symbol
			init_player_symbol=player2_symbol

		while(not game_over):
			if(current_player_symbol==player1_symbol):
				action=player1.choose_action(board_state)
			else:
				action=player2.choose_action(board_state)
			board_state,reward,game_over,info=env.step(action,init_player_symbol,current_player_symbol)
			current_player_symbol=player2_symbol if current_player_symbol==player1_symbol else player1_symbol
			env.render()
		
		status=input("Do you want to continue playing(y/n):\t")
		
		if(status=='y'):
			flag=True
		else:
			flag=False	
	
	env.close()	


def plot_training_graph(p1='RA',p2='QLA',max_epochs=300,e_range=100):
	p1_win_cnts,p2_win_cnts,draw_cnts=[],[],[]
	for i in range(100,max_epochs,e_range):	
		status=train(i,p1,p2)
		p1_win_cnts.append(status[0]*100/float(sum(status)))
		p2_win_cnts.append(status[1]*100/float(sum(status)))
		draw_cnts.append(status[2]*100/float(sum(status)))

	plt.plot(range(100,max_epochs,e_range),p1_win_cnts,color='g')
	plt.plot(range(100,max_epochs,e_range),p2_win_cnts,color='b')	
	plt.plot(range(100,max_epochs,e_range),draw_cnts,color='r')
	plt.show()



#plot_training_graph(p1='QLA',p2='RA',max_epochs=10000,e_range=500)
#cnt=train(max_episodes=10000,p1='QLA',p2='RA')
#print(cnt)
#play_against_human(filename='qtables.csv')
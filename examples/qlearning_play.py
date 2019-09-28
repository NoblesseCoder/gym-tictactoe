import itertools
import gym_tictactoe.envs.tictactoe_env as ttt
from agents.q_learning_agent import QLearningAgent
from agents.base_agents import HumanAgent



def train(max_episodes=3):
	episode=0
	player1_symbol,player2_symbol='X','O'
	env=ttt.TicTacToeEnv(player1_symbol,player2_symbol)
	player1=QLearningAgent(player1_symbol) #Initialize agents
	player2=QLearningAgent(player2_symbol)
	current_player_symbol=player1_symbol
	status_cnt=[0,0,0]

	while(episode<max_episodes):
		print("Episode:"+str(episode))
		game_history=[]
		action_history=[]
		rewards=[]
		board_state,current_player_symbol=env.reset(current_player_symbol)
		print(current_player_symbol)
		game_over=False
		while(not game_over):
			if(current_player_symbol==player1_symbol):
				action=player1.choose_action(board_state)
			else:
				action=player2.choose_action(board_state)
			
			state,reward,game_over,info=env.step(action)
			board_state,current_player_symbol=state
			game_history.append([list(itertools.chain(*board_state))])
			action_history.append(action)
			rewards.append(reward)
			env.render()

		if(episode%2==0):
			player1._update_q_table(game_history,action_history,rewards)
			if(reward==1):
				status_cnt[0]=status_cnt[0]+1	#player-1 wins
			if(reward==-1):
				status_cnt[1]=status_cnt[1]+1	#player-2 wins
			elif(reward==0):
				status_cnt[2]=status_cnt[2]+1	#draw
		else:
			player2._update_q_table(game_history,action_history,rewards)
			if(reward==1):
				status_cnt[1]=status_cnt[1]+1	#player-2 wins
			elif(reward==-1):
				status_cnt[0]=status_cnt[0]+1	#player-1 wins
			elif(reward==0):
				status_cnt[2]=status_cnt[2]+1	#draw		
		episode=episode+1
	print(status_cnt)		
	env.close()

def play_against_human(q_table):
	flag=True
	episode=0
	player1_symbol,player2_symbol='X','O'
	env=ttt.TicTacToeEnv(player1_symbol,player2_symbol)
	player1=QLearningAgent(player1_symbol)
	player1.q_table=q_table
	player2=HumanAgent(player2_symbol)
	current_player_symbol=player1_symbol
	
	while(flag):
		print("Episode:"+str(episode))
		board_state,current_player_symbol=env.reset(current_player_symbol)
		game_over=False
		game_history=[]
		while(not game_over):
			if(current_player_symbol==player1_symbol):
				action=player1.choose_action(board_state)
			else:
				action=player2.choose_action(board_state)
			state,reward,game_over,info=env.step(action)
			board_state,current_player_symbol=state
			env.render()
			print(reward)
		status=input("Do you want to continue playing(y/n):\t")
		if(status=='y'):
			flag=True
		else:
			flag=False	
	env.close()	

train()
#print(status_cnt)
#play_against_human(q_table)

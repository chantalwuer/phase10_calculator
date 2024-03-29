import pandas as pd
import streamlit as st

# Functions

def register_players():
    '''
    Function that registers number of players and players names
    '''

    num_players = int(input("How many players are playing? "))
    players = [input(f'Who is player {player+1}?') for player in range(0,num_players)]
    return players

def setup_game():
    '''
    Registers players, creates score board and phase board
    '''

    players = register_players()
    score_board = pd.DataFrame(columns=players)
    phase_board = pd.DataFrame(columns=['Players','Phase'])
    phase_board['Players'] = players
    phase_board['Phase'] = 1
    return score_board, phase_board, players

def log_phase(players, phase_board):
    '''
    Advances players into next phase if they finished. Updates phase board
    '''

    for player in players:
        player_no = players.index(player)
        current_phase = phase_board.iloc[[player_no], [1]].values[0][0]
        advanced_bool = input(f'Did {player} finish phase {current_phase}?')
        if advanced_bool.upper() == 'Y':
            phase_board.iloc[[player_no], [1]] += 1

    return phase_board

def log_scores(players, score_board):
    '''
    Collects the value of the remaining cards and computes the scores.
    Returns updated score board.
    '''
    point_rules = {
        'cards_1_9': 5,
        'cards_10_12': 10,
        'cards_stop': 15,
        'cards_joker': 20
    }
    final_scores = {}

    for player in players:
        card_values = {}
        card_values['cards_1_9'] = int(input(f'How many cards betweeen 1 and 9 does {player} have?'))
        card_values['cards_10_12'] = int(input(f'How many cards between 10 and 12 does {player} have?'))
        card_values['cards_stop'] = int(input(f'How many ! cards does {player} have?'))
        card_values['cards_joker'] = int(input(f'How many jokers does {player} have?'))
        final_score = sum(point_rules[k]*card_values[k] for k in point_rules)
        final_scores[player] = final_score

    scores = pd.DataFrame([final_scores])
    score_board = pd.concat([score_board, scores], ignore_index=True)
    return score_board

def end_of_round(players, phase_board, score_board):
    '''
    Bundles updating of both phase and score board after each round.
    '''
    phase_board = log_phase(players, phase_board)
    score_board = log_scores(players, score_board)
    return phase_board, score_board

'''
# Welcome to the Phase 10 score keeper
Let's set up the game.
'''

with st.form(key='submit_input'):
    players_nr = st.text_input('How many players are playing?')
    st.form_submit_button('Enter')

players = []

for x in range(0, int(players_nr)):
    player = st.text_input(f'Name of player {x+1}:')
    players.append(player)

score_board, phase_board, players = setup_game()

if st.button('Start playing'):
    phase_board = log_phase(players, phase_board)
    phase_board

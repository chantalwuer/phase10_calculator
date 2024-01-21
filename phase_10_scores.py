import pandas as pd
import ipdb
# Functions

def register_players():
    '''
    Function that registers number of players and players names
    '''

    num_players = int(input("How many players are playing? "))
    players = [input(f'Who is player {player+1}? ') for player in range(0,num_players)]
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
        ipdb.set_trace()
        player_no = players.index(player)
        current_phase = phase_board.loc[[player_no], [1]].values[0][0]
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



if __name__ == '__main__':
    score_board, phase_board, players = setup_game()
    print(phase_board)
    print(players)
    phase_board = log_phase(players, score_board)

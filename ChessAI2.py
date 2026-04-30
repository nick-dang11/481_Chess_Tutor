import random

DEPTH = 3
CHECKMATE_SCORE = 100000
STALEMATE_SCORE = 0

MATERIAL_WEIGHT = 1.0
MOBILITY_WEIGHT = 5

PIECE_VALUES = {
    "K": 0,
    "Q": 900,
    "R": 500,
    "B": 330,
    "N": 320,
    "P": 100,
}

def find_random_move(valid_moves):
    return random.choice(valid_moves)


def evaluate_board(game_state):


    if game_state.checkmate:
        if game_state.white_to_move:
            return -CHECKMATE_SCORE
        else:
            return CHECKMATE_SCORE
        
    if game_state.stalemate:
        return STALEMATE_SCORE
    
    score = 0 
    score += MATERIAL_WEIGHT * material_score(game_state)
    score += MOBILITY_WEIGHT * mobility_score(game_state)
    
    return score

def material_score(game_state):
    score = 0

   for piece in game_state.captured_black_pieces:
       score += PIECE_VALUES[piece[1]]

    for piece in game_state.captured_white_pieces:
       score -= PIECE_VALUES[piece[1]]
    
    return score

def mobility_score(game_state):
    
    original_turn = game_state.white_to_move
    original_checkmate = game_state.checkmate
    original_stalemate = game_state.stalemate

    game_state.white_to_move = True
    white_mobility = len(game_state.get_valid_moves())

    game_state.white_to_move = False
    black_mobility = len(game_state.get_valid_moves())

    game_state.white_to_move = original_turn
    game_state.checkmate = original_checkmate
    game_state.stalemate = original_stalemate

    return white_mobility - black_mobility
    
    

import random

DEPTH = 3
CHECKMATE_SCORE = 100000
STALEMATE_SCORE = 0

MATERIAL_WEIGHT = 1.0

PIECE_VALUES = {
    "K": 0,
    "Q": 900,
    "R": 500,
    "B": 330,
    "N": 320,
    "p": 100,
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
    return score

def material_score(game_state):
    score = 0

    for piece in game_state.captured_black_pieces:
        value = PIECE_VALUES[piece[1]]
        score += value

        print(f"White captured black {piece} worth {value} points")

    for piece in game_state.captured_white_pieces:
        value = PIECE_VALUES[piece[1]]
        score -= value

        print(f"Black captured white {piece} worth {value} points")

    return score

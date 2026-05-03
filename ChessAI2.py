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
piece_positions = {
    'wP': [
        [ 0,  0,  0,  0,  0,  0,  0,  0],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [10, 10, 20, 30, 30, 20, 10, 10],
        [ 5,  5, 10, 25, 25, 10,  5,  5],
        [ 0,  0,  0, 20, 20,  0,  0,  0],
        [ 5, -5,-10,  0,  0,-10, -5,  5],
        [ 5, 10, 10,-20,-20, 10, 10,  5],
        [ 0,  0,  0,  0,  0,  0,  0,  0]],
    'bP': [
        [ 0,  0,  0,  0,  0,  0,  0,  0],
        [ 5, 10, 10,-20,-20, 10, 10,  5],
        [ 5, -5,-10,  0,  0,-10, -5,  5],
        [ 0,  0,  0, 20, 20,  0,  0,  0],
        [ 5,  5, 10, 25, 25, 10,  5,  5],
        [10, 10, 20, 30, 30, 20, 10, 10],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [ 0,  0,  0,  0,  0,  0,  0,  0]],
    'wN': [
        [-50,-40,-30,-30,-30,-30,-40,-50],
        [-40,-20,  0,  0,  0,  0,-20,-40],
        [-30,  0, 10, 15, 15, 10,  0,-30],
        [-30,  5, 15, 20, 20, 15, 50,-30],
        [-30,  0, 15, 20, 20, 15,  0,-30],
        [-30,  5, 10, 15, 15, 10, 50,-30],
        [-40,-20,  0,  5,  5,  0,-20,-40],
        [-50,-40,-30,-30,-30,-30,-40,-50]],
    'bN': [
        [-50,-40,-30,-30,-30,-30,-40,-50],
        [  0,-20,  0,  5,  5,  0,-20,-40],
        [-30,  5, 10, 15, 15, 10,  5,-30],
        [-30,  0, 15, 20, 20, 15,  0,-30],
        [-30,  5, 15, 20, 20, 15,  5,-30],
        [-30,  0, 10, 15, 15, 10,  0,-30],
        [-40,-20,  0,  0,  0,  0,-20,-40],
        [-50,-40,-30,-30,-30,-30,-40,-50]],
    'wB': [
        [-20,-10,-10,-10,-10,-10,-10,-20],
        [-10,  0,  0,  0,  0,  0,  0,-10],
        [-10,  0,  5, 10, 10,  5,  0,-10],
        [-10,  5,  5, 10, 10,  5,  5,-10],
        [-10,  0, 10, 10, 10, 10,  0,-10],
        [-10, 10, 10, 10, 10, 10, 10,-10],
        [-10,  5,  0,  0,  0,  0,  5,-10],
        [-20,-10,-10,-10,-10,-10,-10,-20]],
    'bB': [
        [-20,-10,-10,-10,-10,-10,-10,-20],
        [-10,  5,  0,  0,  0,  0,  5,-10],
        [-10, 10, 10, 10, 10, 10, 10,-10],
        [-10,  0, 10, 10, 10, 10,  0,-10],
        [-10,  5,  5, 10, 10,  5,  5,-10],
        [-10,  0,  5, 10, 10,  5,  0,-10],
        [-10,  0,  0,  0,  0,  0,  0,-10],
        [-20,-10,-10,-10,-10,-10,-10,-20]],
    'wR': [
        [  0,  0,  0,  0,  0,  0,  0,  0],
        [  5, 10, 10, 10, 10, 10, 10,  5],
        [ -5,  0,  0,  0,  0,  0,  0, -5],
        [ -5,  0,  0,  0,  0,  0,  0, -5],
        [ -5,  0,  0,  0,  0,  0,  0, -5],
        [ -5,  0,  0,  0,  0,  0,  0, -5],
        [ -5,  0,  0,  0,  0,  0,  0, -5],
        [  0,  0,  0,  5,  5,  0,  0,  0]],
    'bR': [
        [  0,  0,  0,  5,  5,  0,  0,  0],
        [ -5,  0,  0,  0,  0,  0,  0, -5],
        [ -5,  0,  0,  0,  0,  0,  0, -5],
        [ -5,  0,  0,  0,  0,  0,  0, -5],
        [ -5,  0,  0,  0,  0,  0,  0, -5],
        [ -5,  0,  0,  0,  0,  0,  0, -5],
        [  5, 10, 10, 10, 10, 10, 10,  5],
        [  0,  0,  0,  0,  0,  0,  0,  0]],
    'wQ': [
        [-20,-10,-10, -5, -5,-10,-10,-20],
        [-10,  0,  0,  0,  0,  0,  0,-10],
        [-10,  0,  5,  5,  5,  5,  0,-10],
        [ -5,  0,  5,  5,  5,  5,  0, -5],
        [  0,  0,  5,  5,  5,  5,  0, -5],
        [-10,  5,  5,  5,  5,  5,  0,-10],
        [-10,  0,  5,  0,  0,  0,  0,-10],
        [-20,-10,-10, -5, -5,-10,-10,-20]],
    "bQ": [
        [-20,-10,-10, -5, -5,-10,-10,-20],
        [-10,  0,  5,  0,  0,  0,  0,-10],
        [-10,  5,  5,  5,  5,  5,  0,-10],
        [  0,  0,  5,  5,  5,  5,  0, -5],
        [ -5,  0,  5,  5,  5,  5,  0, -5],
        [-10,  0,  5,  5,  5,  5,  0,-10],
        [-10,  0,  0,  0,  0,  0,  0,-10],
        [-20,-10,-10, -5, -5,-10,-10,-20]],
    'wK': [
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-20,-30,-30,-40,-40,-30,-30,-20],
        [-10,-20,-20,-20,-20,-20,-20,-10],
        [ 20, 20,  0,  0,  0,  0, 20, 20],
        [ 20, 30, 10,  0,  0, 10, 30, 20]],
    'bK': [
        [ 20, 30, 10,  0,  0, 10, 30, 20],
        [ 20, 20,  0,  0,  0,  0, 20, 20],
        [-10,-20,-20,-20,-20,-20,-20,-10],
        [-20,-30,-30,-40,-40,-30,-30,-20],
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-30,-40,-40,-50,-50,-40,-40,-30]]
}
def find_random_move(valid_moves):
    return random.choice(valid_moves)
    
def find_best_move(game_state, valid_moves):
    if len(valid_moves) == 0:
        return None
    player_is_white = game_state.white_to_move

    best_move = None
    best_score = -CHECKMATE_SCORE
    alpha = -CHECKMATE_SCORE
    beta = CHECKMATE_SCORE

    ordered_moves = order_moves(valid_moves)

    for move in ordered_moves:
        game_state.make_move(move)
        next_moves = game_state.get_valid_moves()

        score = min_value(game_state, next_moves, alpha,beta, 1, player_is_white)
        game_state.undo_move()

        if score > best_score:
            best_score = score
            best_move = move

        alpha = max(alpha, best_score)

    return best_move

def max_value(game_state,valid_moves,alpha,beta,depth,player_is_white):
    if cutoff_test(game_state, valid_moves, depth):
        return evaluate_for_player(game_state,player_is_white)

    value = -CHECKMATE_SCORE
    for move in order_moves(valid_moves):
        game_state.make_move(move)
        next_moves = game_state.get_valid_moves()

        value = max(value, min_value(game_state, next_moves, alpha, beta, depth + 1, player_is_white) )
        game_state.undo_move()

        if value >= beta:
            return value

        alpha = max(alpha, value)
         
    return value

def min_value(game_state,valid_moves,alpha,beta,depth,player_is_white):
    if cutoff_test(game_state, valid_moves, depth):
        return evaluate_for_player(game_state,player_is_white)

    value = CHECKMATE_SCORE
    for move in order_moves(valid_moves):
        game_state.make_move(move)
        next_moves = game_state.get_valid_moves()

        value = min(value, max_value(game_state, next_moves, alpha, beta, depth + 1, player_is_white) )
        game_state.undo_move()

        if value <= alpha:
            return value

        beta = min(beta, value)
         
    return value

def cutoff_test(game_state, valid_moves, depth):
    return(depth >= DEPTH or game_state.checkmate or game_state.stalemate or len(valid_moves) == 0)

def evaluate_for_player(game_state, player_is_white):

    score = evaluate_board(game_state)

    if player_is_white:
        return score
    else:
        return -score


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
    original_in_check = game_state.in_check
    original_pins = game_state.pins[:]
    original_checks = game_state.checks[:]
    

    game_state.white_to_move = True
    white_mobility = len(game_state.get_valid_moves())

    game_state.white_to_move = False
    black_mobility = len(game_state.get_valid_moves())

    game_state.white_to_move = original_turn
    game_state.checkmate = original_checkmate
    game_state.stalemate = original_stalemate
    game_state.in_check = original_in_check
    game_state.pins[:] = original_pins
    game_state.checks[:] = original_checks

    return white_mobility - black_mobility

def order_moves(valid_moves):
    moves = list(valid_moves)
    random.shuffle(moves)
    
    moves.sort(key = move_order_score, reverse = True)
    return moves

def move_order_score(move):
    score = 0

    if move.is_pawn_promotion:
        score += 900

    if move.piece_captured != "--":
        captured_piece = move.piece_captured[1]
        moved_piece = move.piece_moved[1]

        score += 10 * PIECE_VALUES[captured_piece]
        score -= PIECE_VALUES[moved_piece]

    if move.is_castle_move:
        score += 50

    return score

    

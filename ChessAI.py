import random
#Changes 1


# Depth of the algorithm determining AI moves. Higher set_depth == harder AI. Lower if engine is too slow.
set_depth = 4
checkmate_points = 100000
stalemate_score = 0

MATERIAL_WEIGHT = 1.0
POSITION_WEIGHT = 0.8
MOBILITY_WEIGHT = 0.2

piece_scores = {
    'P': 100, 'N': 320, 'B': 330, 
    'R': 500, 'Q': 900, 'K': 0
}

transposition_table = {}
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

def order_moves(moves):
    """
    Sorts moves to make Alpha-Beta pruning significantly faster.
    Prioritizes: Captures (MVV-LVA) > Promotions > Castling.
    """
    def move_score(move):
        score = 0
        if move.is_pawn_promotion:
            score += 900
        if move.piece_captured != '--':
            # MVV-LVA: Taking a big piece with a small piece is best
            score += 10 * piece_scores[move.piece_captured[1]] - piece_scores[move.piece_moved[1]]
        if move.is_castle_move:
            score += 50
        return score

    return sorted(list(moves), key=move_score, reverse=True)

            


def find_best_move(game_state, valid_moves):
    """Helper method to make first recursive call"""
    global next_move, transposition_table
    next_move = None
    transposition_table = {}

    valid_moves = order_moves(valid_moves)

    find_negamax_move_alphabeta(game_state, valid_moves, set_depth, -checkmate_points, checkmate_points, 1 if game_state.white_to_move else -1)

    return next_move

def board_key(game_state, depth, turn_multiplier):
    board_tuple = tuple(tuple(row) for row in game_state.board)
    return(board_tuple, 
           game_state.white_to_move, 
           game_state.en_passant_possible, 
           game_state.white_castle_king_side,
           game_state.white_castle_queen_side,
           game_state.black_castle_king_side, 
           game_state.black_castle_queen_side, 
           depth, 
           turn_multiplier)


def find_negamax_move_alphabeta(game_state, valid_moves, depth, alpha, beta, turn_multiplier):
    """
    NegaMax algorithm with alpha beta pruning.

    Alpha beta pruning eliminates the need to check all moves within the game_state tree when
    a better branch has been found or a branch has too low of a score.

    alpha: upper bound (max possible); beta: lower bound (min possible)
    If max score is greater than alpha, that becomes the new alpha value.
    If alpha becomes >= beta, break out of branch.

    White is always trying to maximise score and black is always
    trying to minimise score. Once the possibility of a higher max or lower min
    has been eliminated, there is no need to check further branches.
    """
    global next_move, transposition_table

    key = board_key(game_state, depth, turn_multiplier)
    if key in transposition_table:
        return transposition_table[key]
    
    if depth == 0:
        score = turn_multiplier * evaluate_board(game_state)
        transposition_table[key] = score
        return score

    max_score = -checkmate_points

    for move in order_moves(valid_moves):
        game_state.make_move(move)
        next_moves = game_state.get_valid_moves()
        score = -find_negamax_move_alphabeta(game_state, next_moves, depth - 1, -beta, -alpha, -turn_multiplier)

        game_state.undo_move()

        if score > max_score:
            max_score = score
            if depth == set_depth:
                next_move = move
        
        alpha = max(alpha, max_score)

        # Pruning
        if alpha >= beta:
            break

    transposition_table[key] = max_score
    return max_score


def evaluate_board(game_state):
    """
    Evaluates board state; positive results for white, negative for black.
    """

    if game_state.checkmate:
        return -checkmate_points if game_state.white_to_move else checkmate_points
    if game_state.stalemate:
        return stalemate_score
    
    material_and_pos = 0

    for r in range(len(game_state.board)):
        for c in range(len(game_state.board[r])):
            piece = game_state.board[r][c]
            if piece != '--':
                color = piece[0]
                type = piece[1]

                val = piece_scores[type]
                pos_bonus = piece_positions[piece][r][c]

                if color == 'w':
                    material_and_pos += (val + pos_bonus)
                else:
                    material_and_pos -= (val + pos_bonus)

    white_mobility, black_mobility = get_mobility_counts(game_state)
    mobility_diff = white_mobility - black_mobility

    final_score = (material_and_pos * MATERIAL_WEIGHT) + (mobility_diff * MOBILITY_WEIGHT)
    return final_score

def get_mobility_counts(game_state):
    original_state = {
        'turn': game_state.white_to_move,
        'mate': game_state.checkmate,
        'stale': game_state.stalemate,
        'in_check': game_state.in_check,
        'pins': game_state.pins[:],
        'checks': game_state.checks[:]
    }
    
    game_state.white_to_move = True
    white_m = len(game_state.get_valid_moves())
    
    game_state.white_to_move = False
    black_m = len(game_state.get_valid_moves())
    
    game_state.white_to_move = original_state['turn']
    game_state.checkmate = original_state['mate']
    game_state.stalemate = original_state['stale']
    game_state.in_check = original_state['in_check']
    game_state.pins[:] = original_state['pins']
    game_state.checks[:] = original_state['checks']
    
    return white_m, black_m
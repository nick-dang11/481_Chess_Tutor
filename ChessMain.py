import pygame as p
import ChessEngine, ChessAI
import ChessTutor

# Player settings. Turn player_one to True to play as white and/or player_two to True to play black.
player_one = True  # If the AI is playing white, then False
player_two = True  # Same as above but for black

p.init()  # Initialize pygame

board_width = board_height = 680  # Can switch to 512 if screen is too big
dimension = 8  # Dimensions of a chess board are 8x8
sq_size = board_height // dimension
max_fps = 15  # For animations
images = {}
colours = [p.Color('#EBEBD0'), p.Color('#769455')]  # Board colours

# Move log specifications
move_log_panel_width = 210  # May want to adjust this if the board_width/board_height is changed.
move_log_panel_height = board_height

# Tutor chat specifications
tutor_chat_panel_width = 300
tutor_chat_panel_height = board_height


def load_images():
    """Initialize a global dictionary of images"""
    pieces = ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR', 'bP',
              'wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR', 'wP']
    for piece in pieces:
        images[piece] = p.transform.smoothscale(p.image.load(f'images/{piece}.png'), (sq_size, sq_size))

    move_img = p.image.load('images/chessMove.png').convert_alpha()
    capt_img = p.image.load('images/chessCapture.png').convert_alpha()

    move_img = p.transform.smoothscale(move_img, (sq_size, sq_size))
    capt_img = p.transform.smoothscale(capt_img, (sq_size, sq_size))

    move_img.set_alpha(100) 

    images['movementSquare'] = move_img
    images['captureSquare'] = capt_img

def main():
    """Main function which handles user input and updates graphics"""
    screen = p.display.set_mode((board_width + move_log_panel_width + tutor_chat_panel_width, board_height))
    clock = p.time.Clock()
    screen.fill(p.Color('white'))
    move_log_font = p.font.SysFont('Arial', 14, False, False)
    game_state = ChessEngine.GameState()
    valid_moves = game_state.get_valid_moves()
    move_made = False  # Flag variable for when a move is made
    animate = False  # Flag variable for when a move should be animated
    load_images()
    running = True
    square_selected = ()  # Keeps track of the last click by user (tuple: (row, column))
    player_clicks = []  # Keeps track of player clicks (two tuples: ex. [(6, 4), (4, 4)])
    
    tutor = ChessTutor.ChessTutor()
    tutor_square_selected = ()
    tutor_clicks = []
    tutor_moves_for_tutor = []
    tutor_message = "Hello! I'm your chess tutor. Right Click to see possible moves"
    game_over = False

    while running:
        human_turn = (game_state.white_to_move and player_one) or (not game_state.white_to_move and player_two)

        for event in p.event.get():
            if event.type == p.QUIT:
                running = False

            # Mouse handler
            elif event.type == p.MOUSEBUTTONDOWN:
                if not game_over and human_turn:
                    location = p.mouse.get_pos()  # (x, y) location of mouse
                    column = location[0] // sq_size
                    row = location[1] // sq_size

                    if column >= dimension or row >= dimension:
                        square_selected = ()
                        player_clicks = []
                        tutor_square_selected = ()
                        tutor_clicks = []
                        continue

                    clicked_square = (row, column)
                    current_turn_color = 'w' if game_state.white_to_move else 'b'

                    if event.button == 1:
                        tutor_square_selected = ()
                        tutor_clicks = []


                        if square_selected == clicked_square:  # User clicks same square or move log
                            square_selected = ()  # Deselects
                            player_clicks = []  # Clears player clicks
                        else:
                            square_selected = clicked_square
                            player_clicks.append(square_selected)  # Appends both 1st and 2nd clicks
                        if len(player_clicks) == 2:
                            move = ChessEngine.Move(player_clicks[0], player_clicks[1], game_state.board)
                            move_was_valid = False

                            for i in range(len(valid_moves)):
                                if move == valid_moves[i]:
                                    game_state.make_move(valid_moves[i])
                                    move_made = True
                                    animate = True
                                    move_was_valid = True
                                    square_selected = ()  # Resets user clicks
                                    player_clicks = []
                                    break

                            if not move_was_valid:
                                player_clicks = [square_selected]

                    elif event.button == 3:
                        square_selected = ()
                        player_clicks = []

                        if len(tutor_clicks) == 0:
                            piece = game_state.board[row][column]
                            if piece != "--" and piece[0] == current_turn_color:
                                tutor_square_selected = clicked_square
                                tutor_clicks = [clicked_square]
                                tutor_message = f"You right-clicked {piece} on row {row}, column {column}"
                            else:
                                tutor_square_selected = ()
                                tutor_clicks = []
                                tutor_message = f"You right-clicked an empty square on row {row}, column {column}"
                        else:
                            start_square = tutor_clicks[0]
                            end_square = clicked_square

                            tutor_move = ChessEngine.Move(start_square, end_square, game_state.board)
                            tutor_move_was_valid = False

                            for valid_move in valid_moves:
                                if tutor_move == valid_move:
                                    tutor_message = "Analyzing..."
                                    draw_game_state(screen, game_state, valid_moves, square_selected, tutor_square_selected, move_log_font, tutor_message)
                                    p.display.flip()

                                    tutor_payload = move_to_tutor_payload(valid_move)
                                    tutor_moves_for_tutor.append(tutor_payload)

                                    tutor_message = tutor.get_tutor_response(game_state, valid_move, valid_moves)

                                    tutor_move_was_valid = True
                                    break
                            
                            if tutor_move_was_valid:
                                tutor_square_selected = ()
                                tutor_clicks = []
                            else:
                                piece = game_state.board[row][column]

                                if piece != "--" and piece[0] == current_turn_color:
                                    tutor_square_selected = clicked_square
                                    tutor_clicks = [clicked_square]
                                    tutor_message = f"You right-clicked {piece} on row {row}, column {column}"
                                else:
                                    tutor_message = "That is not a legal move for selected piece"
                        

            # Key handlers
            elif event.type == p.KEYDOWN:
                if event.key == p.K_z:  # Undo move when 'z' is pressed
                    game_state.undo_move()
                    move_made = True
                    animate = False
                    game_over = False
                if event.key == p.K_r:  # Reset board when 'r is pressed
                    game_state = ChessEngine.GameState()
                    valid_moves = game_state.get_valid_moves()
                    square_selected = ()
                    player_clicks = []
                    move_made = False
                    animate = False
                    game_over = False

        # AI move finder
        if not game_over and not human_turn:
            AI_move = ChessAI.find_best_move(game_state, valid_moves)
            if AI_move is None:
                AI_move = ChessAI.find_random_move(valid_moves)
            game_state.make_move(AI_move)
            move_made = True
            animate = True

        if move_made:
            if animate:
                animate_move(game_state.move_log[-1], screen, game_state.board, clock)
            valid_moves = game_state.get_valid_moves()
            move_made = False
            animate = False

        draw_game_state(screen, game_state, valid_moves, square_selected, tutor_square_selected, move_log_font, tutor_message)

        if game_state.checkmate or game_state.stalemate:
            game_over = True
            if game_state.stalemate:
                text = 'Stalemate'
            else:
                text = 'Black wins by checkmate' if game_state.white_to_move else 'White wins by checkmate'
            draw_endgame_text(screen, text)

        clock.tick(max_fps)
        p.display.flip()


def draw_game_state(screen, game_state, valid_moves, square_selected, tutor_square_selected, move_log_font, tutor_message):
    """Responsible for all graphics within a current game state"""
    draw_board(screen)  # Draws squares on the board

    active_square = square_selected if square_selected != () else tutor_square_selected

    highlight_squares(screen, game_state, valid_moves, active_square)  # Adds highlighting
    draw_pieces(screen, game_state.board)  # Draws pieces on the board
    draw_move_log(screen, game_state, move_log_font)  # Draws the move log
    draw_tutor_panel(screen, tutor_message, move_log_font)


def draw_board(screen):
    """Draw squares on the board using a chess.com colouring pattern"""
    for row in range(dimension):
        for column in range(dimension):
            colour = colours[((row + column) % 2)]
            p.draw.rect(screen, colour, p.Rect(column * sq_size, row * sq_size, sq_size, sq_size))


def highlight_squares(screen, game_state, valid_moves,square_selected):
    """Highlights square selected and last move made"""
    # Highlights selected square
    if square_selected != ():
        row, column = square_selected
        if game_state.board[row][column][0] == ('w' if game_state.white_to_move else 'b'):  # Clicks on own piece
            s = p.Surface((sq_size, sq_size))
            s.set_alpha(70)  # Transperancy value; 0 transparent; 255 opaque
            s.fill(p.Color('yellow'))
            screen.blit(s, (column * sq_size, row * sq_size))

            for move in valid_moves:
                if move.start_row == row and move.start_column == column:
                    # if there's a piece to capture or an en passant move
                    if move.piece_captured != '--' or move.is_en_passant_move:
                        screen.blit(images['captureSquare'], (move.end_column * sq_size, move.end_row * sq_size))
                    else:
                        screen.blit(images['movementSquare'], (move.end_column * sq_size, move.end_row * sq_size))

    # Highlights last move
    if len(game_state.move_log) != 0:
        last_move = game_state.move_log[-1]
        start_row, start_column = last_move.start_row, last_move.start_column
        end_row, end_column = last_move.end_row, last_move.end_column
        s = p.Surface((sq_size, sq_size))
        s.set_alpha(70)
        s.fill(p.Color('yellow'))
        screen.blit(s, (start_column * sq_size, start_row * sq_size))
        screen.blit(s, (end_column * sq_size, end_row * sq_size))


def draw_pieces(screen, board):
    """Draws pieces on the board using the current GameState.board"""
    for row in range(dimension):
        for column in range(dimension):
            piece = board[row][column]
            if piece != '--':  # Add pieces if not an empty square
                screen.blit(images[piece], p.Rect(column * sq_size, row * sq_size, sq_size, sq_size))


def draw_move_log(screen, game_state, font):
    """Draws move log to the right of the screen"""
    move_log_area = p.Rect(board_width, 0, move_log_panel_width, move_log_panel_height)
    p.draw.rect(screen, p.Color('#2d2d2e'), move_log_area)
    move_log = game_state.move_log
    move_texts = []
    for i in range(0, len(move_log), 2):
        move_string = f'{i // 2 + 1}. {str(move_log[i])} '
        if i + 1 < len(move_log):  # Makes sure black has made a move
            move_string += f'{str(move_log[i + 1])} '
        move_texts.append(move_string)

    move_per_row = 2
    padding = 5
    line_spacing = 2
    text_y = padding
    for i in range(0, len(move_texts), move_per_row):
        text = ''
        for j in range(move_per_row):
            if i + j < len(move_texts):
                text += move_texts[i + j]
        text_object = font.render(text, True, p.Color('whitesmoke'))
        text_location = move_log_area.move(padding, text_y)
        screen.blit(text_object, text_location)
        text_y += text_object.get_height() + line_spacing


def animate_move(move, screen, board, clock):
    """Animates a move"""
    delta_row = move.end_row - move.start_row  # Change in row
    delta_column = move.end_column - move.start_column  # Change in column
    frames_per_square = 5  # Controls animation speed (frames to move one square)
    frame_count = (abs(delta_row) + abs(delta_column)) * frames_per_square

    for frame in range(frame_count + 1):  # Need +1 to complete the entire animation

        #  Frame/frame_count indicates how far along the action is
        row, column = (move.start_row + delta_row*frame/frame_count, move.start_column + delta_column*frame/frame_count)

        # Draw board and pieces for each frame of the animation
        draw_board(screen)
        draw_pieces(screen, board)

        # Erases the piece from its ending square
        colour = colours[(move.end_row + move.end_column) % 2]
        end_square = p.Rect(move.end_column * sq_size, move.end_row * sq_size, sq_size, sq_size)
        p.draw.rect(screen, colour, end_square)

        # Draws a captured piece onto the rectangle if a piece is captured
        if move.piece_captured != '--':
            if move.is_en_passant_move:
                en_passant_row = move.end_row + 1 if move.piece_captured[0] == 'b' else move.end_row - 1
                end_square = p.Rect(move.end_column * sq_size, en_passant_row * sq_size, sq_size, sq_size)
            screen.blit(images[move.piece_captured], end_square)

        # Draws moving piece
        screen.blit(images[move.piece_moved], p.Rect(column * sq_size, row * sq_size, sq_size, sq_size))

        p.display.flip()
        clock.tick(60)  # Controls fame rate per second for the animation


def draw_endgame_text(screen, text):
    font = p.font.SysFont('Helvetica', 32, True, False)
    text_object = font.render(text, True, p.Color('gray'), p.Color('mintcream'))
    text_location = p.Rect(0, 0, board_width, board_height).move(board_width/2 - text_object.get_width()/2,
                                                                 board_height/2 - text_object.get_height()/2)
    screen.blit(text_object, text_location)

    # Creates a shadowing effect
    text_object = font.render(text, True, p.Color('black'))
    screen.blit(text_object, text_location.move(2, 2))


def draw_tutor_panel(screen, text, font):
    """Draws tutor chat panel to the right of move log"""

    tutor_area = p.Rect(board_width + move_log_panel_width, 0, tutor_chat_panel_width, tutor_chat_panel_height)
    p.draw.rect(screen, p.Color("#272727"), tutor_area)

    words = text.split(' ')
    space = font.size(' ')[0]
    max_width = tutor_chat_panel_width - 20  # Padding of 10 on each
    x,y = tutor_area.left + 10, 10

    line = ""
    
    for word in words: 
        if font.size(line + word)[0] < max_width:
            line += word + " "
        else:
            text_surface = font.render(line, True, p.Color('whitesmoke'))
            screen.blit(text_surface, (x, y))
            line = word + " "
            y += font.get_height() + 5  # Move to next line with spacing
    screen.blit(font.render(line, True, p.Color('whitesmoke')), (x, y))

def move_to_tutor_payload(move):
    return{
        "notation": str(move),
        "start_square": move.get_rank_file(move.start_row, move.start_column),
        "end_square": move.get_rank_file(move.end_row, move.end_column),
        "start_row": move.start_row,
        "start_column":  move.start_column,
        "end_row":  move.end_row,
        "end_column":  move.end_column,
        "piece_moved":  move.piece_moved,
        "is_capture":  move.is_capture,
        "is_castle_move":  move.is_castle_move,
        "is_en_passant_move":  move.is_en_passant_move,
        "is_pawn_promotion":  move.is_pawn_promotion,
    }

if __name__ == '__main__':
    main()
import os
import ChessAI
from google import genai


class ChessTutor:
    def __init__(self):
        # configure Gemini API
        self.client = genai.Client(api_key = os.getenv("GEMINI_API_KEY"))
        self.model_id = "gemini-2.5-flash-lite"

    def get_tutor_response(self, gs, suggested_move, valid_moves):
        """
        Calulates move quality, and generates a response to the user explaining its strengths or weaknesses.
        """
        
        # perspective handling
        turn_multiplier = 1 if gs.white_to_move else -1

        # get AI's best move for comparison
        # uses ChessAI's existing find_best_move
        best_move = ChessAI.find_best_move(gs, valid_moves)

        # score suggested move
        gs.make_move(suggested_move)
        suggested_eval = ChessAI.score_board(gs)
        gs.undo_move() # undo hypothetical suggestion

        # score AI's best move 
        gs.make_move(best_move)
        best_eval = ChessAI.score_board(gs)
        gs.undo_move()

        # normalize
        s_score = suggested_eval * turn_multiplier
        b_score = best_eval * turn_multiplier
        score_diff = max(0, b_score - s_score)

        analysis = {
            'suggested_move': str(suggested_move),
            'best_move': str(best_move),
            'label': self._get_move_label(score_diff),
            'score_diff': round(score_diff, 2),
            'reasoning': self._generate_reasoning(suggested_move, s_score, b_score)
        }

        return self._query_gemini(analysis)
    
    def _get_move_label(self, diff):
        if diff <= 5:    return "Best"       # Loss of < 0.05 pawns
        if diff <= 20:   return "Excellent"  # Loss of < 0.20 pawns
        if diff <= 50:   return "Good"       # Loss of < 0.50 pawns
        if diff <= 100:  return "Inaccuracy" # Loss of ~ 1 pawn
        if diff <= 250:  return "Mistake"    # Loss of ~ 2.5 pawns
        return "Blunder"                     # Significant material/position loss
    
    def _generate_reasoning(self, move, s_score, b_score):
        reasoning = []
        pawn_diff = round((b_score - s_score) / 100, 2)

        # capture
        if move.is_capture:
            reasoning.append(f"Your move captures an opponent's {move.piece_captured[1]}.")

        # piece positioning using ChessAI maps
        piece = move.piece_moved
        start_val = ChessAI.piece_positions[piece][move.start_row][move.start_column]
        end_val = ChessAI.piece_positions[piece][move.end_row][move.end_column]

        if end_val > start_val:
            reasoning.append(f"Your move improves the position of your {piece[1]} from {start_val} to {end_val}.")

        if b_score - s_score > 50:
            reasoning.append(f"However, the best move improves your position by {pawn_diff} pawns compared to your move.")

        return reasoning
    
    def _query_gemini(self, data):
        prompt = f"""
        Role:
        You are the Chess.com game review coach. The goal is to provide a brief, professional evaluation of the move the player is considering.
        
        Context:
        - Suggested Move: {data['suggested_move']}
        - Classification: {data['label']}
        - Best Move: {data['best_move']}
        - Evaluation Change: {data['score_diff']}
        - Tactical Motifs: {", ".join(data['reasoning'])}

        1. START with the move classification in bold, e.g., "{data['suggested_move']} is a {data['label']}."
        2. TONE: Use a supportive yet objective tone. 
        - For "Best/Brilliant": Be enthusiastic ("You found the best move!").
        - For "Inaccuracy/Mistake": Be helpful ("You missed a better way to...").
        - For "Blunder/Miss": Be firm but encouraging ("You lose a piece, leading to a loss of material.").
        3. FOCUS: Prioritize the "Why." If a tactic like a fork or pin was missed or allowed, name it explicitly.
        4. BREVITY: Max 2-3 sentences. No fluff.

        Example Outputs:
        - "e4 is a book move. This is a solid opening choice that fights for control of the center."
        - "Re1 is a mistake. You had an opportunity to develop your knight and challenge the center."
        - "Bxf7+ is best! This sacrifice forces the king into the open and leads to a winning attack."
        - "d5 is a blunder. You are losing a pawn this way and weakening your king's safety."
        """

        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt
            )
            print(response.text.strip()+ "\n")
            return response.text.strip()
        except Exception as e:
            print(f"Error querying Gemini API: {e}")
            return "Sorry, I couldn't analyze that move right now."
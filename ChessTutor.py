import os
import ChessAI
from google import genai


class ChessTutor:
    def __init__(self):
        # configure Gemini API
        self.client = genai.Client(api_key = os.getenv("GEMINI_API_KEY"))
        self.model_id = "gemini-2.0-flash"

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
        if diff <= 0.2: return "Great"
        if diff <= 0.9: return "Good"
        if diff <= 2.0: return "Mistake"
        return "Blunder"
    
    def _generate_reasoning(self, move, s_score, b_score):
        reasoning = []

        # capture
        if move.is_capture:
            reasoning.append(f"Your move captures an opponent's {move.piece_captured[1]}.")

        # piece positioning using ChessAI maps
        piece = move.piece_moved
        start_val = ChessAI.piece_positions[piece][move.start_row][move.start_column]
        end_val = ChessAI.piece_positions[piece][move.end_row][move.end_column]

        if end_val > start_val:
            reasoning.append(f"Your move improves the position of your {piece[1]} from {start_val} to {end_val}.")

        if b_score - s_score > 1.2:
            reasoning.append(f"However, the best move improves your position by {round(b_score - s_score, 2)} points compared to your move.")

        return reasoning
    
    def _query_gemini(self, data):
        prompt = f"""
        You are a supportive chess tutor. The player is considering {data['suggested_move']}.
        
        Context:
        - Engine's top choice: {data['best_move']}
        - Move Quality: {data['label']}
        - Advantage Loss: {data['score_diff']}
        - Insights: {", ".join(data['reasoning'])}

        Provide a concise, encouraging explanation of the move's strengths and weaknesses based on the above information.
        Focus on whether they should commit to this move or consider alternatives, and why.
        Max 3-5 sentences. 
        """

        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt
            )
            return response.text.strip()
        except Exception as e:
            print(f"Error querying Gemini API: {e}")
            return "Sorry, I couldn't analyze that move right now."
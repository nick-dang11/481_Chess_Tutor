Operation Instructions:
To run this project, you will need a Gemini API key. 
1. Retrieve API key from https://aistudio.google.com/api-keys.
2. Create config.py in root directory (481_Chess_Tutor/config.py) and add your API key: GEMINI_API_KEY=your_API_key_here

This chess tutor is a friendly agent that advises moves, along with explanations based on the fundamentals and properties of chess. 
Using either chess.com or lichess.com, the explanations should include analysis as well as move ratings (great, best, brilliant).
This intends to ease newer players with a basic understanding of chess into understanding what moves are beneficial, and for what purpose.

Potential concepts that could scale the “score” of a move include:
Positioning
Gaining material
Maintaining material
Forced mate
Maintaining pressure
Controlling diagonals with bishops, files with rooks
and more concepts.

For Python specifically, we will use PyGame to create a visual representation that players are more familiar with, rather than just chess notation (Qd4).

We intend to use minimax with alpha-beta pruning, an adversarial search algorithm to determine the best moves by simulating future moves while not exceeding a specified depth to lower time complexity.

Week 1: Implement existing chess code and ensure the model understands game flow and logic.

Week 2: Implement model move detection and debugging 

Week 3: Implement move grading, may either advise a move to take based on the depth of its search, or perhaps review the move the player suggests. For both approaches, the model will grade it on a scale based on effectiveness.

Week 4: Debugging and polishing; testing, demoing, and integrating with chess.com or lichess.com.

Chess code provided courtesy of Katrina Alaimo https://github.com/katkaypettitt/chess/tree/main
See LICENSE for more details.
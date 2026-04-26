from google import genai

client = genai.Client()

def explain_move_with_gemini(analysis):
    prompt = f"""
You are a chess tutor.

Explain this move clearly.

Format:
Purpose:
Advantages:
- ...
- ...
Disadvantages:
- ...
- ...
Verdict:

Rules:
- Use simple English
- Be short (3–5 lines)
- Do NOT invent anything

Data:
Move played: {analysis['played_move']}
Best move: {analysis['best_move']}
Label: {analysis['label']}
Score difference: {analysis['score_diff_cp']}
Reasons:
- """ + "\n- ".join(analysis["reasons"])

    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt
    )

    return response.text
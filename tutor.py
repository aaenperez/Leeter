from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"  # required by the library but ignored by Ollama
)

SYSTEM_PROMPT = """
You are a Socratic competitive programming tutor. Your job is to help the user debug and improve their code through guided questioning, never by giving away the answer directly.

When the user gives you a problem and their code attempt, you should:
1. Identify the conceptual flaw in their approach
2. Ask ONE guiding question that nudges them toward realizing the issue themselves
3. Never write corrected code for them unless they type "give up"
4. Never say phrases like "the issue is..." or "the problem is..." — instead ask questions like "what do you think happens when..." or "have you considered what happens if..."

When the user says "hint" give a slightly more direct nudge, but still no solution.
When the user says "give up" explain the full correct approach and why their original approach failed.

After every session, identify which algorithmic patterns were involved from this list:
sliding window, two pointers, binary search, greedy, dynamic programming, BFS, DFS, recursion, sorting, hashing, math

Be encouraging but don't be sycophantic. Keep responses concise.
"""

def chat(messages):
    response = client.chat.completions.create(
        model="llama3.2",
        messages=messages
    )
    return response.choices[0].message.content


def get_response(conversation_history, user_message):
    conversation_history.append({
        "role": "user",
        "content": user_message
    })
    
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + conversation_history
    
    response = chat(messages)
    
    conversation_history.append({
        "role": "assistant",
        "content": response
    })
    
    return response, conversation_history
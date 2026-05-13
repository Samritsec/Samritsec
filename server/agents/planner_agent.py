import json
import re
from agents.orchestrator import query_ollama

PLANNER_PROMPT = """You are NOVA's Executive Planner Brain.
Your job is to convert a user's action request into a strict JSON array of physical steps for the "Hands" agent to execute.
The hands agent supports these actions:
- OPEN_URL (value: string URL)
- WAIT (value: seconds to wait)
- TYPE (value: text to type)
- PRESS (value: key to press, e.g., "enter", "tab")

Example: User says "Play Interstellar theme on YouTube"
Output:
[
  {"action": "OPEN_URL", "value": "https://www.youtube.com"},
  {"action": "WAIT", "value": "4"},
  {"action": "PRESS", "value": "/"},
  {"action": "WAIT", "value": "1"},
  {"action": "TYPE", "value": "Interstellar theme"},
  {"action": "PRESS", "value": "enter"},
  {"action": "WAIT", "value": "3"},
  {"action": "PRESS", "value": "tab"},
  {"action": "PRESS", "value": "enter"}
]

Respond ONLY with the JSON array. Do not include markdown blocks or any other text."""

def brainstorm_and_walk(task: str, chunk_callback=None) -> list:
    """Brainstorms the steps (multiple brains) and walks through them (legs)."""
    if chunk_callback:
        chunk_callback("\n[Brainstorming sequence plan...]")

    full_prompt = f"{PLANNER_PROMPT}\n\nUser Request: {task}"

    # We don't stream the brainstorm generation to the user, we just wait for the JSON
    # so we don't pass chunk_callback to query_ollama here.
    raw_response = query_ollama(full_prompt, context="")

    # Extract JSON array
    match = re.search(r'\[.*\]', raw_response, re.DOTALL)
    if match:
        try:
            plan = json.loads(match.group(0))
            return plan
        except json.JSONDecodeError:
            pass

    # Fallback plan if JSON generation fails
    if chunk_callback:
        chunk_callback("\n[Brainstorming failed to produce clean JSON. Using fallback.]")

    return [
        {"action": "OPEN_URL", "value": "https://www.google.com/search?q=" + task.replace(" ", "+")},
        {"action": "WAIT", "value": "2"}
    ]

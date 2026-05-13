import time
import webbrowser
from pynput.keyboard import Controller as KeyboardController, Key
from pynput.mouse import Controller as MouseController

keyboard = KeyboardController()
mouse = MouseController()

def execute_action_plan(plan_steps, chunk_callback=None):
    """
    Executes a sequence of steps.
    Steps format: list of dicts e.g. [{"action": "OPEN_URL", "value": "https://youtube.com"}, {"action": "WAIT", "value": 3}]
    """
    for step in plan_steps:
        action = step.get("action")
        value = step.get("value")

        if chunk_callback:
            chunk_callback(f"\n[Executing Hand Action]: {action} -> {value}")

        if action == "OPEN_URL":
            webbrowser.open(value)
        elif action == "WAIT":
            try:
                time.sleep(float(value))
            except:
                time.sleep(1)
        elif action == "TYPE":
            keyboard.type(str(value))
        elif action == "PRESS":
            if value.lower() == "enter":
                keyboard.press(Key.enter)
                keyboard.release(Key.enter)
            elif value.lower() == "tab":
                keyboard.press(Key.tab)
                keyboard.release(Key.tab)
            elif value.lower() == "space":
                keyboard.press(Key.space)
                keyboard.release(Key.space)
            else:
                keyboard.press(value)
                keyboard.release(value)

    if chunk_callback:
        chunk_callback(f"\n[Hand Execution Complete]")

    return "I have executed the physical sequence using my hands, sir."

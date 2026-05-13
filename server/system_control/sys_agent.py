import os
import platform
import subprocess
import webbrowser

def execute_system_command(command: str) -> str:
    """Executes a basic system command and returns a status string."""
    command = command.lower().strip()

    # Web surfing capabilities
    if "open youtube" in command:
        webbrowser.open("https://www.youtube.com")
        return "I have opened YouTube for you, sir."
    elif "open google" in command:
        webbrowser.open("https://www.google.com")
        return "I have opened Google for you, sir."
    elif "open github" in command:
        webbrowser.open("https://github.com/Samritsec")
        return "I have opened your GitHub profile, sir."
    elif "open linkedin" in command:
        webbrowser.open("https://www.linkedin.com/in/samrit-shrestha")
        return "I have opened your LinkedIn profile, sir."

    # Basic system apps (Windows specific since user is on Windows)
    if platform.system() == "Windows":
        if "open notepad" in command:
            os.startfile("notepad.exe")
            return "I have launched Notepad, sir."
        elif "open calculator" in command:
            os.startfile("calc.exe")
            return "I have launched the Calculator, sir."
        elif "open browser" in command:
            webbrowser.open("https://www.google.com")
            return "I have launched your default browser, sir."

    return None

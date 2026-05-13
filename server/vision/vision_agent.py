import base64
import io
import requests
from PIL import ImageGrab

OLLAMA_URL = "http://localhost:11434/api/generate"
# Use a local vision model like llava for image analysis
VISION_MODEL = "llava"

def capture_and_analyze_screen(task_context: str, chunk_callback=None) -> str:
    """Takes a screenshot and asks the local vision model to verify if the task succeeded."""
    if chunk_callback:
        chunk_callback("\n[Activating optic sensors to verify task completion...]")

    try:
        # Take screenshot
        screenshot = ImageGrab.grab()

        # Convert to base64
        buffered = io.BytesIO()
        screenshot.save(buffered, format="JPEG", quality=70)
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

        prompt = f"You are NOVA, an AI verifying a task. The user requested: '{task_context}'. Look at this screenshot of the desktop. Briefly confirm if it looks like the task was completed successfully based on what is visible on the screen."

        payload = {
            "model": VISION_MODEL,
            "prompt": prompt,
            "images": [img_str],
            "stream": bool(chunk_callback)
        }

        response = requests.post(OLLAMA_URL, json=payload, timeout=120, stream=bool(chunk_callback))

        if response.status_code == 200:
            if chunk_callback:
                chunk_callback("\n[Visual Verification]: ")
                full_response = ""
                for line in response.iter_lines():
                    if line:
                        import json
                        data = json.loads(line)
                        chunk = data.get("response", "")
                        if chunk:
                            chunk_callback(chunk)
                            full_response += chunk
                return full_response
            else:
                import json
                return response.json().get("response", "Visual analysis complete.")
        elif response.status_code == 404:
            # Attempt to auto-pull the model in the background so it works next time
            import threading
            def pull_model():
                try:
                    requests.post("http://localhost:11434/api/pull", json={"model": VISION_MODEL}, timeout=600)
                except:
                    pass
            threading.Thread(target=pull_model, daemon=True).start()

            msg = f"\n[Vision Disabled]: The vision model '{VISION_MODEL}' is currently not installed. I have initiated a background download of my optic core. It will be ready shortly."
            if chunk_callback: chunk_callback(msg)
            return msg
        else:
            return f"\n[Vision Error]: Status code {response.status_code}"

    except Exception as e:
        msg = f"\n[Optic Sensor Failure]: {e}"
        if chunk_callback: chunk_callback(msg)
        return msg

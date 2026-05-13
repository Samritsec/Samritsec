import asyncio
import json
import threading
import customtkinter as ctk
import websockets
import math
import time

# Set modern UI theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

WS_URL = "ws://127.0.0.1:8000/ws/chat"

class NovaClientUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("NOVA - Neural Operative Virtual Assistant")
        self.geometry("900x600")

        self.ws = None
        self.loop = asyncio.new_event_loop()
        self.is_speaking = False
        self.animation_step = 0

        self.setup_ui()

        # Start websocket thread
        threading.Thread(target=self.start_async_loop, daemon=True).start()

        # Start animation loop
        self.update_animation()

    def setup_ui(self):
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)

        # Left panel (Visualizer / Jarvis Orb)
        self.left_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#1a1a1a")
        self.left_frame.grid(row=0, column=0, sticky="nsew")

        self.orb_canvas = ctk.CTkCanvas(self.left_frame, width=200, height=200, bg="#1a1a1a", highlightthickness=0)
        self.orb_canvas.pack(expand=True)
        self.draw_orb(50)

        # Right panel (Chat interface)
        self.right_frame = ctk.CTkFrame(self, corner_radius=0)
        self.right_frame.grid(row=0, column=1, sticky="nsew")
        self.right_frame.grid_rowconfigure(0, weight=1)
        self.right_frame.grid_columnconfigure(0, weight=1)

        self.chat_box = ctk.CTkTextbox(self.right_frame, font=("Consolas", 14), wrap="word", state="disabled")
        self.chat_box.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.input_frame = ctk.CTkFrame(self.right_frame, fg_color="transparent")
        self.input_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.input_frame.grid_columnconfigure(0, weight=1)

        self.entry = ctk.CTkEntry(self.input_frame, placeholder_text="Command NOVA...", font=("Consolas", 14), height=40)
        self.entry.grid(row=0, column=0, sticky="ew")
        self.entry.bind("<Return>", self.send_message)

        self.mic_btn = ctk.CTkButton(self.input_frame, text="🎤", width=40, height=40, command=self.toggle_listening)
        self.mic_btn.grid(row=0, column=1, padx=(10, 0))

        self.send_btn = ctk.CTkButton(self.input_frame, text="Send", width=80, height=40, command=lambda: self.send_message(None))
        self.send_btn.grid(row=0, column=2, padx=(10, 0))

        self.append_chat("SYSTEM", "NOVA Interface Initialized. Awaiting Connection...")

    def draw_orb(self, radius):
        self.orb_canvas.delete("all")
        x, y = 100, 100

        # Draw glowing layers
        colors = ["#001133", "#002266", "#0044cc", "#3388ff", "#99ccff"]
        steps = len(colors)

        for i in range(steps):
            r = radius + (steps - i) * 5
            self.orb_canvas.create_oval(x-r, y-r, x+r, y+r, fill=colors[i], outline="")

        self.orb_canvas.create_oval(x-radius, y-radius, x+radius, y+radius, fill="#ffffff", outline="")

    def update_animation(self):
        if self.is_speaking:
            # Pulsing animation
            self.animation_step += 0.2
            radius = 50 + math.sin(self.animation_step) * 15
        else:
            # Idle animation
            self.animation_step += 0.05
            radius = 50 + math.sin(self.animation_step) * 2

        self.draw_orb(radius)
        self.after(30, self.update_animation)

    def append_chat(self, sender, text):
        self.chat_box.configure(state="normal")
        self.chat_box.insert("end", f"[{sender}] {text}\n\n")
        self.chat_box.see("end")
        self.chat_box.configure(state="disabled")

    def start_async_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.connect_ws())

    async def connect_ws(self):
        try:
            async with websockets.connect(WS_URL) as ws:
                self.ws = ws
                # Send fake token for initial connection
                await ws.send(json.dumps({"token": "dev_token_placeholder"}))

                while True:
                    response_str = await ws.recv()
                    data = json.loads(response_str)

                    if data.get("type") == "connected":
                        self.after(0, self.append_chat, "NOVA", "Connection established. Secure channel active.")
                    elif data.get("type") == "response":
                        msg = data.get("content", "")
                        self.after(0, self.append_chat, "NOVA", msg)
                        self.after(0, self.trigger_speaking_animation)

        except Exception as e:
            self.after(0, self.append_chat, "ERROR", f"Connection failed: {e}")

    def trigger_speaking_animation(self):
        self.is_speaking = True
        # Keep pulsing for 2 seconds to simulate talking
        self.after(2000, self.stop_speaking_animation)

    def stop_speaking_animation(self):
        self.is_speaking = False

    def toggle_listening(self):
        self.mic_btn.configure(fg_color="red")
        self.append_chat("SYSTEM", "Listening...")
        try:
            from voice.listener import listen_and_transcribe
            listen_and_transcribe(self._on_transcription)
        except Exception as e:
            self.append_chat("ERROR", f"Could not initialize microphone: {e}")
            self.mic_btn.configure(fg_color=["#3a7ebf", "#1f538d"]) # Reset color

    def _on_transcription(self, text):
        def update_ui():
            self.mic_btn.configure(fg_color=["#3a7ebf", "#1f538d"]) # Reset color
            if text and "Error" not in text and "Indecipherable" not in text:
                self.entry.delete(0, "end")
                self.entry.insert(0, text)
                self.send_message(None)
            else:
                self.append_chat("SYSTEM", text)
        self.after(0, update_ui)

    def send_message(self, event):
        msg = self.entry.get().strip()
        if not msg:
            return

        self.entry.delete(0, "end")
        self.append_chat("SAM", msg)

        if self.ws:
            payload = json.dumps({"message": msg})
            asyncio.run_coroutine_threadsafe(self.ws.send(payload), self.loop)

if __name__ == "__main__":
    app = NovaClientUI()
    app.mainloop()

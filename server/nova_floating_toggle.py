import customtkinter as ctk
from PIL import Image
import os
import subprocess
import sys

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ICON_PATH = os.path.join(BASE_DIR, "assets", "icon.png")

class NovaFloatingToggle(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("NOVA Toggle")
        self.geometry("80x80")

        # Make frameless and always on top
        self.overrideredirect(True)
        self.attributes("-topmost", True)

        # Transparent background if possible (Windows)
        self.attributes("-transparentcolor", "black")
        self.configure(fg_color="black")

        # Position on bottom right screen
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = screen_width - 100
        y = screen_height - 150
        self.geometry(f"+{x}+{y}")

        # Load the image
        try:
            self.nova_image = ctk.CTkImage(light_image=Image.open(ICON_PATH),
                                           dark_image=Image.open(ICON_PATH),
                                           size=(60, 60))

            self.button = ctk.CTkButton(self, text="", image=self.nova_image,
                                        width=60, height=60,
                                        fg_color="transparent", hover_color="#222222",
                                        command=self.launch_nova)
            self.button.pack(expand=True, fill="both", padx=10, pady=10)
        except Exception as e:
            print(f"Error loading image: {e}")
            self.button = ctk.CTkButton(self, text="N", width=60, height=60,
                                        command=self.launch_nova)
            self.button.pack(expand=True, fill="both", padx=10, pady=10)

        # Dragging functionality
        self.bind("<ButtonPress-1>", self.start_move)
        self.bind("<ButtonRelease-1>", self.stop_move)
        self.bind("<B1-Motion>", self.do_move)

        # Allow closing the widget with right click
        self.bind("<Button-3>", self.close_widget)

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def stop_move(self, event):
        self.x = None
        self.y = None

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay
        self.geometry(f"+{x}+{y}")

    def launch_nova(self):
        print("Launching NOVA...")
        try:
            # Launch client and server
            client_script = os.path.join(BASE_DIR, "nova_client.py")
            server_script = os.path.join(BASE_DIR, "server_v6.py")

            subprocess.Popen([sys.executable, server_script])
            subprocess.Popen([sys.executable, client_script])
        except Exception as e:
            print(f"Error launching NOVA: {e}")

    def close_widget(self, event):
        self.destroy()

if __name__ == "__main__":
    app = NovaFloatingToggle()
    app.mainloop()

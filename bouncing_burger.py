import tkinter as tk
from PIL import Image, ImageTk
import random
import os

"""
Bouncing Burger Animation (Resilient Version)
--------------------------------------------
• Shows a burger image that bounces, or an 🍔 emoji fallback if the file is missing.
• Student name overlays the sprite and changes colour on each rebound.
• <space> toggles pause / resume.

Requirements
------------
    pip install pillow
Place a PNG/JPG named as indicated below in the same folder as this script. If the
file is missing the program switches to the emoji sprite automatically.
"""

# ── USER SETTINGS ─────────────────────────────────────────────────────────────
STUDENT_NAME = "Kenn Martin C. De La Cierra"      # your name
BGR_IMG_PATH = "burger.png"                       # sprite file (.png in your case)
CANVAS_W, CANVAS_H = 800, 600                     # window size (px)
FPS = 60                                           # frames per second
EMOJI_SIZE = 64                                    # font‑pt for 🍔 fallback
# ──────────────────────────────────────────────────────────────────────────────

FRAME_DELAY = int(1000 / FPS)                      # ms per frame

class BouncingBurgerApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title(f"Bouncing Burger – {STUDENT_NAME}")
        self.canvas = tk.Canvas(root, width=CANVAS_W, height=CANVAS_H, bg="white")
        self.canvas.pack()

        # --------------------------------------------------------------
        # 1. Try to load the burger image. Fallback to emoji if missing.
        # --------------------------------------------------------------
        self.using_emoji = False
        if os.path.exists(BGR_IMG_PATH):
            pil_img = Image.open(BGR_IMG_PATH)
            # scale image if too tall (max 20% of window height)
            max_h = int(CANVAS_H * 0.2)
            if pil_img.height > max_h:
                scale = max_h / pil_img.height
                pil_img = pil_img.resize((int(pil_img.width * scale), max_h), Image.LANCZOS)
            self.burger_tk = ImageTk.PhotoImage(pil_img)
        else:
            self.using_emoji = True

        # --------------------------------------------------------------
        # 2. Initial position & velocity
        # --------------------------------------------------------------
        self.x, self.y = CANVAS_W // 2, CANVAS_H // 2
        self.dx, self.dy = 4, 3  # pixels per frame

        # --------------------------------------------------------------
        # 3. Create canvas items
        # --------------------------------------------------------------
        if self.using_emoji:
            self.sprite_id = self.canvas.create_text(self.x, self.y, text="🍔",
                                                     font=("Segoe UI Emoji", EMOJI_SIZE))
            sprite_bbox = self.canvas.bbox(self.sprite_id)
            self.sprite_half_w = (sprite_bbox[2] - sprite_bbox[0]) // 2
            self.sprite_half_h = (sprite_bbox[3] - sprite_bbox[1]) // 2
        else:
            self.sprite_id = self.canvas.create_image(self.x, self.y, image=self.burger_tk)
            self.sprite_half_w = self.burger_tk.width() // 2
            self.sprite_half_h = self.burger_tk.height() // 2

        self.text_id = self.canvas.create_text(self.x, self.y, text=STUDENT_NAME,
                                               font=("Helvetica", 20, "bold"), fill="black")

        # --------------------------------------------------------------
        self.paused = False
        root.bind("<space>", self.toggle_pause)
        self.animate()

    # --------------------------------------------------------------
    def toggle_pause(self, _ev=None):
        self.paused = not self.paused

    # --------------------------------------------------------------
    def animate(self):
        if not self.paused:
            self.x += self.dx
            self.y += self.dy

            # collision detection using sprite_half_w/h
            if self.x + self.sprite_half_w >= CANVAS_W or self.x - self.sprite_half_w <= 0:
                self.dx *= -1
                self.change_text_colour()
            if self.y + self.sprite_half_h >= CANVAS_H or self.y - self.sprite_half_h <= 0:
                self.dy *= -1
                self.change_text_colour()

            # move items
            self.canvas.coords(self.sprite_id, self.x, self.y)
            self.canvas.coords(self.text_id, self.x, self.y)

        self.root.after(FRAME_DELAY, self.animate)

    # --------------------------------------------------------------
    def change_text_colour(self):
        colour = "#" + "".join(f"{random.randint(64, 255):02x}" for _ in range(3))
        self.canvas.itemconfig(self.text_id, fill=colour)


# ── RUN ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app = BouncingBurgerApp(root)
    root.mainloop()

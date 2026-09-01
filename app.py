"""
PROFILE QUEST - a small retro menu that shows off Justin Dunbar's profile.

Two interactions, that's it:

    UP / DOWN ... hover over an entry
    ENTER ....... reveal it

    python app.py
"""

import tkinter as tk

WIDTH, HEIGHT = 720, 520
MONO = "Courier New"

# --------------------------------------------------------------- daygreen
INK = "#1f4d2a"       # darkest green, used as ink
MOSS = "#3f8f4f"      # mid green
LEAF = "#7ed957"      # bright lime accent
PAGE = "#e8f6df"      # pale leaf background
LINE = "#cfe6bd"      # retro grid lines
CARD = "#ffffff"
SHADOW = "#a8d39a"
GOLD = "#f7d94c"

ENTRIES = [
    ("CODENAME", "JUSTIN DUNBAR"),
    ("MAJOR", "COMPUTER SCIENCE"),
    ("TECH INTEREST", "SYSTEM CONFIGURATIONS"),
    ("DESIRED SKILL", "ENHANCED FULL STACK DEVELOPMENT"),
]

CARD_X, CARD_W = 60, WIDTH - 120
CARD_Y, CARD_H, CARD_GAP = 140, 62, 14


class ProfileMenu:
    def __init__(self, root):
        self.root = root
        root.title("PROFILE QUEST // Justin Dunbar")
        root.resizable(False, False)

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT,
                                bg=PAGE, highlightthickness=0)
        self.canvas.pack()

        self.hover = 0                       # which entry the cursor is on
        self.shown = [0] * len(ENTRIES)      # typewriter progress per entry
        self.revealed = [False] * len(ENTRIES)
        self.frame = 0

        root.bind("<Up>", lambda e: self.move(-1))
        root.bind("<Down>", lambda e: self.move(1))
        root.bind("<Return>", lambda e: self.reveal())
        root.bind("<Escape>", lambda e: root.destroy())

        self.draw_background()
        self.tick()

    # ------------------------------------------------------------ actions
    def move(self, step):
        self.hover = (self.hover + step) % len(ENTRIES)

    def reveal(self):
        self.revealed[self.hover] = True

    # ------------------------------------------------------------ drawing
    def draw_background(self):
        c = self.canvas
        for x in range(0, WIDTH, 24):
            c.create_line(x, 0, x, HEIGHT, fill=LINE)
        for y in range(0, HEIGHT, 24):
            c.create_line(0, y, WIDTH, y, fill=LINE)

        c.create_rectangle(36, 36, WIDTH - 36, 104, fill=INK, outline=LEAF, width=3)
        c.create_text(WIDTH / 2, 60, text="PROFILE QUEST", fill=LEAF,
                      font=(MONO, 20, "bold"))
        c.create_text(WIDTH / 2, 84, text="HOWARD UNIVERSITY  //  PLAYER FILE",
                      fill=SHADOW, font=(MONO, 9, "bold"))

    def draw_cards(self):
        c = self.canvas
        c.delete("ui")

        for i, (label, value) in enumerate(ENTRIES):
            y = CARD_Y + i * (CARD_H + CARD_GAP)
            on = i == self.hover

            c.create_rectangle(CARD_X + 5, y + 5, CARD_X + CARD_W + 5, y + CARD_H + 5,
                               fill=SHADOW, outline="", tags="ui")
            c.create_rectangle(CARD_X, y, CARD_X + CARD_W, y + CARD_H,
                               fill=CARD, outline=LEAF if on else LINE,
                               width=4 if on else 2, tags="ui")

            # blinking pixel arrow on the hovered row
            if on and self.frame // 8 % 2 == 0:
                ax, ay = CARD_X - 26, y + CARD_H / 2
                c.create_polygon(ax, ay - 9, ax + 14, ay, ax, ay + 9,
                                 fill=INK, outline="", tags="ui")

            c.create_rectangle(CARD_X + 12, y + 12, CARD_X + 42, y + CARD_H - 12,
                               fill=GOLD if self.revealed[i] else LINE,
                               outline=INK, width=2, tags="ui")
            c.create_text(CARD_X + 27, y + CARD_H / 2,
                          text=label[0] if self.revealed[i] else "?",
                          fill=INK, font=(MONO, 13, "bold"), tags="ui")

            c.create_text(CARD_X + 56, y + 16, anchor="nw", text=label,
                          fill=MOSS, font=(MONO, 9, "bold"), tags="ui")

            if self.revealed[i]:
                text = value[: self.shown[i]]
                if self.shown[i] < len(value) and self.frame // 6 % 2 == 0:
                    text += "_"
                color = INK
            else:
                text = "PRESS ENTER TO REVEAL" if on else "- - - LOCKED - - -"
                color = MOSS if on else SHADOW
            c.create_text(CARD_X + 56, y + 32, anchor="nw", text=text,
                          fill=color, font=(MONO, 12, "bold"), tags="ui")

        done = all(self.revealed)
        footer = ("PROFILE COMPLETE!" if done
                  else "UP / DOWN  HOVER          ENTER  REVEAL          ESC  QUIT")
        c.create_text(WIDTH / 2, HEIGHT - 40, text=footer,
                      fill=INK if done else MOSS, font=(MONO, 10, "bold"), tags="ui")

    # --------------------------------------------------------------- loop
    def tick(self):
        self.frame += 1
        for i, (_, value) in enumerate(ENTRIES):
            if self.revealed[i] and self.shown[i] < len(value):
                self.shown[i] += 1
        self.draw_cards()
        self.root.after(33, self.tick)


def main():
    root = tk.Tk()
    ProfileMenu(root)
    root.mainloop()


if __name__ == "__main__":
    main()

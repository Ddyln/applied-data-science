from manim import *


# ── Small grid icons (embedding columns) beside encoder ───────────────
def mini_grid(rows=4, cols=4, cell=0.13, color=GREY_A):
    g = VGroup()
    for r in range(rows):
        for c in range(cols):
            sq = Square(
                side_length=cell, color=color, fill_opacity=0.35, stroke_width=0.8
            )
            sq.move_to([c * (cell + 0.02), -r * (cell + 0.02), 0])
            g.add(sq)
    return g

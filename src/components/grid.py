from manim import *


# ── Small grid icons (embedding columns) beside encoder ───────────────
def mini_grid(
    rows=3, cols=3, cell=0.13, edge_color=GREY_A, fill_color=None, opacity=None
):
    g = VGroup()
    for r in range(rows):
        for c in range(cols):
            sq = Square(
                side_length=cell, color=edge_color, fill_opacity=0.35, stroke_width=0.8
            ).set_fill(color=fill_color, opacity=opacity)
            sq.move_to([c * (cell + 0.02), -r * (cell + 0.02), 0])
            g.add(sq)
    return g


__all__ = ["mini_grid"]

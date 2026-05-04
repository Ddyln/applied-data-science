from manim import *

#  ─── Colour palette for Navigator Bar ──────────────────────────────────────────
NAV_COLORS  = [PURPLE, ORANGE, BLUE_B, GOLD_B]
NAV_LABELS  = ["① Retrieval", "② Prediction", "③ Fusion", "④ Optimizer"]
NAV_DIM_BG  = "#2E2E2B"
NAV_DIM_TXT = "#6A6A62"

# ─── Navigator bar ───────────────────────────────────────────────────────────────
def make_nav_bar(active_idx: int = -1):
    pills = VGroup()
    for i, (lbl, col) in enumerate(zip(NAV_LABELS, NAV_COLORS)):
        active = (i == active_idx)
        box = RoundedRectangle(
            width=2.90, height=0.48, corner_radius=0.24,
            color=col if active else NAV_DIM_BG,
            fill_color=col if active else NAV_DIM_BG,
            fill_opacity=0.28 if active else 0.55,
        )
        txt = Text(lbl, font_size=15,
                   color=col if active else NAV_DIM_TXT)
        txt.move_to(box)
        pills.add(VGroup(box, txt))
    pills.arrange(RIGHT, buff=0.22)
    pills.move_to([0.0, -3.56, 0])
    return pills

"""Function steps for scenes 12-16."""

from manim import *

import formulas

from utils.navigator_bar import make_nav_bar

def play_scene12_lagrangian(scene):
    # ══════════════════════════════════════════════════════════════════════
    #  ACT 1  (0s – 15s): Objective trapped by 3 constraint walls
    # ══════════════════════════════════════════════════════════════════════
    title = Text("Lagrangian Formulation", font_size=40).to_edge(UP, buff=0.45)

    # Objective formula in the centre
    obj = MathTex(
        r"\min \sum_{i,j} c_{i,j}\, x_{i,j}",
        font_size=44,
        color=GOLD,
    ).move_to(ORIGIN)

    scene.play(FadeIn(title, shift=DOWN * 0.2))
        
    # ── Add Navigator Bar (highlight tab 1: Training/Prediction) ────
    nav_line = Line([-7.00, -3.10, 0], [7.00, -3.10, 0],
                    stroke_width=0.7, color=GREY_B, stroke_opacity=0.55)
    nav_bar  = make_nav_bar(active_idx=3)
    scene.play(Create(nav_line), FadeIn(nav_bar), run_time=0.5)

    scene.play(Write(obj), run_time=1.2)
    scene.wait(0.5)

    # Three constraint wall boxes flying in from 3 directions
    def wall(label, color, w=3.8, h=0.90):
        rect = RoundedRectangle(
            width=w,
            height=h,
            corner_radius=0.12,
            color=color,
            fill_color=color,
            fill_opacity=0.18,
            stroke_width=2.5,
        )
        lbl = Text(label, font_size=19, color=color).move_to(rect)
        return VGroup(rect, lbl)

    wall_q = wall("Quality Constraint", BLUE_B)
    wall_cap = wall("Capacity Constraint", RED_B)
    wall_asgn = wall("Assignment Constraint", GREEN_B)

    # Start positions (off-screen)
    wall_q.move_to(LEFT * 9 + UP * 1.5)
    wall_cap.move_to(RIGHT * 9 + DOWN * 0.0)
    wall_asgn.move_to(DOWN * 5 + DOWN * 0.5)

    # End positions (surrounding the objective)
    wall_q_end = obj.get_center() + UP * 1.35
    wall_cap_end = obj.get_center() + RIGHT * 3.80
    wall_asgn_end = obj.get_center() + DOWN * 1.35

    scene.add(wall_q, wall_cap, wall_asgn)
    scene.play(
        wall_q.animate.move_to(wall_q_end),
        wall_cap.animate.move_to(wall_cap_end),
        wall_asgn.animate.move_to(wall_asgn_end),
        run_time=1.1,
    )

    # Objective shakes (trapped feeling)
    scene.play(
        obj.animate.shift(RIGHT * 0.12),
        run_time=0.10,
    )
    for _ in range(3):
        scene.play(obj.animate.shift(LEFT * 0.12), run_time=0.08)
        scene.play(obj.animate.shift(RIGHT * 0.12), run_time=0.08)
    scene.play(obj.animate.shift(LEFT * 0.06), run_time=0.06)
    scene.wait(0.5)

    # ══════════════════════════════════════════════════════════════════════
    #  ACT 2  (15s – 25s): Constraint walls move right and stay visible
    # ══════════════════════════════════════════════════════════════════════
    wall_q_right = RIGHT * 4.9 + UP * 1.9
    wall_cap_right = RIGHT * 4.9 + UP * 0.45
    wall_asgn_right = RIGHT * 4.9 + DOWN * 1.0

    scene.play(
        wall_q.animate.move_to(wall_q_right),
        wall_cap.animate.move_to(wall_cap_right),
        wall_asgn.animate.move_to(wall_asgn_right),
        run_time=0.85,
    )
    scene.wait(0.25)

    # Objective anchor for the full Lagrangian block
    obj_anchor = UP * 2.2 + LEFT

    # ══════════════════════════════════════════════════════════════════════
    #  ACT 3  (25s – 45s): Build Lagrangian line by line, colour coded
    # ══════════════════════════════════════════════════════════════════════
    # Line 0 – header + cost term (GOLD)
    line0 = MathTex(
        r"\mathcal{L}(x,\lambda_1,\lambda_2,\mu)",  # [0]
        r"=",  # [1]
        r"\sum_{i,j} c_{i,j}\,x_{i,j}",  # [2]  cost – GOLD
        font_size=34,
    )
    line0[2].set_color(GOLD)
    line0.next_to(obj_anchor + DOWN * 0.65, RIGHT, buff=0.0).to_edge(LEFT, buff=0.55)
    line0.shift(DOWN * 0.05)

    # Line 1 – quality penalty (BLUE_B)
    line1 = MathTex(
        r"+\;",  # [0]
        r"\lambda_1",  # [1]  ← Indicate
        r"\!\left(\alpha - \tfrac{1}{N}\sum_{i,j} a_{i,j}\,x_{i,j}\right)",  # [2]
        font_size=34,
    )
    line1[0].set_color(BLUE_B)
    line1[1].set_color(BLUE_B)
    line1[2].set_color(BLUE_B)
    line1.next_to(line0, DOWN, aligned_edge=LEFT, buff=0.28)

    # Line 2 – capacity penalty (RED_B)
    line2 = MathTex(
        r"+\;",  # [0]
        r"\sum_j \lambda_{2,j}",  # [1]  ← Indicate
        r"\!\left(\sum_i x_{i,j} - L_j\right)",  # [2]
        font_size=34,
    )
    line2[0].set_color(RED_B)
    line2[1].set_color(RED_B)
    line2[2].set_color(RED_B)
    line2.next_to(line1, DOWN, aligned_edge=LEFT, buff=0.28)

    # Line 3 – assignment penalty (GREEN_B)
    line3 = MathTex(
        r"+\;",  # [0]
        r"\sum_i \mu_i",  # [1]  ← Indicate
        r"\!\left(\sum_j x_{i,j} - 1\right)",  # [2]
        font_size=34,
    )
    line3[0].set_color(GREEN_B)
    line3[1].set_color(GREEN_B)
    line3[2].set_color(GREEN_B)
    line3.next_to(line2, DOWN, aligned_edge=LEFT, buff=0.28)

    # --- Animate line by line ---
    # Line 0: header appears; objective morphs into cost term
    scene.play(Write(line0[0]), Write(line0[1]), run_time=0.9)
    scene.play(ReplacementTransform(obj, line0[2]), run_time=0.9)
    scene.play(Indicate(line0[2], color=GOLD, scale_factor=1.12), run_time=0.6)

    # Line 1: quality penalty
    scene.play(FadeIn(line1[0]), Write(line1[1]), run_time=0.5)
    arr_q = Arrow(
        line1.get_right() + RIGHT * 0.12,
        wall_q.get_left() + LEFT * 0.02,
        buff=0.10,
        stroke_width=3,
        color=BLUE_B,
    )
    scene.play(
        Indicate(line1[1], color=BLUE_B, scale_factor=1.3),
        GrowArrow(arr_q),
        Indicate(wall_q, color=BLUE_B, scale_factor=1.03),
        run_time=0.6,
    )
    scene.play(Write(line1[2]), run_time=0.9)

    # Line 2: capacity penalty
    scene.play(FadeIn(line2[0]), Write(line2[1]), run_time=0.5)
    arr_cap = Arrow(
        line2.get_right() + RIGHT * 0.12,
        wall_cap.get_left() + LEFT * 0.02,
        buff=0.10,
        stroke_width=3,
        color=RED_B,
    )
    scene.play(
        Indicate(line2[1], color=RED_B, scale_factor=1.3),
        GrowArrow(arr_cap),
        Indicate(wall_cap, color=RED_B, scale_factor=1.03),
        run_time=0.6,
    )
    scene.play(Write(line2[2]), run_time=0.9)

    # Line 3: assignment penalty
    scene.play(FadeIn(line3[0]), Write(line3[1]), run_time=0.5)
    arr_asgn = Arrow(
        line3.get_right() + RIGHT * 0.12,
        wall_asgn.get_left() + LEFT * 0.02,
        buff=0.10,
        stroke_width=3,
        color=GREEN_B,
    )
    scene.play(
        Indicate(line3[1], color=GREEN_B, scale_factor=1.3),
        GrowArrow(arr_asgn),
        Indicate(wall_asgn, color=GREEN_B, scale_factor=1.03),
        run_time=0.6,
    )
    scene.play(Write(line3[2]), run_time=0.9)
    scene.wait(0.4)

    # ══════════════════════════════════════════════════════════════════════
    #  ACT 4  (45s – 55s): Wrap in glowing box → "Minimize L" + x_{i,j}?
    # ══════════════════════════════════════════════════════════════════════
    full_lagrangian = VGroup(line0, line1, line2, line3)
    link_arrows = VGroup(arr_q, arr_cap, arr_asgn)

    # Shrink and surround with glowing rect
    scene.play(
        full_lagrangian.animate.move_to(ORIGIN),
        FadeOut(
            VGroup(
                link_arrows,
                wall_q,
                wall_cap,
                wall_asgn,
            )
        ),
        run_time=0.9,
    )

    glow_rect = SurroundingRectangle(
        full_lagrangian,
        color=GOLD,
        buff=0.22,
        corner_radius=0.14,
        stroke_width=2.0,
    )
    scene.play(Create(glow_rect), run_time=0.6)
    scene.play(glow_rect.animate.set_stroke(opacity=0.55), run_time=0.4)

    # # "Minimize L" label below
    # min_lbl = MathTex(r"\text{Minimize}\;\mathcal{L}", font_size=40, color=GOLD)
    # min_lbl.next_to(glow_rect, DOWN, buff=0.35)
    # scene.play(FadeIn(min_lbl, shift=UP * 0.15))

    # # x_{i,j} with a blinking question mark → "how to find x?"
    # x_lbl = MathTex(r"x_{i,j}", font_size=34, color=WHITE)
    # q_mark = MathTex(r"?", font_size=38, color=YELLOW)
    # x_lbl.next_to(min_lbl, RIGHT, buff=0.55)
    # q_mark.next_to(x_lbl, RIGHT, buff=0.10)
    # scene.play(FadeIn(x_lbl), FadeIn(q_mark))

    # Blink the question mark 3 times
    # for _ in range(3):
    #     scene.play(q_mark.animate.set_opacity(0.0), run_time=0.25)
    #     scene.play(q_mark.animate.set_opacity(1.0), run_time=0.25)

    scene.wait(1.2)


def play_scene13_optimality_condition(scene):
    # ══════════════════════════════════════════════════════════════════════
    #  Layout constants
    #  Left half  : Lagrangian  (centred at x = -3.0)
    #  Right half : derivative  (centred at x = +2.8)
    # ══════════════════════════════════════════════════════════════════════
    LAG_X = -3.2  # centre-x of the Lagrangian column
    DERIV_X = 2.8  # centre-x of the derivative / coefficient column

    # ══════════════════════════════════════════════════════════════════════
    #  ACT 1  (0s – 12s): Title + Lagrangian on LEFT + deriv prompt on RIGHT
    # ══════════════════════════════════════════════════════════════════════
    title = Text("Optimality Condition (KKT)", font_size=38).to_edge(UP, buff=0.45)
    scene.play(FadeIn(title, shift=DOWN * 0.2))

    # ── Add Navigator Bar (highlight tab 1: Training/Prediction) ────
    nav_line = Line([-7.00, -3.10, 0], [7.00, -3.10, 0],
                    stroke_width=0.7, color=GREY_B, stroke_opacity=0.55)
    nav_bar  = make_nav_bar(active_idx=3)
    scene.play(Create(nav_line), FadeIn(nav_bar), run_time=0.5)

    # ── Lagrangian (left column) ──────────────────────────────────────────
    line0 = MathTex(
        r"\mathcal{L}(x,\lambda_1,\lambda_2,\mu)",
        r"=",
        r"\sum_{i,j} c_{i,j}\,x_{i,j}",
        font_size=28,
    )
    line0[2].set_color(GOLD)

    line1 = MathTex(
        r"+\;",
        r"\lambda_1",
        r"\!\left(\alpha - \tfrac{1}{N}\sum_{i,j} a_{i,j}\,x_{i,j}\right)",
        font_size=28,
    )
    line1.set_color(BLUE_B)

    line2 = MathTex(
        r"+\;",
        r"\sum_j \lambda_{2,j}",
        r"\!\left(\sum_i x_{i,j} - L_j\right)",
        font_size=28,
    )
    line2.set_color(RED_B)

    line3 = MathTex(
        r"+\;",
        r"\sum_i \mu_i",
        r"\!\left(\sum_j x_{i,j} - 1\right)",
        font_size=28,
    )
    line3.set_color(GREEN_B)

    line1.next_to(line0, DOWN, aligned_edge=LEFT, buff=0.22)
    line2.next_to(line1, DOWN, aligned_edge=LEFT, buff=0.22)
    line3.next_to(line2, DOWN, aligned_edge=LEFT, buff=0.22)

    lag_group = VGroup(line0, line1, line2, line3)
    lag_group.move_to([LAG_X, 0.3, 0])  # left half, slightly above centre

    scene.play(FadeIn(lag_group, shift=RIGHT * 0.15), run_time=0.9)

    # Vertical divider
    divider = DashedLine(
        UP * 3.2,
        DOWN * 3.2,
        color=GREY_B,
        stroke_width=1.2,
        dash_length=0.12,
    ).move_to(ORIGIN)
    scene.play(Create(divider), run_time=0.5)

    # ── Derivative prompt (right column) ─────────────────────────────────
    deriv_prompt = MathTex(
        r"\frac{\partial \mathcal{L}}{\partial x_{i,j}} = \;\dots",
        font_size=36,
        color=YELLOW,
    )
    deriv_prompt.move_to([DERIV_X, 2.2, 0])
    scene.play(FadeIn(deriv_prompt, shift=LEFT * 0.15))
    for _ in range(2):
        scene.play(deriv_prompt.animate.set_opacity(0.2), run_time=0.22)
        scene.play(deriv_prompt.animate.set_opacity(1.0), run_time=0.22)
    scene.wait(0.4)

    # Coefficient landing positions on the right (stacked vertically)
    # Each coeff appears below the previous one on the right side
    COEFF_X = DERIV_X
    COEFF_TOP = deriv_prompt.get_bottom()[1] - 0.55  # y of first coeff

    # ══════════════════════════════════════════════════════════════════════
    #  ACT 2  (12s – 35s): Highlight each line, shoot coefficient to right
    # ══════════════════════════════════════════════════════════════════════
    def line_pointer(line, color=YELLOW):
        return Arrow(
            line.get_left() + LEFT * 0.95,
            line.get_left() + LEFT * 0.06,
            buff=0.0,
            stroke_width=3,
            color=color,
            max_tip_length_to_length_ratio=0.35,
        )

    # ── c_{i,j} from line0 ───────────────────────────────────────────────
    scan_arrow = line_pointer(line0)
    scene.play(
        GrowArrow(scan_arrow),
        Indicate(line0, color=GOLD, scale_factor=1.03),
        run_time=0.45,
    )

    coeff_c = MathTex(r"c_{i,j}", font_size=34, color=GOLD)
    coeff_c.move_to(line0[2].get_center())
    scene.add(coeff_c)
    dest_c = [COEFF_X, COEFF_TOP, 0]
    scene.play(coeff_c.animate.move_to(dest_c), run_time=0.65)

    # ── -λ₁a_{i,j}/N from line1 ──────────────────────────────────────────
    next_arrow = line_pointer(line1)
    scene.play(
        ReplacementTransform(scan_arrow, next_arrow),
        Indicate(line1, color=BLUE_B, scale_factor=1.03),
        run_time=0.40,
    )
    scan_arrow = next_arrow

    coeff_lam1 = MathTex(r"-\,\tfrac{\lambda_1 a_{i,j}}{N}", font_size=34, color=BLUE_B)
    coeff_lam1.move_to(line1.get_center())
    scene.add(coeff_lam1)
    dest_lam1 = [COEFF_X, COEFF_TOP - 0.85, 0]
    scene.play(coeff_lam1.animate.move_to(dest_lam1), run_time=0.65)
    scene.play(Indicate(coeff_lam1, color=BLUE_B, scale_factor=1.18), run_time=0.45)

    # ── +λ_{2,j} from line2 ──────────────────────────────────────────────
    next_arrow = line_pointer(line2)
    scene.play(
        ReplacementTransform(scan_arrow, next_arrow),
        Indicate(line2, color=RED_B, scale_factor=1.03),
        run_time=0.40,
    )
    scan_arrow = next_arrow

    coeff_lam2 = MathTex(r"+\,\lambda_{2,j}", font_size=34, color=RED_B)
    coeff_lam2.move_to(line2.get_center())
    scene.add(coeff_lam2)
    dest_lam2 = [COEFF_X, COEFF_TOP - 1.70, 0]
    scene.play(coeff_lam2.animate.move_to(dest_lam2), run_time=0.65)
    scene.play(Indicate(coeff_lam2, color=RED_B, scale_factor=1.18), run_time=0.45)

    # ── +μ_i from line3 ───────────────────────────────────────────────────
    next_arrow = line_pointer(line3)
    scene.play(
        ReplacementTransform(scan_arrow, next_arrow),
        Indicate(line3, color=GREEN_B, scale_factor=1.03),
        run_time=0.40,
    )
    scan_arrow = next_arrow

    coeff_mu = MathTex(r"+\,\mu_i", font_size=34, color=GREEN_B)
    coeff_mu.move_to(line3.get_center())
    scene.add(coeff_mu)
    dest_mu = [COEFF_X, COEFF_TOP - 2.55, 0]
    scene.play(coeff_mu.animate.move_to(dest_mu), run_time=0.65)
    scene.play(Indicate(coeff_mu, color=GREEN_B, scale_factor=1.18), run_time=0.45)
    scene.play(FadeOut(scan_arrow), run_time=0.2)

    scene.wait(0.4)

    # ══════════════════════════════════════════════════════════════════════
    #  ACT 3  (35s – 50s): Clear left side, merge coefficients → final eq
    # ══════════════════════════════════════════════════════════════════════
    scene.play(
        FadeOut(lag_group),
        FadeOut(divider),
        FadeOut(deriv_prompt),
        run_time=0.7,
    )

    # Full stationarity equation centred on screen
    final_eq = MathTex(
        r"\frac{\partial \mathcal{L}}{\partial x_{i,j}}",  # [0]
        r"=",  # [1]
        r"c_{i,j}",  # [2]  GOLD
        r"-\,\frac{\lambda_1 a_{i,j}}{N}",  # [3]  BLUE_B
        r"+\,\lambda_{2,j}",  # [4]  RED_B
        r"+\,\mu_i",  # [5]  GREEN_B
        r"=\;0",  # [6]  RED_A
        font_size=40,
    )
    final_eq[2].set_color(GOLD)
    final_eq[3].set_color(BLUE_B)
    final_eq[4].set_color(RED_B)
    final_eq[5].set_color(GREEN_B)
    final_eq[6].set_color(RED_A)
    final_eq.move_to(ORIGIN)

    # Floating coefficients morph into their positions in final_eq
    scene.play(
        Transform(coeff_c, final_eq[2]),
        Transform(coeff_lam1, final_eq[3]),
        Transform(coeff_lam2, final_eq[4]),
        Transform(coeff_mu, final_eq[5]),
        run_time=1.0,
    )
    scene.play(
        Write(final_eq[0]),
        Write(final_eq[1]),
        Write(final_eq[6]),
        run_time=0.9,
    )
    scene.remove(coeff_c, coeff_lam1, coeff_lam2, coeff_mu)
    scene.add(final_eq)

    # Glowing frame
    glow_rect = SurroundingRectangle(
        final_eq, color=GOLD, buff=0.20, corner_radius=0.12, stroke_width=2.2
    )
    scene.play(Create(glow_rect), run_time=0.55)

    # Pulse "= 0"
    scene.play(Indicate(final_eq[6], color=RED_A, scale_factor=1.30), run_time=0.55)
    scene.play(Indicate(final_eq[6], color=RED_A, scale_factor=1.30), run_time=0.55)

    # # Annotation
    # annot = Text(
    #     "Marginal Net Cost = 0  (optimality balance)", font_size=17, color=GREY_A
    # )
    # annot.next_to(glow_rect, DOWN, buff=0.30)
    # scene.play(FadeIn(annot, shift=UP * 0.1))

    # # Tease scene 14
    # mu_hint = MathTex(
    #     r"\mu_i \text{ cancels} \;\rightarrow\; \text{Scene 14}",
    #     font_size=20,
    #     color=GREEN_B,
    # )
    # mu_hint.next_to(annot, DOWN, buff=0.20)
    # scene.play(FadeIn(mu_hint, shift=UP * 0.1))
    # scene.play(Indicate(final_eq[5], color=GREEN_B, scale_factor=1.25), run_time=0.55)

    scene.wait(1.5)


def play_scene14_decision_rule(scene):
    # ══════════════════════════════════════════════════════════════════════
    #  ACT 1  (0s – 25s): Two stationarity equations → µ_i cancels
    # ══════════════════════════════════════════════════════════════════════
    title = Text("Decision Rule  &  Dual Function", font_size=36).to_edge(UP, buff=0.45)
    scene.play(FadeIn(title, shift=DOWN * 0.2))

    # ── Add Navigator Bar (highlight tab 1: Training/Prediction) ────
    nav_line = Line([-7.00, -3.10, 0], [7.00, -3.10, 0],
                    stroke_width=0.7, color=GREY_B, stroke_opacity=0.55)
    nav_bar  = make_nav_bar(active_idx=3)
    scene.play(Create(nav_line), FadeIn(nav_bar), run_time=0.5)


    # Two equations — same colour coding as scene 13
    eq_j = MathTex(
        r"c_{i,j}",  # [0] GOLD
        r"-\,\frac{\lambda_1 a_{i,j}}{N}",  # [1] BLUE_B
        r"+\,\lambda_{2,j}",  # [2] RED_B
        r"+\,\mu_i",  # [3] GREEN_B  ← cancel
        r"= 0",  # [4]
        font_size=34,
    )
    eq_j[0].set_color(GOLD)
    eq_j[1].set_color(BLUE_B)
    eq_j[2].set_color(RED_B)
    eq_j[3].set_color(GREEN_B)

    eq_k = MathTex(
        r"c_{i,k}",
        r"-\,\frac{\lambda_1 a_{i,k}}{N}",
        r"+\,\lambda_{2,k}",
        r"+\,\mu_i",  # [3] ← cancel
        r"= 0",
        font_size=34,
    )
    eq_k[0].set_color(GOLD)
    eq_k[1].set_color(BLUE_B)
    eq_k[2].set_color(RED_B)
    eq_k[3].set_color(GREEN_B)

    eq_j.move_to(UP * 1.2)
    eq_k.next_to(eq_j, DOWN, buff=0.55)

    # Subtraction sign between the two rows
    minus_sign = MathTex(r"-", font_size=44, color=WHITE)
    minus_sign.move_to(
        [eq_j.get_left()[0] - 0.55, (eq_j.get_bottom()[1] + eq_k.get_top()[1]) / 2, 0]
    )
    h_rule = Line(
        eq_k.get_left() + LEFT * 0.1,
        eq_k.get_right() + RIGHT * 0.1,
        color=GREY_A,
        stroke_width=1.5,
    ).next_to(eq_k, DOWN, buff=0.15)

    scene.play(Write(eq_j), run_time=1.0)
    scene.play(Write(eq_k), run_time=1.0)
    scene.play(FadeIn(minus_sign), Create(h_rule))
    scene.wait(0.3)

    # Cross out µ_i in both rows simultaneously
    cross_j = Cross(eq_j[3], color=RED, stroke_width=5)
    cross_k = Cross(eq_k[3], color=RED, stroke_width=5)
    scene.play(Create(cross_j), Create(cross_k), run_time=0.6)
    scene.play(
        eq_j[3].animate.set_opacity(0.18),
        eq_k[3].animate.set_opacity(0.18),
        run_time=0.4,
    )

    mu_note = Text(
        "µᵢ is identical for all j  →  cancels out!", font_size=17, color=GREEN_B
    )
    mu_note.next_to(h_rule, DOWN, buff=0.28)
    scene.play(FadeIn(mu_note, shift=UP * 0.1))
    scene.wait(0.5)

    # Result drops below the rule: show the equality that remains
    result_eq = MathTex(
        r"\Bigl(c_{i,j} - \tfrac{\lambda_1 a_{i,j}}{N} + \lambda_{2,j}\Bigr)",
        r"=",
        r"\Bigl(c_{i,k} - \tfrac{\lambda_1 a_{i,k}}{N} + \lambda_{2,k}\Bigr)",
        font_size=28,
    )
    result_eq[0].set_color(BLUE_B)
    result_eq[2].set_color(RED_B)
    result_eq.next_to(mu_note, DOWN, buff=0.30)
    scene.play(FadeIn(result_eq, shift=UP * 0.1))
    scene.wait(0.6)

    # ══════════════════════════════════════════════════════════════════════
    #  ACT 2  (25s – 45s): argmin decision rule
    # ══════════════════════════════════════════════════════════════════════
    scene.play(
        FadeOut(
            VGroup(eq_j, eq_k, minus_sign, h_rule, cross_j, cross_k, mu_note, result_eq)
        ),
        run_time=0.7,
    )

    rule = MathTex(
        r"j^*",  # [0]
        r"= \arg\min_j \Bigl(",  # [1]
        r"c_{i,j}",  # [2] GOLD
        r"-\,\frac{\lambda_1\,a_{i,j}}{N}",  # [3] BLUE_B
        r"+\,\lambda_{2,j}",  # [4] RED_B
        r"\Bigr)",  # [5]
        font_size=44,
    )
    rule[2].set_color(GOLD)
    rule[3].set_color(BLUE_B)
    rule[4].set_color(RED_B)
    rule.move_to(UP * 0.8)

    scene.play(Write(rule), run_time=1.4)

    # Annotate the three components
    annots = [
        (rule[2], "Base Cost", GOLD, DOWN),
        (rule[3], "Quality Discount", BLUE_B, DOWN),
        (rule[4], "Capacity Penalty", RED_B, DOWN),
    ]
    for mob, txt, col, direction in annots:
        lbl = Text(txt, font_size=15, color=col).next_to(
            mob, direction * 2.2, buff=0.05
        )
        arr = Arrow(
            mob.get_bottom(),
            lbl.get_top(),
            buff=0.06,
            stroke_width=2,
            color=col,
            max_tip_length_to_length_ratio=0.28,
        )
        scene.play(Indicate(mob, color=col, scale_factor=1.25), run_time=0.45)
        scene.play(GrowArrow(arr), FadeIn(lbl), run_time=0.4)

    scene.wait(0.5)

    # ══════════════════════════════════════════════════════════════════════
    #  ACT 3  (45s – 75s): Birth of the Dual Function g(λ₁, λ₂)
    # ══════════════════════════════════════════════════════════════════════
    # Clear annotations, shrink rule to top-left corner
    scene.play(
        *[FadeOut(m) for m in scene.mobjects if m not in [title, rule, nav_line, nav_bar]],
        rule.animate.scale(0.52).to_corner(UL, buff=0.55).shift(DOWN * 0.5),
        run_time=0.8,
    )

    # Show the dual function directly

    dual_eq = MathTex(
        r"g(\lambda_1,\lambda_2)",
        r"=\min_{x_{i,j}}\Biggl\{",
        r"\sum_{i=1}^{N}\sum_{j=1}^{M} x_{i,j}",
        r"\Bigl(c_{i,j}",
        r"-\,\frac{\lambda_1 a_{i,j}}{N}",
        r"+\,\lambda_{2,j}\Bigr)",
        r"+\,\lambda_1\alpha",
        r"-\,\sum_{j=1}^{M}\lambda_{2,j}L_j",
        r"\Biggr\}",
        font_size=26,
    )
    dual_eq[0].set_color(GOLD)
    dual_eq[3].set_color(GOLD)
    dual_eq[4].set_color(BLUE_B)
    dual_eq[5].set_color(RED_B)
    dual_eq[6].set_color(BLUE_B)
    dual_eq[7].set_color(RED_B)
    dual_eq.move_to(ORIGIN + DOWN * 0.2)

    scene.play(Write(dual_eq), run_time=1.5)
    scene.wait(0.4)

    # Glowing frame around the full dual function
    glow = SurroundingRectangle(
        dual_eq, color=GOLD, buff=0.22, corner_radius=0.14, stroke_width=2.2
    )
    scene.play(Create(glow), run_time=0.6)

    # Bridge to scene 15
    to15 = Text("→  maximise g(λ₁, λ₂) via Gradient Ascent", font_size=17, color=GREY_A)
    to15.next_to(glow, DOWN, buff=0.30)
    scene.play(FadeIn(to15, shift=UP * 0.1))

    scene.wait(1.5)


def play_scene15_dual_updates(scene):
    # ══════════════════════════════════════════════════════════════════════
    #  ACT 1  (0s – 15s): Title + iterative time loop
    # ══════════════════════════════════════════════════════════════════════
    title = Text("Dual Updates  (Gradient Ascent)", font_size=38).to_edge(UP, buff=0.45)
    scene.play(FadeIn(title, shift=DOWN * 0.2))

    # ── Add Navigator Bar (highlight tab 1: Training/Prediction) ────
    nav_line = Line([-7.00, -3.10, 0], [7.00, -3.10, 0],
                    stroke_width=0.7, color=GREY_B, stroke_opacity=0.55)
    nav_bar  = make_nav_bar(active_idx=3)
    scene.play(Create(nav_line), FadeIn(nav_bar), run_time=0.5)


    # Iterative time display  t = 0 → 1 → 2 → …
    t_label = MathTex(r"t = 0", font_size=44, color=YELLOW).move_to(ORIGIN)
    scene.play(Write(t_label))
    for t in range(1, 4):
        new_t = MathTex(rf"t = {t}", font_size=44, color=YELLOW).move_to(ORIGIN)
        scene.play(Transform(t_label, new_t), run_time=0.45)
    dots = MathTex(
        r"t = 0 \;\rightarrow\; 1 \;\rightarrow\; 2 \;\rightarrow\; \cdots",
        font_size=34,
        color=YELLOW,
    ).move_to(ORIGIN)
    scene.play(Transform(t_label, dots), run_time=0.6)
    scene.wait(0.4)
    scene.play(FadeOut(t_label), run_time=0.5)

    # ══════════════════════════════════════════════════════════════════════
    #  ACT 2  (15s – 35s): λ₁ update formula (quality penalty)
    # ══════════════════════════════════════════════════════════════════════
    # Formula WITHOUT max() first — we add it later
    eq1_no_max = MathTex(
        r"\lambda_1^{t+1}",  # [0]
        r"=",  # [1]
        r"\lambda_1^t",  # [2]
        r"+",  # [3]
        r"\eta_1",  # [4]  ← Indicate (learning rate)
        r"\left(\alpha - \frac{1}{N}\sum_{i,j} a_{i,j}\,x_{i,j}\right)",  # [5] ← Indicate (violation)
        font_size=36,
    )
    eq1_no_max[0].set_color(BLUE_B)
    eq1_no_max[2].set_color(BLUE_B)
    eq1_no_max[4].set_color(YELLOW)
    eq1_no_max[5].set_color(BLUE_B)
    eq1_no_max.move_to(UP * 1.2)

    scene.play(Write(eq1_no_max), run_time=1.4)

    # Annotate η₁ → "Learning Rate"
    eta1_annot = Text("Learning Rate / Step size", font_size=16, color=YELLOW)
    eta1_arr = Arrow(
        eq1_no_max[4].get_bottom() + DOWN * 0.05,
        eq1_no_max[4].get_bottom() + DOWN * 0.55,
        buff=0.0,
        stroke_width=2,
        color=YELLOW,
        max_tip_length_to_length_ratio=0.30,
    )
    eta1_annot.next_to(eta1_arr, DOWN, buff=0.06)
    scene.play(Indicate(eq1_no_max[4], color=YELLOW, scale_factor=1.35), run_time=0.55)
    scene.play(GrowArrow(eta1_arr), FadeIn(eta1_annot))
    scene.wait(0.3)

    # Annotate (α − …) → "Quality Violation (Gradient)"
    viol1_annot = Text("Quality Violation  (Gradient)", font_size=16, color=BLUE_B)
    viol1_arr = Arrow(
        eq1_no_max[5].get_bottom() + DOWN * 0.05,
        eq1_no_max[5].get_bottom() + DOWN * 0.55,
        buff=0.0,
        stroke_width=2,
        color=BLUE_B,
        max_tip_length_to_length_ratio=0.30,
    )
    viol1_annot.next_to(viol1_arr, DOWN, buff=0.06)
    scene.play(Indicate(eq1_no_max[5], color=BLUE_B, scale_factor=1.12), run_time=0.55)
    scene.play(GrowArrow(viol1_arr), FadeIn(viol1_annot))
    scene.wait(0.4)

    # ══════════════════════════════════════════════════════════════════════
    #  ACT 3  (35s – 45s): λ_{2,j} update formula (capacity penalty)
    # ══════════════════════════════════════════════════════════════════════
    scene.play(
        FadeOut(VGroup(eta1_arr, eta1_annot, viol1_arr, viol1_annot)),
        eq1_no_max.animate.scale(0.82).move_to(UP * 2.0),
        run_time=0.6,
    )

    eq2_no_max = MathTex(
        r"\lambda_{2,j}^{t+1}",  # [0]
        r"=",  # [1]
        r"\lambda_{2,j}^t",  # [2]
        r"+",  # [3]
        r"\eta_2",  # [4]  ← Indicate
        r"\left(\sum_i x_{i,j} - L_j\right)",  # [5]  ← Indicate
        font_size=36,
    )
    eq2_no_max[0].set_color(RED_B)
    eq2_no_max[2].set_color(RED_B)
    eq2_no_max[4].set_color(YELLOW)
    eq2_no_max[5].set_color(RED_B)
    eq2_no_max.move_to(DOWN * 0.0)

    scene.play(Write(eq2_no_max), run_time=1.2)

    # Annotate (Σ x − L_j) → "Capacity Violation"
    viol2_annot = Text("Capacity Violation", font_size=16, color=RED_B)
    viol2_arr = Arrow(
        eq2_no_max[5].get_bottom() + DOWN * 0.05,
        eq2_no_max[5].get_bottom() + DOWN * 0.55,
        buff=0.0,
        stroke_width=2,
        color=RED_B,
        max_tip_length_to_length_ratio=0.30,
    )
    viol2_annot.next_to(viol2_arr, DOWN, buff=0.06)
    scene.play(Indicate(eq2_no_max[5], color=RED_B, scale_factor=1.18), run_time=0.55)
    scene.play(GrowArrow(viol2_arr), FadeIn(viol2_annot))
    scene.wait(0.4)

    # ══════════════════════════════════════════════════════════════════════
    #  ACT 4  (45s – 60s): Wrap both in max(…, 0) — Dual Feasibility
    # ══════════════════════════════════════════════════════════════════════
    scene.play(
        FadeOut(VGroup(viol2_arr, viol2_annot)),
        run_time=0.4,
    )

    # Build the final complete formulas with max(…, 0)
    eq1_max = MathTex(
        r"\lambda_1^{t+1}",
        r"= \max\!\Bigl(",
        r"\lambda_1^t + \eta_1\!\left(\alpha - \tfrac{1}{N}\sum_{i,j} a_{i,j}x_{i,j}\right)",
        r",\;0\Bigr)",
        font_size=30,
    )
    eq1_max[0].set_color(BLUE_B)
    eq1_max[2].set_color(BLUE_B)
    eq1_max[1].set_color(WHITE)
    eq1_max[3].set_color(WHITE)
    eq1_max.move_to(UP * 1.5)

    eq2_max = MathTex(
        r"\lambda_{2,j}^{t+1}",
        r"= \max\!\Bigl(",
        r"\lambda_{2,j}^t + \eta_2\!\left(\sum_i x_{i,j} - L_j\right)",
        r",\;0\Bigr)",
        font_size=30,
    )
    eq2_max[0].set_color(RED_B)
    eq2_max[2].set_color(RED_B)
    eq2_max[1].set_color(WHITE)
    eq2_max[3].set_color(WHITE)
    eq2_max.next_to(eq1_max, DOWN, buff=0.55)

    # GrowFromCenter for the max(…,0) wrappers to feel like they "snap on"
    scene.play(
        TransformMatchingShapes(eq1_no_max, eq1_max),
        TransformMatchingShapes(eq2_no_max, eq2_max),
        run_time=1.1,
    )

    # Flash the max() parts
    scene.play(
        Indicate(eq1_max[1], color=WHITE, scale_factor=1.22),
        Indicate(eq1_max[3], color=WHITE, scale_factor=1.22),
        Indicate(eq2_max[1], color=WHITE, scale_factor=1.22),
        Indicate(eq2_max[3], color=WHITE, scale_factor=1.22),
        run_time=0.65,
    )

    # "Penalty ≥ 0" explanation
    neg_note = Text(
        "Penalty < 0 makes no sense  →  max( · , 0) clamps it to zero",
        font_size=17,
        color=GREY_A,
    )
    neg_note.next_to(eq2_max, DOWN, buff=0.40)
    scene.play(FadeIn(neg_note, shift=UP * 0.1))
    scene.wait(0.3)

    # Green-tick Dual Feasibility badge (top-right)
    # feasibility_grp = VGroup(
    #     Text("✓", font_size=34, color=GREEN_A),
    #     Text("Dual Feasibility  (λ ≥ 0)", font_size=20, color=GREEN_A),
    # ).arrange(RIGHT, buff=0.18)
    # feasibility_grp.to_corner(UR, buff=0.55)
    # feas_rect = SurroundingRectangle(
    #     feasibility_grp,
    #     color=GREEN_A,
    #     buff=0.14,
    #     corner_radius=0.10,
    #     stroke_width=1.8,
    # )
    # scene.play(FadeIn(feasibility_grp, shift=LEFT * 0.1), Create(feas_rect))
    # scene.play(
    #     Flash(
    #         feasibility_grp.get_center(),
    #         color=GREEN_A,
    #         flash_radius=0.5,
    #         line_length=0.18,
    #     )
    # )

    scene.wait(1.5)


def play_scene16_dual_intuition(scene):
    # ══════════════════════════════════════════════════════════════════════
    #  Layout: two model boxes side by side
    #    Model 1: Cheap & Weak  (left,  x = -3.0)
    #    Model 2: Strong & Costly (right, x = +3.0)
    # ══════════════════════════════════════════════════════════════════════
    M1_X, M2_X = -3.0, 3.0
    BASE_Y = -0.3  # neutral vertical position for boxes

    # ── ValueTrackers ────────────────────────────────────────────────────
    lam1 = ValueTracker(0.5)  # quality penalty
    lam2 = ValueTracker(0.2)  # capacity penalty for model 1

    # Model intrinsics
    M1_COST, M1_QUAL = 0.5, 0.4  # cheap, weak
    M2_COST, M2_QUAL = 1.2, 1.0  # costly, strong

    # ── Model box factory ─────────────────────────────────────────────────
    def model_box(label, color):
        rect = RoundedRectangle(
            width=2.0,
            height=0.80,
            corner_radius=0.12,
            color=color,
            fill_color=color,
            fill_opacity=0.20,
            stroke_width=2.5,
        )
        lbl = Text(label, font_size=18, color=color).move_to(rect)
        return VGroup(rect, lbl)

    box1 = model_box("Model 1\n(Cheap & Weak)", WHITE)
    box2 = model_box("Model 2\n(Strong & Costly)", WHITE)
    box1.move_to([M1_X, BASE_Y, 0])
    box2.move_to([M2_X, BASE_Y, 0])

    # ── always_redraw helpers ─────────────────────────────────────────────
    # Balloon: radius grows with lam1 * quality; attached above its box
    def make_balloon(box, qual):
        def draw():
            r = 0.15 + lam1.get_value() * qual * 0.22
            r = min(r, 0.70)
            circ = Circle(
                radius=r,
                color=BLUE_B,
                fill_color=BLUE_E,
                fill_opacity=0.60,
                stroke_width=1.8,
            )
            circ.next_to(box, UP, buff=0.10)
            txt = MathTex(r"-\lambda_1 a", font_size=14, color=WHITE).move_to(circ)
            line = DashedLine(
                box.get_top(),
                circ.get_bottom(),
                color=BLUE_A,
                stroke_width=1.5,
                dash_length=0.07,
            )
            return VGroup(line, circ, txt)

        return always_redraw(draw)

    # Weight: size grows with base cost + lam2 (only for box1)
    def make_weight_base(box, cost):
        def draw():
            w = 0.35 + cost * 0.18
            h = 0.28 + cost * 0.10
            rect = Rectangle(
                width=w,
                height=h,
                fill_color=GOLD_E,
                fill_opacity=0.85,
                stroke_color=GOLD,
                stroke_width=1.5,
            )
            rect.next_to(box, DOWN, buff=0.08)
            lbl = Text("c", font_size=13, color=WHITE).move_to(rect)
            line = Line(
                box.get_bottom(), rect.get_top(), color=GREY_A, stroke_width=1.5
            )
            return VGroup(line, rect, lbl)

        return always_redraw(draw)

    def make_cap_weight(box):
        def draw():
            w = 0.28 + lam2.get_value() * 0.55
            h = 0.22 + lam2.get_value() * 0.38
            rect = Rectangle(
                width=w,
                height=h,
                fill_color=RED_E,
                fill_opacity=0.85,
                stroke_color=RED_B,
                stroke_width=1.5,
            )
            rect.next_to(box, DOWN, buff=0.38)  # below the base-cost weight
            lbl = MathTex(r"+\lambda_2", font_size=12, color=WHITE).move_to(rect)
            return VGroup(rect, lbl)

        return always_redraw(draw)

    # Box vertical position tracks net "weight" = cost + lam2 - lam1*qual
    def make_box_updater(box, cost, qual, x_pos):
        def update(m):
            net = (
                cost
                + lam2.get_value() * (1 if x_pos < 0 else 0)
                - lam1.get_value() * qual * 0.55
            )
            m.move_to([x_pos, BASE_Y - net * 0.35, 0])

        box.add_updater(update)

    make_box_updater(box1, M1_COST, M1_QUAL, M1_X)
    make_box_updater(box2, M2_COST, M2_QUAL, M2_X)

    balloon1 = make_balloon(box1, M1_QUAL)
    balloon2 = make_balloon(box2, M2_QUAL)
    weight1 = make_weight_base(box1, M1_COST)
    weight2 = make_weight_base(box2, M2_COST)
    cap_w1 = make_cap_weight(box1)

    # ══════════════════════════════════════════════════════════════════════
    #  ACT 1  (0s – 15s): Title + introduce two models
    # ══════════════════════════════════════════════════════════════════════
    title = Text("The Economic Intuition", font_size=38).to_edge(UP, buff=0.45)
    scene.play(FadeIn(title, shift=DOWN * 0.2))

    scene.add(balloon1, balloon2, weight1, weight2, cap_w1)
    scene.play(FadeIn(box1), FadeIn(box2), run_time=0.8)

    # Labels explaining the visual elements
    legend = VGroup(
        VGroup(
            Circle(radius=0.12, color=BLUE_B, fill_color=BLUE_E, fill_opacity=0.6),
            Text("Quality lift  −λ₁a", font_size=14, color=GREY_A),
        ).arrange(RIGHT, buff=0.10),
        VGroup(
            Square(
                side_length=0.22,
                fill_color=GOLD_E,
                fill_opacity=0.8,
                stroke_color=GOLD,
                stroke_width=1,
            ),
            Text("Base cost  c", font_size=14, color=GREY_A),
        ).arrange(RIGHT, buff=0.10),
        VGroup(
            Square(
                side_length=0.22,
                fill_color=RED_E,
                fill_opacity=0.8,
                stroke_color=RED_B,
                stroke_width=1,
            ),
            Text("Capacity tax  +λ₂", font_size=14, color=GREY_A),
        ).arrange(RIGHT, buff=0.10),
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    legend.to_corner(UR, buff=0.55)
    scene.play(FadeIn(legend))
    scene.wait(0.5)

    # ══════════════════════════════════════════════════════════════════════
    #  ACT 2  (15s – 35s): λ₁ rises → balloon on Model 2 expands → M2 floats up
    # ══════════════════════════════════════════════════════════════════════
    # Slider for λ₁
    lam1_bar = NumberLine(
        x_range=[0, 5, 1], length=4.5, include_numbers=False, color=GREY_B
    )
    lam1_bar.move_to(DOWN * 2.8 + LEFT * 1.5)
    lam1_lbl = Text("Quality Penalty  λ₁", font_size=16, color=BLUE_B)
    lam1_lbl.next_to(lam1_bar, UP, buff=0.12)

    lam1_dot = always_redraw(
        lambda: Dot(lam1_bar.n2p(lam1.get_value()), radius=0.12, color=BLUE_B)
    )
    lam1_val = always_redraw(
        lambda: MathTex(
            rf"\lambda_1 = {lam1.get_value():.1f}", font_size=20, color=BLUE_B
        ).next_to(lam1_bar, DOWN, buff=0.10)
    )

    scene.play(Create(lam1_bar), FadeIn(lam1_lbl), FadeIn(lam1_dot), FadeIn(lam1_val))

    # Raise λ₁ → Model 2's balloon grows, M2 floats up
    scene.play(lam1.animate.set_value(4.2), run_time=2.2)

    # Highlight Model 2 as winner
    win_rect2 = SurroundingRectangle(
        box2, color=GREEN_A, buff=0.20, corner_radius=0.12, stroke_width=2.5
    )
    tick2 = Text("✓", font_size=38, color=GREEN_A).next_to(box2, UR, buff=0.05)
    msg1 = Text("Higher λ₁ favors High-Quality models", font_size=19, color=BLUE_B)
    msg1.next_to(lam1_bar, DOWN, buff=0.50)

    scene.play(Create(win_rect2), FadeIn(tick2))
    scene.play(FadeIn(msg1, shift=UP * 0.1))
    scene.wait(0.7)

    # ══════════════════════════════════════════════════════════════════════
    #  ACT 3  (35s – 55s): Model 1 overloaded → λ₂ rises → M1 sinks
    # ══════════════════════════════════════════════════════════════════════
    scene.play(
        FadeOut(VGroup(win_rect2, tick2, msg1)),
        lam1.animate.set_value(0.6),  # reset λ₁
        run_time=0.7,
    )

    # Packets rushing into Model 1
    packets = VGroup(
        *[
            Dot(radius=0.08, color=YELLOW).move_to(
                box1.get_center() + LEFT * (2.5 + i * 0.5) + UP * (0.15 * (i % 3 - 1))
            )
            for i in range(6)
        ]
    )
    scene.play(LaggedStart(*[FadeIn(p) for p in packets], lag_ratio=0.12))
    scene.play(
        LaggedStart(
            *[p.animate.move_to(box1.get_center()) for p in packets], lag_ratio=0.10
        ),
        run_time=1.0,
    )
    scene.play(FadeOut(packets))

    # "Load: 150%" overload indicator on Model 1
    load_lbl = Text("Load: 150% ⚠", font_size=18, color=RED_B)
    load_lbl.next_to(box1, UP, buff=1.10)
    scene.play(FadeIn(load_lbl))

    # Slider for λ₂
    lam2_bar = NumberLine(
        x_range=[0, 5, 1], length=4.5, include_numbers=False, color=GREY_B
    )
    lam2_bar.next_to(lam1_bar, DOWN, buff=0.65)
    lam2_lbl = Text("Capacity Penalty  λ₂₁", font_size=16, color=RED_B)
    lam2_lbl.next_to(lam2_bar, UP, buff=0.12)

    lam2_dot = always_redraw(
        lambda: Dot(lam2_bar.n2p(lam2.get_value()), radius=0.12, color=RED_B)
    )
    lam2_val = always_redraw(
        lambda: MathTex(
            rf"\lambda_{{2,1}} = {lam2.get_value():.1f}", font_size=20, color=RED_B
        ).next_to(lam2_bar, DOWN, buff=0.10)
    )

    scene.play(Create(lam2_bar), FadeIn(lam2_lbl), FadeIn(lam2_dot), FadeIn(lam2_val))

    # Raise λ₂ → red weight on M1 grows, M1 sinks
    scene.play(lam2.animate.set_value(4.5), run_time=2.2)

    msg2 = Text("Higher λ₂ penalizes Overloaded models", font_size=19, color=RED_B)
    msg2.next_to(lam2_bar, DOWN, buff=0.50)
    scene.play(FadeIn(msg2, shift=UP * 0.1))

    # Packets reroute to Model 2
    reroute = VGroup(
        *[
            Dot(radius=0.08, color=YELLOW).move_to(
                box1.get_center() + LEFT * (1.0 + i * 0.4)
            )
            for i in range(4)
        ]
    )
    scene.play(LaggedStart(*[FadeIn(p) for p in reroute], lag_ratio=0.12))
    scene.play(
        LaggedStart(
            *[p.animate.move_to(box2.get_center()) for p in reroute], lag_ratio=0.12
        ),
        run_time=1.0,
    )
    scene.play(FadeOut(VGroup(reroute, load_lbl)))
    scene.wait(0.4)

    # ══════════════════════════════════════════════════════════════════════
    #  ACT 4  (55s – 60s): Both sliders oscillate → equilibrium
    # ══════════════════════════════════════════════════════════════════════
    scene.play(FadeOut(msg2))

    equilibrium_lbl = Text(
        "System finds optimal equilibrium  ⚖", font_size=22, color=GOLD
    )
    equilibrium_lbl.to_edge(DOWN, buff=0.35)

    # Oscillate both trackers toward equilibrium values
    scene.play(
        lam1.animate.set_value(2.0),
        lam2.animate.set_value(1.5),
        run_time=1.2,
    )
    scene.play(
        lam1.animate.set_value(1.5),
        lam2.animate.set_value(1.0),
        run_time=0.9,
    )
    scene.play(
        lam1.animate.set_value(1.8),
        lam2.animate.set_value(1.2),
        run_time=0.7,
    )
    scene.play(FadeIn(equilibrium_lbl, shift=UP * 0.1))
    scene.wait(1.5)

"""Function steps for scenes 12-16."""

from manim import *

import formulas


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
        full_lagrangian.animate.scale(0.80).move_to(ORIGIN + UP * 0.4),
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

    # "Minimize L" label below
    min_lbl = MathTex(r"\text{Minimize}\;\mathcal{L}", font_size=40, color=GOLD)
    min_lbl.next_to(glow_rect, DOWN, buff=0.35)
    scene.play(FadeIn(min_lbl, shift=UP * 0.15))

    # x_{i,j} with a blinking question mark → "how to find x?"
    x_lbl = MathTex(r"x_{i,j}", font_size=34, color=WHITE)
    q_mark = MathTex(r"?", font_size=38, color=YELLOW)
    x_lbl.next_to(min_lbl, RIGHT, buff=0.55)
    q_mark.next_to(x_lbl, RIGHT, buff=0.10)
    scene.play(FadeIn(x_lbl), FadeIn(q_mark))

    # Blink the question mark 3 times
    for _ in range(3):
        scene.play(q_mark.animate.set_opacity(0.0), run_time=0.25)
        scene.play(q_mark.animate.set_opacity(1.0), run_time=0.25)

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

    # Annotation
    annot = Text(
        "Marginal Net Cost = 0  (optimality balance)", font_size=17, color=GREY_A
    )
    annot.next_to(glow_rect, DOWN, buff=0.30)
    scene.play(FadeIn(annot, shift=UP * 0.1))

    # Tease scene 14
    mu_hint = MathTex(
        r"\mu_i \text{ cancels} \;\rightarrow\; \text{Scene 14}",
        font_size=20,
        color=GREEN_B,
    )
    mu_hint.next_to(annot, DOWN, buff=0.20)
    scene.play(FadeIn(mu_hint, shift=UP * 0.1))
    scene.play(Indicate(final_eq[5], color=GREEN_B, scale_factor=1.25), run_time=0.55)

    scene.wait(1.5)


def play_scene14_decision_rule(scene):
    # ══════════════════════════════════════════════════════════════════════
    #  Helpers
    # ══════════════════════════════════════════════════════════════════════
    def make_weight_box(label, base_cost, quality_disc, capacity_tax, x_pos):
        """
        Returns a VGroup with:
          - a rounded rect labelled `label`
          - a downward weight  (base_cost)     → pulls down
          - an upward balloon  (quality_disc)  → lifts up   (dashed line)
          - a downward hammer  (capacity_tax)  → pushes down (different colour)
        The net vertical offset is  base_cost + capacity_tax - quality_disc
        (positive = heavier / lower on screen).
        """
        # LLM box
        rect = RoundedRectangle(
            width=1.8,
            height=0.75,
            corner_radius=0.12,
            color=WHITE,
            fill_color=GREY_D,
            fill_opacity=0.30,
            stroke_width=2,
        )
        lbl = Text(label, font_size=17, color=WHITE).move_to(rect)
        box = VGroup(rect, lbl)

        # Base-cost weight (gold, below box)
        w_rect = Rectangle(
            width=0.55,
            height=0.38,
            fill_color=GOLD_E,
            fill_opacity=0.80,
            stroke_color=GOLD,
            stroke_width=1.5,
        )
        w_lbl = Text("c", font_size=14, color=WHITE).move_to(w_rect)
        weight = VGroup(w_rect, w_lbl)
        weight.next_to(box, DOWN, buff=0.06)
        w_line = Line(
            box.get_bottom(), weight.get_top(), color=GREY_A, stroke_width=1.5
        )

        # Quality-discount balloon (blue, above box, dashed line)
        b_circ = Circle(
            radius=0.28 + quality_disc * 0.10,
            color=BLUE_B,
            fill_color=BLUE_E,
            fill_opacity=0.55,
            stroke_width=1.5,
        )
        b_lbl = Text("a", font_size=13, color=WHITE).move_to(b_circ)
        balloon = VGroup(b_circ, b_lbl)
        balloon.next_to(box, UP, buff=0.06)
        b_line = DashedLine(
            box.get_top(),
            balloon.get_bottom(),
            color=BLUE_A,
            stroke_width=1.5,
            dash_length=0.07,
        )

        # Capacity-tax hammer (red, above box, solid)
        h_rect = Rectangle(
            width=0.50,
            height=0.32,
            fill_color=RED_E,
            fill_opacity=0.80,
            stroke_color=RED_B,
            stroke_width=1.5,
        )
        h_lbl = Text("λ", font_size=14, color=WHITE).move_to(h_rect)
        hammer = VGroup(h_rect, h_lbl)
        hammer.next_to(balloon, UP, buff=0.06)
        h_line = Line(
            balloon.get_top(), hammer.get_bottom(), color=RED_B, stroke_width=1.5
        )

        # Net offset: positive → lower (heavier)
        net = base_cost + capacity_tax - quality_disc
        group = VGroup(box, w_line, weight, b_line, balloon, h_line, hammer)
        group.move_to([x_pos, -net * 0.35, 0])  # scale offset for visual
        return group, net

    # ══════════════════════════════════════════════════════════════════════
    #  ACT 1  (0s – 15s): Two stationarity equations → μ_i cancels
    # ══════════════════════════════════════════════════════════════════════
    title = Text("Decision Rule", font_size=38).to_edge(UP, buff=0.45)
    scene.play(FadeIn(title, shift=DOWN * 0.2))

    # Two equations for model j and model k
    eq_j = MathTex(
        r"c_{i,j}",  # [0] GOLD
        r"-\,\frac{\lambda_1 a_{i,j}}{N}",  # [1] BLUE_B
        r"+\,\lambda_{2,j}",  # [2] RED_B
        r"+\,\mu_i",  # [3] GREEN_B  ← will be crossed out
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
        r"+\,\mu_i",  # [3] ← same μ_i, will be crossed out
        r"= 0",
        font_size=34,
    )
    eq_k[0].set_color(GOLD)
    eq_k[1].set_color(BLUE_B)
    eq_k[2].set_color(RED_B)
    eq_k[3].set_color(GREEN_B)

    eq_j.move_to(UP * 1.1)
    eq_k.next_to(eq_j, DOWN, buff=0.55)

    minus_sign = MathTex(r"-", font_size=42, color=WHITE)
    minus_sign.move_to(
        [(eq_j.get_left()[0] - 0.5), (eq_j.get_bottom()[1] + eq_k.get_top()[1]) / 2, 0]
    )

    scene.play(Write(eq_j), run_time=1.1)
    scene.play(Write(eq_k), run_time=1.1)
    scene.play(FadeIn(minus_sign))
    scene.wait(0.3)

    # Cross out μ_i in both equations simultaneously
    cross_j = Cross(eq_j[3], color=RED, stroke_width=5)
    cross_k = Cross(eq_k[3], color=RED, stroke_width=5)
    scene.play(Create(cross_j), Create(cross_k), run_time=0.6)
    scene.play(
        eq_j[3].animate.set_opacity(0.20),
        eq_k[3].animate.set_opacity(0.20),
        run_time=0.4,
    )

    mu_cancel_lbl = Text(
        "μᵢ  is the same for all j  →  cancels out!", font_size=18, color=GREEN_B
    )
    mu_cancel_lbl.next_to(eq_k, DOWN, buff=0.35)
    scene.play(FadeIn(mu_cancel_lbl, shift=UP * 0.1))
    scene.wait(0.6)

    # ══════════════════════════════════════════════════════════════════════
    #  ACT 2  (15s – 30s): Decision rule formula appears
    # ══════════════════════════════════════════════════════════════════════
    scene.play(
        FadeOut(VGroup(eq_j, eq_k, minus_sign, cross_j, cross_k, mu_cancel_lbl)),
        run_time=0.7,
    )

    rule = MathTex(
        r"j^*",  # [0]
        r"= \arg\min_j \Bigl(",  # [1]
        r"c_{i,j}",  # [2]  GOLD
        r"-\,\frac{\lambda_1\,a_{i,j}}{N}",  # [3]  BLUE_B
        r"+\,\lambda_{2,j}",  # [4]  RED_B
        r"\Bigr)",  # [5]
        font_size=44,
    )
    rule[2].set_color(GOLD)
    rule[3].set_color(BLUE_B)
    rule[4].set_color(RED_B)
    rule.move_to(UP * 1.5)

    scene.play(Write(rule), run_time=1.5)

    # Arrow from j* down to "Select the best model" box
    select_box = RoundedRectangle(
        width=3.2,
        height=0.65,
        corner_radius=0.12,
        color=YELLOW,
        fill_color=YELLOW,
        fill_opacity=0.18,
        stroke_width=2,
    )
    select_lbl = Text("Select the best model", font_size=20, color=YELLOW)
    select_lbl.move_to(select_box)
    select_group = VGroup(select_box, select_lbl)
    select_group.next_to(rule, DOWN, buff=0.65)

    arr_select = Arrow(
        rule[0].get_bottom(),
        select_group.get_top(),
        buff=0.08,
        stroke_width=3,
        color=YELLOW,
        max_tip_length_to_length_ratio=0.22,
    )
    scene.play(GrowArrow(arr_select), FadeIn(select_group, shift=UP * 0.1))
    scene.wait(0.5)

    # ══════════════════════════════════════════════════════════════════════
    #  ACT 3  (30s – 50s): Scale → visual "balance" with 3 LLM boxes
    # ══════════════════════════════════════════════════════════════════════
    scene.play(
        rule.animate.scale(0.58).to_corner(UL, buff=0.55),
        FadeOut(VGroup(arr_select, select_group)),
        run_time=0.7,
    )

    # Three model boxes with different costs/quality/capacity
    # (base_cost, quality_disc, capacity_tax)
    model_data = [
        ("GPT-4o", 1.8, 1.5, 0.4),  # moderate cost, high quality, low tax
        ("Claude-3", 1.2, 0.7, 1.1),  # cheap, low quality, high capacity tax
        ("Llama-3", 0.9, 0.5, 0.2),  # cheapest, low quality, low tax → winner
    ]
    x_positions = [-3.8, 0.0, 3.8]

    model_boxes = []
    nets = []
    for (lbl, bc, qd, ct), xp in zip(model_data, x_positions):
        grp, net = make_weight_box(lbl, bc, qd, ct, xp)
        model_boxes.append(grp)
        nets.append(net)

    scene.play(LaggedStart(*[FadeIn(g) for g in model_boxes], lag_ratio=0.25))

    # Legend for the three components
    leg_items = VGroup(
        VGroup(
            Square(
                side_length=0.22,
                fill_color=GOLD_E,
                fill_opacity=0.8,
                stroke_color=GOLD,
                stroke_width=1,
            ),
            Text("Base Cost  c_{i,j}", font_size=15, color=GREY_A),
        ).arrange(RIGHT, buff=0.12),
        VGroup(
            Circle(
                radius=0.11,
                fill_color=BLUE_E,
                fill_opacity=0.8,
                stroke_color=BLUE_B,
                stroke_width=1,
            ),
            Text("Quality Discount  −λ₁a/N", font_size=15, color=GREY_A),
        ).arrange(RIGHT, buff=0.12),
        VGroup(
            Square(
                side_length=0.22,
                fill_color=RED_E,
                fill_opacity=0.8,
                stroke_color=RED_B,
                stroke_width=1,
            ),
            Text("Capacity Tax  +λ₂ⱼ", font_size=15, color=GREY_A),
        ).arrange(RIGHT, buff=0.12),
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
    leg_items.to_corner(UR, buff=0.55)
    scene.play(FadeIn(leg_items, shift=LEFT * 0.1))
    scene.wait(0.5)

    # Scanning dashed rect sweeps left → right across models
    scan_rect = DashedVMobject(
        Rectangle(width=2.1, height=4.8, color=WHITE),
        num_dashes=28,
    )
    scan_rect.move_to([x_positions[0], -0.2, 0])
    scene.play(FadeIn(scan_rect))
    scene.play(scan_rect.animate.move_to([x_positions[1], -0.2, 0]), run_time=0.6)
    scene.play(scan_rect.animate.move_to([x_positions[2], -0.2, 0]), run_time=0.6)

    # Winner: model with smallest net (index of min nets)
    winner_idx = int(np.argmin(nets))
    winner_grp = model_boxes[winner_idx]

    # Green tick + highlight winner
    tick = Text("✓", font_size=46, color=GREEN_A)
    tick.next_to(winner_grp, UP, buff=0.15)
    win_rect = SurroundingRectangle(
        winner_grp, color=GREEN_A, buff=0.18, corner_radius=0.12, stroke_width=2.5
    )
    scene.play(
        FadeOut(scan_rect),
        Create(win_rect),
        FadeIn(tick),
        Flash(
            winner_grp.get_center(), color=GREEN_A, flash_radius=0.8, line_length=0.25
        ),
    )
    scene.wait(1.5)


def play_scene15_dual_updates(scene):
    title = Text("Dual Variable Updates", font_size=48).to_edge(UP)
    eq1 = MathTex(
        r"\lambda_1^{t+1}=\max\!\left(\lambda_1^t+\eta_1\left(\alpha-\frac{1}{N}\sum_{i,j}a_{i,j}x_{i,j}\right),0\right)"
    ).scale(0.72)
    eq2 = MathTex(
        r"\lambda_{2,j}^{t+1}=\max\!\left(\lambda_{2,j}^t+\eta_2\left(\sum_i x_{i,j}-L_j\right),0\right)"
    ).scale(0.74)
    eq2.next_to(eq1, DOWN, buff=0.28)
    eq_group = VGroup(eq1, eq2).to_edge(LEFT, buff=0.5).shift(DOWN * 0.2)

    quality_label = (
        Text("Average Quality", font_size=24).to_edge(RIGHT, buff=1.2).shift(UP * 1.4)
    )
    quality_bar = Rectangle(width=0.5, height=2.2, stroke_color=WHITE).next_to(
        quality_label, DOWN, buff=0.2
    )
    quality_fill = Rectangle(
        width=0.5, height=1.0, fill_color=GREEN_E, fill_opacity=0.9, stroke_width=0
    )
    quality_fill.move_to(quality_bar.get_bottom() + UP * 0.5)
    alpha_line = DashedLine(
        quality_bar.get_left() + UP * 1.45,
        quality_bar.get_right() + UP * 1.45,
        color=YELLOW,
    )
    alpha_tag = MathTex(r"\alpha").scale(0.7).next_to(alpha_line, RIGHT, buff=0.08)

    lambda1 = DecimalNumber(0.2, num_decimal_places=2, color=YELLOW).next_to(
        quality_bar, RIGHT, buff=0.35
    )
    lambda1_tag = MathTex(r"\lambda_1").scale(0.8).next_to(lambda1, UP, buff=0.08)

    cap_label = (
        Text("Model 1 Load", font_size=24).to_edge(RIGHT, buff=1.2).shift(DOWN * 1.2)
    )
    cap_bar = Rectangle(width=2.2, height=0.45, stroke_color=WHITE).next_to(
        cap_label, DOWN, buff=0.2
    )
    cap_fill = Rectangle(
        width=1.4, height=0.45, fill_color=BLUE_E, fill_opacity=0.9, stroke_width=0
    )
    cap_fill.move_to(cap_bar.get_left() + RIGHT * 0.7)
    limit_line = DashedLine(
        cap_bar.get_left() + RIGHT * 1.4 + UP * 0.28,
        cap_bar.get_left() + RIGHT * 1.4 + DOWN * 0.28,
        color=YELLOW,
    )
    limit_tag = MathTex(r"L_j").scale(0.7).next_to(limit_line, DOWN, buff=0.07)

    lambda2 = DecimalNumber(0.15, num_decimal_places=2, color=ORANGE).next_to(
        cap_bar, RIGHT, buff=0.35
    )
    lambda2_tag = MathTex(r"\lambda_{2,j}").scale(0.8).next_to(lambda2, UP, buff=0.08)

    scene.play(FadeIn(title), FadeIn(eq_group))
    scene.play(
        FadeIn(
            VGroup(
                quality_label,
                quality_bar,
                quality_fill,
                alpha_line,
                alpha_tag,
                lambda1,
                lambda1_tag,
            )
        )
    )
    scene.play(
        quality_fill.animate.stretch_to_fit_height(0.55).move_to(
            quality_bar.get_bottom() + UP * 0.275
        ),
        lambda1.animate.set_value(0.95),
        run_time=1.5,
    )
    scene.play(
        FadeIn(
            VGroup(
                cap_label,
                cap_bar,
                cap_fill,
                limit_line,
                limit_tag,
                lambda2,
                lambda2_tag,
            )
        )
    )
    scene.play(
        cap_fill.animate.stretch_to_fit_width(2.05).move_to(
            cap_bar.get_left() + RIGHT * 1.025
        ),
        lambda2.animate.set_value(1.12),
        run_time=1.5,
    )
    scene.wait(1.0)


def play_scene16_dual_intuition(scene):
    title = Text("Intuition for Multipliers", font_size=48).to_edge(UP)
    left_panel = RoundedRectangle(
        width=5.8, height=2.3, corner_radius=0.12, color=YELLOW
    )
    right_panel = RoundedRectangle(
        width=5.8, height=2.3, corner_radius=0.12, color=ORANGE
    )
    panels = VGroup(left_panel, right_panel).arrange(DOWN, buff=0.55).shift(DOWN * 0.5)

    left_text = Text("Quality below target -> lambda_1 rises", font_size=28).move_to(
        left_panel
    )
    right_text = Text("Model overload -> lambda_2 rises", font_size=28).move_to(
        right_panel
    )
    left_impact = (
        MathTex(
            r"-\frac{\lambda_1 a_{i,j}}{N}\ \uparrow\Rightarrow\ \text{favor high-}a_{i,j}"
        )
        .scale(0.72)
        .next_to(left_panel, RIGHT, buff=0.25)
    )
    right_impact = (
        MathTex(
            r"\lambda_{2,j}\uparrow\Rightarrow\ \text{overloaded model becomes expensive}"
        )
        .scale(0.72)
        .next_to(right_panel, RIGHT, buff=0.25)
    )

    scene.play(FadeIn(title), FadeIn(panels), FadeIn(left_text), FadeIn(right_text))
    scene.play(Indicate(left_panel, color=YELLOW), FadeIn(left_impact))
    scene.play(Indicate(right_panel, color=ORANGE), FadeIn(right_impact))
    scene.wait(1.0)

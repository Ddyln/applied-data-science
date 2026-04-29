"""Function steps for scenes 5-6."""

from manim import *

import formulas
from components import text_box, row_of_var, mini_grid


def play_scene05_problem_formulation(scene):
    title = Text("Constrained Optimization Formulation", font_size=48).to_edge(UP)
    intro_title = Text("Setup and Variables", font_size=30, color=YELLOW).next_to(
        title, DOWN, buff=0.3
    )
    intro_n = MathTex(r"N:\ \text{number of queries}").scale(0.74)
    intro_m = MathTex(r"M:\ \text{number of models}").scale(0.74)
    intro_l = MathTex(r"L_j:\ \text{concurrency limit of model }j").scale(0.74)
    intro_alpha = MathTex(r"\alpha:\ \text{target average quality}").scale(0.74)
    intro_x = MathTex(
        r"x_{ij}\in\{0,1\}:\ \text{assign query }i\text{ to model }j"
    ).scale(0.74)
    intro_a = MathTex(r"a_{ij}\in[0,1]:\ \text{success probability/capability}").scale(
        0.74
    )
    intro_c = MathTex(
        r"c_{ij}:\ \text{money cost of using model }j\text{ for query }i"
    ).scale(0.74)
    intro_block = VGroup(
        intro_n,
        intro_m,
        intro_l,
        intro_alpha,
        intro_x,
        intro_a,
        intro_c,
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
    intro_group = VGroup(intro_title, intro_block).arrange(
        DOWN, aligned_edge=LEFT, buff=0.28
    )
    intro_group.move_to(ORIGIN)

    objective = formulas.objective().scale(0.8).next_to(title, DOWN, buff=0.6)
    find_label = Text("Find", font_size=34).next_to(objective, LEFT, buff=0.35)
    c1 = (
        formulas.assignment_constraint()
        .scale(0.74)
        .next_to(objective, DOWN, aligned_edge=LEFT)
    )
    c2 = formulas.quality_constraint().scale(0.74).next_to(c1, DOWN, aligned_edge=LEFT)
    c3 = formulas.capacity_constraint().scale(0.74).next_to(c2, DOWN, aligned_edge=LEFT)
    st_label = MathTex(r"\mathrm{s.t.}").scale(0.95).next_to(c1, LEFT, buff=0.5)
    VGroup(objective, c1, c2, c3).shift(LEFT * 2)
    find_label.shift(LEFT * 2)
    st_label.shift(LEFT * 2)

    tag_objective = Text("Minimize total routing cost", font_size=28, color=YELLOW)
    tag_objective.next_to(objective, RIGHT, buff=0.35).shift(RIGHT * 0.3)
    
    tag_c1 = Text("One model per query", font_size=25, color=BLUE_B).next_to(
        c1, RIGHT, buff=0.35
    ).shift(RIGHT * 1.0)

    tag_c2 = Text("Global quality target", font_size=25, color=GREEN_B).next_to(
        c2, RIGHT, buff=0.35
    )
    tag_c3 = Text("Model concurrency limit", font_size=25, color=ORANGE).next_to(
        c3, RIGHT, buff=0.35
    ).shift(RIGHT * 0.8)

    def focus_formula(formula, color, repeats=2):
        box = SurroundingRectangle(formula, color=color, buff=0.12, stroke_width=4)
        for _ in range(repeats):
            scene.play(Create(box), run_time=0.35)
            scene.play(FadeOut(box), run_time=0.25)

    scene.play(FadeIn(title))
    scene.play(FadeIn(intro_title))
    scene.play(
        LaggedStart(
            FadeIn(intro_n),
            FadeIn(intro_m),
            FadeIn(intro_l),
            FadeIn(intro_alpha),
            FadeIn(intro_x),
            FadeIn(intro_a),
            FadeIn(intro_c),
            lag_ratio=0.12,
        )
    )
    scene.wait(1.8)
    scene.play(FadeOut(intro_group))

    scene.play(FadeIn(find_label), FadeIn(objective), FadeIn(tag_objective))
    focus_formula(objective, YELLOW)

    scene.play(FadeIn(st_label), FadeIn(c1), FadeIn(tag_c1))
    focus_formula(c1, BLUE_B)
    scene.wait(5)
    scene.play(FadeIn(c2), FadeIn(tag_c2))
    focus_formula(c2, GREEN_B)
    scene.wait(5)
    scene.play(FadeIn(c3), FadeIn(tag_c3))
    focus_formula(c3, ORANGE)
    scene.wait(5)


def play_scene06_two_stage_framework(scene):
    # ── Objective label (top) ──────────────────────────────────────────────
    # objective = formulas.objective().scale(0.76).to_edge(UP, buff=0.42)
    # scene.play(FadeIn(objective))

    # ══════════════════════════════════════════════════════════════════════
    #  COORDINATE SYSTEM  (1920×1080 → 14.22 × 8.0 Manim units)
    #  Safe x range: -7.11 … +7.11   Safe y range: -4.0 … +4.0
    # ══════════════════════════════════════════════════════════════════════
    Y_C = -0.1  # vertical centre of the whole diagram (shifted up after title removal)

    q_card = text_box("Queries", w=1.55, h=0.56)
    q_card[1].scale(0.92)
    llm_card = text_box("LLM\nDescriptions", w=1.55, h=0.64)
    llm_card[1].scale(0.86)
    input_col = VGroup(q_card, llm_card).arrange(DOWN, buff=0.34)
    input_col.move_to([-6.05, Y_C, 0])

    # ── EMBEDDING ENCODER ─────────────────────────────────────────────────
    enc_box = RoundedRectangle(
        width=1.45, height=1.60, corner_radius=0.12, color=GREEN_C
    )
    enc_text = Paragraph(
        "Embedding\nEncoder", font_size=17, alignment="center", line_spacing=0.9
    ).move_to(enc_box)
    enc_group = VGroup(enc_box, enc_text)
    enc_group.move_to([-3.85, Y_C, 0])

    arr_q_enc = Arrow(
        q_card.get_right(), enc_box.get_left() + UP * 0.32, buff=0.06, stroke_width=3
    )
    arr_l_enc = Arrow(
        llm_card.get_right(),
        enc_box.get_left() + DOWN * 0.32,
        buff=0.06,
        stroke_width=3,
    )

    # ══════════════════════════════════════════════════════════════════════
    #  PREDICTOR dashed frame
    #  Left edge overlaps the encoder (starts at x ≈ -3.1, encoder centre -4.05)
    # ══════════════════════════════════════════════════════════════════════
    PRED_W = 7.25
    PRED_H = 4.00
    PRED_CX = -1.25  # centre x  →  left edge = -1.25 - 3.625 = -4.875 (covers encoder)
    pred_rect = RoundedRectangle(
        width=PRED_W, height=PRED_H, corner_radius=0.18, color=GREY_B
    )
    pred_frame = DashedVMobject(pred_rect, num_dashes=64)
    pred_frame.move_to([PRED_CX, Y_C, 0])
    pred_label = Text("Predictor", font_size=20, color=GREY_B).next_to(
        pred_frame, DOWN, buff=0.10
    )

    pfc = pred_frame.get_center()  # = [PRED_CX, Y_C, 0]

    # Branch y-levels: 4 equal lanes inside the predictor rectangle
    lane_top = Y_C + 0.90
    lane_2 = Y_C + 0.30
    lane_3 = Y_C - 0.30
    lane_bot = Y_C - 0.90

    grid_top = mini_grid().next_to(enc_box, RIGHT, buff=0.18).shift(UP * 0.62)
    grid_bot = mini_grid().next_to(enc_box, RIGHT, buff=0.18).shift(DOWN * 0.62)
    eq_top_mark = MathTex(r"E_q", font_size=22).next_to(grid_top, UP, buff=0.08)
    el_label = MathTex(r"E_l", font_size=22).next_to(grid_bot, DOWN, buff=0.08)
    grids = VGroup(grid_top, grid_bot, eq_top_mark, el_label)

    # Encoder right-edge x (after grids; use grid right edge as fan-out x)
    fan_x = grid_top.get_right()[0] + 0.08

    # ── TOP branch: E_q → Vector DB ──────────────────────────────────────
    vdb_box = RoundedRectangle(
        width=1.50, height=0.50, corner_radius=0.10, color=PURPLE
    )
    vdb_text = Text("Vector DB", font_size=15).move_to(vdb_box)
    vdb_group = VGroup(vdb_box, vdb_text)
    vdb_group.move_to([pfc[0] + 0.02, lane_top + 0.36, 0])
    vdb_above = Text("Average Top K Scores", font_size=13, color=GREY_A).next_to(
        vdb_group, UP, buff=0.07
    )
    arr_top = Arrow(
        grid_top.get_top(),
        vdb_box.get_left(),
        buff=0.08,
        stroke_width=3,
    )

    # ── MID branch: E_q⊙E_l → Sigmoid → a circles ───────────────────────
    sig_box = RoundedRectangle(
        width=1.40, height=0.54, corner_radius=0.09, color=ORANGE
    )
    sig_text = Text("Sigmoid", font_size=17).move_to(sig_box)
    sig_group = VGroup(sig_box, sig_text)
    sig_group.move_to([pfc[0] + 0.10, grid_top.get_center()[1], 0])

    eq_mid_lbl = MathTex(r"E_q \odot E_l", font_size=20).next_to(
        sig_group, LEFT, buff=0.40
    )

    a_row = VGroup(
        row_of_var("a", 2), MathTex(r"\cdots", font_size=22), row_of_var("a", 1)
    ).arrange(RIGHT, buff=0.12)
    a_row.next_to(sig_group, RIGHT, buff=0.50)
    a_box = SurroundingRectangle(
        a_row, color=BLUE_B, buff=0.07, corner_radius=0.08, stroke_width=2.2
    )

    arr_sig_a = Arrow(
        sig_group.get_right(), a_row.get_left(), buff=0.10, stroke_width=3
    )

    # ── BOT branch: E_q⊕E_l → Softmax → c circles ───────────────────────
    sft_box = RoundedRectangle(
        width=1.40, height=0.54, corner_radius=0.09, color=TEAL_B
    )
    sft_text = Text("Softmax", font_size=17).move_to(sft_box)
    sft_group = VGroup(sft_box, sft_text)
    sft_group.move_to([pfc[0] + 0.10, grid_bot.get_center()[1], 0])

    eq_bot_lbl = MathTex(r"E_q \oplus E_l", font_size=20).next_to(
        sft_group, LEFT, buff=0.40
    )

    arrow_eq_mid = Arrow(
        grid_top.get_right(),
        sig_group.get_left(),
        buff=0.08,
        stroke_width=3,
    )
    arrow_el_bot = Arrow(
        grid_bot.get_right(),
        sft_group.get_left(),
        buff=0.08,
        stroke_width=3,
    )
    arrow_eq_bot = Arrow(
        grid_top.get_right(),
        sft_group.get_left(),
        buff=0.08,
        stroke_width=3,
    )
    arrow_el_mid = Arrow(
        grid_bot.get_right(),
        sig_group.get_left(),
        buff=0.08,
        stroke_width=3,
    )

    c_row = VGroup(
        row_of_var("c", 2), MathTex(r"\cdots", font_size=22), row_of_var("c", 1)
    ).arrange(RIGHT, buff=0.12)
    c_row.next_to(sft_group, RIGHT, buff=0.50)
    c_box = SurroundingRectangle(
        c_row, color=BLUE, buff=0.07, corner_radius=0.08, stroke_width=2.2
    )

    arr_sft_c = Arrow(
        sft_group.get_right(), c_row.get_left(), buff=0.10, stroke_width=3
    )

    # ══════════════════════════════════════════════════════════════════════
    #  OPTIMIZER dashed frame
    #  Left edge just right of predictor right edge
    #  Predictor right = PRED_CX + PRED_W/2 = -1.35 + 3.55 = +2.20
    #  Optimizer right must stay < 7.11
    # ══════════════════════════════════════════════════════════════════════
    OPT_W = 3.30
    OPT_CX = (PRED_CX + PRED_W / 2) + 0.35 + OPT_W / 2  # gap 0.35
    opt_rect = RoundedRectangle(
        width=OPT_W, height=PRED_H, corner_radius=0.18, color=GREY_B
    )
    opt_frame = DashedVMobject(opt_rect, num_dashes=50)
    opt_frame.move_to([OPT_CX, Y_C, 0])
    opt_label = Text("Optimizer", font_size=20, color=GREY_B).next_to(
        opt_frame, DOWN, buff=0.10
    )

    ofc = opt_frame.get_center()

    opt_math = MathTex(
        r"\min\!\left(\sum_{i=1}^{N}\sum_{j=1}^{M} x_{i,j}C_{i,j}\right)\!,\ \text{s.t.}\ \ldots",
        font_size=16,
    ).move_to(ofc + UP * 1.12)

    lagrange_lbl = Text("+Lagrange Multipliers", font_size=14, color=YELLOW_C)
    lagrange_lbl.next_to(opt_math, DOWN, buff=0.18)

    dual_math = MathTex(r"L(x,\lambda_1,\lambda_{2,j},\mu_i)", font_size=16)
    dual_math.next_to(lagrange_lbl, DOWN, buff=0.16)

    dual_text = Text("Dual Optimization", font_size=14, color=GREY_A)
    dual_text.next_to(dual_math, DOWN, buff=0.12)

    model_box = RoundedRectangle(
        width=2.20, height=0.58, corner_radius=0.10, color=GOLD_B
    )
    model_text = Text("Model Indexes", font_size=18).move_to(model_box)
    model_group = VGroup(model_box, model_text).move_to(ofc + DOWN * 1.22)

    arr_pred_opt = Arrow(
        pred_frame.get_right(), opt_frame.get_left(), buff=0.08, stroke_width=4
    )
    arr_dual_mdl = Arrow(
        dual_text.get_bottom(), model_group.get_top(), buff=0.08, stroke_width=3
    )

    # estimated labels on bridge arrow
    est_c = MathTex(r"\hat{c}_{ij}", color=BLUE_B, font_size=26).next_to(
        arr_pred_opt, UP, buff=0.10
    )
    est_a = MathTex(r"\hat{a}_{ij}", color=BLUE_B, font_size=26).next_to(
        est_c, RIGHT, buff=0.18
    )
    vdb_to_a = Arrow(vdb_box.get_right(), a_box.get_left(), buff=0.10, stroke_width=3)
    vdb_to_c = Arrow(vdb_box.get_right(), c_box.get_left(), buff=0.10, stroke_width=3)

    # ══════════════════════════════════════════════════════════════════════
    #  ANIMATE
    # ══════════════════════════════════════════════════════════════════════
    # 1. Inputs
    scene.play(FadeIn(q_card), FadeIn(llm_card))
    scene.wait(5)

    # 2. Predictor frame (drawn behind content already placed)
    scene.play(Create(pred_frame), FadeIn(pred_label))

    # 3. Encoder + grids
    scene.play(GrowArrow(arr_q_enc), GrowArrow(arr_l_enc))
    scene.play(FadeIn(enc_group))
    scene.play(FadeIn(grids))
    scene.wait(5)

    # 4. Top branch – Vector DB
    # scene.play(FadeIn(eq_top_lbl))
    scene.play(Create(arr_top))
    scene.play(FadeIn(vdb_group), FadeIn(vdb_above))
    scene.wait(10)

    # 5. Mid branch – Sigmoid
    # scene.play(FadeIn(eq_mid_lbl))
    scene.play(FadeIn(sig_group), GrowArrow(arrow_eq_mid), GrowArrow(arrow_el_mid))
    scene.wait(5)
    scene.play(FadeIn(a_box), GrowArrow(arr_sig_a), FadeIn(a_row), GrowArrow(vdb_to_a))
    scene.wait(10)

    # 6. Bot branch – Softmax
    # scene.play(FadeIn(eq_bot_lbl))
    scene.play(FadeIn(sft_group), GrowArrow(arrow_el_bot), GrowArrow(arrow_eq_bot))
    scene.wait(5)
    scene.play(FadeIn(c_box), GrowArrow(arr_sft_c), FadeIn(c_row), GrowArrow(vdb_to_c))
    scene.wait(10)

    # 7. Predictor → Optimizer arrow + labels
    scene.play(GrowArrow(arr_pred_opt))
    # scene.play(FadeIn(est_c), FadeIn(est_a))

    # 8. Optimizer
    scene.play(Create(opt_frame), FadeIn(opt_label))
    scene.play(FadeIn(opt_math))
    scene.play(FadeIn(lagrange_lbl))
    scene.play(FadeIn(dual_math), FadeIn(dual_text))
    scene.play(GrowArrow(arr_dual_mdl))
    scene.play(FadeIn(model_group))

    # 9. Pulse
    # scene.play(Indicate(est_c, color=BLUE_B), Indicate(est_a, color=BLUE_B))
    scene.wait(1.5)

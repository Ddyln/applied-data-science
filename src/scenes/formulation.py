"""Function steps for scenes 5-6."""

from manim import *

import formulas
from components import text_box, row_of_var, mini_grid

# ─── Colour palette ───────────────────────────────────────────────────────────
COL_ENCODER       = PINK
COL_RETRIEVAL     = PURPLE
COL_TRAINING_SIG  = ORANGE
COL_TRAINING_SFT  = TEAL_B
COL_TRAINING      = ORANGE
COL_BRIDGE        = BLUE_B
COL_MODEL         = GOLD_B
COL_FUSION        = BLUE_B
COL_OPTIMIZER     = GREY_B
GREY_B            = "#555550"
GREY_A            = "#9C9A92"


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

# ─── Colour palette ───────────────────────────────────────────────────────────
COL_RETRIEVAL     = PURPLE
COL_TRAINING_SIG  = ORANGE
COL_TRAINING_SFT  = TEAL_B
COL_BRIDGE        = BLUE_B
COL_MODEL         = GOLD_B
COL_ACCURACY      = YELLOW_C
COL_LENGTH        = RED_B
GREY_B            = "#555550"
GREY_A            = "#9C9A92"
 
NAV_COLORS  = [PURPLE, ORANGE, BLUE_B, GOLD_B]
NAV_LABELS  = ["① Retrieval", "② Training", "③ Fusion", "④ Optimizer"]
NAV_DIM_BG  = "#2E2E2B"
NAV_DIM_TXT = "#6A6A62"
 
# ─── Navigator bar ────────────────────────────────────────────────────────────
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
 
 
# ══════════════════════════════════════════════════════════════════════════════
def play_scene06_two_stage_framework(scene):
 
    # ── Layout constants ──────────────────────────────────────────────────
    # Layout chữ L: Predictor row nằm trên (Y_C_PRED), Optimizer bên dưới-trái
    Y_C_PRED = 0.8    # Predictor group dịch lên trên
    Y_C_OPT  = -2  # Optimizer group nằm bên dưới

    PRED_W  = 11
    PRED_H  = 4
    PRED_CX = 0.5
    pred_right = PRED_CX + PRED_W / 2   

    OPT_W  = 3
    # Optimizer nằm bên dưới-trái: căn trái theo Predictor
    OPT_CX = pred_right - OPT_W / 2

    LANE_TOP = Y_C_PRED + 1.02
    LANE_MID = Y_C_PRED + 0.15
    LANE_BOT = Y_C_PRED - 0.78

    # ════════════════════════════════════════════════════════════════════
    #  INPUT CARDS
    # ════════════════════════════════════════════════════════════════════
    q_card   = text_box("Queries",           w=1.35, h=0.56,
                         box_color=GREY_B, text_color=WHITE, font_size=17)
    llm_card = text_box("LLM\nDescriptions", w=1.35, h=0.64,
                         box_color=GREY_B, text_color=WHITE, font_size=17)
    q_card[1].scale(0.92)
    llm_card[1].scale(0.86)
    VGroup(q_card, llm_card).arrange(DOWN, buff=0.34)
    VGroup(q_card, llm_card).move_to([-6.05, Y_C_PRED, 0])
 
    # ════════════════════════════════════════════════════════════════════
    #  EMBEDDING ENCODER + mini_grids
    # ════════════════════════════════════════════════════════════════════
    enc_box = RoundedRectangle(
        width=1.50, height=1.50, corner_radius=0.10,
        color=GREEN_C, fill_color=GREEN_C, fill_opacity=0.08
    )
    enc_text = Paragraph(
        "Embedding\nEncoder", font_size=17,
        alignment="center", line_spacing=0.9, color=GREEN_C
    ).move_to(enc_box)
    bert_lbl = Text("(BERT)", font_size=12, color=GREY_A)
    bert_lbl.next_to(enc_box, DOWN, buff=0.05)
    enc_group = VGroup(enc_box, enc_text, bert_lbl)
    enc_group.move_to([-3.85, Y_C_PRED, 0])
 
    arr_q_enc = Arrow(
        q_card.get_right(), enc_box.get_left() + UP * 0.32,
        buff=0.06, stroke_width=2.8, color=GREY_A,
        tip_length=0.16, max_tip_length_to_length_ratio=0.30
    )
    arr_l_enc = Arrow(
        llm_card.get_right(), enc_box.get_left() + DOWN * 0.32,
        buff=0.06, stroke_width=2.8, color=GREY_A,
        tip_length=0.16, max_tip_length_to_length_ratio=0.30
    )
 
    # mini_grids right of encoder
    grid_top = mini_grid()
    grid_bot = mini_grid()
    grid_top.next_to(enc_box, RIGHT, buff=0.18).shift(UP * 0.55)
    grid_bot.next_to(enc_box, RIGHT, buff=0.18).shift(DOWN * 0.55)
 
    eq_lbl = MathTex(r"E_q", font_size=22, color=GREEN_C).next_to(grid_top, UP,   buff=0.07)
    el_lbl = MathTex(r"E_l", font_size=22, color=GREEN_C).next_to(grid_bot, DOWN, buff=0.07)
    grids  = VGroup(grid_top, grid_bot, eq_lbl, el_lbl)
 
    fan_x = grid_top.get_right()[0] + 0.1
 
    # ════════════════════════════════════════════════════════════════════
    #  PREDICTOR dashed frame
    # ════════════════════════════════════════════════════════════════════
    pred_rect  = RoundedRectangle(
        width=PRED_W, height=PRED_H, corner_radius=0.18, color=GREY_B
    )
    pred_frame = DashedVMobject(pred_rect, num_dashes=64)
    pred_frame.move_to([PRED_CX, Y_C_PRED, 0])
    pred_label = Text("Predictor", font_size=17, color=GREY_B).next_to(
        pred_frame, DOWN, buff=0.10
    )
 
    # ════════════════════════════════════════════════════════════════════
    #  TOP LANE — Retrieval
    # ════════════════════════════════════════════════════════════════════
    VDB_CX = fan_x + 1.4
 
    vdb_box  = RoundedRectangle(
        width=1.4, height=0.52, corner_radius=0.10,
        color=COL_RETRIEVAL, fill_color=COL_RETRIEVAL, fill_opacity=0.14
    )
    vdb_text = Text("Vector DB", font_size=17, color=COL_RETRIEVAL).move_to(vdb_box)
    vdb_group = VGroup(vdb_box, vdb_text)
    vdb_group.move_to([VDB_CX, LANE_TOP, 0])
 
    vdb_above = Text("Average Top-K Scores", font_size=13, color=GREY_A).next_to(
        vdb_group, UP, buff=0.06
    )
    ret_lbl = Text("Retrieval-based", font_size=14, color=COL_RETRIEVAL).next_to(
        vdb_above, UP, buff=0.05
    )
 
    arr_top = Arrow(
        [fan_x, grid_top.get_center()[1], 0], vdb_box.get_left(),
        buff=0.06, stroke_width=2.6, color=COL_RETRIEVAL,
        tip_length=0.16, max_tip_length_to_length_ratio=0.28
    )
 
    RET_OUT_CX = VDB_CX + 1.5
    a_ret_row = MathTex(r"\mathbf{a^{ret}_{ij}}", font_size=22, color=COL_RETRIEVAL)
    c_ret_row = MathTex(r"\mathbf{l^{ret}_{ij}}", font_size=22, color=COL_RETRIEVAL)
    a_ret_row.move_to([RET_OUT_CX, LANE_TOP + 0.28, 0])
    c_ret_row.move_to([RET_OUT_CX, LANE_TOP - 0.30, 0])
 
    a_ret_box = SurroundingRectangle(a_ret_row, color=COL_RETRIEVAL, buff=0.07,
                                      corner_radius=0.08, stroke_width=1.8)
    c_ret_box = SurroundingRectangle(c_ret_row, color=COL_RETRIEVAL, buff=0.07,
                                      corner_radius=0.08, stroke_width=1.8)
 
    arr_vdb_a = Arrow(vdb_box.get_right(), a_ret_box.get_left(),
                      buff=0.06, stroke_width=2.2, color=COL_RETRIEVAL,
                      tip_length=0.13, max_tip_length_to_length_ratio=0.28)
    arr_vdb_c = Arrow(vdb_box.get_right(), c_ret_box.get_left(),
                      buff=0.06, stroke_width=2.2, color=COL_RETRIEVAL,
                      tip_length=0.13, max_tip_length_to_length_ratio=0.28)
 
    ret_out_grp = VGroup(
        a_ret_row, a_ret_box,
        c_ret_row, c_ret_box,
        arr_vdb_a, arr_vdb_c,
    )
    
    # ════════════════════════════════════════════════════════════════════
    #  MID LANE — Sigmoid
    # ════════════════════════════════════════════════════════════════════
    SIG_CX = fan_x + 1.4
 
    sig_box  = RoundedRectangle(
        width=1.4, height=0.54, corner_radius=0.09,
        color=COL_TRAINING_SIG, fill_color=COL_TRAINING_SIG, fill_opacity=0.12
    )
    sig_text = Text("Sigmoid", font_size=17, color=COL_TRAINING_SIG).move_to(sig_box)
    sig_group = VGroup(sig_box, sig_text)
    sig_group.move_to([SIG_CX, LANE_MID, 0])
 
    arrow_eq_mid = Arrow(
        grid_top.get_right(), sig_box.get_left(),
        buff=0.08, stroke_width=2.4, color=COL_TRAINING_SIG,
        tip_length=0.13, max_tip_length_to_length_ratio=0.28
    )
    arrow_el_mid = Arrow(
        grid_bot.get_right(), sig_box.get_left(),
        buff=0.08, stroke_width=2.2, color=COL_TRAINING_SIG,
        tip_length=0.12, max_tip_length_to_length_ratio=0.28
    )
 
    PRED_OUT_CX = SIG_CX + 1.6
 
    a_pred_row = MathTex(r"\mathbf{a^{pred}_{ij}}", font_size=22, color=COL_TRAINING_SIG)
    a_pred_row.move_to([PRED_OUT_CX, LANE_MID, 0])
    a_box = SurroundingRectangle(a_pred_row, color=COL_TRAINING_SIG, buff=0.07,
                                  corner_radius=0.08, stroke_width=1.8)
    arr_sig_a = Arrow(sig_box.get_right(), a_box.get_left(),
                      buff=0.08, stroke_width=2.4, color=COL_TRAINING_SIG,
                      tip_length=0.13, max_tip_length_to_length_ratio=0.28)
 
    # ════════════════════════════════════════════════════════════════════
    #  BOT LANE — Softmax
    # ════════════════════════════════════════════════════════════════════
    sft_box  = RoundedRectangle(
        width=1.4, height=0.54, corner_radius=0.09,
        color=COL_TRAINING_SFT, fill_color=COL_TRAINING_SFT, fill_opacity=0.12
    )
    sft_text = Text("Softmax", font_size=17, color=COL_TRAINING_SFT).move_to(sft_box)
    sft_group = VGroup(sft_box, sft_text)
    sft_group.move_to([SIG_CX, LANE_BOT, 0])
 
    arrow_eq_bot = Arrow(
        grid_top.get_right(), sft_box.get_left(),
        buff=0.08, stroke_width=2.2, color=COL_TRAINING_SFT,
        tip_length=0.12, max_tip_length_to_length_ratio=0.28
    )
    arrow_el_bot = Arrow(
        grid_bot.get_right(), sft_box.get_left(),
        buff=0.08, stroke_width=2.4, color=COL_TRAINING_SFT,
        tip_length=0.13, max_tip_length_to_length_ratio=0.28
    )
 
    c_pred_row = MathTex(r"\mathbf{l^{pred}_{ij}}", font_size=22, color=COL_TRAINING_SFT)
    c_pred_row.move_to([PRED_OUT_CX, LANE_BOT, 0])
    c_box = SurroundingRectangle(c_pred_row, color=COL_TRAINING_SFT, buff=0.07,
                                  corner_radius=0.08, stroke_width=1.8)
    arr_sft_c = Arrow(sft_box.get_right(), c_box.get_left(),
                      buff=0.08, stroke_width=2.4, color=COL_TRAINING_SFT,
                      tip_length=0.13, max_tip_length_to_length_ratio=0.28)
 
    # ════════════════════════════════════════════════════════════════════
    #  FUSION
    # ════════════════════════════════════════════════════════════════════
    FUS_X = PRED_OUT_CX + 2

    fus_box = RoundedRectangle(
        width=1.2, height=1.5, corner_radius=0.14,
        color=COL_BRIDGE, fill_color=COL_BRIDGE, fill_opacity=0.12
    )
    fus_box.move_to([FUS_X, Y_C_PRED, 0])

    fus_title = Text("Fusion", font_size=17, color=COL_BRIDGE)
    fus_title.move_to(fus_box.get_center())

    # ── Cổng vào fusion: dùng điểm trên cạnh trái của fus_box ──────────
    # a_ret (LANE_TOP + 0.28) và a_pred (LANE_MID) → cùng vào port trên
    # c_ret (LANE_TOP - 0.30) và c_pred (LANE_BOT) → cùng vào port dưới
    fus_left_x  = fus_box.get_left()[0]
    fus_right_x = fus_box.get_right()[0]
    fus_top_y   = fus_box.get_top()[1]
    fus_bot_y   = fus_box.get_bottom()[1]

    # Chia đều 2 port trên cạnh trái: port a ở 1/3 trên, port c ở 1/3 dưới
    port_in_a  = np.array([fus_left_x,  fus_top_y * 0.8 + fus_bot_y * 0.2, 0])
    port_in_c  = np.array([fus_left_x,  fus_top_y * 0.2 + fus_bot_y * 0.8, 0])

    # 2 port ra bên phải tương ứng
    port_out_a = np.array([fus_right_x, port_in_a[1], 0])
    port_out_c = np.array([fus_right_x, port_in_c[1], 0])

    # Arrows vào fusion — cùng đích = port_in_a
    arr_aret_fus = Arrow(
        a_ret_box.get_right(), port_in_a,
        buff=0.06, stroke_width=2.4, color=COL_ACCURACY,
        tip_length=0.14
    )
    arr_apred_fus = Arrow(
        a_box.get_right(), port_in_a,
        buff=0.06, stroke_width=2.4, color=COL_ACCURACY,
        tip_length=0.14
    )

    # Arrows vào fusion — cùng đích = port_in_c
    arr_cret_fus = Arrow(
        c_ret_box.get_right(), port_in_c,
        buff=0.06, stroke_width=2.4, color=COL_LENGTH,
        tip_length=0.14
    )
    arr_cpred_fus = Arrow(
        c_box.get_right(), port_in_c,
        buff=0.06, stroke_width=2.4, color=COL_LENGTH,
        tip_length=0.14
    )

    # Output từ fusion
    FUS_OUT_CX = FUS_X + 2.0

    a_fus_row = row_of_var("a", n_vars=3, color=COL_ACCURACY)
    a_fus_row.move_to([FUS_OUT_CX, port_out_a[1], 0])

    arr_fus_a = Arrow(
        port_out_a, a_fus_row.get_left(),
        buff=0.06, stroke_width=2.4, color=COL_ACCURACY,
        tip_length=0.14
    )

    c_fus_row = row_of_var("c", n_vars=3, color=COL_LENGTH)
    c_fus_row.move_to([FUS_OUT_CX, port_out_c[1], 0])

    arr_fus_c = Arrow(
        port_out_c, c_fus_row.get_left(),
        buff=0.06, stroke_width=2.4, color=COL_LENGTH,
        tip_length=0.14
    )

    fusion_all = VGroup(
        fus_box, fus_title,
        arr_aret_fus, arr_apred_fus,
        arr_cret_fus, arr_cpred_fus,
        a_fus_row, c_fus_row,
        arr_fus_a, arr_fus_c
    )

    # ════════════════════════════════════════════════════════════════════
    #  OPTIMIZER — bên dưới-trái tạo hình chữ L
    # ════════════════════════════════════════════════════════════════════
    opt_rect  = RoundedRectangle(
        width=OPT_W, height=0.9, corner_radius=0.18, color=GREY_B
    )
    opt_frame = DashedVMobject(opt_rect, num_dashes=50)
    opt_frame.move_to([OPT_CX, Y_C_OPT, 0])
    opt_label = Text("Optimizer", font_size=17, color=GREY_B).next_to(
        opt_frame, DOWN, buff=0.10
    )
 
    ofc = np.array([OPT_CX, Y_C_OPT, 0])

    lagrange_lbl = Text("Lagrange Multipliers", font_size=17, color=YELLOW_C)
    lagrange_lbl.next_to(opt_frame.get_center() + UP * 0.02, UP, buff=0.06)

    dual_text = Text("Dual Optimization", font_size=17, color=GREY_A)
    dual_text.next_to(lagrange_lbl, DOWN, buff=0.16)
 
    model_box  = RoundedRectangle(
        width=2.22, height=0.58, corner_radius=0.10,
        color=COL_MODEL, fill_color=COL_MODEL, fill_opacity=0.12
    )
    model_text = Text("Model Indexes", font_size=17, color=COL_MODEL).move_to(model_box)
    model_group = VGroup(model_box, model_text)
    # model_group.move_to(ofc + DOWN * 1.35)
    model_group.move_to([OPT_CX - OPT_W / 2 - 1.6, Y_C_OPT, 0])  # bên trái opt_frame

    # ── Mũi tên nối Predictor → Optimizer theo hình chữ L ───────────────
    # Đi từ cạnh dưới của pred_frame xuống, rồi rẽ trái đến opt_frame
    pred_bot_pt = np.array([OPT_CX, pred_frame.get_bottom()[1], 0])
    
    opt_top_pt  = np.array([OPT_CX, opt_frame.get_top()[1], 0])
  

    arr_pred_opt = Arrow(
        pred_bot_pt, opt_top_pt,
        buff=0.08, stroke_width=3.8, color=GREY_B
    )

    # arr_dual_mdl = Arrow(
    #     dual_text.get_bottom(), model_group.get_top(),
    #     buff=0.08, stroke_width=2.8, color=COL_MODEL
    # )
    arr_dual_mdl = Arrow(
        opt_frame.get_left(), model_group.get_right(),  # từ opt sang trái → model
        buff=0.08, stroke_width=2.8, color=COL_MODEL
    )
 
    # ════════════════════════════════════════════════════════════════════
    #  NAVIGATOR BAR + divider
    # ════════════════════════════════════════════════════════════════════
    nav_line = Line([-7.00, -3.10, 0], [7.00, -3.10, 0],
                    stroke_width=0.7, color=GREY_B, stroke_opacity=0.55)
    nav_bar  = make_nav_bar(active_idx=-1)

    phase1_title = Text(
        "Overview of OmniRouter Architecture",
        font_size=34,
        color=WHITE,
    ).to_edge(UP * 0.8)
 
    # ════════════════════════════════════════════════════════════════════
    #  HIGHLIGHT GROUPS
    # ════════════════════════════════════════════════════════════════════
    retrieval_grp = VGroup(
        ret_lbl, vdb_above, arr_top, vdb_group, ret_out_grp
    )
    training_grp = VGroup(
        sig_group, arrow_eq_mid, arrow_el_mid,
        arr_sig_a, a_pred_row, a_box,
        sft_group, arrow_eq_bot, arrow_el_bot,
        arr_sft_c, c_pred_row, c_box,
    )
    optimizer_grp = VGroup(
        opt_frame, opt_label,
        lagrange_lbl,
        dual_text,
        arr_dual_mdl, model_group,
    )
    all_pipeline = VGroup(
        q_card, llm_card,
        arr_q_enc, arr_l_enc, enc_group, grids,
        pred_frame, pred_label,
        retrieval_grp, training_grp, fusion_all,
        arr_pred_opt,
        optimizer_grp,
    )
 
    # ════════════════════════════════════════════════════════════════════
    #  ANIMATE
    # ════════════════════════════════════════════════════════════════════
    # scene.add(nav_line, nav_bar)

    scene.play(FadeIn(phase1_title), run_time=0.6)
 
    # 1. Inputs
    scene.play(FadeIn(q_card), FadeIn(llm_card), run_time=0.7)
    scene.wait(4)
 
    # 2. Predictor frame
    scene.play(Create(pred_frame), FadeIn(pred_label), run_time=0.9)
 
    # 3. Encoder + grids
    scene.play(GrowArrow(arr_q_enc), GrowArrow(arr_l_enc), run_time=0.6)
    scene.play(GrowFromCenter(enc_group), run_time=0.6)
    scene.play(FadeIn(grids), run_time=0.5)
    scene.wait(4)
 
    # 4. TOP lane — Vector DB
    scene.play(FadeIn(ret_lbl), run_time=0.3)
    scene.play(GrowArrow(arr_top), run_time=0.5)
    scene.play(GrowFromCenter(vdb_group), FadeIn(vdb_above), run_time=0.6)
    scene.play(
        GrowArrow(arr_vdb_a), GrowArrow(arr_vdb_c),
        FadeIn(a_ret_row), FadeIn(a_ret_box),
        FadeIn(c_ret_row), FadeIn(c_ret_box),
        run_time=0.7
    )
    scene.wait(8)
 
    # 5. MID lane — Sigmoid
    scene.play(
        GrowFromCenter(sig_group),
        GrowArrow(arrow_eq_mid), GrowArrow(arrow_el_mid),
        run_time=0.65
    )
    scene.wait(4)
    scene.play(
        GrowArrow(arr_sig_a),
        FadeIn(a_pred_row), FadeIn(a_box),
        run_time=0.6
    )
    scene.wait(8)
 
    # 6. BOT lane — Softmax
    scene.play(
        GrowFromCenter(sft_group),
        GrowArrow(arrow_el_bot), GrowArrow(arrow_eq_bot),
        run_time=0.65
    )
    scene.wait(4)
    scene.play(
        GrowArrow(arr_sft_c),
        FadeIn(c_pred_row), FadeIn(c_box),
        run_time=0.6
    )
    scene.wait(8)
 
    # 7. Fusion
    scene.play(FadeIn(fusion_all), run_time=0.7)
 
    # 8. Mũi tên xuống theo chiều L
    scene.play(GrowArrow(arr_pred_opt), run_time=0.6)
 
    # 9. Optimizer contents
    scene.play(Create(opt_frame), FadeIn(opt_label), run_time=0.7)
    scene.play(FadeIn(lagrange_lbl), run_time=0.4)
    scene.play(FadeIn(dual_text), run_time=0.5)
    scene.wait(4)
    scene.play(GrowArrow(arr_dual_mdl), run_time=0.5)
    scene.play(FadeIn(model_group), run_time=0.5)
    scene.wait(8)
 
    # ════════════════════════════════════════════════════════════════════
    #  PHASE 2 — NAVIGATOR BAR HIGHLIGHT
    # ════════════════════════════════════════════════════════════════════
    scene.play(FadeOut(phase1_title), run_time=0.5)
    scene.play(all_pipeline.animate.set_opacity(0.12), run_time=0.6)
 
    highlight_data = [
        (0, retrieval_grp, "① Retrieval-based  —  Vector DB, Average Top-K",  PURPLE),
        (1, training_grp,  "② Training-based  —  Sigmoid (a) & Softmax (c)",  ORANGE),
        (2, fusion_all,    "③ Fusion  —  VDB scores fuse với pred outputs",   BLUE_B),
        (3, optimizer_grp, "④ Optimizer  —  Lagrangian Dual → Model Indexes", GOLD_B),
    ]
 
    preview_text = None
    current_nav  = nav_bar
 
    for nav_idx, group, label_str, color in highlight_data:
        new_nav  = make_nav_bar(active_idx=nav_idx)
        new_text = Text(label_str, font_size=20, color=color).to_edge(UP, buff=0.22)
 
        anims = [
            group.animate.set_opacity(1.0),
            Transform(current_nav, new_nav),
        ]
        if preview_text is None:
            anims.append(FadeIn(new_text))
        else:
            anims.append(ReplacementTransform(preview_text, new_text))
 
        scene.play(*anims, run_time=0.55)
        preview_text = new_text
        current_nav  = new_nav
        scene.wait(2.0)
        scene.play(group.animate.set_opacity(0.12), run_time=0.40)
 
    # Restore all
    final_nav = make_nav_bar(active_idx=-1)
    scene.play(
        all_pipeline.animate.set_opacity(1.0),
        Transform(current_nav, final_nav),
        FadeOut(preview_text),
        run_time=0.75
    )
    scene.wait(2.0)
"""Function steps for scenes 7-11."""

from manim import *

from components import vector_strip, text_box
import formulas


def play_scene08_capability_prediction(scene):
    # ══════════════════════════════════════════════════════════════════════
    #  ACT 1: Title + full formula reveal
    # ══════════════════════════════════════════════════════════════════════
    title = Text("Capability Prediction", font_size=42).to_edge(UP, buff=0.45)
    formula = formulas.capability_prediction().move_to(ORIGIN)

    scene.play(FadeIn(title, shift=DOWN * 0.2))
    scene.play(Write(formula), run_time=2.2)
    scene.wait(2.0)

    # ══════════════════════════════════════════════════════════════════════
    #  ACT 2: Highlight E_q, E_l → pull out static vector strips
    # ══════════════════════════════════════════════════════════════════════
    # Dim everything except E_q^i [6] and E_l^j [8]
    highlight_idx = [6, 8]
    scene.play(
        *[
            formula[k].animate.set_opacity(0.25)
            for k in range(len(formula))
            if k not in highlight_idx
        ],
        *[formula[k].animate.set_opacity(1.0).set_color(YELLOW) for k in highlight_idx],
        run_time=0.8,
    )

    # Static vector strips
    vec_q = vector_strip(edge_color=GREEN_A, fill_color=GREEN_E)
    vec_q.next_to(formula[6], DOWN, buff=0.60).shift(LEFT * 2.4)
    eq_lbl = MathTex(r"E_q^i", font_size=26, color=GREEN_A).next_to(
        vec_q, LEFT, buff=0.18
    )

    vec_l = vector_strip(edge_color=TEAL_A, fill_color=TEAL_E)
    vec_l.next_to(formula[8], DOWN, buff=0.60).shift(RIGHT * 1.4)
    el_lbl = MathTex(r"E_l^j", font_size=26, color=TEAL_A).next_to(
        vec_l, LEFT, buff=0.18
    )

    scene.play(TransformFromCopy(formula[6], vec_q), FadeIn(eq_lbl), run_time=0.9)
    scene.play(TransformFromCopy(formula[8], vec_l), FadeIn(el_lbl), run_time=0.9)
    scene.wait(0.6)

    # ══════════════════════════════════════════════════════════════════════
    #  ACT 3: Dot product → "Similarity Score" box
    # ══════════════════════════════════════════════════════════════════════
    # Highlight the dot operator
    scene.play(
        formula[7].animate.set_opacity(1.0).set_color(YELLOW).scale(1.5),
        run_time=0.45,
    )

    # Vectors point to Dot Product
    sim_box = text_box("Dot Product", box_color=YELLOW_D, text_color=WHITE)
    sim_box.move_to(DOWN * 2.5)
    arrow_eq_merge_point = Arrow(vec_q.get_bottom(), sim_box.get_top(), stroke_width=3)
    arrow_el_merge_point = Arrow(vec_l.get_bottom(), sim_box.get_top(), stroke_width=3)

    scene.play(GrowArrow(arrow_eq_merge_point), GrowArrow(arrow_el_merge_point))

    scene.play(
        # FadeOut(VGroup(vec_q, vec_l, eq_lbl, el_lbl)),
        FadeIn(sim_box),
        run_time=0.6,
    )
    scene.wait(0.5)

    scene.play(
        FadeOut(
            VGroup(
                arrow_eq_merge_point, arrow_el_merge_point, vec_q, vec_l, eq_lbl, el_lbl
            )
        )
    )

    # ══════════════════════════════════════════════════════════════════════
    #  ACT 4: W1, b1 neural gate → "Raw Score" box
    # ══════════════════════════════════════════════════════════════════════
    # Highlight W1 and b1 in formula
    scene.play(
        formula[4].animate.set_opacity(1.0).set_color(BLUE_B),
        formula[5].animate.set_opacity(1.0).set_color(BLUE_B),
        formula[9].animate.set_opacity(1.0).set_color(BLUE_B),
        formula[10].animate.set_opacity(1.0).set_color(BLUE_B),
        formula[11].animate.set_opacity(1.0).set_color(BLUE_B),
        run_time=0.5,
    )

    # move simbox left
    scene.play(sim_box.animate.shift(LEFT * 2 + UP * 0.5), run_time=1)

    # Neural node gate (W1, b1)
    node_circ = Circle(
        radius=0.45,
        color=BLUE_B,
        fill_color=BLUE_E,
        fill_opacity=0.30,
        stroke_width=2.5,
    )
    node_lbl = MathTex(r"W_1,\,b_1", font_size=20, color=BLUE_B).move_to(node_circ)
    node = VGroup(node_circ, node_lbl)
    node.next_to(sim_box, RIGHT, buff=1.1)

    arr_in = Arrow(
        sim_box.get_right(), node.get_left(), buff=0.10, stroke_width=3, color=WHITE
    )
    scene.play(GrowArrow(arr_in), FadeIn(node))

    # Transform: new "Raw Score" box exits the gate in ORANGE
    raw_box = text_box("score", w=1.4, box_color=ORANGE, text_color=WHITE)
    raw_box.next_to(node, RIGHT, buff=1.1)

    arr_out = Arrow(
        node.get_right(), raw_box.get_left(), buff=0.10, stroke_width=3, color=WHITE
    )
    scene.play(GrowArrow(arr_out), FadeIn(raw_box))
    scene.wait(0.5)

    # ══════════════════════════════════════════════════════════════════════
    #  ACT 5: Sigmoid curve → "Capability Score" box
    # ══════════════════════════════════════════════════════════════════════
    # Highlight sigma
    scene.play(
        formula[2].animate.set_opacity(1.0).set_color(GOLD),
        formula[3].animate.set_opacity(1.0).set_color(GOLD),
        formula[12].animate.set_opacity(1.0).set_color(GOLD),
        run_time=0.4,
    )
    scene.wait(1)

    # Sigmoid axes
    axes = Axes(
        x_range=[-6, 6, 2],
        y_range=[-0.05, 1.1, 0.5],
        x_length=5.2,
        y_length=3.0,
        axis_config={"color": GREY_B, "stroke_width": 2},
        tips=False,
    ).shift(DOWN * 0.5)

    sigmoid_curve = axes.plot(
        lambda x: 1 / (1 + np.exp(-x)),
        color=GOLD,
        stroke_width=3,
    )
    x_lbl = MathTex(r"z", font_size=24).next_to(axes.x_axis.get_end(), RIGHT, buff=0.08)
    y_lbl = MathTex(r"\sigma(z)", font_size=22).next_to(
        axes.y_axis.get_end(), UP, buff=0.08
    )
    # "Raw Score" box glides along the sigmoid curve
    # We animate it moving left→right across the x-axis while tracking the curve
    INPUT_X = 2.2  # representative x value on the sigmoid
    INPUT_Y = 1 / (1 + np.exp(-INPUT_X))  # ≈ 0.90

    # Raw Score box travels from its position to the x-axis entry point
    x_entry = axes.c2p(INPUT_X, 0)
    # scene.play(, run_time=0.8)

    # Clear the gate area; shrink formula to top-left
    scene.play(
        FadeOut(VGroup(arr_in, node, arr_out, sim_box)),
        formula.animate.scale(0.75).shift(UP * 2 + LEFT * 3),
        raw_box.animate.move_to(x_entry).shift(DOWN * 0.75),
        run_time=0.7,
    )

    scene.play(
        Create(axes),
        Write(x_lbl),
        Write(y_lbl),
        run_time=0.8,
    )
    scene.play(Create(sigmoid_curve), run_time=1.0)

    # Vertical dashed line from x-axis up to the curve
    v_line = DashedLine(
        axes.c2p(INPUT_X, 0),
        axes.c2p(INPUT_X, INPUT_Y),
        color=GREY_A,
        stroke_width=2,
        dash_length=0.09,
    )
    curve_dot = Dot(axes.c2p(INPUT_X, INPUT_Y), color=GOLD, radius=0.10)
    scene.play(Create(v_line), FadeIn(curve_dot))

    # Horizontal dashed line from curve to y-axis
    h_line = DashedLine(
        axes.c2p(INPUT_X, INPUT_Y),
        axes.c2p(0, INPUT_Y),
        color=GREY_A,
        stroke_width=2,
        dash_length=0.09,
    )
    y_dot = Dot(axes.c2p(0, INPUT_Y), color=GOLD, radius=0.10)
    scene.play(Create(h_line), FadeIn(y_dot))
    scene.wait(0.3)

    # Raw Score box transforms into "Capability Score (85%)" in GREEN
    cap_box = text_box(
        "Predicted Capability",
        box_color=GREEN_D,
        text_color=WHITE,
        w=3.0,
        font_size=20,
    )
    cap_box.move_to(axes.c2p(INPUT_X, INPUT_Y) + UP * 0.55)

    scene.play(
        Transform(raw_box, cap_box),
        run_time=0.75,
    )
    scene.play(
        Flash(cap_box.get_center(), color=GREEN_A, flash_radius=0.6, line_length=0.22)
    )
    scene.wait(0.4)

    # Capability Score box flies back and lands on a^pred_{i,j} in the formula
    lhs_pos = formula[0].get_center()
    scene.play(
        raw_box.animate.scale(0.55).move_to(lhs_pos).set_opacity(0),
        # FadeOut(raw_box),
        formula[0].animate.set_opacity(1.0).set_color(GREEN_D),
        formula[1].animate.set_opacity(1.0).set_color(GREEN_D),
    )

    scene.wait(1)

    scene.play(
        FadeOut(
            VGroup(axes, x_lbl, y_lbl, sigmoid_curve, v_line, h_line, curve_dot, y_dot)
        ),
        formula.animate.scale(1.3).move_to(ORIGIN),
    )

    scene.wait(1.5)


def play_scene09_length_prediction(scene):
    # ══════════════════════════════════════════════════════════════════════
    #  ACT 1: Title + formula reveal
    # ══════════════════════════════════════════════════════════════════════
    title = Text("Length Prediction", font_size=42).to_edge(UP, buff=0.45)

    formula = formulas.length_prediction().move_to(ORIGIN)

    # Small annotation under l^pred
    pred_annot = Text("Predicted Token Length", font_size=16, color=GREY_A)
    pred_annot.next_to(formula[0], DOWN, buff=0.18)

    scene.play(FadeIn(title, shift=DOWN * 0.2))
    scene.play(Write(formula), run_time=2.2)
    scene.play(FadeIn(pred_annot, shift=UP * 0.1))
    scene.wait(1.5)

    # ══════════════════════════════════════════════════════════════════════
    #  ACT 2 : E_q + E_l vector addition → "Combined Context"
    # ══════════════════════════════════════════════════════════════════════
    # Dim everything except E_q^i [8] and E_l^j [10]
    highlight_idx = [8, 10]  # also highlight the "+" operator
    scene.play(
        *[
            formula[k].animate.set_opacity(0.22)
            for k in range(len(formula))
            if k not in highlight_idx
        ],
        *[formula[k].animate.set_opacity(1.0).set_color(YELLOW) for k in highlight_idx],
        FadeOut(pred_annot),
        run_time=0.8,
    )

    # Two static vector strips appear below formula
    vec_q = vector_strip(edge_color=GREEN_A, fill_color=GREEN_E)
    vec_q.next_to(formula[8], DOWN, buff=0.65).shift(LEFT * 2.8)
    eq_lbl = MathTex(r"E_q^i", font_size=26, color=GREEN_A).next_to(
        vec_q, LEFT, buff=0.18
    )

    vec_l = vector_strip(edge_color=TEAL_A, fill_color=TEAL_E)
    vec_l.next_to(formula[10], DOWN, buff=0.65).shift(RIGHT)
    el_lbl = MathTex(r"E_l^j", font_size=26, color=TEAL_A).next_to(
        vec_l, LEFT, buff=0.18
    )

    scene.play(TransformFromCopy(formula[8], vec_q), FadeIn(eq_lbl), run_time=0.85)
    scene.play(TransformFromCopy(formula[10], vec_l), FadeIn(el_lbl), run_time=0.85)
    scene.wait(0.4)

    # Addition: strips slide ON TOP of each other (not collide — overlap/stack)
    merge_point = DOWN * 1.65
    scene.play(
        formula[9].animate.set_opacity(1.0).set_color(YELLOW),
        VGroup(vec_q, eq_lbl).animate.move_to(merge_point + LEFT * 0.02),
        VGroup(vec_l, el_lbl).animate.move_to(merge_point + LEFT * 0.02),
        run_time=0.9,
    )

    combined_box = text_box(
        "Combined Context",
        box_color=PURPLE_B,
        text_color=WHITE,
        w=2.8,
        h=0.68,
        font_size=21,
    )
    combined_box.move_to(merge_point)

    scene.play(
        FadeOut(VGroup(vec_q, vec_l, eq_lbl, el_lbl)),
        FadeIn(combined_box),
        run_time=0.6,
    )
    scene.play(Flash(merge_point, color=PURPLE_A, flash_radius=0.70, line_length=0.25))
    scene.wait(0.5)

    # ══════════════════════════════════════════════════════════════════════
    #  ACT 3: W2/b2 gate → Softmax → Bar chart (buckets)
    # ══════════════════════════════════════════════════════════════════════
    # Highlight W2, b2
    scene.play(
        formula[6].animate.set_opacity(1.0).set_color(BLUE_B),
        formula[7].animate.set_opacity(1.0).set_color(BLUE_B),
        formula[11].animate.set_opacity(1.0).set_color(BLUE_B),
        formula[12].animate.set_opacity(1.0).set_color(BLUE_B),
        formula[13].animate.set_opacity(1.0).set_color(BLUE_B),
        run_time=0.5,
    )

    scene.play(combined_box.animate.shift(LEFT * 2.3))

    # Neural gate node
    node_circ = Circle(
        radius=0.45,
        color=BLUE_B,
        fill_color=BLUE_E,
        fill_opacity=0.30,
        stroke_width=2.5,
    )
    node_lbl = MathTex(r"W_2,\,b_2", font_size=20, color=BLUE_B).move_to(node_circ)
    node = VGroup(node_circ, node_lbl)
    node.next_to(combined_box, RIGHT, buff=1.0)

    arr_to_node = Arrow(
        combined_box.get_right(),
        node.get_left(),
        buff=0.10,
        stroke_width=3,
        color=WHITE,
    )
    scene.play(GrowArrow(arr_to_node), FadeIn(node))
    # scene.wait(2)

    # Softmax box exits the node
    softmax_box = text_box(
        "softmax", box_color=ORANGE, text_color=WHITE, w=1.9, h=0.65, font_size=22
    )
    softmax_box.next_to(node, RIGHT, buff=1.0)
    arr_to_sm = Arrow(
        node.get_right(), softmax_box.get_left(), buff=0.10, stroke_width=3, color=WHITE
    )

    # Highlight softmax in formula
    scene.play(
        formula[4].animate.set_opacity(1.0).set_color(ORANGE),
        formula[5].animate.set_opacity(1.0).set_color(ORANGE),
        formula[14].animate.set_opacity(1.0).set_color(ORANGE),
        run_time=0.4,
    )
    scene.wait(0.25)
    scene.play(GrowArrow(arr_to_sm), FadeIn(softmax_box))
    scene.wait(1)
    scene.play(
        FadeOut(VGroup(arr_to_node, node, arr_to_sm, combined_box, softmax_box)),
        formula.animate.scale(0.75).move_to(UP * 2 + LEFT * 3),
    )

    # Bar chart (bucket histogram) shoots out below the softmax box
    bucket_labels = ["0-50", "50-150", "150-350", "350-600", "600+"]
    bucket_heights = [0.5, 1.0, 2.2, 1.3, 0.6]  # "150-350" bucket wins

    bar_width = 0.52
    bar_group = VGroup()
    for h in bucket_heights:
        bar = Rectangle(
            width=bar_width,
            height=h,
            fill_color=TEAL_D,
            fill_opacity=0.75,
            stroke_color=TEAL_A,
            stroke_width=1.5,
        )
        bar_group.add(bar)
    bar_group.arrange(RIGHT, aligned_edge=DOWN, buff=0.18)

    # x-axis tick labels
    tick_labels = VGroup(
        *[
            Text(lbl, font_size=12, color=GREY_A).next_to(bar_group[i], DOWN, buff=0.10)
            for i, lbl in enumerate(bucket_labels)
        ]
    )
    x_axis = Line(
        bar_group.get_corner(DL) + LEFT * 0.18,
        bar_group.get_corner(DR) + RIGHT * 0.18,
        color=GREY_B,
        stroke_width=2,
    )
    x_axis.add_tip(tip_length=0.12, tip_width=0.12)
    y_axis = Line(
        bar_group.get_corner(DL) + LEFT * 0.18,
        bar_group.get_corner(UL) + LEFT * 0.18 + UP * 0.20,
        color=GREY_B,
        stroke_width=2,
    )
    y_axis.add_tip(tip_length=0.12, tip_width=0.12)
    x_axis_lbl = Text("tokens", font_size=13, color=GREY_A)
    y_axis_lbl = Text("score", font_size=13, color=GREY_A).next_to(
        y_axis, UP + LEFT, buff=0.08
    )

    chart = VGroup(x_axis, y_axis, y_axis_lbl, bar_group, tick_labels)
    chart.next_to(softmax_box, DOWN, buff=0.50).shift(UP * 3 + LEFT * 3)
    x_axis_lbl.next_to(x_axis, RIGHT + DOWN, buff=0.12)
    full_chart = VGroup(chart, x_axis_lbl)
    full_chart.scale(1.25)

    scene.play(
        LaggedStart(
            *[GrowFromEdge(b, DOWN) for b in bar_group],
            lag_ratio=0.15,
        ),
        Create(x_axis),
        Create(y_axis),
        FadeIn(y_axis_lbl),
        FadeIn(tick_labels),
        FadeIn(x_axis_lbl),
        run_time=1.1,
    )

    # ══════════════════════════════════════════════════════════════════════
    #  ACT 4: bs × winning bucket → "Estimated Length" box
    # ══════════════════════════════════════════════════════════════════════
    # Highlight bs in formula
    scene.play(
        formula[2].animate.set_opacity(1.0).set_color(GOLD),
        formula[3].animate.set_opacity(1.0).set_color(GOLD),
        run_time=0.4,
    )

    # Move bs to a fixed middle-left anchor and map winning bar -> bucket_i.
    bs_target = chart.get_center() + LEFT * 5.2 + UP * 0.15
    bs_mob = MathTex(r"bs \cdot", font_size=34, color=GOLD).move_to(bs_target)
    scene.play(TransformFromCopy(formula[2], bs_mob), run_time=0.65)

    bucket_box = text_box(
        "bucket_i", box_color=PURPLE_B, text_color=WHITE, w=1.9, h=0.58, font_size=22
    )
    bucket_box.next_to(bs_mob, RIGHT, buff=0.1)
    bar_to_bucket = Arrow(
        bar_group[2].get_left() + UP * 0.10,
        bucket_box.get_right(),
        buff=0.08,
        stroke_width=3,
        color=YELLOW_A,
    )
    bar_group[2].set_fill(YELLOW, opacity=0.90)
    bar_group[2].set_stroke(YELLOW_A, width=2.5)

    scene.play(
        Indicate(bar_group[2], color=YELLOW, scale_factor=1.12),
    )
    scene.wait(0.5)
    scene.play(GrowArrow(bar_to_bucket), FadeIn(bucket_box), run_time=0.6)
    scene.wait(0.3)

    bs_bucket_group = VGroup(bs_mob, bucket_box)
    # Entire chart collapses → "Estimated Length: 250 tokens" blue box
    est_box = text_box(
        "Estimated Length",
        box_color=BLUE_D,
        text_color=WHITE,
        w=3,
        h=0.72,
        font_size=20,
    )
    est_box.move_to(bs_bucket_group.get_center())

    scene.play(
        FadeOut(VGroup(chart, x_axis_lbl, bs_mob, bucket_box, bar_to_bucket)),
        Transform(
            bs_bucket_group,
            est_box,
            replace_mobject_with_target_in_scene=True,
        ),
        FadeOut(bar_to_bucket),
        run_time=0.80,
    )
    scene.play(
        Flash(est_box.get_center(), color=BLUE_A, flash_radius=0.65, line_length=0.24)
    )
    scene.wait(0.3)

    # est box go to l^pred in formula
    scene.play(
        est_box.animate.move_to(formula[0].get_center()).scale(0.55).set_opacity(0),
        formula[0].animate.set_opacity(1.0).set_color(GREEN_D),
        formula[1].animate.set_opacity(1.0).set_color(GREEN_D),
    )
    scene.play(
        Flash(
            formula[0].get_center(), color=GREEN_A, flash_radius=0.5, line_length=0.18
        )
    )
    scene.wait(1)

    scene.play(
        formula.animate.scale(1.3).move_to(ORIGIN),
        FadeOut(full_chart),
    )

    scene.wait(1)


def play_scene10_retrieval_augmentation(scene):
    # ══════════════════════════════════════════════════════════════════════
    #  ACT 1: Title + Vector space with radar scan
    # ══════════════════════════════════════════════════════════════════════
    title = Text("Retrieval Augmentation", font_size=42).to_edge(UP, buff=0.45)
    scene.play(FadeIn(title, shift=DOWN * 0.2))

    rng = np.random.default_rng(7)
    bg_coords = [(rng.uniform(-5.5, 5.5), rng.uniform(-2.8, 1.6)) for _ in range(38)]

    history_coords = [
        (-0.6, 0.5),  # idx 0  – nearest
        (0.8, 0.7),  # idx 1  – nearest
        (-0.9, -0.4),  # idx 2  – nearest
        (0.4, -0.8),  # idx 3  – medium
        (-1.6, 1.0),  # idx 4  – farther
        (1.5, -0.5),  # idx 5  – farther
    ]
    sim_weights = [0.92, 0.85, 0.78, 0.61, 0.44, 0.38]
    hist_a = [1, 1, 0, 1, 0, 1]
    hist_l = [210, 190, 230, 175, 260, 220]

    bg_dots = VGroup(
        *[
            Dot(point=[x, y, 0], radius=0.035, color=BLUE_E, fill_opacity=0.45)
            for x, y in bg_coords
        ]
    )
    hist_dots = VGroup(
        *[
            Dot(point=[x, y, 0], radius=0.060, color=BLUE_B, fill_opacity=0.80)
            for x, y in history_coords
        ]
    )

    EQ_POS = np.array([0.0, 0.0, 0.0])
    eq_dot = Dot(EQ_POS, radius=0.10, color=YELLOW)
    eq_dot_lbl = MathTex(r"E_q^i", font_size=26, color=YELLOW).next_to(
        eq_dot, UR, buff=0.08
    )

    scene.play(FadeIn(bg_dots), FadeIn(hist_dots))
    scene.play(FadeIn(eq_dot), Write(eq_dot_lbl))

    # Radar ripple
    for scale in [1.0, 2.0, 3.2]:
        ripple = Circle(
            radius=0.18 * scale,
            color=YELLOW,
            stroke_width=2,
            stroke_opacity=max(0.1, 0.7 - scale * 0.18),
        )
        ripple.move_to(EQ_POS)
        scene.play(ShowPassingFlash(ripple, time_width=0.6), run_time=0.55)

    # ══════════════════════════════════════════════════════════════════════
    #  ACT 2: Top-K highlight + similarity lines
    # ══════════════════════════════════════════════════════════════════════
    scene.play(
        *[d.animate.set_color(TEAL_A).scale(1.15) for d in hist_dots], run_time=0.5
    )

    TOP_K = [0, 1, 2]
    top_dots = VGroup(*[hist_dots[i] for i in TOP_K])
    far_dots = VGroup(
        *[hist_dots[i] for i in range(len(history_coords)) if i not in TOP_K]
    )

    scene.play(
        *[d.animate.set_color(BLUE_E).set_opacity(0.35) for d in far_dots],
        *[d.animate.set_color(TEAL_A).scale(1.1) for d in top_dots],
        run_time=0.6,
    )

    # Similarity lines – thickness ∝ sim weight
    sim_lines = VGroup()
    for i in TOP_K:
        x, y = history_coords[i]
        w = sim_weights[i]
        line = Line(
            EQ_POS,
            [x, y, 0],
            color=YELLOW_A,
            stroke_width=1.5 + w * 4.5,
            stroke_opacity=0.4 + w * 0.55,
        )
        sim_lines.add(line)

    scene.play(LaggedStart(*[Create(l) for l in sim_lines], lag_ratio=0.25))
    scene.wait(0.4)

    # ══════════════════════════════════════════════════════════════════════
    #  ACT 2b: Q_k label box — arrows from Top-K dots point to it
    # ══════════════════════════════════════════════════════════════════════
    # Build  Q_k = { E_q^{m_1}, E_q^{m_2},... E_q^{m_k} }  label in bottom-right
    qk_label = MathTex(
        r"Q_k = \{E_q^{m_1},\; E_q^{m_2},...\; E_q^{m_k}\}",
        font_size=28,
        color=TEAL_A,
    )
    qk_box = SurroundingRectangle(
        qk_label,
        color=TEAL_A,
        buff=0.18,
        corner_radius=0.10,
        stroke_width=1.8,
    )
    qk_group = VGroup(qk_label, qk_box)
    qk_group.shift(RIGHT * 4 + UP * 2)

    scene.play(FadeIn(qk_group, shift=UP * 0.15))

    # One arrow per Top-K dot → the Q_k box
    # Arrows originate from each highlighted dot and converge on the left edge of the box
    qk_arrows = VGroup()
    for i in TOP_K:
        x, y = history_coords[i]
        start = np.array([x, y, 0])
        end = qk_box.get_left()
        arr = DashedLine(
            start,
            end,
            buff=0.10,
            stroke_width=2.2,
            color=TEAL_A,
        )
        qk_arrows.add(arr)

    scene.play(
        LaggedStart(*[Create(a) for a in qk_arrows], lag_ratio=0.25),
        run_time=1.0,
    )
    scene.wait(0.6)

    # ══════════════════════════════════════════════════════════════════════
    #  ACT 3: Fade space → two weighted-average formulas
    # ══════════════════════════════════════════════════════════════════════
    scene.play(
        bg_dots.animate.set_opacity(0.10),
        hist_dots.animate.set_opacity(0.12),
        sim_lines.animate.set_opacity(0.12),
        eq_dot.animate.set_opacity(0.15),
        eq_dot_lbl.animate.set_opacity(0.15),
        qk_arrows.animate.set_opacity(0.15),
        run_time=0.7,
    )

    # Two formulas
    formula_l = formulas.retrieval_length()
    formula_a = formulas.retrieval_capability()

    formula_group = VGroup(formula_l, formula_a).arrange(DOWN, buff=0.70)
    # Shift left so the Q_k box (bottom-right) stays visible beside the formulas
    formula_group.move_to(ORIGIN + LEFT * 1.0)

    scene.play(Write(formula_l), run_time=1.6)
    scene.play(Write(formula_a), run_time=1.6)
    scene.wait(0.4)

    # Highlight sim() in numerator AND denominator of both formulas
    sim_parts = [
        *formula_l.get_parts_by_tex(r"\mathrm{sim}(E_q^i, E_{q_m})"),
        *formula_a.get_parts_by_tex(r"\mathrm{sim}(E_q^i, E_{q_m})"),
    ]
    scene.play(
        *[p.animate.set_color(YELLOW).set_opacity(1.0) for p in sim_parts],
        run_time=0.6,
    )

    # Also re-highlight the Q_k box to bridge the visual connection
    scene.play(
        qk_box.animate.set_color(YELLOW).set_stroke(width=2.5),
        qk_label.animate.set_color(YELLOW),
        run_time=0.5,
    )

    # Highlight the ∑_{m∈Q_k} parts in the formulas that reference Q_k
    qk_parts = [
        *formula_l.get_parts_by_tex(r"Q_k"),
        *formula_a.get_parts_by_tex(r"Q_k"),
    ]
    scene.play(
        *[Indicate(p, color=TEAL_A, scale_factor=1.22) for p in qk_parts],
        run_time=0.7,
    )
    scene.wait(0.3)

    # Weighted-average label
    wa_label = VGroup(
        MathTex(r"\rightarrow", font_size=17, color=GREY_A),
        Text("Weighted Average (weight = similarity)", font_size=17, color=GREY_A),
    ).arrange(RIGHT, buff=0.1)
    wa_label.next_to(formula_group, DOWN, buff=0.40)
    scene.play(FadeIn(wa_label, shift=UP * 0.1))

    # Pulse sim parts twice
    for _ in range(2):
        scene.play(
            *[Indicate(p, color=YELLOW, scale_factor=1.18) for p in sim_parts],
            run_time=0.7,
        )

    scene.wait(1.5)


def play_scene11_fusion(scene):
    # ══════════════════════════════════════════════════════════════════════
    #  ACT 1: Title + two-column recap
    # ══════════════════════════════════════════════════════════════════════
    title = Text("Fusion", font_size=42).to_edge(UP, buff=0.45)
    scene.play(FadeIn(title, shift=DOWN * 0.2))

    # ── Left column: Neural Net (prediction) ─────────────────────────────
    nn_icon = RoundedRectangle(
        width=2.2,
        height=1.1,
        corner_radius=0.14,
        color=BLUE_B,
        fill_color=BLUE_E,
        fill_opacity=0.30,
        stroke_width=2,
    )
    nn_lbl = Text("Neural Net", font_size=20, color=BLUE_B).move_to(nn_icon)
    nn_group = VGroup(nn_icon, nn_lbl).move_to(LEFT * 3.5 + UP * 1.2)

    pred_a = MathTex(r"a^{pred}_{i,j}", font_size=30, color=BLUE_A)
    pred_l = MathTex(r"l^{pred}_{i,j}", font_size=30, color=BLUE_A)
    pred_vals = VGroup(pred_a, pred_l).arrange(DOWN, buff=0.30)
    pred_vals.next_to(nn_group, DOWN, buff=0.28)

    # ── Right column: Vector DB (retrieval) ──────────────────────────────
    db_icon = RoundedRectangle(
        width=2.2,
        height=1.1,
        corner_radius=0.14,
        color=TEAL_B,
        fill_color=TEAL_E,
        fill_opacity=0.30,
        stroke_width=2,
    )
    db_lbl = Text("Vector DB", font_size=20, color=TEAL_B).move_to(db_icon)
    db_group = VGroup(db_icon, db_lbl).move_to(RIGHT * 3.5 + UP * 1.2)

    ret_a = MathTex(r"a^{ret}_{i,j}", font_size=30, color=TEAL_A)
    ret_l = MathTex(r"l^{ret}_{i,j}", font_size=30, color=TEAL_A)
    ret_vals = VGroup(ret_a, ret_l).arrange(DOWN, buff=0.30)
    ret_vals.next_to(db_group, DOWN, buff=0.28)

    # VS divider
    vs_lbl = Text("vs", font_size=26, color=GREY_A).move_to(ORIGIN + UP * 1.2)

    scene.play(
        FadeIn(nn_group),
        FadeIn(db_group),
        FadeIn(vs_lbl),
        run_time=0.7,
    )
    scene.play(
        FadeIn(pred_vals, shift=UP * 0.15),
        FadeIn(ret_vals, shift=UP * 0.15),
        run_time=0.7,
    )
    scene.wait(0.6)

    # ══════════════════════════════════════════════════════════════════════
    #  ACT 2: Capability formula + gamma slider
    # ══════════════════════════════════════════════════════════════════════
    scene.play(
        Indicate(pred_a, color=BLUE),
        Indicate(ret_a, color=BLUE),
    )

    # Formula a_ij
    eq_a = formulas.fused_capability().move_to(UP * 0.6)

    # Dim the recap, bring a^pred and a^ret toward centre
    scene.play(
        nn_group.animate.set_opacity(0.20),
        db_group.animate.set_opacity(0.20),
        vs_lbl.animate.set_opacity(0.20),
        pred_l.animate.set_opacity(0.20),
        ret_l.animate.set_opacity(0.20),
        pred_a.animate.set_opacity(0).move_to(eq_a[3]),
        ret_a.animate.set_opacity(0).move_to(eq_a[7]),
        Write(eq_a),
        run_time=0.8,
    )

    eq_a[3].set_color(BLUE)
    eq_a[7].set_color(BLUE)
    scene.play(
        Indicate(eq_a[3], color=BLUE),
        Indicate(eq_a[7], color=BLUE),
    )

    # Gamma slider
    gamma = ValueTracker(0.5)
    SLIDER_Y = -0.30
    slider_a = NumberLine(
        x_range=[0, 1, 1], length=5.5, include_numbers=False, color=GREY_B
    )
    slider_a.move_to([0, SLIDER_Y, 0])

    # Labels at each end
    pred_end_lbl = Text("Prediction", font_size=15, color=BLUE_A).next_to(
        slider_a.get_left(), DOWN, buff=0.12
    )
    ret_end_lbl = Text("Retrieval", font_size=15, color=TEAL_A).next_to(
        slider_a.get_right(), DOWN, buff=0.12
    )

    gamma_dot = always_redraw(
        lambda: Dot(slider_a.n2p(gamma.get_value()), radius=0.13, color=YELLOW)
    )
    gamma_lbl = always_redraw(
        lambda: MathTex(
            rf"\gamma = {gamma.get_value():.2f}", font_size=24, color=YELLOW
        ).next_to(slider_a, UP, buff=0.18)
    )

    scene.play(
        Create(slider_a),
        FadeIn(pred_end_lbl),
        FadeIn(ret_end_lbl),
        FadeIn(gamma_dot),
        FadeIn(gamma_lbl),
        run_time=0.7,
    )
    eq_a[2].set_color(YELLOW)
    eq_a[5].set_color(YELLOW)
    scene.play(
        Indicate(
            VGroup(
                gamma_lbl,
                eq_a[2],
                eq_a[5],
            )
        )
    )

    intro_gamma_box = text_box("Learnable Parameter", w=3.4).shift(RIGHT + UP * 2)
    intro_gamma_line = DashedLine(
        gamma_lbl.get_top(), intro_gamma_box.get_bottom(), buff=0.1
    )
    surround_gamma_lbl_rect = SurroundingRectangle(gamma_lbl, color=WHITE)
    scene.play(
        FadeIn(
            VGroup(
                intro_gamma_box,
                intro_gamma_line,
                surround_gamma_lbl_rect,
            )
        )
    )
    scene.wait(2)
    scene.play(
        FadeOut(
            VGroup(
                intro_gamma_box,
                intro_gamma_line,
                surround_gamma_lbl_rect,
            )
        )
    )

    # Slide gamma: lean toward prediction, then retrieval, then settle at 0.6
    scene.play(gamma.animate.set_value(0.85), run_time=1.1)
    scene.play(gamma.animate.set_value(0.20), run_time=1.1)
    scene.play(gamma.animate.set_value(0.60), run_time=0.8)
    scene.wait(0.4)

    scene.play(
        Flash(eq_a[0].get_center(), color=GREEN_A, flash_radius=0.5, line_length=0.18)
    )

    # ══════════════════════════════════════════════════════════════════════
    #  ACT 3: Cost formula + tp_j price table + delta slider
    # ══════════════════════════════════════════════════════════════════════
    # Fade out capability content, bring length variables to centre
    scene.play(
        FadeOut(
            VGroup(
                eq_a,
                slider_a,
                gamma_dot,
                gamma_lbl,
                pred_end_lbl,
                ret_end_lbl,
                pred_a,
                ret_a,
            )
        ),
        nn_group.animate.set_opacity(1),
        db_group.animate.set_opacity(1),
        vs_lbl.animate.set_opacity(1),
        pred_l.animate.set_opacity(1),
        ret_l.animate.set_opacity(1),
        run_time=0.8,
    )

    # Formula c_ij
    eq_c = formulas.fused_length().move_to(UP * 0.6)

    scene.play(
        Indicate(
            VGroup(
                pred_l,
                ret_l,
            ),
            color=BLUE,
        )
    )

    scene.play(
        nn_group.animate.set_opacity(0.20),
        db_group.animate.set_opacity(0.20),
        vs_lbl.animate.set_opacity(0.20),
        pred_l.animate.set_opacity(0).move_to(eq_c[5]),
        ret_l.animate.set_opacity(0).move_to(eq_c[12]),
        Write(eq_c),
        run_time=1.4,
    )
    eq_c[5].set_color(BLUE)
    eq_c[12].set_color(BLUE)
    scene.play(
        Indicate(
            VGroup(
                eq_c[5],
                eq_c[12],
            ),
            color=BLUE,
        )
    )
    scene.wait(1)

    # Highlight tp_j and pull out price table
    price_rows = VGroup(
        Text("GPT-4o:   $10 / 1M tokens", font_size=16, color=GREY_A),
        Text("Claude 3: $ 3 / 1M tokens", font_size=16, color=GREY_A),
        Text("Llama-3:  $0.5/ 1M tokens", font_size=16, color=GREY_A),
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
    price_box_rect = SurroundingRectangle(
        price_rows, color=GOLD, buff=0.18, corner_radius=0.10, stroke_width=1.8
    )
    price_header = Text("Token Price", font_size=17, color=GOLD)
    price_header.next_to(price_box_rect, UP, buff=0.08)
    price_widget = VGroup(price_box_rect, price_rows, price_header)
    price_widget.next_to(eq_c, DOWN * 2, buff=0.38)

    tp_arrow_1 = Arrow(
        eq_c[4].get_bottom(),
        price_widget.get_top(),
        buff=0.10,
        stroke_width=2.2,
        color=GOLD,
        max_tip_length_to_length_ratio=0.22,
    )
    tp_arrow_2 = Arrow(
        eq_c[11].get_bottom(),
        price_widget.get_top(),
        buff=0.10,
        stroke_width=2.2,
        color=GOLD,
        max_tip_length_to_length_ratio=0.22,
    )
    scene.play(
        eq_c[4].animate.set_color(GOLD),
        eq_c[6].animate.set_color(GOLD),
        eq_c[11].animate.set_color(GOLD),
        eq_c[13].animate.set_color(GOLD),
        GrowArrow(tp_arrow_1),
        GrowArrow(tp_arrow_2),
        FadeIn(price_widget, shift=UP * 0.12),
    )
    scene.wait(1)
    scene.play(
        FadeOut(
            VGroup(
                tp_arrow_1,
                tp_arrow_2,
                price_widget,
            )
        ),
    )

    # Delta slider
    delta = ValueTracker(0.5)
    slider_c = NumberLine(
        x_range=[0, 1, 1], length=5.5, include_numbers=False, color=GREY_B
    )
    slider_c.move_to([0, SLIDER_Y, 0])

    pred_end_lbl2 = Text("Prediction", font_size=15, color=BLUE_A).next_to(
        slider_c.get_left(), DOWN, buff=0.12
    )
    ret_end_lbl2 = Text("Retrieval", font_size=15, color=TEAL_A).next_to(
        slider_c.get_right(), DOWN, buff=0.12
    )

    delta_dot = always_redraw(
        lambda: Dot(slider_c.n2p(delta.get_value()), radius=0.13, color=ORANGE)
    )
    delta_lbl = always_redraw(
        lambda: MathTex(
            rf"\delta = {delta.get_value():.2f}", font_size=24, color=ORANGE
        ).next_to(slider_c, UP, buff=0.18)
    )

    scene.play(
        Create(slider_c),
        FadeIn(pred_end_lbl2),
        FadeIn(ret_end_lbl2),
        FadeIn(delta_dot),
        FadeIn(delta_lbl),
        run_time=0.7,
    )
    scene.play(
        Indicate(
            VGroup(
                delta_lbl,
                eq_c[2],
                eq_c[8],
            )
        )
    )
    surround_delta_lbl_rect = SurroundingRectangle(delta_lbl, color=WHITE)
    intro_delta_box = text_box("Learnable Parameter", w=3.4).shift(RIGHT + UP * 2)
    intro_delta_line = DashedLine(
        delta_lbl.get_top(), intro_delta_box.get_bottom(), buff=0.1
    )
    scene.play(
        FadeIn(
            VGroup(
                intro_delta_box,
                intro_delta_line,
                surround_delta_lbl_rect,
            )
        )
    )
    scene.wait(2)
    scene.play(
        FadeOut(
            VGroup(
                intro_delta_box,
                intro_delta_line,
                surround_delta_lbl_rect,
            )
        )
    )

    scene.play(delta.animate.set_value(0.80), run_time=1.0)
    scene.play(delta.animate.set_value(0.30), run_time=1.0)
    scene.play(delta.animate.set_value(0.55), run_time=0.7)
    scene.wait(0.3)

    scene.play(
        Flash(eq_c[0].get_center(), color=GREEN_A, flash_radius=0.5, line_length=0.18)
    )

    # ══════════════════════════════════════════════════════════════════════
    #  ACT 4: Zoom out to two glowing output boxes → To Optimizer
    # ══════════════════════════════════════════════════════════════════════
    scene.play(
        FadeOut(
            VGroup(
                eq_c,
                slider_c,
                delta_dot,
                delta_lbl,
                pred_end_lbl2,
                ret_end_lbl2,
                pred_l,
                ret_l,
                nn_group,
                db_group,
                vs_lbl,
            )
        ),
        run_time=0.7,
    )

    # Re-create the two output boxes centred
    box_a = text_box("Final Capability", box_color=GREEN_D, font_size=22, w=3.5, h=0.85)
    box_c = text_box("Final Cost", box_color=GOLD, font_size=22, w=3.5, h=0.85)
    outputs = VGroup(box_a, box_c).arrange(UP, buff=0.9)
    outputs.move_to(ORIGIN + DOWN * 0.2)

    scene.play(
        FadeIn(box_a, shift=UP * 0.2),
        FadeIn(box_c, shift=UP * 0.2),
        run_time=0.8,
    )
    scene.play(
        Flash(box_a.get_center(), color=GREEN_A, flash_radius=0.7, line_length=0.25),
        Flash(box_c.get_center(), color=GOLD, flash_radius=0.7, line_length=0.25),
    )

    scene.play(outputs.animate.shift(LEFT))

    # "To Optimizer"
    to_opt = Text("To Optimizer", font_size=26, color=WHITE)
    to_opt.next_to(outputs, RIGHT, buff=0.55)
    to_opt_arr = Arrow(
        outputs.get_right(),
        to_opt.get_left() + LEFT * 0.1,
        buff=0.10,
        stroke_width=3.5,
        color=WHITE,
    )

    scene.play(GrowArrow(to_opt_arr), FadeIn(to_opt, shift=LEFT * 0.15))
    scene.play(
        to_opt.animate.set_color(YELLOW),
        to_opt_arr.animate.set_color(YELLOW),
        run_time=0.5,
    )

    scene.wait(1.5)

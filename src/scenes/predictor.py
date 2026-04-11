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
    title = Text("Retrieval Augmentation", font_size=48).to_edge(UP)
    axes = Axes(
        x_range=[-3, 3, 1], y_range=[-2, 2, 1], x_length=7, y_length=4.5, tips=False
    )
    axes.shift(DOWN * 0.2)
    current = Dot(axes.c2p(0.3, 0.2), color=YELLOW, radius=0.08)
    history_coords = [
        (-1.8, 0.9),
        (-1.0, -0.7),
        (1.7, 1.0),
        (2.1, -1.1),
        (0.9, 0.4),
        (-0.2, 1.2),
    ]
    history = VGroup(
        *[Dot(axes.c2p(x, y), color=BLUE_B, radius=0.055) for x, y in history_coords]
    )
    radar = Circle(radius=0.25, color=YELLOW).move_to(current)
    nearest_ids = [1, 4, 5]
    nearest = VGroup(*[history[i] for i in nearest_ids])
    links = VGroup(
        *[Line(current.get_center(), p.get_center(), color=YELLOW_A) for p in nearest]
    )
    sim_label = Text("Cosine similarity -> nearest Q_k", font_size=24).to_edge(DOWN)
    eq = (
        MathTex(
            r"a^{ret}_{i,j}=\frac{\sum_{m\in Q_k}\mathrm{sim}(E_q^i,E_q^m)a_{m,j}}{\sum_{m\in Q_k}\mathrm{sim}(E_q^i,E_q^m)}"
        )
        .scale(0.75)
        .next_to(title, DOWN, buff=0.3)
    )

    scene.play(FadeIn(title), Create(axes), FadeIn(history), FadeIn(current))
    scene.play(ShowPassingFlash(radar.copy().scale(3.5), time_width=0.8), run_time=1.0)
    scene.play(
        *[p.animate.set_color(TEAL_A).scale(1.2) for p in nearest], Create(links)
    )
    scene.play(FadeIn(eq), FadeIn(sim_label))
    scene.wait(1.2)


def play_scene11_fusion(scene):
    title = Text("Prediction + Retrieval Fusion", font_size=48).to_edge(UP)
    eq1 = (
        MathTex(r"a_{i,j}=\gamma a^{pred}_{i,j} + (1-\gamma)a^{ret}_{i,j}")
        .scale(0.86)
        .next_to(title, DOWN, buff=0.45)
    )
    eq2 = (
        MathTex(r"c_{i,j}=\delta\,c^{pred}_{i,j} + (1-\delta)\,c^{ret}_{i,j}")
        .scale(0.86)
        .next_to(eq1, DOWN, buff=0.35)
    )

    gamma = ValueTracker(0.2)
    delta = ValueTracker(0.7)
    gamma_bar = NumberLine(x_range=[0, 1, 0.2], length=4.2, include_numbers=False)
    delta_bar = NumberLine(x_range=[0, 1, 0.2], length=4.2, include_numbers=False)
    gamma_bar.next_to(eq2, DOWN, buff=0.55)
    delta_bar.next_to(gamma_bar, DOWN, buff=0.45)
    gamma_dot = always_redraw(
        lambda: Dot(gamma_bar.n2p(gamma.get_value()), color=YELLOW)
    )
    delta_dot = always_redraw(
        lambda: Dot(delta_bar.n2p(delta.get_value()), color=ORANGE)
    )
    gamma_text = always_redraw(
        lambda: VGroup(
            Text("gamma", font_size=22),
            DecimalNumber(gamma.get_value(), num_decimal_places=2),
        )
        .arrange(RIGHT, buff=0.15)
        .next_to(gamma_bar, RIGHT, buff=0.2)
    )
    delta_text = always_redraw(
        lambda: VGroup(
            Text("delta", font_size=22),
            DecimalNumber(delta.get_value(), num_decimal_places=2),
        )
        .arrange(RIGHT, buff=0.15)
        .next_to(delta_bar, RIGHT, buff=0.2)
    )
    out_a = always_redraw(
        lambda: DecimalNumber(
            gamma.get_value() * 0.92 + (1 - gamma.get_value()) * 0.64,
            num_decimal_places=3,
            color=YELLOW,
        ).next_to(eq1, RIGHT, buff=0.35)
    )
    out_c = always_redraw(
        lambda: DecimalNumber(
            delta.get_value() * 1.45 + (1 - delta.get_value()) * 0.95,
            num_decimal_places=3,
            color=ORANGE,
        ).next_to(eq2, RIGHT, buff=0.35)
    )

    scene.play(FadeIn(title), FadeIn(eq1), FadeIn(eq2))
    scene.play(
        Create(gamma_bar), Create(delta_bar), FadeIn(gamma_dot), FadeIn(delta_dot)
    )
    scene.play(FadeIn(gamma_text), FadeIn(delta_text), FadeIn(out_a), FadeIn(out_c))
    scene.play(
        gamma.animate.set_value(0.82), delta.animate.set_value(0.25), run_time=2.0
    )
    scene.play(
        gamma.animate.set_value(0.45), delta.animate.set_value(0.75), run_time=2.0
    )
    scene.wait(1.0)

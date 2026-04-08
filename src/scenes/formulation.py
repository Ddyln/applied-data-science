"""Function steps for scenes 5-6."""

from manim import *

from formulas import omnirouter


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
    intro_a = MathTex(r"a_{ij}\in[0,1]:\ \text{success probability/capability}").scale(0.74)
    intro_c = MathTex(r"c_{ij}:\ \text{money cost of using model }j\text{ for query }i").scale(
        0.74
    )
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

    objective = omnirouter.objective().scale(0.8).next_to(title, DOWN, buff=0.6)
    find_label = Text("Find", font_size=34).next_to(objective, LEFT, buff=0.35)
    c1 = (
        omnirouter.assignment_constraint()
        .scale(0.74)
        .next_to(objective, DOWN, aligned_edge=LEFT)
    )
    c2 = (
        omnirouter.quality_constraint().scale(0.74).next_to(c1, DOWN, aligned_edge=LEFT)
    )
    c3 = (
        omnirouter.capacity_constraint()
        .scale(0.74)
        .next_to(c2, DOWN, aligned_edge=LEFT)
    )
    st_label = MathTex(r"\mathrm{s.t.}").scale(0.95).next_to(c1, LEFT, buff=0.5)
    VGroup(objective, c1, c2, c3).shift(LEFT * 2)
    find_label.shift(LEFT * 2)
    st_label.shift(LEFT * 2)

    tag_objective = Text("Minimize total routing cost", font_size=28, color=YELLOW)
    tag_objective.next_to(objective, RIGHT, buff=0.35)
    tag_c1 = Text("One model per query", font_size=25, color=BLUE_B).next_to(
        c1, RIGHT, buff=0.35
    )
    tag_c2 = Text("Global quality target", font_size=25, color=GREEN_B).next_to(
        c2, RIGHT, buff=0.35
    )
    tag_c3 = Text("Model concurrency limit", font_size=25, color=ORANGE).next_to(
        c3, RIGHT, buff=0.35
    )

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
    objective = omnirouter.objective().scale(0.9).to_edge(UP, buff=0.8)
    unknown_prompt = Text(
        "At query time,", font_size=30, color=RED_C
    ).next_to(objective, DOWN, buff=0.45)

    unknown_math = VGroup(
        Text("we do not know", font_size=26, color=RED_C),
        MathTex(r"c_{ij}", color=RED_C).scale(1.15),
        Text("or", font_size=26, color=RED_C),
        MathTex(r"a_{ij}", color=RED_C).scale(1.15),
    ).arrange(RIGHT, buff=0.18)
    unknown_math.next_to(unknown_prompt, DOWN, buff=0.22)

    cost_term = MathTex(r"c_{ij}", color=RED_C).scale(1.2)
    cap_term = MathTex(r"a_{ij}", color=RED_C).scale(1.2)
    q1 = MathTex(r"?").scale(1.2)
    q2 = MathTex(r"?").scale(1.2)
    unknown_cards = VGroup(
        VGroup(cost_term, q1).arrange(RIGHT, buff=0.18),
        VGroup(cap_term, q2).arrange(RIGHT, buff=0.18),
    ).arrange(DOWN, buff=0.35)
    unknown_cards.next_to(unknown_math, DOWN, buff=0.35)

    scene.play(FadeIn(objective))
    scene.play(FadeIn(unknown_prompt))
    scene.play(FadeIn(unknown_math))
    scene.play(LaggedStart(FadeIn(unknown_cards[0]), FadeIn(unknown_cards[1]), lag_ratio=0.25))
    scene.play(Indicate(unknown_cards[0], color=RED_C), Indicate(unknown_cards[1], color=RED_C))
    scene.wait(0.8)

    scene.play(
        FadeOut(unknown_cards),
        FadeOut(unknown_math),
        FadeOut(unknown_prompt),
        objective.animate.scale(0.6).to_corner(UL).shift(RIGHT * 0.4 + DOWN * 0.3),
    )

    frame = RoundedRectangle(width=13.4, height=3.6, corner_radius=0.2)
    frame.move_to(DOWN * 0.35)

    query_box = RoundedRectangle(width=2.5, height=1.0, corner_radius=0.12, color=WHITE)
    predictor_box = RoundedRectangle(width=2.9, height=1.2, corner_radius=0.12, color=BLUE_B)
    optimizer_box = RoundedRectangle(width=2.9, height=1.2, corner_radius=0.12, color=GREEN_B)
    select_box = RoundedRectangle(width=3.0, height=1.0, corner_radius=0.12, color=WHITE)
    stage_row = VGroup(query_box, predictor_box, optimizer_box, select_box).arrange(
        RIGHT, buff=0.52
    )
    stage_row.move_to(frame)

    query_text = Text("Queries", font_size=24).move_to(query_box)
    predictor_text = Text("Predictor", font_size=24).move_to(predictor_box)
    optimizer_text = Text("Optimizer", font_size=24).move_to(optimizer_box)
    select_text = Text("Model Selection", font_size=24).move_to(select_box)
    labels = VGroup(query_text, predictor_text, optimizer_text, select_text)

    a1 = Arrow(query_box.get_right(), predictor_box.get_left(), buff=0.08, stroke_width=4)
    a2 = Arrow(predictor_box.get_right(), optimizer_box.get_left(), buff=0.08, stroke_width=4)
    a3 = Arrow(optimizer_box.get_right(), select_box.get_left(), buff=0.08, stroke_width=4)
    edges = VGroup(a1, a2, a3)

    est_cost = MathTex(r"\hat{c}_{ij}", color=BLUE_B).scale(0.9).next_to(predictor_box, UP, buff=0.16).shift(RIGHT * 0.5)
    est_cap = MathTex(r"\hat{a}_{ij}", color=BLUE_B).scale(0.9).next_to(est_cost, RIGHT, buff=0.25).shift(RIGHT * 0.5)
    est_group = VGroup(est_cost, est_cap)
    est_callout = Arrow(
        a2.get_center() + UP * 0.02,
        est_group.get_bottom() + DOWN * 0.05,
        buff=0.08,
        stroke_width=4,
        color=YELLOW,
    )

    packet = Dot(radius=0.07, color=YELLOW).move_to(a1.get_start())
    bridge_1 = ArcBetweenPoints(a1.get_end(), a2.get_start(), angle=PI / 6)
    bridge_2 = ArcBetweenPoints(a2.get_end(), a3.get_start(), angle=PI / 6)

    scene.play(FadeIn(frame, shift=UP * 0.15))
    scene.play(FadeIn(query_box), FadeIn(query_text))

    scene.play(FadeIn(predictor_box), FadeIn(predictor_text), GrowArrow(a1))
    scene.add(packet)
    scene.play(MoveAlongPath(packet, a1), run_time=0.8)
    scene.play(MoveAlongPath(packet, bridge_1), run_time=0.45)

    scene.play(FadeIn(optimizer_box), FadeIn(optimizer_text), GrowArrow(a2))
    scene.play(GrowArrow(est_callout), FadeIn(est_group))
    scene.play(MoveAlongPath(packet, a2), run_time=0.8)
    scene.play(MoveAlongPath(packet, bridge_2), run_time=0.45)

    scene.play(FadeIn(select_box), FadeIn(select_text), GrowArrow(a3))
    scene.play(MoveAlongPath(packet, a3), run_time=0.8)


    scene.wait(1.2)

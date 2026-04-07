"""Function steps for scenes 5-6."""

from manim import *

from formulas import omnirouter


def play_scene05_problem_formulation(scene):
    title = Text("Constrained Optimization Formulation", font_size=48).to_edge(UP)
    var_x = MathTex(
        r"x_{ij}\in\{0,1\}:\ \text{assign query }i\text{ to model }j"
    ).scale(0.7)
    var_a = MathTex(
        r"a_{ij}\in[0,1]:\ \text{success probability/capability}"
    ).scale(0.7)
    var_c = MathTex(r"c_{ij}:\ \text{cost of using model }j\text{ for query }i").scale(
        0.7
    )
    variable_entries = VGroup(var_x, var_a, var_c).arrange(
        DOWN, aligned_edge=LEFT, buff=0.38
    )
    variable_entries.move_to(ORIGIN)

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

    hook = VGroup(
        Text("Where do", font_size=30),
        MathTex(r"c_{ij}").scale(1),
        Text("and", font_size=30),
        MathTex(r"a_{ij}").scale(1),
        Text("come from?", font_size=30),
    ).arrange(RIGHT, buff=0.15)
    hook.to_edge(DOWN)

    scene.play(FadeIn(title))
    scene.play(LaggedStart(FadeIn(var_x), FadeIn(var_a), FadeIn(var_c), lag_ratio=0.2))
    scene.wait(5)
    scene.play(FadeOut(variable_entries))

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
    scene.play(
        # FadeOut(tag_objective),
        # FadeOut(tag_c1),
        # FadeOut(tag_c2),
        # FadeOut(tag_c3),
        FadeIn(hook),
    )
    scene.wait(5)


def play_scene06_two_stage_framework(scene):
    title = Text("Two-Stage Framework", font_size=48).to_edge(UP)
    pipeline = Text("Query -> Predictor -> Optimizer -> Model Selection", font_size=34)
    scene.play(FadeIn(title))
    scene.play(FadeIn(pipeline))
    scene.wait(0.8)

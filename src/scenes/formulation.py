"""Function steps for scenes 5-6."""

from manim import *

from formulas import omnirouter


def play_scene05_problem_formulation(scene):
    title = Text("Constrained Optimization Formulation", font_size=48).to_edge(UP)
    objective = omnirouter.objective().scale(0.8).next_to(title, DOWN, buff=0.6)
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
    scene.play(FadeIn(title))
    scene.play(FadeIn(objective))
    scene.play(FadeIn(VGroup(c1, c2, c3)))
    scene.wait(1.0)


def play_scene06_two_stage_framework(scene):
    title = Text("Two-Stage Framework", font_size=48).to_edge(UP)
    pipeline = Text("Query -> Predictor -> Optimizer -> Model Selection", font_size=34)
    scene.play(FadeIn(title))
    scene.play(FadeIn(pipeline))
    scene.wait(0.8)

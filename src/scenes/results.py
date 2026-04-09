"""Function steps for scenes 17-18."""

from manim import *


def play_scene17_results(scene):
    title = Text("Evaluation Results", font_size=48).to_edge(UP)
    acc_title = Text("Accuracy", font_size=28).to_edge(LEFT, buff=1.2).shift(UP * 0.8)
    cost_title = (
        Text("Operational Cost", font_size=28).to_edge(RIGHT, buff=1.2).shift(UP * 0.8)
    )

    acc_baseline = Rectangle(
        width=0.7, height=1.6, fill_color=BLUE_E, fill_opacity=0.85
    )
    acc_omni = Rectangle(width=0.7, height=2.0, fill_color=YELLOW_E, fill_opacity=0.9)
    acc_group = (
        VGroup(acc_baseline, acc_omni)
        .arrange(RIGHT, buff=0.35)
        .next_to(acc_title, DOWN, buff=0.35)
    )
    acc_labels = (
        VGroup(Text("Base", font_size=20), Text("Omni", font_size=20))
        .arrange(RIGHT, buff=0.6)
        .next_to(acc_group, DOWN, buff=0.15)
    )
    acc_gain = Text("+6.30%", font_size=28, color=YELLOW).next_to(
        acc_group, UP, buff=0.18
    )

    cost_baseline = Rectangle(
        width=0.7, height=2.0, fill_color=BLUE_E, fill_opacity=0.85
    )
    cost_omni = Rectangle(width=0.7, height=1.55, fill_color=GREEN_E, fill_opacity=0.9)
    cost_group = (
        VGroup(cost_baseline, cost_omni)
        .arrange(RIGHT, buff=0.35)
        .next_to(cost_title, DOWN, buff=0.35)
    )
    cost_labels = (
        VGroup(Text("Base", font_size=20), Text("Omni", font_size=20))
        .arrange(RIGHT, buff=0.6)
        .next_to(cost_group, DOWN, buff=0.15)
    )
    cost_gain = Text("-10.15%", font_size=28, color=GREEN_A).next_to(
        cost_group, UP, buff=0.18
    )

    scene.play(FadeIn(title))
    scene.play(FadeIn(acc_title), FadeIn(cost_title))
    scene.play(GrowFromEdge(acc_baseline, DOWN), GrowFromEdge(cost_baseline, DOWN))
    scene.play(GrowFromEdge(acc_omni, DOWN), GrowFromEdge(cost_omni, DOWN))
    scene.play(
        FadeIn(acc_labels), FadeIn(cost_labels), FadeIn(acc_gain), FadeIn(cost_gain)
    )
    scene.wait(1.1)


def play_scene18_conclusion(scene):
    title = Text("Conclusion", font_size=48).to_edge(UP)
    line1 = Text("Predictor estimates c_ij and a_ij", font_size=30)
    line2 = Text("Optimizer enforces global constraints", font_size=30).next_to(
        line1, DOWN, buff=0.25
    )
    line3 = Text(
        "Global constrained optimization > greedy routing", font_size=34, color=YELLOW
    ).next_to(line2, DOWN, buff=0.4)
    scene.play(FadeIn(title))
    scene.play(FadeIn(line1), FadeIn(line2))
    scene.play(Indicate(line3, color=YELLOW), FadeIn(line3))
    scene.wait(1.2)

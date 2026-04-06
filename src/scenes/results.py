"""Function steps for scenes 17-18."""

from manim import *


def play_scene17_results(scene):
    title = Text("Results", font_size=48).to_edge(UP)
    line1 = Text("Accuracy increases", font_size=36)
    line2 = Text("Cost decreases", font_size=36).next_to(line1, DOWN)
    scene.play(FadeIn(title), FadeIn(line1), FadeIn(line2))
    scene.wait(0.8)


def play_scene18_conclusion(scene):
    title = Text("Conclusion", font_size=48).to_edge(UP)
    msg = Text("Global constrained optimization > greedy routing", font_size=34)
    scene.play(FadeIn(title), FadeIn(msg))
    scene.wait(1.2)

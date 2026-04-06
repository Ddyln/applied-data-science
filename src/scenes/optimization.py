"""Function steps for scenes 12-16."""

from manim import *

from formulas import omnirouter


def play_scene12_lagrangian(scene):
    title = Text("Lagrangian Formulation", font_size=48).to_edge(UP)
    eq = omnirouter.lagrangian().scale(0.66).next_to(title, DOWN, buff=0.5)
    scene.play(FadeIn(title), FadeIn(eq))
    scene.wait(0.8)


def play_scene13_optimality_condition(scene):
    title = Text("Optimality Condition", font_size=48).to_edge(UP)
    eq = MathTex(
        r"\frac{\partial \mathcal{L}}{\partial x_{i,j}}"
        r"= c_{i,j} - \frac{\lambda_1 a_{i,j}}{N} + \lambda_{2,j} + \mu_i = 0"
    ).scale(0.82)
    scene.play(FadeIn(title), FadeIn(eq))
    scene.wait(0.8)


def play_scene14_decision_rule(scene):
    title = Text("Decision Rule", font_size=48).to_edge(UP)
    eq = omnirouter.decision_rule().scale(0.86)
    scene.play(FadeIn(title), FadeIn(eq))
    scene.wait(0.8)


def play_scene15_dual_updates(scene):
    title = Text("Dual Variable Updates", font_size=48).to_edge(UP)
    eq1 = MathTex(
        r"\lambda_1^{t+1}=\max\!\left(\lambda_1^t+\eta_1\left(\alpha-\frac{1}{N}\sum_{i,j}a_{i,j}x_{i,j}\right),0\right)"
    ).scale(0.72)
    eq2 = MathTex(
        r"\lambda_{2,j}^{t+1}=\max\!\left(\lambda_{2,j}^t+\eta_2\left(\sum_i x_{i,j}-L_j\right),0\right)"
    ).scale(0.74)
    eq2.next_to(eq1, DOWN)
    scene.play(FadeIn(title), FadeIn(VGroup(eq1, eq2)))
    scene.wait(0.8)


def play_scene16_dual_intuition(scene):
    title = Text("Intuition for Multipliers", font_size=48).to_edge(UP)
    line1 = Text("Quality too low -> increase lambda_1", font_size=32)
    line2 = Text("Model overloaded -> increase lambda_2", font_size=32).next_to(
        line1, DOWN
    )
    scene.play(FadeIn(title), FadeIn(line1), FadeIn(line2))
    scene.wait(0.8)

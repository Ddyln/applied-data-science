"""Function steps for scenes 12-16."""

from manim import *

from formulas import omnirouter


def play_scene12_lagrangian(scene):
    title = Text("Lagrangian Formulation", font_size=48).to_edge(UP)
    obj = omnirouter.objective().scale(0.86).next_to(title, DOWN, buff=0.55)
    q = omnirouter.quality_constraint().scale(0.76).next_to(obj, DOWN, aligned_edge=LEFT, buff=0.25)
    cap = omnirouter.capacity_constraint().scale(0.76).next_to(q, DOWN, aligned_edge=LEFT, buff=0.2)
    assign = omnirouter.assignment_constraint().scale(0.76).next_to(cap, DOWN, aligned_edge=LEFT, buff=0.2)
    lag = omnirouter.lagrangian().scale(0.62).next_to(title, DOWN, buff=0.55)

    scene.play(FadeIn(title), FadeIn(obj))
    scene.play(FadeIn(VGroup(q, cap, assign), shift=UP * 0.2))
    scene.wait(0.6)
    scene.play(TransformMatchingTex(VGroup(obj, q, cap, assign).copy(), lag), FadeIn(lag))

    colors = [YELLOW, GREEN_B, ORANGE, BLUE_B]
    for i, c in enumerate(colors, start=1):
        if i < len(lag):
            box = SurroundingRectangle(lag[i], color=c, buff=0.08)
            scene.play(Create(box), run_time=0.35)
            scene.play(FadeOut(box), run_time=0.25)
    scene.wait(1.0)


def play_scene13_optimality_condition(scene):
    title = Text("Optimality Condition", font_size=48).to_edge(UP)
    eq = MathTex(
        r"\frac{\partial \mathcal{L}}{\partial x_{i,j}}"
        r"= c_{i,j} - \frac{\lambda_1 a_{i,j}}{N} + \lambda_{2,j} + \mu_i = 0"
    ).scale(0.82)
    core = MathTex(r"c_{i,j} - \frac{\lambda_1 a_{i,j}}{N} + \lambda_{2,j}").scale(1.05)
    core.next_to(eq, DOWN, buff=0.7)
    core_tag = Text("effective score", font_size=26, color=YELLOW).next_to(core, DOWN, buff=0.2)

    scene.play(FadeIn(title), FadeIn(eq))
    scene.play(Indicate(eq[1], color=YELLOW), run_time=1.0)
    scene.play(FadeIn(core), FadeIn(core_tag))
    scene.wait(1.0)


def play_scene14_decision_rule(scene):
    title = Text("Decision Rule", font_size=48).to_edge(UP)
    eq = omnirouter.decision_rule().scale(0.86)
    caption = Text("Pick model with minimum adjusted score", font_size=28, color=YELLOW)
    caption.next_to(eq, DOWN, buff=0.35)
    box = SurroundingRectangle(eq, color=YELLOW, buff=0.2)
    scene.play(FadeIn(title), FadeIn(eq))
    scene.play(Create(box), FadeIn(caption))
    scene.wait(1.0)


def play_scene15_dual_updates(scene):
    title = Text("Dual Variable Updates", font_size=48).to_edge(UP)
    eq1 = MathTex(
        r"\lambda_1^{t+1}=\max\!\left(\lambda_1^t+\eta_1\left(\alpha-\frac{1}{N}\sum_{i,j}a_{i,j}x_{i,j}\right),0\right)"
    ).scale(0.72)
    eq2 = MathTex(
        r"\lambda_{2,j}^{t+1}=\max\!\left(\lambda_{2,j}^t+\eta_2\left(\sum_i x_{i,j}-L_j\right),0\right)"
    ).scale(0.74)
    eq2.next_to(eq1, DOWN, buff=0.28)
    eq_group = VGroup(eq1, eq2).to_edge(LEFT, buff=0.5).shift(DOWN * 0.2)

    quality_label = Text("Average Quality", font_size=24).to_edge(RIGHT, buff=1.2).shift(UP * 1.4)
    quality_bar = Rectangle(width=0.5, height=2.2, stroke_color=WHITE).next_to(quality_label, DOWN, buff=0.2)
    quality_fill = Rectangle(width=0.5, height=1.0, fill_color=GREEN_E, fill_opacity=0.9, stroke_width=0)
    quality_fill.move_to(quality_bar.get_bottom() + UP * 0.5)
    alpha_line = DashedLine(quality_bar.get_left() + UP * 1.45, quality_bar.get_right() + UP * 1.45, color=YELLOW)
    alpha_tag = MathTex(r"\alpha").scale(0.7).next_to(alpha_line, RIGHT, buff=0.08)

    lambda1 = DecimalNumber(0.2, num_decimal_places=2, color=YELLOW).next_to(quality_bar, RIGHT, buff=0.35)
    lambda1_tag = MathTex(r"\lambda_1").scale(0.8).next_to(lambda1, UP, buff=0.08)

    cap_label = Text("Model 1 Load", font_size=24).to_edge(RIGHT, buff=1.2).shift(DOWN * 1.2)
    cap_bar = Rectangle(width=2.2, height=0.45, stroke_color=WHITE).next_to(cap_label, DOWN, buff=0.2)
    cap_fill = Rectangle(width=1.4, height=0.45, fill_color=BLUE_E, fill_opacity=0.9, stroke_width=0)
    cap_fill.move_to(cap_bar.get_left() + RIGHT * 0.7)
    limit_line = DashedLine(cap_bar.get_left() + RIGHT * 1.4 + UP * 0.28, cap_bar.get_left() + RIGHT * 1.4 + DOWN * 0.28, color=YELLOW)
    limit_tag = MathTex(r"L_j").scale(0.7).next_to(limit_line, DOWN, buff=0.07)

    lambda2 = DecimalNumber(0.15, num_decimal_places=2, color=ORANGE).next_to(cap_bar, RIGHT, buff=0.35)
    lambda2_tag = MathTex(r"\lambda_{2,j}").scale(0.8).next_to(lambda2, UP, buff=0.08)

    scene.play(FadeIn(title), FadeIn(eq_group))
    scene.play(FadeIn(VGroup(quality_label, quality_bar, quality_fill, alpha_line, alpha_tag, lambda1, lambda1_tag)))
    scene.play(quality_fill.animate.stretch_to_fit_height(0.55).move_to(quality_bar.get_bottom() + UP * 0.275), lambda1.animate.set_value(0.95), run_time=1.5)
    scene.play(FadeIn(VGroup(cap_label, cap_bar, cap_fill, limit_line, limit_tag, lambda2, lambda2_tag)))
    scene.play(cap_fill.animate.stretch_to_fit_width(2.05).move_to(cap_bar.get_left() + RIGHT * 1.025), lambda2.animate.set_value(1.12), run_time=1.5)
    scene.wait(1.0)


def play_scene16_dual_intuition(scene):
    title = Text("Intuition for Multipliers", font_size=48).to_edge(UP)
    left_panel = RoundedRectangle(width=5.8, height=2.3, corner_radius=0.12, color=YELLOW)
    right_panel = RoundedRectangle(width=5.8, height=2.3, corner_radius=0.12, color=ORANGE)
    panels = VGroup(left_panel, right_panel).arrange(DOWN, buff=0.55).shift(DOWN * 0.5)

    left_text = Text("Quality below target -> lambda_1 rises", font_size=28).move_to(left_panel)
    right_text = Text("Model overload -> lambda_2 rises", font_size=28).move_to(right_panel)
    left_impact = MathTex(r"-\frac{\lambda_1 a_{i,j}}{N}\ \uparrow\Rightarrow\ \text{favor high-}a_{i,j}").scale(0.72).next_to(left_panel, RIGHT, buff=0.25)
    right_impact = MathTex(r"\lambda_{2,j}\uparrow\Rightarrow\ \text{overloaded model becomes expensive}").scale(0.72).next_to(right_panel, RIGHT, buff=0.25)

    scene.play(FadeIn(title), FadeIn(panels), FadeIn(left_text), FadeIn(right_text))
    scene.play(Indicate(left_panel, color=YELLOW), FadeIn(left_impact))
    scene.play(Indicate(right_panel, color=ORANGE), FadeIn(right_impact))
    scene.wait(1.0)

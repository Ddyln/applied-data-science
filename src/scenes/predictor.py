"""Function steps for scenes 7-11."""

from manim import *


def play_scene07_embeddings(scene):
    title = Text("Embedding Queries and Models", font_size=48).to_edge(UP)
    query = RoundedRectangle(width=3.6, height=1.0, corner_radius=0.12, color=WHITE)
    model = RoundedRectangle(width=3.6, height=1.0, corner_radius=0.12, color=WHITE)
    query_label = Text("Query text", font_size=24).move_to(query)
    model_label = Text("Model profile", font_size=24).move_to(model)
    source = VGroup(VGroup(query, query_label), VGroup(model, model_label)).arrange(
        DOWN, buff=0.55
    )
    source.to_edge(LEFT, buff=0.9)

    encoder = RoundedRectangle(width=2.4, height=3.0, corner_radius=0.15, color=BLUE_B)
    encoder.move_to(ORIGIN)
    encoder_label = Text("Encoder", font_size=24, color=BLUE_B).move_to(encoder)

    vec_q = VGroup(*[Square(0.24, color=TEAL_A).set_fill(TEAL_E, opacity=0.6) for _ in range(8)]).arrange(RIGHT, buff=0.08)
    vec_l = VGroup(*[Square(0.24, color=PURPLE_A).set_fill(PURPLE_E, opacity=0.6) for _ in range(8)]).arrange(RIGHT, buff=0.08)
    vec_q_text = MathTex(r"E_q").next_to(vec_q, DOWN, buff=0.15)
    vec_l_text = MathTex(r"E_l").next_to(vec_l, DOWN, buff=0.15)
    vectors = VGroup(VGroup(vec_q, vec_q_text), VGroup(vec_l, vec_l_text)).arrange(DOWN, buff=0.7)
    vectors.to_edge(RIGHT, buff=1.0)

    arrows = VGroup(
        Arrow(query.get_right(), encoder.get_left(), buff=0.1),
        Arrow(model.get_right(), encoder.get_left(), buff=0.1),
        Arrow(encoder.get_right(), vec_q.get_left(), buff=0.15),
        Arrow(encoder.get_right(), vec_l.get_left(), buff=0.15),
    )

    scene.play(FadeIn(title))
    scene.play(FadeIn(source))
    scene.play(FadeIn(encoder), FadeIn(encoder_label))
    scene.play(LaggedStart(*[GrowArrow(a) for a in arrows[:2]], lag_ratio=0.2))
    scene.play(LaggedStart(*[GrowArrow(a) for a in arrows[2:]], lag_ratio=0.2), FadeIn(vectors))
    scene.wait(1.2)


def play_scene08_capability_prediction(scene):
    title = Text("Capability Prediction", font_size=48).to_edge(UP)
    vec_q = VGroup(*[Square(0.25, color=TEAL_A).set_fill(TEAL_E, opacity=0.6) for _ in range(6)]).arrange(RIGHT, buff=0.08)
    vec_l = VGroup(*[Square(0.25, color=PURPLE_A).set_fill(PURPLE_E, opacity=0.6) for _ in range(6)]).arrange(RIGHT, buff=0.08)
    vec_q.to_edge(LEFT, buff=1.0).shift(UP * 1.1)
    vec_l.to_edge(LEFT, buff=1.0).shift(DOWN * 1.1)
    dot_label = MathTex(r"E_q^i\cdot E_l^j").next_to(VGroup(vec_q, vec_l), RIGHT, buff=0.6)
    sigma = MathTex(r"\sigma(\cdot)").next_to(dot_label, RIGHT, buff=0.7)
    output = DecimalNumber(0.0, num_decimal_places=3, include_sign=False).next_to(sigma, RIGHT, buff=0.7)
    output_tag = MathTex(r"a^{pred}_{i,j}").next_to(output, DOWN, buff=0.15)
    eq = MathTex(r"a^{pred}_{i,j}=\sigma(W_1(E_q^i\cdot E_l^j)+b_1)").scale(0.86).to_edge(DOWN)

    scene.play(FadeIn(title), FadeIn(vec_q), FadeIn(vec_l))
    scene.play(Indicate(vec_q), Indicate(vec_l))
    scene.play(FadeIn(dot_label))
    scene.play(Flash(dot_label, color=YELLOW, flash_radius=0.45), FadeIn(sigma))
    scene.play(output.animate.set_value(0.842), FadeIn(output_tag), run_time=1.2)
    scene.play(FadeIn(eq))
    scene.wait(1.2)


def play_scene09_length_prediction(scene):
    title = Text("Length Prediction", font_size=48).to_edge(UP)
    add_expr = MathTex(r"E_q^i + E_l^j").to_edge(LEFT, buff=1.2)
    nn_box = RoundedRectangle(width=2.3, height=1.4, corner_radius=0.12, color=BLUE_B)
    nn_box.move_to(ORIGIN)
    nn_label = Text("NN", font_size=24, color=BLUE_B).move_to(nn_box)
    softmax = MathTex(r"\mathrm{softmax}").to_edge(RIGHT, buff=2.5)
    bars = VGroup(
        Rectangle(width=0.25, height=0.4, fill_color=TEAL_E, fill_opacity=0.8),
        Rectangle(width=0.25, height=0.8, fill_color=TEAL_E, fill_opacity=0.8),
        Rectangle(width=0.25, height=1.2, fill_color=TEAL_E, fill_opacity=0.8),
        Rectangle(width=0.25, height=0.6, fill_color=TEAL_E, fill_opacity=0.8),
    ).arrange(RIGHT, aligned_edge=DOWN, buff=0.12)
    bars.next_to(softmax, DOWN, buff=0.25)
    eq = MathTex(r"l^{pred}_{i,j}=b_s\cdot \mathrm{softmax}(W_2(E_q^i+E_l^j)+b_2)").scale(0.82).to_edge(DOWN)

    a1 = Arrow(add_expr.get_right(), nn_box.get_left(), buff=0.12)
    a2 = Arrow(nn_box.get_right(), softmax.get_left(), buff=0.12)
    a3 = Arrow(softmax.get_bottom(), bars.get_top(), buff=0.08)

    scene.play(FadeIn(title), FadeIn(add_expr))
    scene.play(FadeIn(nn_box), FadeIn(nn_label), GrowArrow(a1))
    scene.play(GrowArrow(a2), FadeIn(softmax))
    scene.play(GrowArrow(a3), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.15))
    scene.play(FadeIn(eq))
    scene.wait(1.1)


def play_scene10_retrieval_augmentation(scene):
    title = Text("Retrieval Augmentation", font_size=48).to_edge(UP)
    axes = Axes(x_range=[-3, 3, 1], y_range=[-2, 2, 1], x_length=7, y_length=4.5, tips=False)
    axes.shift(DOWN * 0.2)
    current = Dot(axes.c2p(0.3, 0.2), color=YELLOW, radius=0.08)
    history_coords = [(-1.8, 0.9), (-1.0, -0.7), (1.7, 1.0), (2.1, -1.1), (0.9, 0.4), (-0.2, 1.2)]
    history = VGroup(*[Dot(axes.c2p(x, y), color=BLUE_B, radius=0.055) for x, y in history_coords])
    radar = Circle(radius=0.25, color=YELLOW).move_to(current)
    nearest_ids = [1, 4, 5]
    nearest = VGroup(*[history[i] for i in nearest_ids])
    links = VGroup(*[Line(current.get_center(), p.get_center(), color=YELLOW_A) for p in nearest])
    sim_label = Text("Cosine similarity -> nearest Q_k", font_size=24).to_edge(DOWN)
    eq = MathTex(
        r"a^{ret}_{i,j}=\frac{\sum_{m\in Q_k}\mathrm{sim}(E_q^i,E_q^m)a_{m,j}}{\sum_{m\in Q_k}\mathrm{sim}(E_q^i,E_q^m)}"
    ).scale(0.75).next_to(title, DOWN, buff=0.3)

    scene.play(FadeIn(title), Create(axes), FadeIn(history), FadeIn(current))
    scene.play(ShowPassingFlash(radar.copy().scale(3.5), time_width=0.8), run_time=1.0)
    scene.play(*[p.animate.set_color(TEAL_A).scale(1.2) for p in nearest], Create(links))
    scene.play(FadeIn(eq), FadeIn(sim_label))
    scene.wait(1.2)


def play_scene11_fusion(scene):
    title = Text("Prediction + Retrieval Fusion", font_size=48).to_edge(UP)
    eq1 = MathTex(r"a_{i,j}=\gamma a^{pred}_{i,j} + (1-\gamma)a^{ret}_{i,j}").scale(0.86).next_to(title, DOWN, buff=0.45)
    eq2 = MathTex(r"c_{i,j}=\delta\,c^{pred}_{i,j} + (1-\delta)\,c^{ret}_{i,j}").scale(0.86).next_to(eq1, DOWN, buff=0.35)

    gamma = ValueTracker(0.2)
    delta = ValueTracker(0.7)
    gamma_bar = NumberLine(x_range=[0, 1, 0.2], length=4.2, include_numbers=False)
    delta_bar = NumberLine(x_range=[0, 1, 0.2], length=4.2, include_numbers=False)
    gamma_bar.next_to(eq2, DOWN, buff=0.55)
    delta_bar.next_to(gamma_bar, DOWN, buff=0.45)
    gamma_dot = always_redraw(lambda: Dot(gamma_bar.n2p(gamma.get_value()), color=YELLOW))
    delta_dot = always_redraw(lambda: Dot(delta_bar.n2p(delta.get_value()), color=ORANGE))
    gamma_text = always_redraw(lambda: VGroup(Text("gamma", font_size=22), DecimalNumber(gamma.get_value(), num_decimal_places=2)).arrange(RIGHT, buff=0.15).next_to(gamma_bar, RIGHT, buff=0.2))
    delta_text = always_redraw(lambda: VGroup(Text("delta", font_size=22), DecimalNumber(delta.get_value(), num_decimal_places=2)).arrange(RIGHT, buff=0.15).next_to(delta_bar, RIGHT, buff=0.2))
    out_a = always_redraw(lambda: DecimalNumber(gamma.get_value() * 0.92 + (1 - gamma.get_value()) * 0.64, num_decimal_places=3, color=YELLOW).next_to(eq1, RIGHT, buff=0.35))
    out_c = always_redraw(lambda: DecimalNumber(delta.get_value() * 1.45 + (1 - delta.get_value()) * 0.95, num_decimal_places=3, color=ORANGE).next_to(eq2, RIGHT, buff=0.35))

    scene.play(FadeIn(title), FadeIn(eq1), FadeIn(eq2))
    scene.play(Create(gamma_bar), Create(delta_bar), FadeIn(gamma_dot), FadeIn(delta_dot))
    scene.play(FadeIn(gamma_text), FadeIn(delta_text), FadeIn(out_a), FadeIn(out_c))
    scene.play(gamma.animate.set_value(0.82), delta.animate.set_value(0.25), run_time=2.0)
    scene.play(gamma.animate.set_value(0.45), delta.animate.set_value(0.75), run_time=2.0)
    scene.wait(1.0)

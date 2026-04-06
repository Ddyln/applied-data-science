"""Function steps for scenes 7-11."""

from manim import *


def play_scene07_embeddings(scene):
    title = Text("Embedding Queries and Models", font_size=48).to_edge(UP)
    eq = MathTex(r"E_q,\;E_l").scale(1.2)
    scene.play(FadeIn(title))
    scene.play(FadeIn(eq))
    scene.wait(0.8)


def play_scene08_capability_prediction(scene):
    title = Text("Capability Prediction", font_size=48).to_edge(UP)
    eq = MathTex(r"a^{pred}_{i,j}=\sigma(W_1(E_q^i\cdot E_l^j)+b_1)").scale(0.9)
    scene.play(FadeIn(title), FadeIn(eq))
    scene.wait(0.8)


def play_scene09_length_prediction(scene):
    title = Text("Length Prediction", font_size=48).to_edge(UP)
    eq = MathTex(
        r"l^{pred}_{i,j}=b_s\cdot \mathrm{softmax}(W_2(E_q^i+E_l^j)+b_2)"
    ).scale(0.88)
    scene.play(FadeIn(title), FadeIn(eq))
    scene.wait(0.8)


def play_scene10_retrieval_augmentation(scene):
    title = Text("Retrieval Augmentation", font_size=48).to_edge(UP)
    eq = MathTex(
        r"a^{ret}_{i,j}=\frac{\sum_{m\in Q_k}\mathrm{sim}(E_q^i,E_q^m)\,a_{m,j}}"
        r"{\sum_{m\in Q_k}\mathrm{sim}(E_q^i,E_q^m)}"
    ).scale(0.82)
    scene.play(FadeIn(title), FadeIn(eq))
    scene.wait(0.8)


def play_scene11_fusion(scene):
    title = Text("Prediction + Retrieval Fusion", font_size=48).to_edge(UP)
    eq1 = MathTex(r"a_{i,j}=\gamma a^{pred}_{i,j} + (1-\gamma)a^{ret}_{i,j}").scale(0.9)
    eq2 = MathTex(
        r"c_{i,j}=\delta\,tp_j(l^{pred}_{i,j}) + (1-\delta)\,tp_j(l^{ret}_{i,j})"
    ).scale(0.86)
    eq2.next_to(eq1, DOWN)
    scene.play(FadeIn(title), FadeIn(eq1), FadeIn(eq2))
    scene.wait(0.8)

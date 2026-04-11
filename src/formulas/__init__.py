"""Equation factories used across scenes."""

"""Centralized MathTex definitions for OmniRouter equations."""

from manim import *


def decision_variable():
    return MathTex(
        r"x_{i,j} = \begin{cases}",
        r"1,\ \text{if query } i \text{ is assigned to model } j",
        r"\\ 0,\ \text{otherwise}",
        r"\end{cases}",
    )


def objective():
    return MathTex(r"\min_x \sum_{i=1}^{N} \sum_{j=1}^{M} c_{i,j} x_{i,j}")


def assignment_constraint():
    return MathTex(r"\sum_{j=1}^{M} x_{i,j} = 1,\ \forall i")


def quality_constraint():
    return MathTex(r"\frac{1}{N}\sum_{i=1}^{N}\sum_{j=1}^{M} a_{i,j}x_{i,j} \ge \alpha")


def capacity_constraint():
    return MathTex(r"\sum_{i=1}^{N} x_{i,j} \le L_j,\ \forall j")


def decision_rule():
    return MathTex(
        r"j^* = \arg\min_j \left(c_{i,j} - \frac{\lambda_1 a_{i,j}}{N} + \lambda_{2,j}\right)"
    )


def lagrangian():
    return MathTex(
        r"\mathcal{L}(x,\lambda_1,\lambda_2,\mu)",
        r"= \sum_{i,j} c_{i,j}x_{i,j}",
        r"+ \lambda_1\left(\alpha - \frac{1}{N}\sum_{i,j}a_{i,j}x_{i,j}\right)",
        r"+ \sum_j \lambda_{2,j}(\sum_i x_{i,j}-L_j)",
        r"+ \sum_i \mu_i(\sum_j x_{i,j}-1)",
    )


def capability_prediction():
    return MathTex(
        r"a^{pred}_{i,j}",  # [0]
        r"=",  # [1]
        r"\sigma",  # [2]
        r"\Bigl(",  # [3]
        r"W_1",  # [4]
        r"(",  # [5]
        r"E_q^i",  # [6]
        r"\cdot",  # [7]
        r"E_l^j",  # [8]
        r")",  # [9]
        r"+",  # [10]
        r"b_1",  # [11]
        r"\Bigr)",  # [12]
        font_size=52,
    )


def length_prediction():
    return MathTex(
        r"l^{pred}_{i,j}",  # [0]  LHS
        r"=",  # [1]
        r"bs",  # [2]  bucket size
        r"\cdot",  # [3]
        r"\mathrm{softmax}",  # [4]  softmax
        r"\Bigl(",  # [5]
        r"W_2",  # [6]
        r"(",  # [7]
        r"E_q^i",  # [8]
        r"+",  # [9]
        r"E_l^j",  # [10]
        r")",  # [11]
        r"+",  # [12]
        r"b_2",  # [13]
        r"\Bigr)",  # [14]
        font_size=50,
    )


def retrieval_length():
    return MathTex(
        r"l^{ret}_{i,j} = \frac{\sum_{q_m \in \mathcal{Q}_k}\mathrm{sim}(E_q^i, E_{q_m})\cdot\, l_{m,j}}{\sum_{q_m \in Q_k}\mathrm{sim}(E_q^i, E_{q_m})}",
        font_size=34,
    )


def retrieval_capability():
    return MathTex(
        r"a^{ret}_{i,j} = \frac{\sum_{q_m \in \mathcal{Q}_k}\mathrm{sim}(E_q^i, E_{q_m})\cdot\, a_{m,j}}{\sum_{q_m \in Q_k}\mathrm{sim}(E_q^i, E_{q_m})}",
        font_size=34,
    )

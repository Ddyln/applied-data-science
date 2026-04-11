from manim import *


def text_box(
    label,
    w=1.85,
    h=0.62,
    alignment="center",
    text_color=WHITE,
    box_color=WHITE,
    font_size=19,
    **kwargs,
):
    b = RoundedRectangle(
        width=w, height=h, corner_radius=0.10, color=box_color, **kwargs
    )
    t = Paragraph(
        label,
        font_size=font_size,
        line_spacing=0.85,
        alignment=alignment,
        color=text_color,
        **kwargs,
    ).move_to(b)
    return VGroup(b, t)


def row_of_var(var_name, n_vars=2, color=BLUE_B):
    return VGroup(
        *[
            VGroup(
                Circle(radius=0.20, color=color, fill_opacity=0.25),
                MathTex(rf"{var_name}", font_size=18).move_to(ORIGIN),
            )
            for _ in range(n_vars)
        ]
    ).arrange(RIGHT, buff=0.10)


__all__ = ["text_box", "row_of_var"]

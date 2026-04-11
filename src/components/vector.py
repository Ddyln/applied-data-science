from manim import *


def vector_strip(n=6, cell=0.30, edge_color=WHITE, fill_color=GREY_D):
    """Horizontal row of n solid-colour squares representing a vector."""
    return VGroup(
        *[
            Square(
                side_length=cell,
                color=edge_color,
                fill_color=fill_color,
                fill_opacity=0.65,
                stroke_width=1.5,
            )
            for _ in range(n)
        ]
    ).arrange(RIGHT, buff=0.04)


__all__ = ["vector_strip"]

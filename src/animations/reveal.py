"""Common reveal choreography helpers."""

from manim import *


def staggered_fade_in(*mobjects, shift=0.2, lag_ratio=0.12):
    """Return a lagged fade-in animation for a sequence of mobjects."""
    return LaggedStartMap(FadeIn, mobjects, shift=shift, lag_ratio=lag_ratio)


def pop_in(mobject):
    """Return a short emphasize animation for entering key objects."""
    return AnimationGroup(FadeIn(mobject, scale=0.92), run_time=0.4)

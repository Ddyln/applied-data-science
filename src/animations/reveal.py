"""Common reveal choreography helpers."""

from manim import *


def staggered_fade_in(*mobjects, shift=0.2, lag_ratio=0.12):
    """Return a lagged fade-in animation for a sequence of mobjects."""
    # Manim 0.19's LaggedStartMap does not accept FadeIn kwargs such as `shift`.
    # Build the FadeIn animations explicitly for compatibility.
    if isinstance(shift, (int, float)):
        shift_vector = UP * shift
    else:
        shift_vector = shift

    return LaggedStart(
        *[FadeIn(mobject, shift=shift_vector) for mobject in mobjects],
        lag_ratio=lag_ratio,
    )


def pop_in(mobject):
    """Return a short emphasize animation for entering key objects."""
    return AnimationGroup(FadeIn(mobject, scale=0.92), run_time=0.4)

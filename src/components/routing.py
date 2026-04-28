"""Visual primitives for query-model routing diagrams."""

from manim import *
from style import theme


# ---------------------------------------------------------------------------
# QueryCard
# ---------------------------------------------------------------------------

class QueryCard(VGroup):
    def __init__(self, label: str, hard: bool = False, **kwargs):
        super().__init__(**kwargs)
        color = theme.QUERY_HARD if hard else theme.QUERY_EASY
        box = RoundedRectangle(
            corner_radius=0.12, width=2.6, height=0.85,
            color=color, stroke_width=2,
        )
        text = Text(label, font_size=theme.LABEL_FONT_SIZE)
        text.scale_to_fit_width(box.width - 0.3)
        text.move_to(box.get_center())
        self.add(box, text)
        self.box = box


# ---------------------------------------------------------------------------
# ModelNode  — two-line label (name + subtitle)
# ---------------------------------------------------------------------------

class ModelNode(VGroup):
    def __init__(self, label: str, strength: str = "medium", **kwargs):
        super().__init__(**kwargs)
        color_map = {
            "weak":   theme.MODEL_WEAK,
            "medium": theme.MODEL_MEDIUM,
            "strong": theme.MODEL_STRONG,
        }
        color = color_map.get(strength, theme.MODEL_MEDIUM)

        box = RoundedRectangle(
            corner_radius=0.12, width=2.6, height=1.0,
            color=color, stroke_width=2,
        )
        name_text = Text(label, font_size=theme.LABEL_FONT_SIZE, weight=BOLD)
        name_text.scale_to_fit_width(box.width - 0.3)

        subtitle_map = {"strong": "Strong $$$", "medium": "Medium  $$", "weak": "Weak     $"}
        sub_text = Text(
            subtitle_map.get(strength, ""),
            font_size=theme.DESCRIPTION_FONT_SIZE,
            color=GREY_C,
        )
    
        sub_text.scale_to_fit_width(box.width - 0.4)
        sub_text.set_opacity(0.95)

        VGroup(name_text, sub_text).arrange(DOWN, buff=0.08).move_to(box.get_center())

        self.add(box, name_text, sub_text)
        self.box = box
        self.name_text = name_text
        self.sub_text = sub_text
        self.strength = strength
        self.color = color

    def get_strength_color(self):
        return self.color


# ---------------------------------------------------------------------------
# AISystemContainer
# ---------------------------------------------------------------------------

class AISystemContainer(VGroup):
    def __init__(self, width: float = 7.5, height: float = 5.5, **kwargs):
        super().__init__(**kwargs)
        self.container_box = RoundedRectangle(
            corner_radius=0.3, width=width, height=height,
            color=GREY_C, stroke_width=2, fill_opacity=0.06,
        )
        self.system_label = Text("AI System", font_size=18, color=GREY_B)
        self.system_label.next_to(self.container_box, UP, buff=0.15)
        self.system_label.set_x(self.container_box.get_center()[0])
        self.add(self.container_box, self.system_label)


# ---------------------------------------------------------------------------
# RouterBox
# ---------------------------------------------------------------------------

class RouterBox(VGroup):
    def __init__(self, label: str = "Router", **kwargs):
        super().__init__(**kwargs)
        box = RoundedRectangle(
            corner_radius=0.15, width=1.8, height=1.1,
            color=PURPLE_B, stroke_width=2.5,
        )
        text = Text(label, font_size=20, color=WHITE, weight=BOLD)
        text.move_to(box.get_center())
        self.add(box, text)


# ---------------------------------------------------------------------------
# LegendEntry
# ---------------------------------------------------------------------------

class LegendEntry(VGroup):
    def __init__(self, label: str, color, **kwargs):
        super().__init__(**kwargs)
        indicator = RoundedRectangle(
            corner_radius=0.07, width=0.32, height=0.32,
            color=color, fill_opacity=1.0,
        )
        text = Text(label, font_size=16, color=WHITE)
        text.next_to(indicator, RIGHT, buff=0.18)
        self.add(indicator, text)


# ---------------------------------------------------------------------------
# Helper factories
# ---------------------------------------------------------------------------

def make_query_column(labels):
    cards = VGroup(*[QueryCard(label, hard=("Hard" in label)) for label in labels])
    cards.arrange(DOWN, buff=0.35)
    return cards


def make_model_column(labels, strengths):
    nodes = VGroup(*[
        ModelNode(label, strength=strength)
        for label, strength in zip(labels, strengths)
    ])
    nodes.arrange(DOWN, buff=0.45)
    return nodes


def connect(src: VGroup, dst: VGroup, good: bool = True):
    """Arrow from right edge of src to left edge of dst."""
    color = theme.ROUTE_GOOD if good else theme.ROUTE_BAD
    return Arrow(src.get_right(), dst.get_left(), buff=0.1, color=color,
                 stroke_width=2.5, max_tip_length_to_length_ratio=0.12)


def create_legend() -> VGroup:
    title = Text("Legend", font_size=18, color=GREY_B, weight=BOLD)
    entries = VGroup(
        LegendEntry("Strong (Expensive)", theme.MODEL_STRONG),
        LegendEntry("Medium", theme.MODEL_MEDIUM),
        LegendEntry("Weak  (Cheap)", theme.MODEL_WEAK),
    )
    entries.arrange(DOWN, buff=0.22, aligned_edge=LEFT)
    group = VGroup(title, entries)
    group.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
    return group


# ---------------------------------------------------------------------------
# Animation helpers
# ---------------------------------------------------------------------------

def staggered_fade_in(*mobjects, lag_ratio: float = 0.15, shift_vec=None):
    """LaggedStart FadeIn for a sequence of mobjects."""
    anims = []
    for mob in mobjects:
        kwargs = {}
        if shift_vec is not None:
            kwargs["shift"] = shift_vec
        anims.append(FadeIn(mob, **kwargs))
    return LaggedStart(*anims, lag_ratio=lag_ratio)


def shake(mobject, intensity: float = 0.06, n: int = 4):
    """Return a Succession of tiny left-right shifts to simulate shaking.

    The original center is captured and restored at the end to avoid
    cumulative positional drift.
    """
    original_center = mobject.get_center()
    anims = []
    for i in range(n):
        direction = RIGHT if i % 2 == 0 else LEFT
        anims.append(mobject.animate(run_time=0.08).shift(direction * intensity))
    # Restore original position
    anims.append(mobject.animate(run_time=0.08).move_to(original_center))
    return Succession(*anims)


__all__ = [
    "QueryCard", "ModelNode", "AISystemContainer", "RouterBox",
    "LegendEntry", "make_query_column", "make_model_column",
    "connect", "create_legend", "staggered_fade_in", "shake",
]
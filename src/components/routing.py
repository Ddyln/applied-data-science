"""Visual primitives for query-model routing diagrams."""

from manim import *

from style import theme


class QueryCard(VGroup):
    def __init__(self, label: str, hard: bool = False, **kwargs):
        super().__init__(**kwargs)
        color = theme.QUERY_HARD if hard else theme.QUERY_EASY
        box = RoundedRectangle(corner_radius=0.12, width=2.6, height=0.9, color=color)
        text = Text(label, font_size=theme.LABEL_FONT_SIZE)
        text.scale_to_fit_width(box.width - 0.25)
        text.move_to(box.get_center())
        self.add(box, text)


class ModelNode(VGroup):
    def __init__(self, label: str, strength: str = "medium", **kwargs):
        super().__init__(**kwargs)
        color_map = {
            "weak": theme.MODEL_WEAK,
            "medium": theme.MODEL_MEDIUM,
            "strong": theme.MODEL_STRONG,
        }
        color = color_map.get(strength, theme.MODEL_MEDIUM)
        box = RoundedRectangle(corner_radius=0.12, width=2.8, height=1.0, color=color)
        text = Text(label, font_size=theme.LABEL_FONT_SIZE)
        self.add(box, text)


def make_query_column(labels):
    cards = VGroup(*[QueryCard(label, hard=("Hard" in label)) for label in labels])
    cards.arrange(DOWN, buff=0.35).to_edge(LEFT, buff=0.8)
    return cards


def make_model_column(labels, strengths):
    nodes = VGroup(
        *[
            ModelNode(label, strength=strength)
            for label, strength in zip(labels, strengths)
        ]
    )
    nodes.arrange(DOWN, buff=0.45).to_edge(RIGHT, buff=0.8)
    return nodes


def connect(query_card: QueryCard, model_node: ModelNode, good: bool = True):
    color = theme.ROUTE_GOOD if good else theme.ROUTE_BAD
    return Arrow(query_card.get_right(), model_node.get_left(), buff=0.1, color=color)


__all__ = [
    "QueryCard",
    "ModelNode",
    "make_query_column",
    "make_model_column",
    "connect",
]

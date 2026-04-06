"""Small layout helpers for titles and scene framing."""

from manim import *

from style.theme import SUBTITLE_FONT_SIZE, TITLE_FONT_SIZE


def make_title(title: str, subtitle: str | None = None):
    title_text = Text(title, font_size=TITLE_FONT_SIZE).to_edge(UP)
    if subtitle is None:
        return title_text

    subtitle_text = Text(subtitle, font_size=SUBTITLE_FONT_SIZE).next_to(
        title_text, DOWN
    )
    return title_text, subtitle_text

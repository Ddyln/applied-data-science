"""Function steps for scenes 1-4."""

from manim import *

from animations.reveal import staggered_fade_in
from components.routing import connect, make_model_column, make_query_column
from style.theme import LABEL_FONT_SIZE


def _query_model_setup():
    query_title = (
        Text("Incoming Queries", font_size=LABEL_FONT_SIZE).to_edge(LEFT).shift(UP * 2)
    )
    model_title = (
        Text("Available Models", font_size=LABEL_FONT_SIZE).to_edge(RIGHT).shift(UP * 2)
    )
    queries = make_query_column(["Easy: x^2 - 1 = 0", "Hard: Build website"])
    models = make_model_column(["Small", "Large"], ["weak", "strong"])
    return query_title, model_title, queries, models


def play_scene01_hook_too_many_llms(scene):
    # title = Text("Too Many LLMs", font_size=52).to_edge(UP)
    # subtitle = Text("Fast vs Smart vs Expensive", font_size=32).next_to(title, DOWN)

    models = make_model_column(
        ["Small Model", "Large Model"],
        ["weak", "strong"],
    ).shift(LEFT * 0.6)
    final_model_center = models.get_center()
    models.move_to(ORIGIN)

    queries = make_query_column(["Query A", "Query B", "Query C"]).shift(RIGHT * 0.4)

    # scene.play(FadeIn(title))
    scene.play(staggered_fade_in(*models))
    scene.wait(5)
    scene.play(models.animate.move_to(final_model_center))
    scene.play(staggered_fade_in(*queries))

    flow_arrows = VGroup(
        connect(queries[0], models[0]),
        connect(queries[1], models[1]),
        connect(queries[2], models[0]),
    )
    packets = VGroup(
        *[
            Dot(radius=0.055, color=WHITE).move_to(arrow.get_start())
            for arrow in flow_arrows
        ]
    )

    scene.play(
        LaggedStart(*[GrowArrow(arrow) for arrow in flow_arrows], lag_ratio=0.15)
    )
    scene.add(packets)

    flow_cycles = 5
    for _ in range(flow_cycles):
        for packet, arrow in zip(packets, flow_arrows):
            packet.move_to(arrow.get_start())
        scene.play(
            LaggedStart(
                *[
                    MoveAlongPath(packet, arrow)
                    for packet, arrow in zip(packets, flow_arrows)
                ],
                lag_ratio=0.2,
                run_time=2,
            )
        )
    scene.wait(0.8)


def play_scene02_what_is_routing(scene):
    # title = Text("Routing", font_size=52).to_edge(UP)
    query_title, model_title, queries, models = _query_model_setup()
    arrows = VGroup(
        connect(queries[0], models[0]),
        connect(queries[1], models[1]),
    )
    # scene.play(FadeIn(title), FadeIn(query_title), FadeIn(model_title))
    scene.play(FadeIn(query_title), FadeIn(model_title))
    scene.play(staggered_fade_in(*queries), staggered_fade_in(*models))
    scene.wait(5)
    scene.play(staggered_fade_in(*arrows))
    scene.wait(5)


def play_scene03_greedy_fails(scene):
    title = Text("Problem with current routing strategy", font_size=52).to_edge(UP)
    subtitle = Text("Greedy Routing", font_size=32).next_to(title, DOWN)
    _, _, queries, models = _query_model_setup()
    first_arrival = (
        Text("Easy query arrives first", font_size=30).to_edge(DOWN).shift(UP * 0.6)
    )
    bad_assign_easy = connect(queries[0], models[1], good=False)
    bad_assign_hard = connect(queries[1], models[0], good=False)
    easy_arrow_note = (
        Text("higher success chance", font_size=22, color=YELLOW)
        .next_to(bad_assign_easy, UP)
        .shift(RIGHT * 0.4)
    )
    easy_selection_note = Text(
        "Greedy picks the model with higher success chance",
        font_size=26,
    ).to_edge(DOWN).shift(UP * 1.0)
    hard_selection_note = Text(
        "Only small model left for difficult task :(",
        font_size=26,
    ).to_edge(DOWN).shift(UP * 1.0)

    scene.play(FadeIn(title), FadeIn(subtitle))
    scene.play(staggered_fade_in(*queries), staggered_fade_in(*models))
    scene.play(
        Indicate(queries[0]),
        # FadeIn(first_arrival),
    )
    scene.play(Indicate(models[1], color=YELLOW), FadeIn(easy_selection_note))
    scene.wait(0.5)
    scene.play(FadeIn(bad_assign_easy))
    # scene.play(bad_assign_easy.animate.set_color(YELLOW), FadeIn(easy_arrow_note))
    # scene.play(Indicate(bad_assign_easy, color=YELLOW))
    scene.play(FadeOut(easy_selection_note))
    scene.wait(0.5)
    scene.play(Indicate(queries[1]), FadeIn(hard_selection_note))
    scene.wait(0.5)
    scene.play(FadeIn(bad_assign_hard))
    # scene.play(FadeOut(easy_arrow_note))
    scene.wait(0.8)


def play_scene04_omnirouter_idea(scene):
    title = Text("Optimize Globally", font_size=52).to_edge(UP)
    queries = make_query_column(["Easy Query", "Hard Query"])
    models = make_model_column(["Weak Model", "Strong Model"], ["weak", "strong"])
    good_assign_easy = connect(queries[0], models[0], good=True)
    good_assign_hard = connect(queries[1], models[1], good=True)
    message = Text("Global optimization beats greedy", font_size=34).to_edge(DOWN)
    scene.play(FadeIn(title))
    scene.play(staggered_fade_in(*queries), staggered_fade_in(*models))
    scene.play(FadeIn(good_assign_easy), FadeIn(good_assign_hard))
    scene.play(FadeIn(message))
    scene.wait(0.8)

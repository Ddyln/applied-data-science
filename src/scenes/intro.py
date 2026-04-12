"""Function steps for scenes 1-4."""

from manim import *

from animations.reveal import staggered_fade_in
from components.routing import connect, make_model_column, make_query_column
from style.theme import LABEL_FONT_SIZE


def play_scene00_intro(scene):
    title = Text("OmniRouter", font_size=60, weight=BOLD, color=YELLOW).shift(UP)
    subtitle = Text(
        "Budget and Performance Controllable Multi-LLM Routing",
        font_size=28,
        color=WHITE,
    ).next_to(title, DOWN, buff=0.25)

    members_label = Text("Visualizations by", font_size=26, color=BLUE_B)
    members = VGroup(
        Text("Phan Bá Đức  - 22120071", font_size=24),
        Text("Đặng Duy Lân - 22120182", font_size=24),
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
    members_group = VGroup(members_label, members).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
    members_group.next_to(subtitle, DOWN, buff=0.55)

    members_box = SurroundingRectangle(
        members_group,
        color=GREY_B,
        buff=0.25,
        corner_radius=0.15,
        stroke_width=2,
    )

    scene.play(Write(title), run_time=1.5)
    scene.play(FadeIn(subtitle, shift=UP * 0.1), run_time=0.8)
    scene.play(Create(members_box), FadeIn(members_group, shift=UP * 0.1), run_time=0.9)
    scene.wait(1.8)
    scene.play(
        FadeOut(VGroup(title, subtitle, members_box, members_group)),
        run_time=0.8,
    )


def _query_model_setup():
    query_title = (
        Text("Incoming Queries", font_size=LABEL_FONT_SIZE).to_edge(LEFT).shift(UP * 2)
    )
    model_title = (
        Text("Available Models", font_size=LABEL_FONT_SIZE).to_edge(RIGHT).shift(UP * 2)
    )
    queries = make_query_column(["Easy: x^2 - 1 = 0", "Hard: Build Facebook!"])
    models = make_model_column(["Small", "Large"], ["weak", "strong"])
    return query_title, model_title, queries, models


def play_scene01_hook_too_many_llms(scene):
    # title = Text("Too Many LLMs", font_size=52).to_edge(UP)
    # subtitle = Text("Fast vs Smart vs Expensive", font_size=32).next_to(title, DOWN)

    models = make_model_column(
        ["Model 1", "Model 2", "Model 3", "Model 4"],
        ["weak", "medium", "strong", "strong"],
    )
    models.arrange(RIGHT, buff=0.45)
    models.move_to(ORIGIN)

    queries = make_query_column(["Query 1", "Query 2", "Query 3", "Query 4"]).shift(
        LEFT * 0.3
    )

    # scene.play(FadeIn(title))
    scene.play(staggered_fade_in(*models))
    scene.wait(5)

    models.generate_target()
    models.target.arrange(DOWN, buff=0.45)
    models.target.to_edge(RIGHT, buff=0.9)
    scene.play(MoveToTarget(models))

    scene.play(staggered_fade_in(*queries))

    flow_arrows = VGroup(
        connect(queries[0], models[0]),
        connect(queries[1], models[1]),
        connect(queries[2], models[3]),
        connect(queries[3], models[2]),
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
    scene.wait(8)
    scene.play(staggered_fade_in(*arrows))
    scene.wait(7.5)


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
    easy_selection_note = (
        Text(
            "Greedy picks the model with higher success chance",
            font_size=26,
        )
        .to_edge(DOWN)
        .shift(UP * 1.0)
    )
    hard_selection_note = (
        Text(
            "Only small model left for difficult task :(",
            font_size=26,
        )
        .to_edge(DOWN)
        .shift(UP * 1.0)
    )
    weakness = Text(
        "-> OmniRouter: constrained global optimization",
        font_size=24,
        # color=YELLOW,
    )
    weakness.to_edge(DOWN).shift(UP * 0.8)

    scene.play(FadeIn(title), FadeIn(subtitle))
    scene.play(staggered_fade_in(*models))
    scene.wait(1)
    scene.play(staggered_fade_in(queries[0]))
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
    scene.play(staggered_fade_in(queries[1]))
    scene.play(Indicate(queries[1]), FadeIn(hard_selection_note))
    scene.wait(0.5)
    scene.play(FadeIn(bad_assign_hard))
    scene.wait(10)
    # scene.play(
    #     FadeOut(hard_selection_note),
    #     FadeOut(queries),
    #     FadeOut(models),
    #     FadeOut(bad_assign_easy),
    #     FadeOut(bad_assign_hard),
    # )
    scene.play(FadeOut(hard_selection_note), FadeIn(weakness))

    # Persist visible objects so Scene 4 can continue without tearing down/rebuilding.
    scene._scene3_state = {
        "title": title,
        "subtitle": subtitle,
        "queries": queries,
        "models": models,
        "bad_assign_easy": bad_assign_easy,
        "bad_assign_hard": bad_assign_hard,
        "weakness": weakness,
    }
    scene.wait(5)


def play_scene04_omnirouter_idea(scene):
    state = getattr(scene, "_scene3_state", None)
    subtitle = None

    if state:
        title = state["title"]
        subtitle = state["subtitle"]
        queries = state["queries"]
        models = state["models"]
        bad_assign_easy = state["bad_assign_easy"]
        bad_assign_hard = state["bad_assign_hard"]
        weakness = state["weakness"]
        scene.play(FadeOut(weakness))
    else:
        title = Text("Optimize Globally", font_size=52).to_edge(UP)
        queries = make_query_column(["Easy Query", "Hard Query"])
        models = make_model_column(["Weak Model", "Strong Model"], ["weak", "strong"])
        bad_assign_easy = connect(queries[0], models[1], good=False)
        bad_assign_hard = connect(queries[1], models[0], good=False)
        scene.play(FadeIn(title))
        scene.play(staggered_fade_in(*queries), staggered_fade_in(*models))
        scene.play(FadeIn(bad_assign_easy), FadeIn(bad_assign_hard))

    good_assign_easy = connect(queries[0], models[0], good=True)
    good_assign_hard = connect(queries[1], models[1], good=True)
    transition_note = (
        Text(
            "Plan jointly across all queries under constraints",
            font_size=28,
            # color=YELLOW,
        )
        .to_edge(DOWN)
        .shift(UP * 0.9)
    )
    message = Text(
        "-> Joint assignment improves overall success", font_size=28
    ).to_edge(DOWN)
    punchline = Text("But... how does it actually work?!", font_size=42, color=WHITE)

    # punchline.arrange(DOWN, buff=0).move_to(ORIGIN)
    scene.wait(0.3)
    scene.play(FadeIn(transition_note))
    scene.play(
        ReplacementTransform(bad_assign_easy, good_assign_easy),
        ReplacementTransform(bad_assign_hard, good_assign_hard),
    )
    scene.wait(0.6)
    scene.play(FadeIn(message))
    scene.wait(2)
    focus_group = VGroup(
        title,
        subtitle,
        queries,
        models,
        good_assign_easy,
        good_assign_hard,
        message,
        transition_note,
    )
    scene.play(focus_group.animate.set_opacity(0.22))
    scene.play(FadeIn(punchline, scale=0.85))
    scene.wait(3)
    # scene.play(FadeOut(punchline_group), focus_group.animate.set_opacity(1.0))

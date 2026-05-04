"""Function steps for scenes 1-4."""

from manim import *

from animations.reveal import staggered_fade_in
from components.routing import (
    connect,
    make_model_column,
    make_query_column,
    AISystemContainer,
    RouterBox,
    create_legend,
    QueryCard,
    ModelNode,
    shake
)
from style.theme import LABEL_FONT_SIZE, MODEL_STRONG, MODEL_WEAK


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
    members_group = VGroup(members_label, members).arrange(
        DOWN, buff=0.25, aligned_edge=LEFT
    )
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
    models = make_model_column(["Small", "Large"], ["weak", "strong"], _height_box=1.0)
    return query_title, model_title, queries, models

def play_scene01_hook_too_many_llms(scene: Scene):
    """
    Scene 1: Introduction to Multi-Model System
 
    Narrative arc
    ─────────────
    1. Draw the AI System container
    2. Populate it with 4 models in a 2×2 grid
    3. Drop in the query column (left side)
    4. Show legend below queries
    5. Greedy routing (bad) → overload warning
    6. Remove greedy arrows, introduce Router
    7. Optimal routing through the router with animated packets
    8. Conclusion text
    """
 
    system = AISystemContainer(width=9, height=6)
    system.move_to(RIGHT * 2.3)
 
    scene.play(
        Create(system.container_box),
        FadeIn(system.system_label),
        run_time=0.9,
    )

    router = RouterBox(label="Router")
    router.move_to(ORIGIN)

    scene.play(GrowFromCenter(router))
    scene.wait(0.8)
 
    model_labels    = ["Model A", "Model B", "Model C", "Model D"]
    model_strengths = ["strong",  "weak",    "strong",  "medium"]
 
    models = VGroup(*[
        ModelNode(lbl, strength=s)
        for lbl, s in zip(model_labels, model_strengths)
    ])
    models.arrange_in_grid(rows=4, cols=1, buff=0.4)
    models.move_to(system.container_box.get_center()).shift(RIGHT * 2.6)
 
    scene.play(staggered_fade_in(*models, lag_ratio=0.18, shift=UP * 0.2))
    scene.wait(0.8)
 
    # Briefly indicate strong models so viewer notices them
    strong_idx = [i for i, s in enumerate(model_strengths) if s == "strong"]
    scene.play(AnimationGroup(
        *[Indicate(models[i], color=MODEL_STRONG, scale_factor=1.12) for i in strong_idx],
        lag_ratio=0.25,
        run_time=1.2,
    ))
    scene.wait(0.6)
 
    query_labels = ["Query 1", "Query 2", "Query 3", "Query 4"]
    # query_labels = ["Query 1 (Easy)", "Query 2 (Hard)", "Query 3 (Easy)", "Query 4 (Hard)"]
    queries = VGroup(*[
        QueryCard(lbl, hard=("Hard" in lbl))
        for lbl in query_labels
    ])
    queries.arrange(DOWN, buff=0.4)
    queries.to_edge(LEFT, buff=0.8)     
 
    scene.play(staggered_fade_in(*queries, lag_ratio=0.15, shift=RIGHT * 0.3))
    scene.wait(0.8)
 
    # Queries → Router
    q2r_arrows = VGroup(*[
        Arrow(
            queries[i].get_right(), router.get_left(),
            buff=0.12, color=queries[i].box.color,
            stroke_width=2, max_tip_length_to_length_ratio=0.12,
        )
        for i in range(len(queries))
    ])
 
    optimal = [(0, 1), (1, 0), (2, 3), (3, 2)]
 
    r2m_arrows = VGroup(*[
        Arrow(
            router.get_right(), models[mi].get_left(),
            buff=0.12, color=queries[qi].box.color,
            stroke_width=2, max_tip_length_to_length_ratio=0.12,
        )
        for qi, mi in optimal
    ])
 
    scene.play(LaggedStart(
        *[GrowArrow(a) for a in q2r_arrows],
        lag_ratio=0.15, run_time=1.1,
    ))
    scene.wait(0.4)
    scene.play(LaggedStart(
        *[GrowArrow(a) for a in r2m_arrows],
        lag_ratio=0.15, run_time=1.1,
    ))
    scene.wait(0.8)
 
    def _flow_cycle():
        # Phase A: packets travel query → router
        phase_a_dots = [
            Dot(radius=0.07, color=queries[i].box.color)
               .move_to(q2r_arrows[i].get_start())
            for i in range(len(queries))
        ]
        scene.add(*phase_a_dots)
        scene.play(LaggedStart(
            *[MoveAlongPath(d, q2r_arrows[i]) for i, d in enumerate(phase_a_dots)],
            lag_ratio=0.15, run_time=1.0,
        ))
        scene.remove(*phase_a_dots)
 
        # Phase B: packets travel router → assigned model
        phase_b_dots = [
            Dot(radius=0.07, color=queries[qi].box.color)
               .move_to(r2m_arrows[k].get_start())
            for k, (qi, _) in enumerate(optimal)
        ]
        scene.add(*phase_b_dots)
        scene.play(LaggedStart(
            *[MoveAlongPath(d, r2m_arrows[k]) for k, d in enumerate(phase_b_dots)],
            lag_ratio=0.15, run_time=1.0,
        ))
        scene.remove(*phase_b_dots)
 
    _flow_cycle()
    scene.wait(0.3)
    _flow_cycle()
    scene.wait(0.6)
 
    # Persist state for potential use in subsequent scenes
    scene._scene1_state = {
        "system":      system,
        "models":      models,
        "queries":     queries,
        "router":      router,
        "q2r_arrows":  q2r_arrows,
        "r2m_arrows":  r2m_arrows,
    }
    scene.wait(1.0)

def play_scene02_what_is_routing(scene):
    """
    Scene 2: What is Routing?
    
    Combines Scene 1 structure with 2 models and 2 queries.
    Shows flow from queries through router to models.
    """
    
    # Title
    title = Text("What is Routing?", font_size=48, color=YELLOW).to_edge(UP)
    scene.play(Write(title), run_time=1.2)
    scene.wait(0.5)
    query_title, model_title, queries, models = _query_model_setup()
    # ------------------------------------------------------------------
    # AI System container + models (2: weak and strong)
    # ------------------------------------------------------------------
    system = AISystemContainer(width=9, height=4.0)
    system.move_to(RIGHT * 2.3)
    
    scene.play(
        Create(system.container_box),
        FadeIn(system.system_label),
        run_time=0.9,
    )

    router = RouterBox(label="Router")
    router.move_to(ORIGIN)
    
    scene.play(GrowFromCenter(router))
    scene.wait(0.8)

    # model_labels    = ["Small", "Large"]
    # model_strengths = ["weak", "strong"]
    
    # models = VGroup(*[
    #     ModelNode(lbl, strength=s, _height_box = 1.5)
    #     for lbl, s in zip(model_labels, model_strengths)
    # ])
    models.arrange(DOWN, buff=0.5)
    models.move_to(system.container_box.get_center()).shift(RIGHT * 2.5)
    
    scene.play(staggered_fade_in(*models, lag_ratio=0.18, shift=UP * 0.2))
    
    # model_title.move_to(system.container_box.get_top() + UP * 0.5 + RIGHT * 2.6 )

    # scene.play(
    #     FadeIn(model_title),
    #     model_title.animate.set_opacity(0.9)
    # )

    scene.wait(0.6)
    
    # ------------------------------------------------------------------
    # 2 Queries: Easy and Hard
    # ------------------------------------------------------------------
    # query_labels = ["Easy Query", "Hard Query"]
    # queries = VGroup(*[
    #     QueryCard(lbl, hard=("Hard" in lbl))
    #     for lbl in query_labels
    # ])
    queries.arrange(DOWN, buff=0.5)
    queries.to_edge(LEFT, buff=1.0)
    
    scene.play(staggered_fade_in(*queries, lag_ratio=0.2, shift=RIGHT * 0.2))

    query_title.move_to(system.container_box.get_top() + UP * 0.5 + LEFT * 7 )

    scene.play(
        FadeIn(query_title),
        query_title.animate.set_opacity(0.9)
    )
    scene.wait(0.6)
    
    # ------------------------------------------------------------------
    # Flow arrows: queries → router → models
    # ------------------------------------------------------------------
    # Queries → Router
    q2r_arrows = VGroup(*[
        Arrow(
            queries[i].get_right(), router.get_left(),
            buff=0.12, color=queries[i].box.color,
            stroke_width=2.5, max_tip_length_to_length_ratio=0.12,
        )
        for i in range(len(queries))
    ])
    
    # Router → Models
    # Query 0 (easy) → Model 0 (small/weak)
    # Query 1 (hard) → Model 1 (large/strong)
    routing_mapping = [(0, 0), (1, 1)]
    
    r2m_arrows = VGroup(*[
        Arrow(
            router.get_right(), models[m_idx].get_left(),
            buff=0.12, color=queries[q_idx].box.color,
            stroke_width=2.5, max_tip_length_to_length_ratio=0.12,
        )
        for q_idx, m_idx in routing_mapping
    ])
    
    # Draw arrows with stagger
    scene.play(LaggedStart(
        *[GrowArrow(a) for a in q2r_arrows],
        lag_ratio=0.2, run_time=1.0,
    ))
    scene.wait(0.3)
    
    scene.play(LaggedStart(
        *[GrowArrow(a) for a in r2m_arrows],
        lag_ratio=0.2, run_time=1.0,
    ))
    scene.wait(0.8)
    
    # ------------------------------------------------------------------
    # Explanation text
    # ------------------------------------------------------------------
    explanation = Text(
        "Routing: assign queries to models optimally",
        font_size=24, color=GREEN_B,
    ).to_edge(DOWN, buff=0.6)
    
    scene.play(FadeIn(explanation, shift=UP * 0.2))
    scene.wait(1.0)
    
    # ------------------------------------------------------------------
    # Animated flow cycles (2 cycles)
    # ------------------------------------------------------------------
    def _flow_cycle():
        # Phase A: packets query → router
        phase_a_dots = [
            Dot(radius=0.06, color=queries[i].box.color)
               .move_to(q2r_arrows[i].get_start())
            for i in range(len(queries))
        ]
        scene.add(*phase_a_dots)
        scene.play(LaggedStart(
            *[MoveAlongPath(d, q2r_arrows[i]) for i, d in enumerate(phase_a_dots)],
            lag_ratio=0.2, run_time=0.9,
        ))
        scene.remove(*phase_a_dots)
        
        # Phase B: packets router → model
        phase_b_dots = [
            Dot(radius=0.06, color=queries[q_idx].box.color)
               .move_to(r2m_arrows[k].get_start())
            for k, (q_idx, _) in enumerate(routing_mapping)
        ]
        scene.add(*phase_b_dots)
        scene.play(LaggedStart(
            *[MoveAlongPath(d, r2m_arrows[k]) for k, d in enumerate(phase_b_dots)],
            lag_ratio=0.2, run_time=0.9,
        ))
        scene.remove(*phase_b_dots)
    
    _flow_cycle()
    scene.wait(0.3)
    _flow_cycle()
    scene.wait(0.6)
    
    # ------------------------------------------------------------------
    # Persist state
    # ------------------------------------------------------------------
    scene._scene2_state = {
        "title": title,
        "system": system,
        "models": models,
        "queries": queries,
        "router": router,
        "q2r_arrows": q2r_arrows,
        "r2m_arrows": r2m_arrows,
        "explanation": explanation,
    }
    
    scene.wait(1.5)


def play_scene03_greedy_fails(scene):
    title = Text("Problem with current routing strategy", font_size=52).to_edge(UP)
    subtitle = Text("Greedy Routing", font_size=32).next_to(title, DOWN)
    _, _, queries, models = _query_model_setup()

    # ------------------------------------------------------------------
    # Shared layout: queries on the left, router in the middle,
    # AI system + models on the right.
    # ------------------------------------------------------------------
    SHIFT_DOWN = DOWN * 0.2
    system = AISystemContainer(width=9.0, height=3.0)
    system.move_to(RIGHT * 2.3 + SHIFT_DOWN)

    router = RouterBox(label="Router")
    router.move_to(ORIGIN + SHIFT_DOWN)

    models.arrange(DOWN, buff=0.5)
    models.move_to(system.container_box.get_center()).shift(RIGHT * 2.1)

    queries.arrange(DOWN, buff=0.5)
    queries.to_edge(LEFT, buff=1.0).shift(SHIFT_DOWN)

    first_arrival = Text(
        "Easy query arrives first",
        font_size=30,
    ).to_edge(DOWN).shift(UP * 0.3)

    easy_selection_note = Text(
        "Greedy picks the model with higher success chance",
        font_size=26,
    ).to_edge(DOWN).shift(UP * 0.8)

    hard_selection_note = Text(
        "Only small model left for difficult task :(",
        font_size=26,
    ).to_edge(DOWN).shift(UP * 0.8)

    easy_arrow_note = Text(
        "Higher success chance",
        font_size=22,
        color=YELLOW,
    ).next_to(router, UP).shift(RIGHT * 0.8)

    weakness = Text(
        "→ OmniRouter: constrained global optimization",
        font_size=24,
    ).to_edge(DOWN).shift(UP * 0.3)

    strong_idx = [i for i, mob in enumerate(models) if mob.strength == "strong"]

    # ------------------------------------------------------------------
    # Step 1: Introduce the whole system, router, and models.
    # ------------------------------------------------------------------
    scene.play(FadeIn(title), FadeIn(subtitle))
    scene.play(Create(system.container_box), FadeIn(system.system_label))
    scene.play(GrowFromCenter(router))
    scene.play(staggered_fade_in(*models, lag_ratio=0.18, shift=UP * 0.15))
    scene.wait(1.0)

    # Emphasize the strong model box only, so subtitle text stays neutral.
    scene.play(AnimationGroup(
        *[Indicate(models[i].box, color=MODEL_STRONG, scale_factor=1.12) for i in strong_idx],
        lag_ratio=0.2,
        run_time=1.0,
    ))
    scene.wait(0.5)

    # ------------------------------------------------------------------
    # Step 2: First query arrives and greedy routing chooses the strong model.
    # ------------------------------------------------------------------
    scene.play(staggered_fade_in(queries[0], shift=RIGHT * 0.25))
    scene.play(FadeIn(first_arrival, shift=UP * 0.1))
    scene.play(Indicate(queries[0]))

    q0_to_router = Arrow(
        queries[0].get_right(), router.get_left(),
        buff=0.12, color=queries[0].box.color,
        stroke_width=2.5, max_tip_length_to_length_ratio=0.12,
    )
    bad_assign_easy = Arrow(
        router.get_right(), models[1].get_left(),
        buff=0.12, color=queries[0].box.color,
        stroke_width=2.5, max_tip_length_to_length_ratio=0.12,
    )
    easy_packet = Dot(radius=0.06, color=queries[0].box.color).move_to(q0_to_router.get_start())

    scene.play(GrowArrow(q0_to_router))
    scene.add(easy_packet)
    scene.play(MoveAlongPath(easy_packet, q0_to_router))
    scene.remove(easy_packet)

    scene.play(Indicate(models[1].box, color=YELLOW, scale_factor=1.08), FadeIn(easy_selection_note))
    scene.play(GrowArrow(bad_assign_easy), FadeIn(easy_arrow_note))
    scene.wait(1.2)

    scene.play(FadeOut(easy_selection_note), FadeOut(first_arrival), FadeOut(easy_arrow_note))

    # ------------------------------------------------------------------
    # Step 3: Second query arrives, but the remaining choice is poor.
    # ------------------------------------------------------------------
    scene.play(staggered_fade_in(queries[1], shift=RIGHT * 0.25))
    scene.play(Indicate(queries[1]), FadeIn(hard_selection_note))

    q1_to_router = Arrow(
        queries[1].get_right(), router.get_left(),
        buff=0.12, color=queries[1].box.color,
        stroke_width=2.5, max_tip_length_to_length_ratio=0.12,
    )
    bad_assign_hard = Arrow(
        router.get_right(), models[0].get_left(),
        buff=0.12, color=queries[1].box.color,
        stroke_width=2.5, max_tip_length_to_length_ratio=0.12,
    )
    hard_packet = Dot(radius=0.06, color=queries[1].box.color).move_to(q1_to_router.get_start())

    scene.play(GrowArrow(q1_to_router))
    scene.add(hard_packet)
    scene.play(MoveAlongPath(hard_packet, q1_to_router))
    scene.remove(hard_packet)

    scene.play(GrowArrow(bad_assign_hard))
    scene.wait(1.0)

    # ------------------------------------------------------------------
    # Step 4: Show the limitation of greedy routing.
    # ------------------------------------------------------------------
    scene.play(FadeOut(hard_selection_note), FadeIn(weakness))
    scene.play(
        shake(models[1].box, intensity=0.06, n=5),
        Indicate(models[1].box, color=RED_B, scale_factor=1.05),
        run_time=0.9,
    )
    scene.wait(0.8)

    # Persist visible objects so Scene 4 can continue without tearing down/rebuilding.
    scene._scene3_state = {
        "title": title,
        "subtitle": subtitle,
        "system": system,
        "router": router,
        "queries": queries,
        "models": models,
        "bad_assign_easy": bad_assign_easy,
        "bad_assign_hard": bad_assign_hard,
        "weakness": weakness,
    }
    scene.wait(8)


def play_scene04_omnirouter_idea(scene):
    state = getattr(scene, "_scene3_state", None)
    subtitle = None
    system = None
    router = None
    q2r_arrows = None

    if state:
        # Reuse Scene 03 objects to preserve continuity.
        title = state["title"]
        subtitle = state["subtitle"]
        system = state.get("system")
        router = state.get("router")
        queries = state["queries"]
        models = state["models"]
        bad_assign_easy = state["bad_assign_easy"]
        bad_assign_hard = state["bad_assign_hard"]
        weakness = state["weakness"]
        scene.play(FadeOut(weakness))
    else:
        # Fallback layout mirrors Scene 03 visual language.
        shift_down = DOWN * 0.2
        title = Text("Optimize Globally", font_size=52).to_edge(UP)
        subtitle = Text("From Greedy to Global", font_size=32).next_to(title, DOWN)

        system = AISystemContainer(width=9.0, height=3.0)
        system.move_to(RIGHT * 2.3 + shift_down)

        router = RouterBox(label="Router")
        router.move_to(ORIGIN + shift_down)

        # queries = make_query_column(["Easy: x^2 - 1 = 0", "Hard: Build Facebook!"])
        # models = make_model_column(["Small", "Large"], ["weak", "strong"], _height_box=1.0)

        queries = make_query_column(["Easy: x^2 - 1 = 0", "Hard: Build Facebook!"])
        queries.arrange(DOWN, buff=0.5)
        queries.to_edge(LEFT, buff=1.0).shift(shift_down)

        models = make_model_column(["Small", "Large"], ["weak", "strong"])
        models.arrange(DOWN, buff=0.5)
        models.move_to(system.container_box.get_center()).shift(RIGHT * 2.1)

        q2r_arrows = VGroup(
            Arrow(
                queries[0].get_right(), router.get_left(),
                buff=0.12, color=queries[0].box.color,
                stroke_width=2.5, max_tip_length_to_length_ratio=0.12,
            ),
            Arrow(
                queries[1].get_right(), router.get_left(),
                buff=0.12, color=queries[1].box.color,
                stroke_width=2.5, max_tip_length_to_length_ratio=0.12,
            ),
        )

        bad_assign_easy = Arrow(
            router.get_right(), models[1].get_left(),
            buff=0.12, color=queries[0].box.color,
            stroke_width=2.5, max_tip_length_to_length_ratio=0.12,
        )
        bad_assign_hard = Arrow(
            router.get_right(), models[0].get_left(),
            buff=0.12, color=queries[1].box.color,
            stroke_width=2.5, max_tip_length_to_length_ratio=0.12,
        )

        scene.play(FadeIn(title), FadeIn(subtitle))
        scene.play(Create(system.container_box), FadeIn(system.system_label))
        scene.play(GrowFromCenter(router))
        scene.play(staggered_fade_in(*models, lag_ratio=0.18, shift=UP * 0.15))
        scene.play(staggered_fade_in(*queries, lag_ratio=0.18, shift=RIGHT * 0.15))
        scene.play(LaggedStart(*[GrowArrow(a) for a in q2r_arrows], lag_ratio=0.2))
        scene.play(FadeIn(bad_assign_easy), FadeIn(bad_assign_hard))

    # Keep original scene logic: replace bad assignment with globally good assignment.
    if router is not None:
        good_assign_easy = Arrow(
            router.get_right(), models[0].get_left(),
            buff=0.12, color=queries[0].box.color,
            stroke_width=2.5, max_tip_length_to_length_ratio=0.12,
        )
        good_assign_hard = Arrow(
            router.get_right(), models[1].get_left(),
            buff=0.12, color=queries[1].box.color,
            stroke_width=2.5, max_tip_length_to_length_ratio=0.12,
        )
    else:
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
        "→ Joint assignment improves overall success", font_size=28
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
    focus_items = [
        title,
        subtitle,
        system,
        router,
        q2r_arrows,
        queries,
        models,
        good_assign_easy,
        good_assign_hard,
        message,
        transition_note,
    ]
    focus_group = VGroup(*[item for item in focus_items if item is not None])
    scene.play(focus_group.animate.set_opacity(0.22))
    scene.play(FadeIn(punchline, scale=0.85))
    scene.wait(3)
    # scene.play(FadeOut(punchline_group), focus_group.animate.set_opacity(1.0))

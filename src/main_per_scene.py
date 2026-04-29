"""Entrypoint that exposes one Manim Scene class per narrative scene."""

from manim import *

from scenes.formulation import (
    play_scene05_problem_formulation,
    play_scene06_two_stage_framework,
)
from scenes.intro import (
    play_scene00_intro,
    play_scene01_hook_too_many_llms,
    play_scene02_what_is_routing,
    play_scene03_greedy_fails,
    play_scene04_omnirouter_idea,
)
from scenes.optimization import (
    play_scene12_lagrangian,
    play_scene13_optimality_condition,
    play_scene14_decision_rule,
    play_scene15_dual_updates,
    play_scene16_dual_intuition,
)
from scenes.predictor import (
    play_scene08_capability_prediction,
    play_scene09_length_prediction,
    play_scene10_retrieval_augmentation,
    play_scene11_fusion,
)
from scenes.results import play_scene17_results, play_scene18_conclusion


# class Scene00(Scene):
#     def construct(self):
#         play_scene00_intro(self)


# class Scene01(Scene):
#     def construct(self):
#         play_scene01_hook_too_many_llms(self)


# class Scene02(Scene):
#     def construct(self):
#         play_scene02_what_is_routing(self)


# class Scene03(Scene):
#     def construct(self):
#         play_scene03_greedy_fails(self)


class Scene04(Scene):
    def construct(self):
        play_scene04_omnirouter_idea(self)


# class Scene05(Scene):
#     def construct(self):
#         play_scene05_problem_formulation(self)


# class Scene06(Scene):
#     def construct(self):
#         play_scene06_two_stage_framework(self)


# class Scene08(Scene):
#     def construct(self):
#         play_scene08_capability_prediction(self)


# class Scene09(Scene):
#     def construct(self):
#         play_scene09_length_prediction(self)


# class Scene10(Scene):
#     def construct(self):
#         play_scene10_retrieval_augmentation(self)


# class Scene11(Scene):
#     def construct(self):
#         play_scene11_fusion(self)


# class Scene12(Scene):
#     def construct(self):
#         play_scene12_lagrangian(self)


# class Scene13(Scene):
#     def construct(self):
#         play_scene13_optimality_condition(self)


# class Scene14(Scene):
#     def construct(self):
#         play_scene14_decision_rule(self)


# class Scene15(Scene):
#     def construct(self):
#         play_scene15_dual_updates(self)


# class Scene16(Scene):
#     def construct(self):
#         play_scene16_dual_intuition(self)


# class Scene17(Scene):
#     def construct(self):
#         play_scene17_results(self)


# class Scene18(Scene):
#     def construct(self):
#         play_scene18_conclusion(self)


__all__ = [
    # "Scene00",
    # "Scene01",
    # "Scene02",
    # "Scene03",
    "Scene04",
    # "Scene05",
    # "Scene06",
    # "Scene08",
    # "Scene09",
    # "Scene10",
    # "Scene11",
    # "Scene12",
    # "Scene13",
    # "Scene14",
    # "Scene15",
    # "Scene16",
    # "Scene17",
    # "Scene18",
]

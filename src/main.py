"""Single-scene entrypoint for the full OmniRouter walkthrough."""

from manim import *

from scenes.formulation import (
    play_scene05_problem_formulation,
    play_scene06_two_stage_framework,
)
from scenes.intro import (
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
    play_scene07_embeddings,
    play_scene08_capability_prediction,
    play_scene09_length_prediction,
    play_scene10_retrieval_augmentation,
    play_scene11_fusion,
)
from scenes.results import play_scene17_results, play_scene18_conclusion


KEEP_STAGE_AFTER_STEPS = [play_scene03_greedy_fails]
class OmniRouter(Scene):
    def construct(self):
        steps = (
            # play_scene01_hook_too_many_llms,
            # play_scene02_what_is_routing,
            # play_scene03_greedy_fails,
            # play_scene04_omnirouter_idea,
            play_scene05_problem_formulation,
            play_scene06_two_stage_framework,
            # play_scene07_embeddings,
            # play_scene08_capability_prediction,
            # play_scene09_length_prediction,
            # play_scene10_retrieval_augmentation,
            # play_scene11_fusion,
            # play_scene12_lagrangian,
            # play_scene13_optimality_condition,
            # play_scene14_decision_rule,
            # play_scene15_dual_updates,
            # play_scene16_dual_intuition,
            # play_scene17_results,
            # play_scene18_conclusion,
        )

        for idx, step in enumerate(steps):
            step(self)

            keep_stage_for_next = (
                step in KEEP_STAGE_AFTER_STEPS
            )
            if not keep_stage_for_next:
                self._reset_stage()

    def _reset_stage(self):
        if self.mobjects:
            self.play(*[FadeOut(mob) for mob in self.mobjects])


__all__ = ["OmniRouter"]

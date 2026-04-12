"""Function steps for scenes 17-18."""

from manim import *


def play_scene17_results(scene):
    title = Text("Results", font_size=38).to_edge(UP, buff=0.45)
    scene.play(FadeIn(title, shift=DOWN * 0.2))

    # ══════════════════════════════════════════════════════════════════════
    #  ACT 1  (0s – 20s): Overall routing performance table
    # ══════════════════════════════════════════════════════════════════════
    act1_title = Text("Overall Routing Performance", font_size=20, color=YELLOW)
    act1_title.next_to(title, DOWN, buff=0.25)

    table1_data = [
        ["OmniRouter (proposed)", "75.19%", "$0.0515", "Cheapest + most accurate"],
        ["RouterDC", "73.89%", "$0.0874", "High accuracy, expensive"],
        ["EmbedLLM", "72.96%", "$0.0896", "Highest cost"],
        ["CARROT", "72.41%", "$0.0680", "Balanced"],
        ["S3", "69.45%", "$0.0585", "Low cost, lower accuracy"],
    ]
    table1 = Table(
        table1_data,
        col_labels=[
            Text("Method", font_size=17),
            Text("Accuracy", font_size=17),
            Text("Cost", font_size=17),
            Text("Feature", font_size=17),
        ],
        include_outer_lines=True,
        line_config={"stroke_color": GREY_B, "stroke_width": 1.2},
    ).scale(0.52)
    table1.next_to(act1_title, DOWN, buff=0.22)

    table1.add_highlighted_cell((1, 1), color=GOLD)
    table1.add_highlighted_cell((1, 2), color=GOLD)
    table1.add_highlighted_cell((1, 3), color=GOLD)
    table1.add_highlighted_cell((1, 4), color=GOLD)

    callout1 = VGroup(
        Text("+6.30% accuracy and -10.15% cost vs baselines", font_size=17, color=GREEN_A),
        Text("~41% cheaper than RouterDC", font_size=17, color=GREEN_A),
    ).arrange(DOWN, buff=0.10, aligned_edge=LEFT)
    callout1.next_to(table1, DOWN, buff=0.28)

    scene.play(FadeIn(act1_title, shift=UP * 0.1), Create(table1), run_time=1.4)
    scene.play(FadeIn(callout1, shift=UP * 0.1), run_time=0.8)
    scene.wait(1.0)

    # ══════════════════════════════════════════════════════════════════════
    #  ACT 2  (20s – 40s): Controllability charts
    # ══════════════════════════════════════════════════════════════════════
    scene.play(FadeOut(VGroup(act1_title, table1, callout1)), run_time=0.7)

    act2_title = Text("Controllability Under Hard Constraints", font_size=20, color=YELLOW)
    act2_title.next_to(title, DOWN, buff=0.25)

    alpha = [0.7, 0.75, 0.8, 0.85, 0.9]

    cost_data = {
        "OmniRouter": ([0.042, 0.045, 0.049, 0.055, 0.054], BLUE),
        "CARROT": ([0.068, 0.072, 0.078, 0.095, 0.132], YELLOW),
        "RouterDC": ([0.087, 0.091, 0.098, 0.125, 0.208], GREEN),
        "EmbedLLM": ([0.090, 0.095, 0.103, 0.138, 0.230], RED),
        "Hybrid-LLM": ([0.072, 0.078, 0.085, 0.103, 0.168], PURPLE),
        "S3": ([0.058, 0.062, 0.071, 0.088, 0.142], MAROON_B),
        "PO": ([0.060, 0.066, 0.074, 0.092, 0.158], ORANGE),
    }

    acc_data = {
        "OmniRouter": ([75.2, 75.8, 76.5, 77.2, 77.6], BLUE),
        "CARROT": ([72.4, 73.1, 74.1, 75.2, 75.7], YELLOW),
        "RouterDC": ([73.9, 74.2, 74.8, 75.6, 76.2], GREEN),
        "EmbedLLM": ([72.9, 73.5, 74.1, 75.2, 75.8], RED),
        "Hybrid-LLM": ([71.5, 72.3, 73.5, 74.1, 74.9], PURPLE),
        "S3": ([69.4, 70.3, 71.8, 72.9, 73.5], MAROON_B),
        "PO": ([68.7, 69.4, 70.9, 72.3, 73.2], ORANGE),
    }

    def styled_lines(axes, data_dict, x_values):
        lines = []
        for name, (values, color) in data_dict.items():
            line = axes.plot_line_graph(
                x_values=x_values,
                y_values=values,
                line_color=color,
                add_vertex_dots=True,
                vertex_dot_radius=0.028,
            )
            base_curve = line["line_graph"]
            dots = line["vertex_dots"]
            if name == "OmniRouter":
                base_curve.set_stroke(width=4.6)
                dots.set_opacity(1.0)
                styled_line = VGroup(base_curve, dots)
            else:
                dashed_curve = DashedVMobject(base_curve.copy(), num_dashes=28, dashed_ratio=0.60)
                dashed_curve.set_color(color).set_stroke(width=2.0, opacity=0.95)
                dots.set_opacity(0.85)
                styled_line = VGroup(dashed_curve, dots)
            lines.append(styled_line)
        return lines

    axes_cost = Axes(
        x_range=[0.7, 0.9, 0.05],
        y_range=[0.04, 0.24, 0.04],
        x_length=4.2,
        y_length=2.8,
        axis_config={"include_numbers": True, "font_size": 18},
    ).shift(LEFT * 3.2 + DOWN * 0.12)

    axes_acc = Axes(
        x_range=[0.7, 0.9, 0.05],
        y_range=[68, 78, 2],
        x_length=4.2,
        y_length=2.8,
        axis_config={"include_numbers": True, "font_size": 18},
    ).shift(RIGHT * 3.2 + DOWN * 0.12)

    cost_labels = axes_cost.get_axis_labels(MathTex(r"\alpha").scale(0.65), Text("Cost ($)", font_size=16))
    acc_labels = axes_acc.get_axis_labels(MathTex(r"\alpha").scale(0.65), Text("Accuracy (%)", font_size=16))

    cost_lines = styled_lines(axes_cost, cost_data, alpha)
    acc_lines = styled_lines(axes_acc, acc_data, alpha)

    def compact_legend(data_dict, font_size=13):
        rows = []
        for name, (_, color) in data_dict.items():
            marker = Dot(radius=0.045, color=color)
            label = Text(name, font_size=font_size, color=color)
            rows.append(VGroup(marker, label).arrange(RIGHT, buff=0.08))
        return VGroup(*rows).arrange(DOWN, aligned_edge=LEFT, buff=0.04)

    legend_cost = compact_legend(cost_data)
    legend_cost.scale(0.96)
    legend_cost.move_to(axes_cost.c2p(0.735, 0.195))

    legend_acc = compact_legend(acc_data)
    legend_acc.scale(0.96)
    legend_acc.move_to(axes_acc.c2p(0.862, 71.3))

    cap_a = Text("(a) Cost vs. Performance Constraint", font_size=18)
    cap_a.next_to(axes_cost, DOWN, buff=0.12)
    cap_b = Text("(b) Accuracy vs. Performance Constraint", font_size=18)
    cap_b.next_to(axes_acc, DOWN, buff=0.12)

    scene.play(FadeIn(act2_title, shift=UP * 0.1), Create(axes_cost), Create(axes_acc), run_time=1.0)
    scene.play(FadeIn(cost_labels), FadeIn(acc_labels), run_time=0.5)
    scene.play(LaggedStart(*[Create(l) for l in cost_lines], lag_ratio=0.12), run_time=1.2)
    scene.play(LaggedStart(*[Create(l) for l in acc_lines], lag_ratio=0.12), run_time=1.2)
    scene.play(
        cost_lines[0][0].animate.set_stroke(width=6),
        acc_lines[0][0].animate.set_stroke(width=6),
        run_time=0.5,
    )
    scene.play(FadeIn(legend_cost), FadeIn(legend_acc), FadeIn(cap_a), FadeIn(cap_b), run_time=0.6)
    scene.wait(0.6)

    scene.play(
        FadeOut(
            VGroup(
                axes_cost,
                axes_acc,
                cost_labels,
                acc_labels,
                *cost_lines,
                *acc_lines,
                legend_cost,
                legend_acc,
                cap_a,
                cap_b,
            )
        ),
        run_time=0.65,
    )

    next_title = Text("Controllability Under Concurrency Constraint", font_size=20, color=YELLOW)
    next_title.move_to(act2_title)
    scene.play(Transform(act2_title, next_title), run_time=0.35)

    l_vals = [8, 6, 4, 2, 1]
    cost_data_l = {
        "OmniRouter": ([0.040, 0.045, 0.049, 0.056, 0.064], BLUE),
        "CARROT": ([0.066, 0.074, 0.094, 0.120, 0.144], YELLOW),
        "RouterDC": ([0.088, 0.097, 0.125, 0.168, 0.215], GREEN),
        "EmbedLLM": ([0.090, 0.105, 0.138, 0.185, 0.232], RED),
        "Hybrid-LLM": ([0.071, 0.082, 0.104, 0.138, 0.168], PURPLE),
        "S3": ([0.058, 0.067, 0.089, 0.112, 0.132], MAROON_B),
        "PO": ([0.063, 0.071, 0.093, 0.118, 0.141], ORANGE),
    }
    acc_data_l = {
        "OmniRouter": ([75.1, 74.9, 74.7, 74.2, 73.8], BLUE),
        "CARROT": ([72.5, 71.8, 70.9, 69.2, 67.3], YELLOW),
        "RouterDC": ([73.9, 73.2, 72.1, 69.5, 68.1], GREEN),
        "EmbedLLM": ([73.0, 72.1, 70.9, 68.2, 66.4], RED),
        "Hybrid-LLM": ([71.4, 70.5, 69.4, 66.8, 64.5], PURPLE),
        "S3": ([69.4, 68.7, 67.2, 64.5, 62.1], MAROON_B),
        "PO": ([68.7, 67.9, 66.4, 63.7, 61.2], ORANGE),
    }

    axes_cost_l = Axes(
        x_range=[1, 8, 1],
        y_range=[0.03, 0.24, 0.04],
        x_length=4.2,
        y_length=2.8,
        axis_config={"font_size": 18},
        x_axis_config={"include_numbers": False},
        y_axis_config={"include_numbers": True},
    ).shift(LEFT * 3.2 + DOWN * 0.12)
    axes_acc_l = Axes(
        x_range=[1, 8, 1],
        y_range=[60, 76, 2],
        x_length=4.2,
        y_length=2.8,
        axis_config={"font_size": 18},
        x_axis_config={"include_numbers": False},
        y_axis_config={"include_numbers": True},
    ).shift(RIGHT * 3.2 + DOWN * 0.12)

    l_plot_vals = [9 - l for l in l_vals]
    cost_lines_l = styled_lines(axes_cost_l, cost_data_l, l_plot_vals)
    acc_lines_l = styled_lines(axes_acc_l, acc_data_l, l_plot_vals)

    def concurrency_ticks(axes):
        labels = []
        for x in range(1, 9):
            tick = Text(str(9 - x), font_size=14)
            tick.next_to(axes.c2p(x, axes.y_range[0]), DOWN, buff=0.06)
            labels.append(tick)
        return VGroup(*labels)

    x_ticks_cost_l = concurrency_ticks(axes_cost_l)
    x_ticks_acc_l = concurrency_ticks(axes_acc_l)

    y_label_cost_l = Text("Cost ($)", font_size=16).rotate(PI / 2)
    y_label_cost_l.next_to(axes_cost_l.y_axis, LEFT, buff=0.20)

    y_label_acc_l = Text("Accuracy (%)", font_size=16).rotate(PI / 2)
    y_label_acc_l.next_to(axes_acc_l.y_axis, LEFT, buff=0.20)

    legend_cost_l = compact_legend(cost_data_l)
    legend_cost_l.scale(0.96)
    legend_cost_l.move_to(axes_cost_l.c2p(2.0, 0.195))

    legend_acc_l = compact_legend(acc_data_l)
    legend_acc_l.scale(0.96)
    legend_acc_l.move_to(axes_acc_l.c2p(2.1, 63.9))

    cap_c = Text("(a) Cost vs. Concurrency Constraint", font_size=18)
    cap_c.next_to(axes_cost_l, DOWN, buff=0.42)
    cap_d = Text("(b) Accuracy vs. Concurrency Constraint", font_size=18)
    cap_d.next_to(axes_acc_l, DOWN, buff=0.42)

    scene.play(Create(axes_cost_l), Create(axes_acc_l), run_time=0.9)
    scene.play(
        FadeIn(x_ticks_cost_l),
        FadeIn(x_ticks_acc_l),
        FadeIn(y_label_cost_l),
        FadeIn(y_label_acc_l),
        run_time=0.45,
    )
    scene.play(LaggedStart(*[Create(l) for l in cost_lines_l], lag_ratio=0.12), run_time=1.15)
    scene.play(LaggedStart(*[Create(l) for l in acc_lines_l], lag_ratio=0.12), run_time=1.15)
    scene.play(
        cost_lines_l[0][0].animate.set_stroke(width=6),
        acc_lines_l[0][0].animate.set_stroke(width=6),
        run_time=0.45,
    )
    scene.play(FadeIn(legend_cost_l), FadeIn(legend_acc_l), FadeIn(cap_c), FadeIn(cap_d), run_time=0.6)
    scene.wait(1.0)

    # ══════════════════════════════════════════════════════════════════════
    #  ACT 3  (40s – 55s): Predictor performance
    # ══════════════════════════════════════════════════════════════════════
    scene.play(
        FadeOut(
            VGroup(
                act2_title,
                axes_cost_l,
                axes_acc_l,
                x_ticks_cost_l,
                x_ticks_acc_l,
                y_label_cost_l,
                y_label_acc_l,
                *cost_lines_l,
                *acc_lines_l,
                legend_cost_l,
                legend_acc_l,
                cap_c,
                cap_d,
            )
        ),
        run_time=0.7,
    )


def play_scene18_conclusion(scene):
    thanks_text = Text(
        "Thanks for Watching!",
        font_size=58,
        weight=BOLD,
        color=WHITE,
    ).move_to(ORIGIN)
    scene.play(FadeIn(thanks_text, shift=UP * 0.2), run_time=1.4)
    scene.wait(2.0)
    scene.play(FadeOut(thanks_text), run_time=0.9)

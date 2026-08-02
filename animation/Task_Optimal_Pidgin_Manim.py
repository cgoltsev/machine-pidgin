"""Task-Optimal Pidgin — Manim Community Edition source.

Render from this directory with:
    manim -pqh task_optimal_pidgin_manim.py TaskOptimalPidgin

The scene expects task_optimal_pidgin_voiceover.wav in the same directory.
Written for Manim CE 0.19. The source was Python-syntax checked, but the
current execution environment did not provide the Manim package itself.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
from manim import *

BASE = Path(__file__).resolve().parent
TIMING = json.loads((BASE / "timing.json").read_text())

BG = "#080D18"
PANEL = "#121B2B"
PANEL2 = "#192437"
WHITE = "#EFF3F8"
MUTED = "#9EABBE"
BLUE = "#539FE0"
CYAN = "#55D2DE"
GREEN = "#5BCD8F"
ORANGE = "#F7A637"
RED = "#EE5B68"
PURPLE = "#AE7DE8"
YELLOW = "#F8D757"

config.background_color = BG
config.frame_width = 16
config.frame_height = 9
config.pixel_width = 1920
config.pixel_height = 1080
config.frame_rate = 30


class TaskOptimalPidgin(Scene):
    def construct(self) -> None:
        self.elapsed = 0.0
        self.add_sound(str(BASE / "task_optimal_pidgin_voiceover.wav"))

        self.scene_intro(0)
        self.scene_many_meanings(1)
        self.scene_ontologies(2)
        self.scene_information_limit(3)
        self.scene_spherical_cow(4)
        self.scene_frontier(5)
        self.scene_spear(6)
        self.scene_example(7)
        self.scene_clarification(8)
        self.scene_close(9)

    # ---------- timing and style helpers ----------
    def play_for(self, *animations: Animation, run_time: float = 1.0, **kwargs) -> None:
        self.play(*animations, run_time=run_time, **kwargs)
        self.elapsed += run_time

    def wait_for(self, duration: float) -> None:
        if duration > 0:
            self.wait(duration)
            self.elapsed += duration

    def wait_to(self, target: float) -> None:
        self.wait_for(max(0.0, target - self.elapsed))

    def clear_to(self, target: float, run_time: float = 0.38) -> None:
        remaining = max(0.0, target - self.elapsed)
        rt = min(run_time, remaining) if remaining else 0
        if self.mobjects and rt > 0:
            self.play_for(*[FadeOut(m) for m in list(self.mobjects)], run_time=rt)
        elif self.mobjects:
            self.remove(*list(self.mobjects))
        self.wait_to(target)

    def heading(self, text: str, index: int) -> VGroup:
        title = Text(text, font_size=34, weight=BOLD, color=WHITE).to_edge(UP, buff=0.35).to_edge(LEFT, buff=0.55)
        line = Line(LEFT * 7.4, RIGHT * 7.4, color="#3C4B62", stroke_width=1.6).next_to(title, DOWN, buff=0.18)
        progress = Line(
            line.get_left(),
            line.get_left() + RIGHT * line.get_length() * ((index + 0.2) / len(TIMING)),
            color=BLUE,
            stroke_width=4,
        )
        count = Text(f"{index + 1:02d} / {len(TIMING):02d}", font_size=18, color=MUTED).to_edge(UP, buff=0.43).to_edge(RIGHT, buff=0.55)
        return VGroup(title, line, progress, count)

    def box(self, width: float, height: float, color: str, radius: float = 0.18, fill: str = PANEL) -> RoundedRectangle:
        return RoundedRectangle(
            width=width,
            height=height,
            corner_radius=radius,
            stroke_color=color,
            stroke_width=2.5,
            fill_color=fill,
            fill_opacity=0.96,
        )

    # ---------- scene 1 ----------
    def scene_intro(self, i: int) -> None:
        end = TIMING[i]["end"]
        title = Text("TASK-OPTIMAL PIDGIN", font_size=64, weight=BOLD, font="DejaVu Serif", color=WHITE).shift(UP * 2.7)
        subtitle = Text(
            "Information-theoretic specification across human–AI expressiveness gaps",
            font_size=28,
            color=MUTED,
        ).next_to(title, DOWN, buff=0.25)
        self.play_for(FadeIn(title, shift=UP * 0.2), run_time=1.1)
        self.play_for(FadeIn(subtitle), run_time=0.9)

        human = Circle(radius=1.25, color=BLUE, stroke_width=4).shift(LEFT * 3.8 + DOWN * 0.4)
        for ang in (0, TAU / 3, 2 * TAU / 3):
            human.add(Line(human.get_center(), human.get_center() + 1.25 * np.array([math.cos(ang), math.sin(ang), 0]), color=BLUE))
        machine = Circle(radius=1.25, color=PURPLE, stroke_width=4).shift(RIGHT * 3.8 + DOWN * 0.4)
        rays = VGroup(*[
            Line(machine.get_center(), machine.get_center() + 1.25 * np.array([math.cos(k * TAU / 16), math.sin(k * TAU / 16), 0]), color=PURPLE, stroke_opacity=0.55)
            for k in range(16)
        ])
        prompt_box = self.box(2.25, 0.9, ORANGE).move_to(DOWN * 0.4)
        prompt = Text("PROMPT  M", font_size=28, weight=BOLD, color=WHITE).move_to(prompt_box)
        arrows = VGroup(
            Arrow(human.get_right(), prompt_box.get_left(), color=ORANGE, buff=0.18),
            Arrow(prompt_box.get_right(), machine.get_left(), color=ORANGE, buff=0.18),
        )
        labels = VGroup(
            Text("Human apparatus  H₇", font_size=25, color=BLUE).next_to(human, DOWN),
            Text("Machine apparatus  A₃₃", font_size=25, color=PURPLE).next_to(machine, DOWN),
        )
        self.play_for(Create(human), Create(machine), run_time=1.4)
        self.play_for(LaggedStart(Create(rays), FadeIn(prompt_box), FadeIn(prompt), Create(arrows), lag_ratio=0.18), run_time=1.8)
        self.play_for(FadeIn(labels), run_time=0.7)
        phrase = Text("One sentence  →  many task hypotheses", font_size=30, weight=BOLD, color=RED).shift(DOWN * 3.2)
        self.play_for(FadeIn(phrase, shift=UP * 0.2), run_time=0.8)
        self.wait_to(end - 0.4)
        self.clear_to(end)

    # ---------- scene 2 ----------
    def scene_many_meanings(self, i: int) -> None:
        end = TIMING[i]["end"]
        header = self.heading("One prompt, many meanings", i)
        core_box = self.box(4.2, 1.15, ORANGE, fill=PANEL2)
        core = Text("“MAKE IT FASTER”", font_size=42, weight=BOLD, color=WHITE).move_to(core_box)
        self.play_for(FadeIn(header), FadeIn(core_box), Write(core), run_time=1.0)

        labels = [
            ("p99 latency", BLUE, UL * 3.0),
            ("throughput", GREEN, LEFT * 5.1 + UP * 0.2),
            ("compile time", PURPLE, LEFT * 4.8 + DOWN * 2.1),
            ("training time", CYAN, LEFT * 2.2 + DOWN * 3.0),
            ("energy", YELLOW, RIGHT * 2.2 + DOWN * 3.0),
            ("cloud cost", ORANGE, RIGHT * 4.8 + DOWN * 2.1),
            ("time-to-market", RED, RIGHT * 5.1 + UP * 0.2),
            ("model size", BLUE, UR * 3.0),
        ]
        nodes = VGroup()
        branches = VGroup()
        for text, color, pos in labels:
            rect = self.box(2.55, 0.72, color).move_to(pos)
            lab = Text(text, font_size=22, weight=BOLD, color=color).move_to(rect)
            nodes.add(VGroup(rect, lab))
            branches.add(Arrow(core_box.get_center(), rect.get_center(), color=color, buff=0.72, stroke_width=2.5, max_tip_length_to_length_ratio=0.08))
        self.play_for(LaggedStart(*[Create(a) for a in branches], lag_ratio=0.08), run_time=1.4)
        self.play_for(LaggedStart(*[FadeIn(n, scale=0.92) for n in nodes], lag_ratio=0.08), run_time=1.6)
        entropy = MathTex(r"H(Z_T\mid M,C)\ \text{large}", font_size=44, color=RED).shift(DOWN * 2.35)
        caveat = Text("Coherent output does not prove intent fidelity.", font_size=29, weight=BOLD, color=WHITE).next_to(entropy, DOWN, buff=0.25)
        self.play_for(Write(entropy), FadeIn(caveat), run_time=1.2)
        self.wait_to(end - 0.4)
        self.clear_to(end)

    # ---------- scene 3 ----------
    def scene_ontologies(self, i: int) -> None:
        end = TIMING[i]["end"]
        header = self.heading("Unequal representational apparatuses", i)
        left_box = self.box(3.5, 4.7, BLUE).shift(LEFT * 4.4 + DOWN * 0.15)
        left_title = Text("HUMAN CELL", font_size=23, weight=BOLD, color=BLUE).next_to(left_box.get_top(), DOWN, buff=0.45)
        fast = Text("“FAST”", font_size=64, weight=BOLD, font="DejaVu Serif", color=WHITE).move_to(left_box)
        unique = Text("appears unique", font_size=24, color=MUTED).next_to(fast, DOWN, buff=0.65)
        self.play_for(FadeIn(header), FadeIn(left_box), FadeIn(left_title), Write(fast), FadeIn(unique), run_time=1.2)

        right_box = self.box(7.2, 4.9, PURPLE).shift(RIGHT * 2.6 + DOWN * 0.1)
        grid = VGroup()
        for x in (-1.2, 1.2):
            grid.add(Line(right_box.get_center() + UP * 2.45 + RIGHT * x, right_box.get_center() + DOWN * 2.45 + RIGHT * x, color="#586985"))
        for y in (-0.82, 0.82):
            grid.add(Line(right_box.get_center() + LEFT * 3.6 + UP * y, right_box.get_center() + RIGHT * 3.6 + UP * y, color="#586985"))
        labs = [
            ("latency", RED), ("throughput", GREEN), ("compile time", PURPLE),
            ("training time", CYAN), ("energy", YELLOW), ("cloud cost", ORANGE),
            ("tail latency", BLUE), ("time-to-market", RED), ("model size", GREEN),
        ]
        label_group = VGroup()
        for k, (txt, col) in enumerate(labs):
            row, column = divmod(k, 3)
            label_group.add(Text(txt, font_size=21, weight=BOLD, color=col).move_to(
                right_box.get_center() + RIGHT * ((column - 1) * 2.4) + UP * ((1 - row) * 1.64)
            ))
        arrow = Arrow(left_box.get_right(), right_box.get_left(), color=ORANGE, buff=0.35)
        rt = Text("MACHINE REFINEMENT", font_size=25, weight=BOLD, color=PURPLE).next_to(right_box, UP, buff=0.25)
        self.play_for(Create(arrow), FadeIn(right_box), FadeIn(rt), run_time=0.9)
        self.play_for(Create(grid), LaggedStart(*[FadeIn(x) for x in label_group], lag_ratio=0.07), run_time=1.8)
        eq = MathTex(r"D_{\rm task}=H(Z_T\mid Z_H)", font_size=46, color=WHITE).to_edge(DOWN, buff=0.45)
        self.play_for(Write(eq), run_time=0.9)
        self.wait_to(end - 0.4)
        self.clear_to(end)

    # ---------- scene 4 ----------
    def scene_information_limit(self, i: int) -> None:
        end = TIMING[i]["end"]
        header = self.heading("The information limit", i)
        self.play_for(FadeIn(header), run_time=0.5)
        intent = Text("latent intent  Θ", font_size=28, weight=BOLD, color=BLUE).shift(LEFT * 5.5 + UP * 2.65)
        fields = ["objective", "metric", "units", "constraints", "prior", "format", "stakes", "context"]
        field_group = VGroup()
        for k, txt in enumerate(fields):
            col = GREEN if k in (0, 2, 3, 6) else MUTED
            r = self.box(2.15, 0.42, col, radius=0.09).move_to(LEFT * 5.45 + UP * (1.95 - 0.48 * k))
            t = Text(txt, font_size=17, weight=BOLD, color=col).move_to(r)
            g = VGroup(r, t)
            if k not in (0, 2, 3, 6):
                g.add(Line(r.get_corner(UL), r.get_corner(DR), color=RED, stroke_width=3))
            field_group.add(g)
        prompt_box = self.box(2.6, 1.4, ORANGE, fill=PANEL2).shift(LEFT * 1.5)
        prompt = VGroup(
            Text("PROMPT M", font_size=30, weight=BOLD, color=WHITE),
            Text("4 transmitted fields", font_size=18, color=ORANGE),
        ).arrange(DOWN, buff=0.18).move_to(prompt_box)
        decoder = Circle(radius=1.2, color=PURPLE, fill_color=PANEL2, fill_opacity=1, stroke_width=4).shift(RIGHT * 2.2)
        dtext = VGroup(Text("DECODER", font_size=24, weight=BOLD, color=PURPLE), MathTex(r"\delta_{33}", font_size=40, color=WHITE)).arrange(DOWN, buff=0.12).move_to(decoder)
        action_box = self.box(2.1, 1.0, GREEN).shift(RIGHT * 5.35)
        action = Text("ACTION  â", font_size=27, weight=BOLD, color=GREEN).move_to(action_box)
        arrows = VGroup(Arrow(field_group.get_right(), prompt_box.get_left(), color=ORANGE, buff=0.3), Arrow(prompt_box.get_right(), decoder.get_left(), color=BLUE, buff=0.3), Arrow(decoder.get_right(), action_box.get_left(), color=GREEN, buff=0.3))
        self.play_for(FadeIn(intent), LaggedStart(*[FadeIn(x) for x in field_group], lag_ratio=0.05), run_time=1.5)
        self.play_for(FadeIn(prompt_box), FadeIn(prompt), Create(arrows[0]), run_time=0.8)
        self.play_for(FadeIn(decoder), FadeIn(dtext), Create(arrows[1]), run_time=0.8)
        self.play_for(FadeIn(action_box), FadeIn(action), Create(arrows[2]), run_time=0.8)
        self.play_for(decoder.animate.scale(1.25), run_time=0.45, rate_func=there_and_back)
        fano = MathTex(
            r"P_e\geq \frac{H(Z_T)-I(Z_T;M,C)-\log 2}{\log N}",
            font_size=47,
            color=WHITE,
        ).shift(DOWN * 2.45)
        slogan = Text("More computation cannot create missing mutual information.", font_size=28, weight=BOLD, color=RED).next_to(fano, DOWN, buff=0.2)
        self.play_for(Write(fano), FadeIn(slogan), run_time=1.2)
        self.wait_to(end - 0.4)
        self.clear_to(end)

    # ---------- scene 5 ----------
    def scene_spherical_cow(self, i: int) -> None:
        end = TIMING[i]["end"]
        header = self.heading("The spherical-cow theorem", i)
        self.play_for(FadeIn(header), run_time=0.5)
        body = Ellipse(width=5.2, height=2.7, color="#E6EBF1", fill_color="#E6EBF1", fill_opacity=1).shift(LEFT * 3.8 + DOWN * 0.1)
        head = Ellipse(width=1.8, height=1.4, color="#E6EBF1", fill_color="#E6EBF1", fill_opacity=1).next_to(body, RIGHT, buff=-0.2).shift(UP * 0.15)
        muzzle = Ellipse(width=1.0, height=0.62, color="#CDB2AD", fill_color="#CDB2AD", fill_opacity=1).next_to(head, RIGHT, buff=-0.35).shift(DOWN * 0.22)
        legs = VGroup(*[RoundedRectangle(width=0.42, height=1.7, corner_radius=0.12, color="#E6EBF1", fill_color="#E6EBF1", fill_opacity=1).move_to(body.get_center() + RIGHT * x + DOWN * 1.65) for x in (-1.8, -0.65, 0.75, 1.75)])
        spots = VGroup(Ellipse(width=1.3, height=0.9, color="#454E5E", fill_color="#454E5E", fill_opacity=1).move_to(body.get_center()+LEFT*0.9+UP*0.2), Ellipse(width=1.1, height=0.75, color="#454E5E", fill_color="#454E5E", fill_opacity=1).move_to(body.get_center()+RIGHT*1.0+UP*0.35))
        cow = VGroup(body, head, muzzle, legs, spots)
        details = VGroup(*[
            Text(txt, font_size=19, color=MUTED).move_to(pos)
            for txt, pos in [
                ("fur anisotropy", LEFT * 5.4 + UP * 2.3),
                ("local geometry", LEFT * 2.2 + UP * 2.2),
                ("limbs", LEFT * 4.3 + DOWN * 2.85),
                ("posture", LEFT * 2.2 + DOWN * 2.8),
            ]
        ])
        self.play_for(FadeIn(cow), FadeIn(details), run_time=1.2)

        sphere = VGroup(
            Circle(radius=1.75, color=BLUE, fill_color=PANEL2, fill_opacity=1, stroke_width=4),
            Ellipse(width=3.5, height=0.85, color=CYAN, stroke_opacity=0.75),
            Line(ORIGIN, RIGHT * 1.25 + UP * 0.75, color=ORANGE, stroke_width=4),
            Text("r", font_size=28, weight=BOLD, color=ORANGE).shift(RIGHT * 1.1 + UP * 0.9),
        ).shift(LEFT * 3.8 + DOWN * 0.1)
        self.play_for(FadeOut(details), ReplacementTransform(cow, sphere), run_time=1.5)

        preserve_box = self.box(2.45, 3.25, GREEN).shift(RIGHT * 1.4)
        ignore_box = self.box(2.45, 3.25, RED).shift(RIGHT * 4.35)
        preserve = VGroup(
            Text("PRESERVE", font_size=23, weight=BOLD, color=GREEN),
            Text("• surface area\n• mean ΔT\n• coefficient h", font_size=21, line_spacing=1.25, color=WHITE),
        ).arrange(DOWN, buff=0.45).move_to(preserve_box)
        ignore = VGroup(
            Text("IGNORE", font_size=23, weight=BOLD, color=RED),
            Text("• limbs\n• fur texture\n• posture", font_size=21, line_spacing=1.25, color=WHITE),
        ).arrange(DOWN, buff=0.45).move_to(ignore_box)
        self.play_for(FadeIn(preserve_box), FadeIn(preserve), FadeIn(ignore_box), FadeIn(ignore), run_time=1.0)
        quotient = MathTex(r"Z_T^*=\Theta/\!\sim_T", font_size=50, color=WHITE).to_edge(DOWN, buff=0.45)
        self.play_for(Write(quotient), run_time=0.8)
        self.wait_to(end - 0.4)
        self.clear_to(end)

    # ---------- scene 6 ----------
    def scene_frontier(self, i: int) -> None:
        end = TIMING[i]["end"]
        header = self.heading("The pidgin efficiency frontier", i)
        self.play_for(FadeIn(header), run_time=0.5)
        axes = Axes(
            x_range=[0, 10, 1], y_range=[0, 10, 1],
            x_length=11.2, y_length=5.0,
            axis_config={"include_ticks": False, "color": WHITE, "stroke_width": 2},
            tips=True,
        ).shift(DOWN * 0.15)
        xlab = Text("human cognitive cost  B", font_size=25, weight=BOLD, color=WHITE).next_to(axes.x_axis, DOWN, buff=0.22)
        ylab = Text("task-semantic distortion  D", font_size=25, weight=BOLD, color=WHITE).rotate(PI/2).next_to(axes.y_axis, LEFT, buff=0.2)
        curve = axes.plot(lambda x: 8.6 * math.exp(-0.36 * x) + 0.55, x_range=[0.55, 9.5], color=BLUE, stroke_width=5)
        self.play_for(Create(axes), FadeIn(xlab), FadeIn(ylab), run_time=1.0)
        self.play_for(Create(curve), run_time=1.5)
        left = Text("UNDERSPECIFIED\nlow cost, high ambiguity", font_size=22, weight=BOLD, color=RED, line_spacing=0.9).move_to(axes.c2p(1.2, 8.7))
        right = Text("OVERDESCRIBED\nlow distortion, high human cost", font_size=21, weight=BOLD, color=PURPLE, line_spacing=0.9).move_to(axes.c2p(8.1, 2.0))
        self.play_for(FadeIn(left), FadeIn(right), run_time=0.8)
        opt = Dot(axes.c2p(4.3, 2.38), color=ORANGE, radius=0.11)
        opt_label = Text("TASK-OPTIMAL\nminimal sufficient detail", font_size=24, weight=BOLD, color=ORANGE, line_spacing=0.9).move_to(axes.c2p(5.7, 4.8))
        opt_arrow = Arrow(opt_label.get_bottom(), opt.get_center(), color=ORANGE, buff=0.18)
        self.play_for(FadeIn(opt), FadeIn(opt_label), Create(opt_arrow), run_time=1.0)
        self.wait_to(end - 0.4)
        self.clear_to(end)

    # ---------- scene 7 ----------
    def scene_spear(self, i: int) -> None:
        end = TIMING[i]["end"]
        header = self.heading("SPEAR: a shared specification pidgin", i)
        self.play_for(FadeIn(header), run_time=0.5)
        nl_box = self.box(3.5, 1.35, BLUE).shift(LEFT * 5.0 + UP * 2.1)
        nl = Text("natural language\ngoals • context • exceptions", font_size=21, weight=BOLD, color=BLUE, line_spacing=0.9).move_to(nl_box)
        math_box = self.box(3.5, 1.35, PURPLE).shift(RIGHT * 5.0 + UP * 2.1)
        math_text = Text("mathematical notation\ntypes • invariants • constraints", font_size=21, weight=BOLD, color=PURPLE, line_spacing=0.9).move_to(math_box)
        spear = Text("SPEAR", font_size=62, weight=BOLD, font="DejaVu Serif", color=WHITE).shift(UP * 2.1)
        arrows = VGroup(Arrow(nl_box.get_right(), spear.get_left(), color=BLUE, buff=0.25), Arrow(math_box.get_left(), spear.get_right(), color=PURPLE, buff=0.25))
        self.play_for(FadeIn(nl_box), FadeIn(nl), FadeIn(math_box), FadeIn(math_text), run_time=1.0)
        self.play_for(Create(arrows), FadeIn(spear, scale=1.2), run_time=0.9)

        fields = [
            ("TASK", BLUE), ("OBJECTS + TYPES", CYAN), ("ABSTRACTION", GREEN), ("OBJECTIVE", ORANGE), ("CONSTRAINTS", RED),
            ("UNCERTAINTY", PURPLE), ("OUTPUT", BLUE), ("EVALUATION", GREEN), ("INTERACTION", ORANGE), ("EXAMPLES", YELLOW),
        ]
        cards = VGroup()
        for k, (txt, col) in enumerate(fields):
            rect = self.box(2.55, 0.68, col, radius=0.12)
            lab = Text(txt, font_size=18, weight=BOLD, color=col).move_to(rect)
            cards.add(VGroup(rect, lab))
        cards.arrange_in_grid(rows=2, cols=5, buff=(0.22, 0.42)).shift(DOWN * 0.25)
        self.play_for(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in cards], lag_ratio=0.08), run_time=2.1)
        note = Text("A prompt protocol—not a replacement for prose.", font_size=28, weight=BOLD, color=WHITE).to_edge(DOWN, buff=0.65)
        self.play_for(FadeIn(note), run_time=0.7)
        self.wait_to(end - 0.4)
        self.clear_to(end)

    # ---------- scene 8 ----------
    def scene_example(self, i: int) -> None:
        end = TIMING[i]["end"]
        header = self.heading("From vague request to typed specification", i)
        self.play_for(FadeIn(header), run_time=0.5)
        loose_box = self.box(5.0, 4.7, RED).shift(LEFT * 4.2 + DOWN * 0.15)
        loose = VGroup(
            Text("LOOSE PROMPT", font_size=24, weight=BOLD, color=RED),
            Text("“Make the anomaly detector\nfaster without hurting quality.”", font_size=29, weight=BOLD, font="DejaVu Serif", color=WHITE, line_spacing=1.0),
            Text("Which speed?\nWhich quality?\nUnder what load?", font_size=20, color=MUTED, line_spacing=1.0),
        ).arrange(DOWN, buff=0.45).move_to(loose_box)
        self.play_for(FadeIn(loose_box), FadeIn(loose), run_time=1.0)

        spec_box = self.box(7.7, 5.2, GREEN, fill=PANEL2).shift(RIGHT * 3.5 + DOWN * 0.05)
        lines = VGroup(
            self.spec_line("OBJECTIVE:", "minimize latency_p99", ORANGE),
            self.spec_line("CONSTRAINTS:", "throughput ≥ 10⁶ events/s", RED),
            self.spec_line("", "Δ recall ≥ −0.01", RED),
            self.spec_line("", "memory ≤ 64 GB", RED),
            self.spec_line("EVALUATION:", "all hard constraints pass", GREEN),
            self.spec_line("INTERACTION:", "ask if baseline workload is missing", BLUE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(spec_box)
        bridge = Arrow(loose_box.get_right(), spec_box.get_left(), color=ORANGE, buff=0.25)
        self.play_for(Create(bridge), FadeIn(spec_box), run_time=0.8)
        self.play_for(LaggedStart(*[FadeIn(line, shift=RIGHT * 0.2) for line in lines], lag_ratio=0.12), run_time=2.1)
        entropy = VGroup(
            Text("residual task entropy", font_size=20, weight=BOLD, color=MUTED),
            Rectangle(width=6.0, height=0.25, color="#47566E", fill_color=RED, fill_opacity=1),
        ).arrange(RIGHT, buff=0.3).to_edge(DOWN, buff=0.55)
        self.play_for(FadeIn(entropy), run_time=0.5)
        self.play_for(entropy[1].animate.stretch(0.22, 0, about_edge=LEFT).set_fill(GREEN), run_time=1.2)
        self.wait_to(end - 0.4)
        self.clear_to(end)

    def spec_line(self, key: str, value: str, color: str) -> VGroup:
        key_obj = (Text(key, font_size=18, weight=BOLD, font="DejaVu Sans Mono", color=color).set_width(2.0, stretch=True)
                   if key else Rectangle(width=2.0, height=0.01, stroke_opacity=0, fill_opacity=0))
        val_obj = Text(value, font_size=18, font="DejaVu Sans Mono", color=WHITE)
        return VGroup(key_obj, val_obj).arrange(RIGHT, buff=0.25, aligned_edge=DOWN)

    # ---------- scene 9 ----------
    def scene_clarification(self, i: int) -> None:
        end = TIMING[i]["end"]
        header = self.heading("Clarify by value of information", i)
        self.play_for(FadeIn(header), run_time=0.5)
        message_box = self.box(4.0, 1.0, ORANGE, fill=PANEL2).shift(UP * 2.45)
        message = Text("AMBIGUOUS MESSAGE  m", font_size=29, weight=BOLD, color=WHITE).move_to(message_box)
        act_box = self.box(4.0, 1.75, RED).shift(LEFT * 3.8 + DOWN * 0.5)
        act = VGroup(Text("ACT NOW", font_size=30, weight=BOLD, color=RED), MathTex(r"\text{risk }R(m)", font_size=38, color=WHITE)).arrange(DOWN).move_to(act_box)
        ask_box = self.box(4.0, 1.75, GREEN).shift(RIGHT * 3.8 + DOWN * 0.5)
        ask = VGroup(Text("ASK  Q", font_size=30, weight=BOLD, color=GREEN), MathTex(r"c(Q)+\text{post-query risk}", font_size=31, color=WHITE)).arrange(DOWN).move_to(ask_box)
        paths = VGroup(Arrow(message_box.get_bottom(), act_box.get_top(), color=RED, buff=0.25), Arrow(message_box.get_bottom(), ask_box.get_top(), color=GREEN, buff=0.25))
        self.play_for(FadeIn(message_box), FadeIn(message), run_time=0.7)
        self.play_for(Create(paths), FadeIn(act_box), FadeIn(act), FadeIn(ask_box), FadeIn(ask), run_time=1.2)
        voi = MathTex(r"\operatorname{VOI}(Q\mid m)=R(m)-R(m;Q)", font_size=52, color=WHITE).shift(DOWN * 2.25)
        rule = MathTex(r"\text{ASK iff }\operatorname{VOI}(Q\mid m)>c(Q)", font_size=47, color=GREEN).next_to(voi, DOWN, buff=0.35)
        self.play_for(Write(voi), run_time=0.9)
        self.play_for(Write(rule), run_time=0.9)
        self.wait_to(end - 0.4)
        self.clear_to(end)

    # ---------- scene 10 ----------
    def scene_close(self, i: int) -> None:
        end = TIMING[i]["end"]
        line1 = Text("SPECIFY THE INVARIANTS,", font_size=63, weight=BOLD, font="DejaVu Serif", color=WHITE).shift(UP * 1.8)
        line2 = Text("NOT THE UNIVERSE.", font_size=70, weight=BOLD, font="DejaVu Serif", color=ORANGE).next_to(line1, DOWN, buff=0.15)
        objective = MathTex(
            r"\min\ \mathbb E[d]+\lambda\mathbb E[C_H]\quad\text{s.t. task-sufficient information}",
            font_size=43,
            color=WHITE,
        ).shift(DOWN * 0.45)
        footer = VGroup(
            Text("TASK-OPTIMAL PIDGIN", font_size=34, weight=BOLD, color=BLUE),
            Text("Draft preprint • SPEAR/0.1", font_size=22, color=MUTED),
        ).arrange(DOWN, buff=0.15).shift(DOWN * 2.45)
        self.play_for(FadeIn(line1, shift=UP * 0.2), FadeIn(line2, shift=UP * 0.2), run_time=0.9)
        self.play_for(Write(objective), FadeIn(footer), run_time=0.9)
        self.wait_to(end)

from manim import *

class DispersionDemo(Scene):
    def construct(self):
        # Axes for time vs frequency
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[400, 1600, 200],
            x_length=10,
            y_length=5,
            axis_config={"include_tip": False},
        ).add_coordinates()
        axes_labels = axes.get_axis_labels(x_label="Time", y_label="Freq (MHz)")

        self.play(Create(axes), Write(axes_labels))

        # Simulated pulses at 3 freqs: 400, 800, 1400 MHz
        times = [6, 4, 2]  # Dispersion delays: low freq arrives late
        freqs = [400, 800, 1400]
        colors = [BLUE, GREEN, RED]
        dots = VGroup()
        for t, f, c in zip(times, freqs, colors):
            dot = Dot(axes.c2p(t, f), color=c).scale(1.2)
            dots.add(dot)
        self.play(*[FadeIn(dot) for dot in dots])
        self.wait(1)

        # Label the dots
        labels = VGroup()
        for dot, f in zip(dots, freqs):
            label = Text(f"{f} MHz", font_size=24).next_to(dot, RIGHT)
            labels.add(label)
        self.play(*[Write(label) for label in labels])
        self.wait(1)

        # Arrows showing dedispersion
        dedispersed_time = 2  # align all at t=2
        arrows = VGroup()
        for dot in dots:
            start = dot.get_center()
            end = axes.c2p(dedispersed_time, axes.p2c(start)[1])
            arrow = Arrow(start, end, buff=0.1, color=YELLOW)
            arrows.add(arrow)
        self.play(*[GrowArrow(a) for a in arrows])
        self.wait(0.5)

        # Move the dots to aligned time
        self.play(*[dot.animate.move_to(arrow.get_end()) for dot, arrow in zip(dots, arrows)])
        self.wait(1)

        # Done
        self.play(FadeOut(VGroup(*self.mobjects)))

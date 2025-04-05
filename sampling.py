from manim import *
import numpy as np

class SamplingTheorem(Scene):
    def construct(self):
        # Define time axis
        time_axis = NumberLine(x_range=[-4, 4, 1], length=8, include_numbers=True)
        time_label = Text("Time (t)").next_to(time_axis, DOWN)

        # Define a generic continuous signal (modify as needed)
        def continuous_signal(x):
            return np.sin(2 * np.pi * x) * np.exp(-0.3 * abs(x))  # Example: Decaying sine wave
        
        continuous_graph = FunctionGraph(continuous_signal, x_range=[-4, 4], color=BLUE)
        continuous_label = Text("Continuous Signal").set_color(BLUE).to_edge(UP)

        # Sampled points (Nyquist rate)
        sample_rate = 2  # Modify for different sampling rates
        sample_points = np.arange(-4, 4, 1 / sample_rate)
        sampled_dots = VGroup(*[Dot(point=[x, continuous_signal(x), 0], color=RED) for x in sample_points])
        sampled_label = Text("Sampled Points").set_color(RED).next_to(continuous_label, DOWN)
        
        # Impulse train
        impulses = VGroup(*[Arrow(start=[x, 0, 0], end=[x, continuous_signal(x), 0], buff=0, color=YELLOW) for x in sample_points])
        impulse_label = Text("Impulse Train").set_color(YELLOW).next_to(sampled_label, DOWN)
        
        # Display elements
        self.play(Create(time_axis), Write(time_label))
        self.play(Create(continuous_graph), Write(continuous_label))
        self.wait(1)
        self.play(FadeIn(sampled_dots), Write(sampled_label))
        self.play(FadeIn(impulses), Write(impulse_label))
        self.wait(2)
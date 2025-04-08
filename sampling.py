from manim import *
import numpy as np
# to demonstrate sampling and unsmapling of a signal.
class SamplingTheorem(Scene):
# first start by adding a time axis and the signal to the scene.
    def construct(self):
        title = Tex(r"Sampling Theorem")
        basel =MathTex(r"f_s \geq 2f_{\text{max}}", r"\quad \Rightarrow \quad", r"\text{Perfect reconstruction}")
        VGroup(title, basel).arrange(DOWN)
        self.play(
            Write(title),
            FadeIn(basel, shift=DOWN),
        )
        self.wait()

        transform_title = Tex("Signal")
        grid1 = NumberPlane()
        # grid1_title= Tex("Signal")
        # grid1_title.move_to(transform_title)
        transform_title.to_corner(UP + LEFT)
        self.play(
            FadeOut(title),
            # FadeIn(grid1_title, shift=UP),
            Transform(title, transform_title),
            LaggedStart(*[FadeOut(obj, shift=DOWN) for obj in basel]),
            Create(grid1, run_time=3, lag_ratio=0.1),
        )
        self.wait()

        grid = NumberPlane()
        grid_title = Tex("Impluse train")
        grid_title.move_to(transform_title)

        self.add(grid, grid_title)  # Make sure title is on top of grid
        self.play(
            # FadeOut(title),
            FadeIn(grid_title, shift=UP),
            Create(grid, run_time=3, lag_ratio=0.1),
        )
        self.wait()



# class SamplingTheorem(Scene):
#     def construct(self):
#         # Define time axis
#         time_axis = NumberLine(x_range=[-4, 4, 1], length=8, include_numbers=True)
#         time_label = Text("Time (t)").next_to(time_axis, DOWN)

#         # Define a generic continuous signal (modify as needed)
#         def continuous_signal(x):
#             return np.sin(2 * np.pi * x) * np.exp(-0.3 * abs(x))  # Example: Decaying sine wave
        
#         continuous_graph = FunctionGraph(continuous_signal, x_range=[-4, 4], color=BLUE)
#         continuous_label = Text("Continuous Signal").set_color(BLUE).to_edge(UP)

#         # Sampled points (Nyquist rate)
#         sample_rate = 2  # Modify for different sampling rates
#         sample_points = np.arange(-4, 4, 1 / sample_rate)
#         sampled_dots = VGroup(*[Dot(point=[x, continuous_signal(x), 0], color=RED) for x in sample_points])
#         sampled_label = Text("Sampled Points").set_color(RED).next_to(continuous_label, DOWN)
        
#         # Impulse train
#         impulses = VGroup(*[Arrow(start=[x, 0, 0], end=[x, continuous_signal(x), 0], buff=0, color=YELLOW) for x in sample_points])
#         impulse_label = Text("Impulse Train").set_color(YELLOW).next_to(sampled_label, DOWN)
        
#         # Display elements
#         self.play(Create(time_axis), Write(time_label))
#         self.play(Create(continuous_graph), Write(continuous_label))
#         self.wait(1)
#         self.play(FadeIn(sampled_dots), Write(sampled_label))
#         self.play(FadeIn(impulses), Write(impulse_label))
#         self.wait(2)
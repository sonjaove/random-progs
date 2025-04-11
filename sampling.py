from manim import *
import numpy as np
import os 

os.environ["PATH"] = os.environ["PATH"] + r";C:\Users\YOURUSER\AppData\Local\Programs\MiKTeX\miktex\bin\x64\\"
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
        grid1 = NumberPlane(
            x_range=(-4, 11, 1),
            x_length=5,
            y_length=4,
        ).move_to(LEFT*3)

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

        grid = NumberPlane(
            x_range=(-4, 11, 1),
            x_length=5,
            y_length=4,
        ).move_to(RIGHT*3)
        grid_title = Tex("Impluse train")
        grid_title.move_to(transform_title)

        self.add(grid, grid_title)  # Make sure title is on top of grid
        self.play(
            # FadeOut(title),
            FadeIn(grid_title, shift=UP),
            Create(grid, run_time=3, lag_ratio=0.1),
        )
        self.wait()
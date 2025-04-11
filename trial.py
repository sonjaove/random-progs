from manim import *
from manim.utils.color import WHITE, RED    
from manim.utils.rate_functions import squish_rate_func, smooth, linear
from manim import interpolate
from  manim.animation.changing import TracedPath
import numpy as np
from scipy.optimize import leastsq
import math
# from manim.utils.math import ValueTracker
# from manim.utils.math import math
# from manim.utils.math import leastsq
# from manim.utils.math import interpolate
# from manim.utils.math import np

from manim import *

class Pendulum(VGroup):
    def __init__(self, length=3, initial_theta=PI / 6, top_point=ORIGIN, weight_diameter=0.3, gravity=9.8, damping=0, **kwargs):
        super().__init__(**kwargs)
        self.length = length
        self.theta = initial_theta
        self.omega = 0
        self.g = gravity
        self.damping = damping
        self.top_point = top_point

        # Visual components
        self.rod = Line(top_point, self.get_bob_point(), stroke_width=4)
        self.bob = Dot(self.rod.get_end(), radius=weight_diameter)
        self.add(self.rod, self.bob)

        self.add_updater(self.update_pendulum)

    def get_bob_point(self):
        x = self.length * np.sin(self.theta)
        y = -self.length * np.cos(self.theta)
        return self.top_point + np.array([x, y, 0])

    def update_pendulum(self, dt): 
        alpha = -self.g / self.length * np.sin(self.theta) - self.damping * self.omega
        self.omega += alpha * dt
        self.theta += self.omega * dt
        new_end = self.get_bob_point()
        self.rod.put_start_and_end_on(self.top_point, new_end)
        self.bob.move_to(new_end)

    def get_theta(self):
        return self.theta
    
    
class ThetaVsTAxes(Axes):
    def __init__(self, **kwargs):
        super().__init__(
            x_range=[0, 12, 1],
            y_range=[-1.5, 1.5, 0.5],
            x_length=6,
            y_length=3,
            axis_config={"include_tip": True, "numbers_to_include": [2, 4, 6, 8, 10]},
            **kwargs
        )
        self.x_axis.label = self.x_axis.get_axis_label("t")
        self.y_axis.label = self.y_axis.get_axis_label(r"\theta(t)")

    def get_live_drawn_graph(self, pendulum):
        time_tracker = ValueTracker(0)
        graph = VMobject(color=YELLOW)
        graph.set_points_as_corners([self.coords_to_point(0, pendulum.get_theta())])

        def update_graph(mob, dt):
            t = time_tracker.get_value()
            y = pendulum.get_theta()
            point = self.coords_to_point(t, y)
            mob.add_points_as_corners([point])
            time_tracker.increment_value(dt)

        graph.add_updater(update_graph)
        return graph

class Nyquist(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pendulum_config = {
            "initial_theta": 10 * DEGREES,
            "length": 5,
            "gravity": 49.348,
            "weight_diameter": 0.3,
            "damping": 0,
            "top_point": ORIGIN,
        }
        self.axes_config = {
            "y_axis_config": {"unit_size": 0.75},
            "x_axis_config": {
                "unit_size": 0.5,
                "numbers_to_show": range(2, 12, 2),
                "number_scale_val": 0.5,
            },
            "x_max": 12,
            "axis_config": {
                "tip_length": 0.3,
                "stroke_width": 2,
            }
        }
        self.axes_corner = UL

    def construct(self):
        #double frequency is 0.95 Hz
        self.sample(0.7)

    def sample(self, sf):
        l = 5
        g = 49.348
        first_zero = 1 / 2 * math.pi * math.sqrt(l / g)
        total_time = 12
        pendulum = Pendulum(**self.pendulum_config)
        pendulum.shift(2 * UP + 4 * RIGHT)
        axes = ThetaVsTAxes(**self.axes_config)
        axes.center()
        axes.to_corner(self.axes_corner, buff=LARGE_BUFF)
        axes.scale(1.5)
        axes.shift(DOWN + RIGHT)
        graph = axes.get_live_drawn_graph(pendulum)
        graph.scale(1.5)
        graph.shift(DOWN + RIGHT)

        times = np.arange(first_zero, total_time, 1/sf)

        time_tracker = ValueTracker(0)

        flash_rect = FullScreenRectangle(
            stroke_width=0,
            fill_color=WHITE,
            fill_opacity=0.2,
        )
        flash = FadeOut(
            flash_rect,
            rate_func=squish_rate_func(smooth, 0, 0.1)
        )

        self.add(pendulum)
        self.play(Create(axes))
        self.wait(2)
        dot = Dot(color=RED, radius=0.05)
        dot.move_to(graph.get_center())
        dot.shift(UP + LEFT)
        pendulum.start_swinging()
        self.wait(first_zero + 0.032)
        self.add(graph)
        dot_copies = VGroup()
        pendulum_copies = VGroup()
        thetas = np.array([])
        for t1, t2 in zip(times, times[1:]):
            dot_copy = dot.copy()
            dot_copy.clear_updaters()
            dot_copies.add(dot_copy)
            pendulum_copy = pendulum.copy()
            pendulum_copy.clear_updaters()
            pendulum_copy.set_opacity(0.2)
            pendulum_copies.add(pendulum_copy)
            thetas = np.append(thetas, pendulum.get_theta())

            self.add(dot_copy)
            self.add(pendulum_copy)

            # graph.save_state()
            kw = {
                "rate_func": lambda alpha: interpolate(
                    t1,
                    t2,
                    alpha
                )
            }
            anims = [
                # ShowCreation(graph, **kw),
                MoveAlongPath(dot, graph, **kw),
                ApplyMethod(
                    time_tracker.increment_value, 1/sf,
                    rate_func=linear
                ),
            ]
            anims.append(flash)
            self.play(*anims, run_time=1/sf)

        est_amp, est_freq, est_phase, est_mean = self.get_reconstruction(thetas[2:], times[2:-1])
        print(thetas[1:])
        print(times[1:-1])
        graph1 = axes.get_graph(lambda x: est_amp * np.sin(2 * math.PI * est_freq * (x - est_phase)) + est_mean, color=RED)
        print(est_amp, est_freq, est_phase, est_mean)

        self.wait(4)
        self.play(FadeOut(graph))
        self.wait(1)
        self.play(Create(graph1, run_time=5))
        self.wait(3)

    def get_reconstruction(self,thetas, times):
        optimize_func = lambda x: ((x[0] * np.sin(2 * math.pi * x[1] * (times - x[2])) + x[3]) - thetas)
        est_amp, est_freq, est_phase, est_mean = leastsq(optimize_func, [0.3, 0.2, 1, 0])[0]
        return est_amp, est_freq, est_phase, est_mean
        
class AnimatedBoundaryExample(Scene):
    def construct(self):
        text = Text("So shiny!")
        boundary = AnimatedBoundary(text, colors=[RED, GREEN, BLUE],
                                    cycle_rate=3)
        self.add(text, boundary)
        self.wait(2)
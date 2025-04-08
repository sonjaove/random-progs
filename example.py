from manim import *

class PointMovingWithTrace(Scene):
    def construct(self):
        circle = Circle(radius=1, color=BLUE)
        dot = Dot()
        trace = TracedPath(dot.get_center, stroke_color=YELLOW, stroke_width=2)

        self.add(trace, dot)

        dot2 = dot.copy().shift(RIGHT)

        self.play(GrowFromCenter(circle))
        self.play(Transform(dot, dot2))
        self.play(MoveAlongPath(dot, circle), run_time=2, rate_func=linear)
        self.play(Rotating(dot, about_point=[2, 0, 0]), run_time=2)
        self.wait()

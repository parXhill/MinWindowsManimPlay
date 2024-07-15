from manim import *

class MinWindowVisualization(Scene):
    def construct(self):
        # Create a string to visualize
        string = "ADOBECODEBANC"
        text_objects = VGroup(*[Text(char) for char in string])

        # Arrange the characters in a horizontal line
        text_objects.arrange(RIGHT, buff=0.1)

        # Slide the string onto the screen
        self.play(FadeIn(text_objects, shift=DOWN))
        
        # Wait for a moment
        self.wait(1)

        # Create a brace under the initial window
        brace = Brace(text_objects[:2], DOWN)
        brace_text = Text("Current Window").next_to(brace, DOWN)

        self.play(Create(brace), Write(brace_text))
        
        # Wait for a moment
        self.wait(1)

        # Create a red dot labeled 'L' at index 0
        red_dot = Dot(color=RED).next_to(text_objects[0], UP)
        l_label = Text("L", color=RED).next_to(red_dot, UP)

        self.play(FadeIn(red_dot), Write(l_label))

        # Create a blue dot labeled 'R' at index 1
        blue_dot = Dot(color=BLUE).next_to(text_objects[1], UP)
        r_label = Text("R", color=BLUE).next_to(blue_dot, UP)

        self.play(FadeIn(blue_dot), Write(r_label))
        
        # Wait for a moment
        self.wait(1)

        # Move the blue dot and expand the brace to simulate sliding window
        for i in range(2, len(string)):
            new_brace = Brace(text_objects[:i+1], DOWN)
            new_brace_text = Text("Current Window").next_to(new_brace, DOWN)
            new_blue_dot = Dot(color=BLUE).next_to(text_objects[i], UP)
            new_r_label = Text("R", color=BLUE).next_to(new_blue_dot, UP)

            self.play(Transform(brace, new_brace), Transform(brace_text, new_brace_text), Transform(blue_dot, new_blue_dot), Transform(r_label, new_r_label))
            self.wait(0.5)

        # End scene
        self.play(FadeOut(VGroup(brace, brace_text, red_dot, l_label, blue_dot, r_label, text_objects)))

# To run the animation, use the following command:
# manim -pql min_window_visualization.py MinWindowVisualization
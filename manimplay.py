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

        # Create a red dot labeled 'L' immediately before index 0
        red_dot = Dot(color=RED).next_to(text_objects[0], LEFT)
        l_label = Text("L", color=RED).next_to(red_dot, UP)

        self.play(FadeIn(red_dot), Write(l_label))

        # Create a blue dot labeled 'R' immediately before index 0
        blue_dot = Dot(color=BLUE).next_to(text_objects[0], UP)
        r_label = Text("R", color=BLUE).next_to(blue_dot, UP)

        self.play(FadeIn(blue_dot), Write(r_label))
        
        # Wait for a moment
        self.wait(1)

        # Create a box for "Current Letters"
        current_letters_box = Rectangle(width=4, height=3, color=WHITE).to_corner(UP+RIGHT)
        current_letters_title = Text("Current Letters").next_to(current_letters_box, UP)
        current_letters_text = Text("").move_to(current_letters_box.get_center())

        self.play(Create(current_letters_box), Write(current_letters_title), Write(current_letters_text))

        # Create a box for "Target Letters"
        target_letters_box = Rectangle(width=4, height=3, color=WHITE).to_corner(UP+LEFT)
        target_letters_title = Text("Target Letters").next_to(target_letters_box, UP)
        target_letters_text = VGroup(
            *[Text(char, color=WHITE) for char in "ANC"]
        ).arrange(RIGHT, buff=0.1).move_to(target_letters_box.get_center())

        self.play(Create(target_letters_box), Write(target_letters_title), Write(target_letters_text))

        current_letters = []
        brace = None
        brace_text = None

        # Move the blue dot and expand the brace to simulate sliding window
        for i in range(0, len(string)):
            new_blue_dot = Dot(color=BLUE).next_to(text_objects[i], UP)
            new_r_label = Text("R", color=BLUE).next_to(new_blue_dot, UP)

            current_letters.append(string[i])
            updated_letters_text = Text("".join(current_letters)).move_to(current_letters_box.get_center())

            # Turn target letters green if they appear in the current letters
            for j, target_letter in enumerate(target_letters_text):
                if target_letter.text in current_letters:
                    target_letter.set_color(GREEN)

            if i == 0:
                # Create and show the brace when R reaches the first index
                brace = Brace(text_objects[:i+1], DOWN)
                brace_text = Text("Current Window").next_to(brace, DOWN)
                self.play(Create(brace), Write(brace_text))

            if brace and brace_text:
                new_brace = Brace(text_objects[:i+1], DOWN)
                new_brace_text = Text("Current Window").next_to(new_brace, DOWN)

                self.play(
                    Transform(brace, new_brace), 
                    Transform(brace_text, new_brace_text)
                )

            self.play(
                Transform(blue_dot, new_blue_dot), 
                Transform(r_label, new_r_label),
                Transform(current_letters_text, updated_letters_text)
            )
            self.wait(0.5)

        # End scene
        self.play(FadeOut(VGroup(brace, brace_text, red_dot, l_label, blue_dot, r_label, text_objects, current_letters_box, current_letters_title, current_letters_text, target_letters_box, target_letters_title, target_letters_text)))

# To run the animation, use the following command:
# manim -pql min_window_visualization.py MinWindowVisualization
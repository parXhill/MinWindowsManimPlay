from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.azure import AzureService

class MinWindowVisualization(VoiceoverScene):
    def construct(self):

        Text.set_default(font="Courier New")

        self.set_speech_service(
            AzureService(
                voice="en-US-BrianNeural"
            )
        )

        silencer = Circle().scale(0)

        # Create a string to visualize
        string = "ACACCDCBECCDEBACCA"
        text_objects = VGroup(*[Text(char) for char in string])

        # Arrange the characters in a horizontal line
        text_objects.arrange(RIGHT, buff=0.1)
        text_objects.shift(DOWN * 2)

        # Slide the string onto the screen
        with self.voiceover(text="Our goal is to find the minimum window within which our string contains all the target letters.") as tracker:
            self.play(FadeIn(text_objects, shift=RIGHT*3),run_time=tracker.duration)
        
        # Wait for a moment
        self.wait(1)

        # Create a red dot labeled 'L' immediately before index 0
        red_dot = Dot(color=RED).next_to(text_objects[0], LEFT)
        l_label = Text("L", color=RED).next_to(red_dot, UP)

        with self.voiceover(text="We start by setting a left pointer that tracks the index of the start of the window") as tracker:
            self.play(FadeIn(red_dot), Write(l_label),run_time=tracker.duration)

        # Create a blue dot labeled 'R' immediately before index 0
        blue_dot = Dot(color=BLUE).next_to(text_objects[0], UP)
        r_label = Text("R", color=BLUE).next_to(blue_dot, UP)

        with self.voiceover(text="And a right pointer that tracks the index of the end of the window") as tracker:
            self.play(FadeIn(blue_dot), Write(r_label), run_time=tracker.duration)
        
        # Wait for a moment
        self.wait(1)

        # Create a box for "Current Letters"
        current_letters_box = Rectangle(width=4, height=3, color=WHITE).to_corner(UP+RIGHT)
        current_letters_box.shift(DOWN*0.8)
        current_letters_title = Text("Current Letters").next_to(current_letters_box, UP).scale(0.7)
        current_letters_text = VGroup().move_to(current_letters_box.get_center())

        # Create a box for "Target Letters"
        target_letters_box = Rectangle(width=4, height=3, color=WHITE).to_corner(UP+LEFT)
        target_letters_box.shift(DOWN*0.8)
        target_letters_title = Text("Target Letters").next_to(target_letters_box, UP).scale(0.7)
        
        target_letter_counts = {'D': 1, 'E': 1, 'A': 1}
        target_letters_text = VGroup(
            *[Text(f"{key}: {value}", color=WHITE) for key, value in target_letter_counts.items()]
        ).arrange(DOWN, buff=0.1).move_to(target_letters_box.get_center())

        with self.voiceover(text="Now, we create a hashmap of the letters and value counts that are present in our target string") as tracker:
            self.play(Create(target_letters_box), Write(target_letters_title), Write(target_letters_text),run_time=tracker.duration)

        with self.voiceover(text="And a hashmap that will track the characters that appear in our current window") as tracker:
            self.play(Create(current_letters_box), Write(current_letters_title), Write(current_letters_text),run_time=tracker.duration)

        current_letter_counts = {}
        brace = None
        brace_text = None

        self.wait(2)

        with self.voiceover(text="For our window to be complete, it must contain all the values of the target string.") as tracker:
            self.play(Create(silencer))

        # Move the blue dot and expand the brace to simulate sliding window
        for i in range(0, 9):

            new_blue_dot = Dot(color=BLUE).next_to(text_objects[i], UP)
            new_r_label = Text("R", color=BLUE).next_to(new_blue_dot, UP)

            char = string[i]
            if char in current_letter_counts:
                current_letter_counts[char] += 1
            else:
                current_letter_counts[char] = 1

            updated_letters_text = VGroup(
                *[Text(f"{key}: {value}") for key, value in current_letter_counts.items()]
            ).arrange(DOWN, buff=0.1).move_to(current_letters_box.get_center())

            if i == 0:
                # Create and show the brace when R reaches the first index
                brace = Brace(text_objects[:i+1], DOWN)
                brace_text = Text("Current Window").scale(0.7).next_to(brace, DOWN)

                with self.voiceover(text="We start by expanding our window to the right until it contains all the target characters.") as tracker:
                    self.play(Create(brace), Write(brace_text))


            if brace and brace_text:
                new_brace = Brace(text_objects[:i+1], DOWN)
                new_brace_text = Text("Current Window").scale(0.7).next_to(new_brace, DOWN)

                self.play(
                    Transform(brace, new_brace), 
                    Transform(brace_text, new_brace_text),
                    Transform(blue_dot, new_blue_dot), 
                    Transform(r_label, new_r_label),
                    Transform(current_letters_text, updated_letters_text)
                )
            
            # Turn target letters green if they appear in the current letters
            for target_letter in target_letters_text:
                if target_letter.text[0] in current_letter_counts and current_letter_counts[target_letter.text[0]] >= target_letter_counts[target_letter.text[0]]:
                    target_letter.set_color(GREEN)
                if target_letter.text[0] in current_letter_counts:
                    index = [text.text.split(":")[0] for text in updated_letters_text].index(target_letter.text[0])
                    updated_letters_text[index].set_color(GREEN)
                


            else:
                self.play(
                    Transform(blue_dot, new_blue_dot),
                    Transform(r_label, new_r_label)
                )
            
            if all(target_letter.get_color() == GREEN for target_letter in target_letters_text):
                target_letters_box.set_color(GREEN)
                
            else:
                target_letters_box.set_color(WHITE)

            self.wait(0.5)

        self.play(text_objects[0:9].animate.set_color(GREEN),run_time=0.5) #flash?

        with self.voiceover(text="When our window contains all the target characters, we have met the requirements for our first minimum substring. We stop expanding, and record the sequence.") as tracker:
            self.play(Create(silencer))

        # Create a box for "Minimum String"
        minimum_string_box = Rectangle(width=4, height=3, color=WHITE).next_to(target_letters_box, RIGHT, buff=0.6)
        minimum_string_title = Text("Minimum String").next_to(minimum_string_box, UP).scale(0.7)

        self.play(Create(minimum_string_box), Write(minimum_string_title))
       
        copied_text = text_objects[0:9].copy()
        self.play(copied_text.animate.move_to(minimum_string_box.get_center()))
        self.play(text_objects[0:9].animate.set_color(WHITE),run_time=0.5)

        
        with self.voiceover(text="Then, to see whether we can make it any smaller, we begin to contract our window from the left, removing characters one by one to find the smallest viable substring.") as tracker:
            self.play(Create(silencer))

        # Narrow the window brace one index at a time until it reaches the second A in the string
        for i in range(0, 4):

            if i in [2, 3]:
                #self.play(FadeOut(minimum_string_text))
                self.play(text_objects[i-1:9].animate.set_color(GREEN),run_time=0.5) #flash?
                self.play(FadeOut(copied_text))
                copied_text = text_objects[i-1:9].copy()
                self.play(copied_text.animate.move_to(minimum_string_box.get_center()))
                self.play(text_objects[i-1:9].animate.set_color(WHITE),run_time=0.5)
                #new_current_window_string = ''.join(string[2:9])
                #new_minimum_string_text = Text(new_current_window_string).move_to(minimum_string_box.get_center())
                #new_minimum_string_text.set_color(GREEN)
                #self.play(Transform(minimum_string_text, new_minimum_string_text))
                self.wait(1)

            new_red_dot = Dot(color=RED).next_to(text_objects[i], UP)
            new_l_label = Text("L", color=RED).next_to(new_red_dot, UP)

            new_brace = Brace(text_objects[i:9], DOWN)
            new_brace_text = Text("Current Window").scale(0.7).next_to(new_brace, DOWN)

            # Update current letters hashmap

            if i == 0:
                pass

            else:
                char_to_remove = string[i-1]
                if char_to_remove in current_letter_counts:
                    current_letter_counts[char_to_remove] -= 1
                    if current_letter_counts[char_to_remove] == 0:
                        del current_letter_counts[char_to_remove]

            for target_letter in target_letters_text:
                if target_letter.text[0] not in current_letter_counts or current_letter_counts[target_letter.text[0]] < target_letter_counts[target_letter.text[0]]:
                    target_letter.set_color(WHITE)

            updated_letters_text = VGroup(
                *[Text(f"{key}: {value}") for key, value in current_letter_counts.items()]
            ).arrange(DOWN, buff=0.1).move_to(current_letters_box.get_center())

            if all(target_letter.get_color() == GREEN for target_letter in target_letters_text):
                target_letters_box.set_color(GREEN)
                
            else:
                target_letters_box.set_color(WHITE)
            

            self.play(
                Transform(red_dot, new_red_dot),
                Transform(l_label, new_l_label),
                Transform(brace, new_brace),
                Transform(brace_text, new_brace_text),
                Transform(current_letters_text, updated_letters_text)
            )
            
            self.wait(0.5)

            if i == 3:
                with self.voiceover(text="Once our window no longer contains all the target letters, we have found the smallest viable sub-string so far. And so, we begin to expand again towards the right to find the next viable window.") as tracker:
                    self.play(Create(silencer))
                
        for i in range(9, 15):


            new_blue_dot = Dot(color=BLUE).next_to(text_objects[i], UP)
            new_r_label = Text("R", color=BLUE).next_to(new_blue_dot, UP)
            new_red_dot = Dot(color=RED).next_to(text_objects[3], UP)
            new_l_label = Text("L", color=RED).next_to(new_red_dot, UP)

            char = string[i]
            if char in current_letter_counts:
                current_letter_counts[char] += 1
            else:
                current_letter_counts[char] = 1

            updated_letters_text = VGroup(
                *[Text(f"{key}: {value}") for key, value in current_letter_counts.items()]
            ).arrange(DOWN, buff=0.1).move_to(current_letters_box.get_center())

            #if i == 0:
                # Create and show the brace when R reaches the first index
                #brace = Brace(text_objects[:i+1], DOWN)
                #brace_text = Text("Current Window").scale(0.7).next_to(brace, DOWN)
                #self.play(Create(brace), Write(brace_text))

            if brace and brace_text:
                new_brace = Brace(text_objects[3:i+1], DOWN)
                new_brace_text = Text("Current Window").scale(0.7).next_to(new_brace, DOWN)

                self.play(
                    Transform(brace, new_brace), 
                    Transform(brace_text, new_brace_text),
                    Transform(blue_dot, new_blue_dot), 
                    Transform(r_label, new_r_label),
                    Transform(red_dot, new_red_dot),
                    Transform(l_label, new_l_label),
                    Transform(current_letters_text, updated_letters_text)
                )
            
            # Turn target letters green if they appear in the current letters
            for target_letter in target_letters_text:
                if target_letter.text[0] in current_letter_counts and current_letter_counts[target_letter.text[0]] >= target_letter_counts[target_letter.text[0]]:
                    target_letter.set_color(GREEN)
                if target_letter.text[0] in current_letter_counts:
                    index = [text.text.split(":")[0] for text in updated_letters_text].index(target_letter.text[0])
                    updated_letters_text[index].set_color(GREEN)
                if target_letter.text[0] not in current_letter_counts or current_letter_counts[target_letter.text[0]] < target_letter_counts[target_letter.text[0]]:
                    target_letter.set_color(WHITE)

            #else:
                #self.play(
                    #Transform(blue_dot, new_blue_dot),
                    #Transform(r_label, new_r_label))
                
            

            if all(target_letter.get_color() == GREEN for target_letter in target_letters_text):
                target_letters_box.set_color(GREEN)
                
            else:
                target_letters_box.set_color(WHITE)

            self.wait(0.5)

            if i == 14:
                with self.voiceover(text="Once we have found another viable window, we stop expanding. If the string is smaller than the minimum, we record it. Otherwise, we begin to contract the window from the left again, to see if we can find a viable string that is smaller than the minimum.") as tracker:
                    self.play(Create(silencer))

         # Narrow the window brace one index at a time until it reaches the second A in the string
        for i in range(4, 13):

            if i in [10, 11, 12]:
                self.play(text_objects[i-1:15].animate.set_color(GREEN),run_time=0.5) #flash?
                self.play(FadeOut(copied_text))
                copied_text = text_objects[i-1:15].copy()
                self.play(copied_text.animate.move_to(minimum_string_box.get_center()))
                self.play(text_objects[i-1:15].animate.set_color(WHITE),run_time=0.5)
                self.wait(3)

            new_red_dot = Dot(color=RED).next_to(text_objects[i], UP)
            new_l_label = Text("L", color=RED).next_to(new_red_dot, UP)

            new_brace = Brace(text_objects[i:15], DOWN)
            new_brace_text = Text("Current Window").scale(0.7).next_to(new_brace, DOWN)
            
            # Update current letters hashmap
            char_to_remove = string[i-1]
            if char_to_remove in current_letter_counts:
                current_letter_counts[char_to_remove] -= 1
                if current_letter_counts[char_to_remove] == 0:
                    del current_letter_counts[char_to_remove]

            updated_letters_text = VGroup(
                *[Text(f"{key}: {value}") for key, value in current_letter_counts.items()]
            ).arrange(DOWN, buff=0.1).move_to(current_letters_box.get_center())

            for target_letter in target_letters_text:
                if target_letter.text[0] in current_letter_counts and current_letter_counts[target_letter.text[0]] >= target_letter_counts[target_letter.text[0]]:
                    target_letter.set_color(GREEN)
                if target_letter.text[0] in current_letter_counts:
                    index = [text.text.split(":")[0] for text in updated_letters_text].index(target_letter.text[0])
                    #updated_letters_text[index].set_color(GREEN)
                if target_letter.text[0] not in current_letter_counts or current_letter_counts[target_letter.text[0]] < target_letter_counts[target_letter.text[0]]:
                    target_letter.set_color(WHITE)


            if all(target_letter.get_color() == GREEN for target_letter in target_letters_text):
                target_letters_box.set_color(GREEN)
                
            else:
                target_letters_box.set_color(WHITE)

            self.play(
                Transform(red_dot, new_red_dot),
                Transform(l_label, new_l_label),
                Transform(brace, new_brace),
                Transform(brace_text, new_brace_text),
                Transform(current_letters_text, updated_letters_text)
            )
            self.wait(1)
        
        for i in range(14, 18):
            new_blue_dot = Dot(color=BLUE).next_to(text_objects[i], UP)
            new_r_label = Text("R", color=BLUE).next_to(new_blue_dot, UP)
            new_red_dot = Dot(color=RED).next_to(text_objects[12], UP)
            new_l_label = Text("L", color=RED).next_to(new_red_dot, UP)

            char = string[i]
            if char in current_letter_counts:
                current_letter_counts[char] += 1
            else:
                current_letter_counts[char] = 1

            updated_letters_text = VGroup(
                *[Text(f"{key}: {value}") for key, value in current_letter_counts.items()]
            ).arrange(DOWN, buff=0.1).move_to(current_letters_box.get_center())

            if i == 0:
                # Create and show the brace when R reaches the first index
                brace = Brace(text_objects[:i+1], DOWN)
                brace_text = Text("Current Window").scale(0.7).next_to(brace, DOWN)
                self.play(Create(brace), Write(brace_text))

            if brace and brace_text:
                new_brace = Brace(text_objects[12:i+1], DOWN)
                new_brace_text = Text("Current Window").scale(0.7).next_to(new_brace, DOWN)

                self.play(
                    Transform(brace, new_brace), 
                    Transform(brace_text, new_brace_text),
                    Transform(blue_dot, new_blue_dot), 
                    Transform(r_label, new_r_label),
                    Transform(red_dot, new_red_dot),
                    Transform(l_label, new_l_label),
                    Transform(current_letters_text, updated_letters_text)
                )
            
            
            else:
                self.play(
                    Transform(blue_dot, new_blue_dot),
                    Transform(r_label, new_r_label)
                )
            
            for target_letter in target_letters_text:
                if target_letter.text[0] in current_letter_counts and current_letter_counts[target_letter.text[0]] >= target_letter_counts[target_letter.text[0]]:
                    target_letter.set_color(GREEN)
                if target_letter.text[0] in current_letter_counts:
                    index = [text.text.split(":")[0] for text in updated_letters_text].index(target_letter.text[0])
                    #updated_letters_text[index].set_color(GREEN)
                if target_letter.text[0] not in current_letter_counts or current_letter_counts[target_letter.text[0]] < target_letter_counts[target_letter.text[0]]:
                    target_letter.set_color(WHITE)


            if all(target_letter.get_color() == GREEN for target_letter in target_letters_text):
                target_letters_box.set_color(GREEN)
                
            else:
                target_letters_box.set_color(WHITE)

            self.wait(0.5)

        # End scene
        self.play(FadeOut(VGroup(brace, brace_text, red_dot, l_label, blue_dot, r_label, text_objects, current_letters_box, current_letters_title, current_letters_text, target_letters_box, target_letters_title, target_letters_text, minimum_string_box, minimum_string_title, copied_text)))

# To run the animation, use the following command:
# manim -pql min_window_visualization.py MinWindowVisualization
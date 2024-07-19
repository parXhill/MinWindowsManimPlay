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
        intro_circle = Circle().set_color(RED)
        intro_square = Square().set_color(ORANGE)

        self.play(FadeIn(intro_circle))

        with self.voiceover(text="Welcome") as tracker:
            self.play(Transform(intro_circle, intro_square), run_time=tracker.duration)

        self.play(FadeOut(intro_circle))

        # Create a string to visualize
        t_string = "DEA"
        string = "ACACCDCBECCDEBACCA"
        t_object = VGroup(*[Text(char) for char in t_string])
        text_objects = VGroup(*[Text(char) for char in string])

        # Arrange the characters in a horizontal line
        text_objects.arrange(RIGHT, buff=0.1)
        text_objects.shift(DOWN * 2)

        t_object.arrange(RIGHT, buff=0.1)

        
        self.play(FadeIn(text_objects, shift=RIGHT*3))
        self.play(FadeIn(t_object, shift=LEFT*3))
        

        with self.voiceover(text="For this coding challenge, we are given two strings.") as tracker:
            self.play(Create(silencer))

        with self.voiceover(text="-a main string-") as tracker:
            self.play(text_objects.animate.set_color(RED))
            self.play(text_objects.animate.set_color(WHITE))

        with self.voiceover(text="-and a target string.") as tracker:
            self.play(t_object.animate.set_color(YELLOW))
            self.play(t_object.animate.set_color(WHITE))

        # Slide the string onto the screen
        with self.voiceover(text="Our goal is to find the smallest section of the main string that contains all the characters in the target string.") as tracker:
            self.play(Create(silencer), run_time=tracker.duration)
        
        self.play(text_objects[11:15].animate.set_color(YELLOW),run_time=2) 
        self.play(text_objects[11:15].animate.set_color(WHITE),run_time=0.5) 

        self.play(FadeOut(t_object))

        with self.voiceover(text="To do this, we will code a sliding window that dynamically adjusts its boundaries, while using a hashmap to keep track of the elements within the window") as tracker:
            self.play(Create(silencer))

        # Wait for a moment
        self.wait(1)

        # Create a red dot labeled 'L' immediately before index 0
        red_dot = Dot(color=RED).next_to(text_objects[0], LEFT)
        l_label = Text("L", color=RED).next_to(red_dot, UP)

        with self.voiceover(text="We start by setting a left pointer that tracks the start of our window") as tracker:
            self.play(FadeIn(red_dot), Write(l_label),run_time=tracker.duration)

        # Create a blue dot labeled 'R' immediately before index 0
        blue_dot = Dot(color=BLUE).next_to(text_objects[0], UP)
        r_label = Text("R", color=BLUE).next_to(blue_dot, UP)

        with self.voiceover(text="And a right pointer that tracks the end") as tracker:
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

        with self.voiceover(text="For any window to be viable as a sub-string, it must contain all the characters of the target string.") as tracker:
            self.play(Create(silencer))

        with self.voiceover(text="So, we create a hashmap to store the counts of the characters in our target string") as tracker:
            self.play(Create(target_letters_box), Write(target_letters_title), Write(target_letters_text),run_time=tracker.duration)

        self.wait(2)

        with self.voiceover(text="And a hashmap to store the counts of the characters in our window") as tracker:
            self.play(Create(current_letters_box), Write(current_letters_title), Write(current_letters_text),run_time=tracker.duration)

        current_letter_counts = {}
        brace = None
        brace_text = None

        self.wait(1)

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
                target_letters_box.set_fill(color=GREEN, opacity=0.3)
                
                
            else:
                target_letters_box.set_color(WHITE)
                target_letters_box.set_fill(color=BLACK)
                


        self.play(text_objects[0:9].animate.set_color(GREEN),run_time=0.5) #flash?


        with self.voiceover(text="Once our window contains all the target characters, it becomes a viable substring. So, we stop expanding, and record it as the minimum sub-string we have found.") as tracker:
            self.play(Create(silencer))

        # Create a box for "Minimum String"
        minimum_string_box = Rectangle(width=4, height=3, color=WHITE).next_to(target_letters_box, RIGHT, buff=0.6)
        minimum_string_title = Text("Minimum Substring").next_to(minimum_string_box, UP).scale(0.7)

        self.play(Create(minimum_string_box), Write(minimum_string_title))
       
        copied_text = text_objects[0:9].copy()
        self.play(copied_text.animate.move_to(minimum_string_box.get_center()))
        #self.play(text_objects[0:9].animate.set_color(WHITE),run_time=0.5)

        
        with self.voiceover(text="Then, to see whether we can make it any smaller, we begin to shorten the window from the left, removing characters one by one.") as tracker:
            self.play(Create(silencer))

        # Narrow the window brace one index at a time until it reaches the second A in the string
        for i in range(0, 4):
            

            if i in [2, 3]:
                #self.play(FadeOut(minimum_string_text))
                self.play(text_objects[i-1:9].animate.set_color(YELLOW),run_time=0.5) #flash?
                self.play(text_objects[i-1:9].animate.set_color(GREEN),run_time=0.5)
                self.play(FadeOut(copied_text))
                copied_text = text_objects[i-1:9].copy()
                self.play(copied_text.animate.move_to(minimum_string_box.get_center()))
                

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

            
            

            self.play(
                Transform(red_dot, new_red_dot),
                Transform(l_label, new_l_label),
                Transform(brace, new_brace),
                Transform(brace_text, new_brace_text),
                Transform(current_letters_text, updated_letters_text)
            )
            if all(target_letter.get_color() == GREEN for target_letter in target_letters_text):
                target_letters_box.set_fill(color=GREEN)
                
            else:
                target_letters_box.set_color(WHITE)
                target_letters_box.set_fill(color=BLACK)

            # Change the color of the window string to green if all items are found, make everything else white
            text_objects.set_color(WHITE)
            if all(target_letter.get_color() == GREEN for target_letter in target_letters_text):
                text_objects[i:9].set_color(GREEN)
            

            if i == 1: 
                self.wait(1)
                with self.voiceover(text="After each contraction, we check to see if the window is still viable, and if it's the smallest window so far.") as tracker:
                    self.play(Create(silencer))

            if i == 3:
                with self.voiceover(text="Once our window no longer contains all the target letters, it is no longer viable, and we stop contracting. Then, we begin to expand again towards the right to find the next viable window.") as tracker:
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

                
            

            if all(target_letter.get_color() == GREEN for target_letter in target_letters_text):
                target_letters_box.set_fill(color=GREEN, opacity=0.3)
                
            else:
                target_letters_box.set_color(WHITE)
                target_letters_box.set_fill(color=BLACK)


            if i == 14:
                text_objects[3:15].set_color(GREEN)
                with self.voiceover(text="Once the window becomes viable again, we stop expanding. We check the string to see if it's smaller than the minimum. Then, we begin to shorten the window from the left again.") as tracker:
                    self.play(Create(silencer))

         # Narrow the window brace one index at a time until it reaches the second A in the string
        for i in range(4, 13):


            if i == 5:
                with self.voiceover(text="Once again, at every round, we check to see whether our window is the smallest found so far.") as tracker:
                    self.play(Create(silencer))

            if i == 10:
                with self.voiceover(text="And record it if it is.") as tracker:
                    self.play(Create(silencer))


            if i in [10, 11, 12]:
                self.play(text_objects[i-1:15].animate.set_color(YELLOW),run_time=0.5) #flash?
                self.play(text_objects[i-1:15].animate.set_color(GREEN),run_time=0.5) #flash
                self.play(FadeOut(copied_text))
                copied_text = text_objects[i-1:15].copy()
                self.play(copied_text.animate.move_to(minimum_string_box.get_center()))
                self.wait(1)

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


            

            self.play(
                Transform(red_dot, new_red_dot),
                Transform(l_label, new_l_label),
                Transform(brace, new_brace),
                Transform(brace_text, new_brace_text),
                Transform(current_letters_text, updated_letters_text)
            )
            if all(target_letter.get_color() == GREEN for target_letter in target_letters_text):
                target_letters_box.set_fill(color=GREEN)
                
            else:
                target_letters_box.set_color(WHITE)
                target_letters_box.set_fill(color=BLACK)

            text_objects.set_color(WHITE)
            if all(target_letter.get_color() == GREEN for target_letter in target_letters_text):
                text_objects[i:15].set_color(GREEN)
        
        for i in range(14, 18):

            if i == 14:
                with self.voiceover(text="And once our window is again no longer viable, we stop contracting and expand to the right once more") as tracker:
                    self.play(Create(silencer))

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
                target_letters_box.set_fill(color=GREEN, opacity=0.3)
                
            else:
                target_letters_box.set_color(WHITE)
                target_letters_box.set_fill(color=BLACK)


        with self.voiceover(text="Finally, we reach the end of the string. Since our final window is non-viable-") as tracker:
            self.play(Create(silencer))

        self.wait(2)
        # End scene
       
        with self.voiceover(text="-we return the value of our smallest substring and end the program.") as tracker:
            self.play(copied_text.animate.scale(2))
        
        self.play(FadeOut(VGroup(brace, brace_text, red_dot, l_label, blue_dot, r_label, text_objects, current_letters_box, current_letters_title, current_letters_text, target_letters_box, target_letters_title, target_letters_text, minimum_string_box, minimum_string_title)))
        
        self.play(FadeOut(copied_text))
        
        with self.voiceover(text="If you'd like to see how these steps are coded, please continue to watch") as tracker:

            self.play(Create(silencer))


# To run the animation, use the following command:
# manim -pql min_window_visualization.py MinWindowVisualization
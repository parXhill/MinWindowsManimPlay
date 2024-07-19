from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.azure import AzureService

class MinWindowVisualization(VoiceoverScene):
    def construct(self):

        current_letters_box = Rectangle(width=4, height=3, color=WHITE).to_corner(UP+RIGHT)
        current_letters_box.shift(DOWN*0.8)
        current_letters_text = VGroup(Text("TEXT IN HERE").set_color(GREEN)).move_to(current_letters_box.get_center())

        self.play(FadeIn(current_letters_box, current_letters_text))

        self.wait(1)

        current_letters_box.set_fill(color=GREEN, opacity=0.3)

        self.wait(1)

        self.play(FadeOut(current_letters_box, current_letters_text))
# Screen that plays a video
from kivy.uix.screenmanager import Screen
from kivy.uix.video import Video
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.utils import platform
import os

class VideoScreen(Screen):
    def __init__(self, **kwargs):
        super(VideoScreen, self).__init__(**kwargs)

        # Set the background color
        with self.canvas.before:
            Color(rgba=(176/255, 198/255, 206/255, 1))  # Convert HEX B0C6CE to RGBA
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # Main layout
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=[50, 50], size_hint=(1, 1))

        # Logo
        self.layout.add_widget(Image(source='assets/logo.png', size_hint=(1, 0.3)))

        # Title
        self.layout.add_widget(Label(text='Video Player', font_size=50, size_hint=(1, 0.1)))

        # Video player
        self.video = Video(source='assets/video.mp4', state='play', options={'allow_stretch': True})
        self.layout.add_widget(self.video)

        # Controls
        self.controls = GridLayout(cols=3, spacing=10, size_hint=(1, 0.1))
        self.play_button = Button(text='Play', font_size=40)
        self.play_button.bind(on_press=self.play)
        self.controls.add_widget(self.play_button)

        self.pause_button = Button(text='Pause', font_size=40)
        self.pause_button.bind(on_press=self.pause)
        self.controls.add_widget(self.pause_button)

        self.stop_button = Button(text='Stop', font_size=40)
        self.stop_button.bind(on_press=self.stop)
        self.controls.add_widget(self.stop_button)

        self.layout.add_widget(self.controls)

        # Add layout to the screen
        self.add_widget(self.layout)

    def play(self, instance):
        self.video.state = 'play'

    def pause(self, instance):
        self.video.state = 'pause'

    def stop(self, instance):
        self.video.state = 'stop'

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

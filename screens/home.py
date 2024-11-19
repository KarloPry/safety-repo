from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
from db import DbConnection as db

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)

        # Set the background color
        with self.canvas.before:
            Color(rgba=(176/255, 198/255, 206/255, 1))  # Convert HEX B0C6CE to RGBA
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # Main layout
        self.layout = GridLayout(cols=1, spacing=10, padding=[0, 10], size_hint=(1, 1), pos_hint={'center_x': 0.5, 'center_y': 0.5})

        # Navbar on top that contains the logo and the logout button on top
        self.navbar = GridLayout(cols=2, size_hint=(1, 0.1))
        self.navbar.add_widget(Image(source='assets/logo.png', size_hint=(0.2, 1)))
        self.layout.add_widget(self.navbar)

        # Title
        self.layout.add_widget(Label(text='Iniciar Sesión', font_size=50, size_hint=(1, 0.1)))

        # Form fields
        self.username_input = TextInput(hint_text='ESTA ES LA 2DA', size_hint=(1, 0.1))
        self.password_input = TextInput(hint_text='Contraseña', password=True, size_hint=(1, 0.1))
        self.layout.add_widget(self.username_input)
        self.layout.add_widget(self.password_input)

        # Add layout to the screen
        self.add_widget(self.layout)

    def logout(self, instance):
        print("Logging out")
        # Navigate back to login screen
        self.manager.current = 'main'

    def _update_rect(self, instance, value):
        self.rect.size = self.size
        self.rect.pos = self.pos

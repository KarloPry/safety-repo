from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
from db import DbConnection as db

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

        # Set the background color
        with self.canvas.before:
            Color(rgba=(176/255, 198/255, 206/255, 1))  # Convert HEX B0C6CE to RGBA
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # Main layout
        self.layout = GridLayout(cols=1, spacing=10, padding=[50, 50], size_hint=(0.6, 0.8), pos_hint={'center_x': 0.5, 'center_y': 0.5})

        # Logo
        self.layout.add_widget(Image(source='assets/logo.png', size_hint=(1, 0.3)))

        # Title
        self.layout.add_widget(Label(text='Iniciar Sesión', font_size=50, size_hint=(1, 0.1)))

        # Form fields
        self.username_input = TextInput(hint_text='Usuario', size_hint=(1, 0.1))
        self.password_input = TextInput(hint_text='Contraseña', password=True, size_hint=(1, 0.1))
        self.layout.add_widget(self.username_input)
        self.layout.add_widget(self.password_input)

        # Login button
        self.login_button = Button(text='Iniciar sesión', font_size=40, size_hint=(1, 0.1))
        self.login_button.bind(on_press=self.login)
        self.layout.add_widget(self.login_button)
        self.error_label = Label(text='', color=(1, 0, 0, 1), size_hint=(1, 0.1))
        self.layout.add_widget(self.error_label)

        # Add layout to the screen
        self.add_widget(self.layout)

    def login(self, instance):
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()
        if username and password:
            print(f'Username: {username}, Password: {password}')
            user = db().query(f"SELECT * FROM users WHERE username='{username}' AND password='{password}'")
            if not user:
                # Show alert in UI
                self.username_input.text = ''
                self.password_input.text = ''
                self.error_label.text = 'Usuario o contraseña incorrectos'
                print('Invalid username or password')
            else:
                print('Login successful')
                self.username_input.text = ''
                self.password_input.text = ''
                self.manager.current = 'home'  # Change 'home' to your target screen's name
        else:
            print('Please enter both username and password')

    def _update_rect(self, instance, value):
        self.rect.size = self.size
        self.rect.pos = self.pos

# Entrypoint for kivy app that import screens from ./screens and runs the app

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from screens.login import LoginScreen
from screens.home import HomeScreen
from screens.video import VideoScreen


class MainApp(App):
    def build(self):

        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='main'))
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(VideoScreen(name='video'))
        return sm

if __name__ == '__main__':
    MainApp().run()
from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window


class PongApp(App):
    def build(self):
        # Konfigurace rozměrů hlavního okna aplikace
        # viz https://kivy.org/doc/stable/api-kivy.config.html
        Config.set('graphics', 'width', '800')
        Config.set('graphics', 'height', '600')
        # Nebude možné měnit velikost hlavního okna
        Config.set('graphics', 'resizable', False)
        Config.write()
        Window.size = (800, 600)

PongApp().run()
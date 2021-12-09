from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from game import PongGame

# Třída pro obrazovku s menu
class MenuScreen(Screen):
    pass


 # Třída pro obrazovku s plátnem - budoucí hrací plocha
class CanvasScreen(Screen):
    def start_game(self):
        try:
            if not self.manager.playing[0]:
                self.manager.models[0] = None
            if not self.manager.playing[1]:
                self.manager.models[1] = None
            game = PongGame(self.manager.models)
        except:
            self.manager.models = [None, None]
            game = PongGame(self.manager.models)

        self.add_widget(game)
        game.start()


class PongApp(App):
    def build(self):
        # Vytvoření objektu ScreenManageru do proměnné sm (https://kivy.org/doc/stable/api-kivy.uix.screenmanager.html)
        sm = ScreenManager()
        # Přidání dvou widgetů-obrazovek do sm
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(CanvasScreen(name='canvas'))

        # Konfigurace rozměrů hlavního okna aplikace
        # viz https://kivy.org/doc/stable/api-kivy.config.html
        Config.set('graphics', 'width', '800')
        Config.set('graphics', 'height', '600')
        # Nebude možné měnit velikost hlavního okna
        Config.set('graphics', 'resizable', False)
        Config.write()
        Window.size = (800, 600)
        # Vrací objekt sm - zobrazí se základní GUI aplikace
        return sm

PongApp().run()
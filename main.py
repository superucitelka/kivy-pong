from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.config import Config
from kivy.core.window import Window
from game import PongGame
import random
from kivy.core.text import LabelBase

# Registrace uživatelských fontů
LabelBase.register(name='Monoton', fn_regular='fonts/Monoton-Regular.ttf')
LabelBase.register(name='Bungee', fn_regular='fonts/BungeeShade-Regular.ttf')
LabelBase.register(name='Fredericka', fn_regular='fonts/FrederickatheGreat-Regular.ttf')

# Třída pro obrazovku s menu
class MenuScreen(Screen):
    STATES = ['ARG', 'AUS', 'AUT', 'BEL', 'BLR', 'BRA', 'BUL', 'CAN', 'COL', 'CRO', 'CUB', 'CZE', 'DEN', 'EGY', 'ESP',
              'EST', 'FIN', 'FRA', 'GBR', 'GER', 'GRE', 'HUN', 'CHN', 'IND', 'IRL', 'IRN', 'ISL', 'ISR', 'ITA', 'JAP',
              'KOR', 'LAT', 'LIT', 'MAR', 'MEX', 'NED', 'NGR', 'NOR', 'NZL', 'PAK', 'POL', 'POR', 'ROM', 'RUS', 'SLO',
              'SRB', 'SUI', 'SVK', 'SWE', 'TUN', 'TUR', 'UKR', 'URU', 'USA']
    left_index = random.randrange(0, int(len(STATES) / 2))
    right_index = random.randrange(int(len(STATES) / 2), len(STATES))


 # Třída pro obrazovku s plátnem - budoucí hrací plocha
class CanvasScreen(Screen):
    def start_game(self):
        try:
            if not self.manager.playing[0]:
                self.manager.models[0] = None
            if not self.manager.playing[1]:
                self.manager.models[1] = None
            self.game = PongGame(self.manager.models)
        except:
            self.manager.models = [None, None]
            self.game = PongGame(self.manager.models)

        self.add_widget(self.game)
        self.game.start()


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
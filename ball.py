from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty

"""
    Třída PongBall - míček
    Atributy:
        velocity - směr, kterým se míček pohybuje
        speed - rychlost míčku
    Metody:
        move(self, players, width) - pohyb míčkem a test kolize s pádly (players)
            - pohybuje s míčkem po částech aby neproletěl skrz pádlo
"""


class PongBall(Widget):
    # Zrychlení míčku v jednotlivých osách - vytvoření číselných atributů v Kivy
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    # Rychlost míčku - výchozí hodnota 1
    speed = NumericProperty(1)

    # Konstruktor
    def __init__(self, **kwargs):
        # Vyvolání konstruktoru předka (třídy Widget)
        super(PongBall, self).__init__(**kwargs)
        # Nastavení minimální a maximální rychlosti míčku
        self.min_speed = 5
        self.max_speed = 10
        # Odrazí se míček od horní či spodní stěny?
        self.bounce = False
        self.last_velocity_x = 0

    # Metoda pro pohyb a test kolize s pádly
    def move(self, players, width):
        # Do proměnné s se uloží aktuální nastavená rychlost míčku
        s = self.speed
        # Index zpomalení před nárazem do pádla/hráče
        slow = 10
        self.bounce = False
        # Pohybuje s míčkem po malých částech aby neproletěl pádly
        while s > 0:
            # Pohne míčkem
            self.x += self.velocity_x / self.speed / slow
            self.y += self.velocity_y / self.speed / slow
            # Pro oba hráče
            for player in players:
                # Testuje kolizi s hráčem
                if not self.bounce:
                    self.bounce = player.bounce_ball(self, width)
            s -= 1 / slow
from kivy.uix.widget import Widget

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
    pass
from kivy.uix.widget import Widget
from paddle import PongPaddle
from ball import PongBall


# Třída pro herní plochu (potomek třídy Widget)
class PongGame(Widget):
    def __init__(self, models, **kwargs):
        super(PongGame, self).__init__(**kwargs)

    def start(self):
        pass

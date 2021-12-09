from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, NumericProperty
from kivy.core.window import Window
from kivy.vector import Vector
from random import randint
from kivy.clock import Clock
from paddle import PongPaddle
from ball import PongBall


class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)
    next_player = False
    width = NumericProperty(640)
    height = NumericProperty(360)

    def __init__(self, models, **kwargs):
        super(PongGame, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)
        self.player2.x = 624

    def start(self):
        self.serve_ball()
        Clock.schedule_interval(self.update, 1.0 / 60.0)

    # Metoda pro umístění míčku na střed a zahájení hry
    def serve_ball(self):
        # Nastavení rychlosti míčku na 4
        self.ball.speed = self.ball.min_speed
        # Umístění míčku na střed
        if not self.next_player:
            self.ball.x = (self.width - self.ball.width) / 2
            self.ball.y = (self.height - self.ball.height) / 2
        else:
            self.ball.x = self.next_player.x
            self.ball.y = self.next_player.y + self.next_player.height / 2

        self.next_player = False

        # Nastavení směru míčku
        self.ball.velocity = Vector(self.ball.speed, 0).rotate(randint(-45, 45) + 180 * randint(0, 1))
        self.ball.last_velocity_x = self.ball.velocity_x

    # Hlavní smyčka
    def update(self, dt):
        self.player1.last_score = self.player1.score
        self.player2.last_score = self.player2.score
        self.ball.last_velocity_x = self.ball.velocity_x

        # Volám metodu ball.move(), která pohybuje s míčem a zjišťuje kolize s pádly
        players = [self.player1, self.player2]
        self.ball.move(players, self.width)

        for player in players:
            player.move(self.height)

        # Pokuď se míč dotkne horního nebo dolního okraje, odrazí se
        if self.ball.y <= 0 and self.ball.velocity_y < 0:
            self.ball.velocity_y *= -1

        if self.ball.y >= self.height - self.ball.height and self.ball.velocity_y > 0:
            self.ball.velocity_y *= -1

        if not self.next_player:
            # Pokuď se míček dotkne levého okraje
            if self.ball.x < 0:
                # Přičte bod hráči vpravo
                self.player2.score += 1
                self.next_player = self.player1

            # Pokuď se míček dotkne pravého okraje
            if self.ball.x > self.width - self.ball.width:
                # Přičte bod hráči vlevo
                self.player1.score += 1
                self.next_player = self.player2



    # Ovládání pádel pomocí klávesnice, stisknutí tlačítka
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        # print(keycode)
        # Testy pro tlačítka, která nás zajímají
        if keycode[1] == 'w':
            self.player1.up = True
            self.player1.down = False
        if keycode[1] == 'up':
            self.player2.up = True
            self.player2.down = False
        if keycode[1] == 's':
            self.player1.down = True
            self.player1.up = False
        if keycode[1] == 'down':
            self.player2.down = True
            self.player2.up = False

    # Ovládání pádel pomocí klávesnice, puštění tlačítka
    def _on_keyboard_up(self, keyboard, keycode):
        # print("---------")
        # print(keycode)
        # Testy pro tlačítka, která nás zajímají
        if keycode[1] == 'w':
            self.player1.up = False
        if keycode[1] == 'up':
            self.player2.up = False
        if keycode[1] == 's':
            self.player1.down = False
        if keycode[1] == 'down':
            self.player2.down = False
        if keycode[1] == 'spacebar':
            if self.next_player:
                self.serve_ball()

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard.unbind(on_key_up=self._on_keyboard_up)
        self._keyboard = None

    def test_bounce(self):
        return False if self.ball.last_velocity_x * self.ball.velocity_x > 0 else True

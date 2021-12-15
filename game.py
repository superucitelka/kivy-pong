from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, NumericProperty, BooleanProperty, ListProperty
from kivy.core.window import Window
from kivy.vector import Vector
from random import randint, randrange
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from paddle import PongPaddle
from ball import PongBall


class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)
    next_player = False
    width = NumericProperty(800)
    height = NumericProperty(600)
    time = NumericProperty(0)
    end_time = NumericProperty(0)
    playing = BooleanProperty(False)
    goals = ListProperty()
    timer = False

    def __init__(self, models, **kwargs):
        super(PongGame, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)
        self.player2.x = self.width - 20
        self.goal_sound = SoundLoader.load('sounds/goal.mp3')
        self.goal_sound.volume = .5
        self.pong_sound = SoundLoader.load('sounds/pong.mp3')
        # self.pong.pitch = .5
        self.fans_sound = SoundLoader.load('sounds/fans.mp3')
        self.fans_sound.loop = True
        self.fans_sound.volume = .3

    def get_time(self, time):
        s = int(time / 60)
        m = int(s / 60)
        d = int(time % 60)
        sec = str(s % 60) if s % 60 > 9 else '0' + str(s % 60)
        return f'{m}:{sec},{d}' if s > 0 else '0:00,0'

    def start(self):
        self.fans_sound.play()
        self.player1.quality = 2.28
        self.player2.quality = 2.57
        self.serve_ball()
        self.playing = True
        self.timer = Clock.schedule_interval(self.update, 1.0 / 60.0)

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
        self.playing = True

        # Nastavení směru míčku
        self.ball.velocity = Vector(self.ball.speed, 0).rotate(randint(-45, 45) + 180 * randint(0, 1))
        self.ball.last_velocity_x = self.ball.velocity_x

    # Hlavní smyčka
    def update(self, dt):
        if self.goal_sound.state == 'stop' and self.next_player:
            if self.next_player.ai:
                self.serve_ball()
        if self.time >= self.end_time:
            self.playing = False
            self.timer.cancel()

        if self.playing:
            self.time += 1
        self.player1.last_score = self.player1.score
        self.player2.last_score = self.player2.score
        self.ball.last_velocity_x = self.ball.velocity_x

        # Volám metodu ball.move(), která pohybuje s míčem a zjišťuje kolize s pádly
        players = [self.player1, self.player2]
        self.ball.move(players, self.width)

        for player in players:
            if player.ai:
                if self.ball.y + 10 < player.y + (randrange(int(-player.height * (1/player.quality)),
                                                            int(player.height + player.height * (1/player.quality)))):
                    player.up = False
                    player.down = True
                else:
                    player.up = True
                    player.down = False
            player.move(self.height)

        # Pokuď se míč dotkne horního nebo dolního okraje, odrazí se
        if self.ball.y <= 0 and self.ball.velocity_y < 0:
            self.ball.velocity_y *= -1
            self.pong_sound.play()

        if self.ball.y >= self.height - self.ball.height and self.ball.velocity_y > 0:
            self.ball.velocity_y *= -1
            self.pong_sound.play()

        if not self.next_player:
            # Pokuď se míček dotkne levého okraje
            if self.ball.x < - self.ball.width:
                # Přičte bod hráči vpravo
                self.ball.speed = 0
                self.goal_sound.play()
                self.player2.score += 1
                self.next_player = self.player1
                self.playing = False
                self.goals.append({'player': self.player2.state, 'time': self.get_time(self.time), 'place': self.height - self.ball.y,
                                'score': f'{self.player1.score}:{self.player2.score}'})
                print(self.goals[-1])

            # Pokuď se míček dotkne pravého okraje
            if self.ball.x > self.width - self.ball.width:
                # Přičte bod hráči vlevo
                self.ball.speed = 0
                self.goal_sound.play()
                self.player1.score += 1
                self.next_player = self.player2
                self.playing = False
                self.goals.append({'player': self.player1.state, 'time': self.get_time(self.time), 'place': self.height - self.ball.y,
                                'score': f'{self.player1.score}:{self.player2.score}'})
                print(self.goals[-1])


    # Ovládání pádel pomocí klávesnice, stisknutí tlačítka
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        # print(keycode)
        # Testy pro tlačítka, která nás zajímají
        if keycode[1] == 'w' and not self.player1.ai:
            self.player1.up = True
            self.player1.down = False
        if keycode[1] == 'up' and not self.player2.ai:
            self.player2.up = True
            self.player2.down = False
        if keycode[1] == 's' and not self.player1.ai:
            self.player1.down = True
            self.player1.up = False
        if keycode[1] == 'down' and not self.player2.ai:
            self.player2.down = True
            self.player2.up = False

    # Ovládání pádel pomocí klávesnice, puštění tlačítka
    def _on_keyboard_up(self, keyboard, keycode):
        # print("---------")
        # print(keycode)
        # Testy pro tlačítka, která nás zajímají
        if keycode[1] == 'w' and not self.player1.ai:
            self.player1.up = False
        if keycode[1] == 'up' and not self.player2.ai:
            self.player2.up = False
        if keycode[1] == 's' and not self.player1.ai:
            self.player1.down = False
        if keycode[1] == 'down' and not self.player2.ai:
            self.player2.down = False
        if keycode[1] == 'spacebar':
            if self.next_player:
                self.serve_ball()
        if keycode[1] == 'm':
            if not self.playing:
                self.fans_sound.stop()
                self.parent.parent.current = 'menu'


    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard.unbind(on_key_up=self._on_keyboard_up)
        self._keyboard = None

    def test_bounce(self):
        return False if self.ball.last_velocity_x * self.ball.velocity_x > 0 else True

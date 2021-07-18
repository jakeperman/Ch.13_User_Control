'''
USER CONTROL PROJECT
-----------------
Your choice!!! Have fun and be creative.
Create a background and perhaps animate some objects.
Pick a user control method and navigate an object around your screen.
Make your object more interesting than a ball.
Create your object with a new class.
Perhaps move your object through a maze or move the object to avoid other moving objects.
Incorporate some sound.
Type the directions to this project below:

DIRECTIONS:
----------
Please type directions for this game here.

'''
import arcade
import random
import os
import timeit
import json
SW, SH = 600, 600


# GameShell KEymap
GAMESHELL_A = arcade.key.J
GAMESHELL_Y = arcade.key.I
GAMESHELL_X = arcade.key.U
GAMESHELL_B = arcade.key.K
GAMESHELL_START = arcade.key.ENTER
GAMESHELL_MENU = arcade.key.ESCAPE
GAMESHELL_SELECT = arcade.key.SPACE
GAMESHELL_SHIFT_A = arcade.key.H
GAMESHELL_SHIFT_Y = arcade.key.O
GAMESHELL_SHIFT_X = arcade.key.Y
GAMESHELL_SHIFT_B = arcade.key.L
GAMESHELL_SHIFT_SELECT = arcade.key.MINUS
GAMESHELL_SHIFT_START = arcade.key.PLUS
GAMESHELL_SHIFT_MENU = arcade.key.BACKSPACE
# dictionary of window borders
window_borders = {"x_min": 0, "x_max": 600, "y_min": 0, "y_max": 600}
music, music_volume = True, .3  # music settings
# sound files to use for music tracks
arcade_tracks = ("TourneyFight.wav", "TourneyFightBoss.wav", "Floordown.wav", "Evergreen.wav")
tracks = ("fallen.wav", "tnt.wav", "girlfriend.wav", "that_way.wav", "broke.wav", "take_back.wav", "oops.wav")
difficulties = {
            "Easy": {
                "pipe_speed": -3,
                "bird_speed": -2.5,
                "bird_jump": 45,
                "pipes_distance": 170
            },
            "Medium": {
                "pipe_speed": -4,
                "bird_speed": -2.65,
                "bird_jump": 49,
                "pipes_distance": 155
            },
            "Hard": {
                "pipe_speed": -5,
                "bird_speed": -3,
                "bird_jump": 55,
                "pipes_distance": 140
            },
            "Impossible": {
                "pipe_speed": -6,
                "bird_speed": -3.2,
                "bird_jump": 61,
                "pipes_distance": 120
            }
        }
difficulty = "Medium"


class Pipe:
    def __init__(self, x, y, dx):
        self.x, self.y, self.dx = x, y, dx  # set x and y positions, and change in x
        self.length = 200  # default length is 200
        self.rad = self.length/2  # length and length/2
        self.width = 60  # width of pipe
        self.edge_r, self.edge_l = self.x + self.width/2, self.x - self.width/2  # left and right edges for hitbox

    def draw(self):
        return arcade.draw_rectangle_filled(self.x, self.y, 60, self.length, arcade.color.GO_GREEN)

    def update(self):
        self.edge_r = self.x + 30
        self.edge_l = self.x - 30
        self.x += self.dx  # update current x by adding the x velocity


# bottom pipe class
class BottomPipe(Pipe):
    def __init__(self, x, y, dx):
        super().__init__(x, y, dx)
        self.length = y * 2  # length equals y * 2, so pipe will not be too short or long
        self.rad = self.length/2  # radius for collision hitbox
        self.top = self.y + self.rad  # top of pipe hitbox for collision detection

    # return hitbox
    def get_bounds(self):
        return self.top

    # def random(self):
    #     x, y =


# top pipe class
class TopPipe(Pipe):
    def __init__(self, x, y, dx, length):
        super().__init__(x, y, dx)
        self.length = length  # total length of pipe to be drawn
        self.rad = self.length/2  # radius to use for collision hitbox
        self.bottom = self.y - self.rad  # calculate bottom of pipe for collision detection

    # return the hitbox of the pipe
    def get_bounds(self):
        return self.bottom


class Bird:
    def __init__(self, x, y, dy, size):
        self.x, self.y = x, y  # initialize x and y positions of bird
        self.dx, self.dy = 0, dy   # initialize the x and y velocity
        self.size = size  # initialize the size of bird (width and height are equal_
        self.rad = self.size/2  # create radius for hit-box checking
        self.edges = {}  # create empty dictionary of edges
        self.tilt = self.wing_tilt = 15  # set tilt to an angle of 0
        self.eye_x, self.eye_y = self.x + self.rad / 2, self.y + self.rad * .7
        self.wing_height, self.wing_width = self.rad * .8, self.size * .8
        self.beak_tilt = -100

    # draw the bird
    def create(self):
        # beak
        arcade.draw_parabola_filled(self.x + self.rad * .3, self.y - 100, self.x - self.rad * .5, 100, arcade.color.ORANGE, self.beak_tilt)
        # main body
        arcade.draw_rectangle_filled(self.x, self.y, self.size, self.size, arcade.color.CANARY_YELLOW, self.tilt)
        # bird wing
        arcade.draw_arc_filled(self.x - 6, self.y - 2, self.wing_width, self.wing_height, arcade.color.BLACK, -180, 0, self.wing_tilt)
        # arcade.draw_rectangle_filled(self.x - 3, self.y - 4, self.rad, self.size * .3, arcade.color.BLACK,
        #                              self.wing_tilt)
        # mouth
        # eye
        arcade.draw_rectangle_filled(self.eye_x, self.eye_y, 12, 12, arcade.color.WHITE, self.tilt)
        arcade.draw_rectangle_filled(self.eye_x, self.eye_y, 6, 6, arcade.color.BLACK, self.tilt)
        # MOUTH
        points = [(self.x + self.rad, self.y + self.rad/2),
                  (self.x+self.rad, self.y-self.rad),
                  (self.x + self.rad * 1.5, self.y)]
        # arcade.draw_triangle_filled(points, arcade.color.ORANGE_RED)



    def update(self):
        self.eye_x, self.eye_y = self.x + self.rad / 2, self.y + self.rad * .7
        self.beak_tilt = -100
        if self.tilt < 0:
            self.wing_tilt = 25
            self.eye_x += 2
            self.eye_y -= 0
            self.beak_tilt += 45
        else:
            self.beak_tilt += 15
            self.wing_tilt = 10
            self.eye_x += 8
            self.eye_y -= 8


        # dictionary of reset points for collision with edges
        reset_points = {
                "x_min": 0 + self.rad,
                "x_max": SW - self.rad,
                "y_min": 0 + self.rad,
                "y_max": SH - self.rad
        }
        # sets the current edge of the bird
        self.edges = {
                "x_min": self.x - self.rad,
                "x_max": self.x + self.rad,
                "y_min": self.y - self.rad,
                "y_max": self.y + self.rad
        }
        # check if the bird is colliding with any window borders
        for edge, point in zip(self.edges.keys(), self.edges.values()):
            win = window_borders[edge]
            if point in range(win-10, win+10):
                if "x_" in edge:
                    self.x = reset_points[edge]
                elif "y_" in edge:
                    self.y = reset_points[edge]
        # update position of bird based on velocity
        self.x += self.dx
        self.y += self.dy

    def get_edges(self):
        return self.edges

def check_collision(p1, p2, zone, direct="none"):
    if direct == "x":  # check for direction only on the x axis
        p2_x = range(p2 - zone, p2 + zone)  # create range based on specified zone to check for collision in
        if p1 in p2_x:  # check if the first point x is in the x range of point two
            return True
        return # exit function if checking only for x
    # creates a list of coordinates for point two in the specified range (zone)
    p2_x, p2_y = range(p2[0] - zone, p2[0] + zone), range(p2[1] - zone, p2[1] + zone)
    p1_x, p1_y = p1
    # check if the x and y of point one are in the range list of the second point
    if p1_x in p2_x and p1_y in p2_y:
        return True


class Score:
    def __init__(self):
        try:
            if os.path.isfile("score.txt"):
                with open("score.txt", "r") as score:
                    self.high_score = json.load(score)
                    # self.high_score = score.read()
            else:
                with open("score.txt", "w") as score:
                    self.high_score = {"Easy": 0, "Medium": 0, "Hard": 0, "Impossible": 0}
                    json.dump(self.high_score, score)
                    # score.write(self.high_score)
        except json.decoder.JSONDecodeError:
            with open("score.txt", "w") as file:
                self.high_score = {"Easy": 0, "Medium": 0, "Hard": 0, "Impossible": 0}
                json.dump(self.high_score, file)


    def get_high(self, difficulty):
        return self.high_score[difficulty]

    def set_high(self, new_score, difficulty):
        self.high_score[difficulty] = new_score
        with open("score.txt", "w") as score:
            json.dump(self.high_score, score, indent=4)
            # score.write(self.high_score)


class Window(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.set_mouse_visible(False)
        # variables for measuring performance
        self.processing_time = 0
        self.draw_time = 0
        self.set_vsync(True)
        self.frame_count = 0
        self.fps_start_timer = None
        self.fps = None
        self.SFX_VOLUME = .03
        self.MUSIC_VOLUME = .06
        # initialize the window settings
        self.width, self.height, self.title = width, height, title
        arcade.set_background_color(arcade.color.SKY_BLUE)
        self.settings = {49: "Easy", 50: "Medium", 51: "Hard", 52: "Impossible"}
        self.key_actions = {114: self.reset, 97: self.play_music, 65288: self.reset_high, 109: self.toggle_music,
                            110: self.toggle_sfx,
                            49: self.change_diff, 50: self.change_diff, 51: self.change_diff, 52: self.change_diff}
        self.keys = self.key_actions.keys()

        # set track number to 0 and initialize tracklist
        self.track = 0
        self.tracks = []
        self.tracks2 = []
        self.music_enabled = True
        music_path = "resources/music/"
        self.tracks = [arcade.Sound(music_path+track) for track in arcade_tracks]
        self.tracks2 = [arcade.Sound(music_path + track) for track in tracks]
        self.tracklist = self.tracks.copy()
        self.music = random.choice(self.tracklist)

        # initialize game sounds
        self.music.play(0)
        self.death_sound = arcade.Sound("resources/sounds/oof.wav")
        self.flap = arcade.Sound("resources/sounds/wing_flap.wav")
        self.score_sound = arcade.Sound("resources/sounds/add_point.wav")
        # setup variables influenced by difficulty setting
        self.diff = difficulty
        self.difficulty = difficulties[self.diff]
        self.pipe_speed = self.difficulty['pipe_speed']
        self.bird_speed = self.difficulty['bird_speed']
        self.bird_jump = self.difficulty['bird_jump']
        self.pipes_distance = self.difficulty['pipes_distance']

        # setup score tracker
        self.scoring = Score()
        self.high_score = self.scoring.get_high(self.diff)

        # create the bird character
        self.bird = Bird(SW / 2, SH / 2, self.bird_speed, 50)
        self.key_pressed = False
        # create the starting pipes
        self.bottom_pipes, self.top_pipes = [], []
        self.old_pipes = []
        self.bottom_pipes.append(BottomPipe(SW + 50, 100, self.pipe_speed))
        self.bottom_pipes.append(BottomPipe(SW + 300, 150, self.pipe_speed))
        self.top_pipes.append(TopPipe(SW + 50, 500, self.pipe_speed, 200))
        self.top_pipes.append(TopPipe(SW + 300, 550, self.pipe_speed, 200))

        # setup game variables
        self.score = 0
        self.over = False
        self.death_vol = .7

    def on_draw(self):
        draw_start_time = timeit.default_timer()
        if self.frame_count % 60 == 0:
            if self.fps_start_timer is not None:
                total_time = timeit.default_timer() - self.fps_start_timer
                self.fps = 60 / total_time
            self.fps_start_timer = timeit.default_timer()
        self.frame_count += 1
        arcade.start_render()
        # draw each pipe
        for bpipe, tpipe in zip(self.bottom_pipes, self.top_pipes):
            bpipe.draw()
            tpipe.draw()
        for old in self.old_pipes:
            old.draw()
        # draw the bird
        self.bird.create()
        # draw the current score in the middle of the screen
        arcade.draw_text(str(self.score), SW / 2, 500, arcade.color.BLACK, 30)
        arcade.draw_text(f"High Score: {self.high_score}", 0, SH-30, arcade.color.WHITE, 20)
        arcade.draw_text(f"Difficulty: {self.diff}", 0, 0, arcade.color.WHITE, 20)
        arcade.draw_text(f"Press [1], [2], [3], or [4] to select a new difficulty", 285, 0, arcade.color.WHITE, 12)
        # if the user collides with a pipe, display the game over screen
        if self.over:
            arcade.draw_text("GAME OVER", 100, SH/2, arcade.color.RED, 50)
            arcade.draw_text(f"High Score: {self.high_score}", 190, SH/2 - 30, arcade.color.RED, 25, align="center")
            arcade.draw_text("[R]estart or select a new difficulty\n[1], [2], [3], [4]", SW/2 -165, SH/2 - 30, arcade.color.BLACK, 18, anchor_y= "top", align="center")

        # Display timings
        # output = f"Processing time: {self.processing_time:.5f}"
        # arcade.draw_text(output, 20, SH - 20, arcade.color.BLACK, 16)
        #
        # output = f"Drawing time: {self.draw_time:.3f}"
        # arcade.draw_text(output, 20, SH - 40, arcade.color.BLACK, 16)

        if self.fps is not None:
            output = f"FPS: {self.fps:.0f}"
            arcade.draw_text(output, SW-100, SH - 30, arcade.color.BLACK, 16)

        self.draw_time = timeit.default_timer() - draw_start_time
    def on_update(self, delta_time: float):
        start_time = timeit.default_timer()
        collision_check = True
        old = self.old_pipes
        # as soon as pipes move off screen, create more coming from the other side
        while len(self.bottom_pipes) < 2:
            pipe_x = SW + self.pipes_distance
            pb = BottomPipe(pipe_x, random.randint(80, 150), self.pipe_speed)
            self.bottom_pipes.append(pb)
            # pipe generation has some wonky values, oh well, it works
            pt = TopPipe(pipe_x, pb.y + 150 + pb.length + 60, self.pipe_speed, pb.length + 150)
            self.top_pipes.append(pt)
        # update position of bird
        self.bird.update()
        # update position of each pipe
        for bpipe, tpipe in zip(self.bottom_pipes, self.top_pipes):
            bpipe.update()
            tpipe.update()
        if not self.over and old:
            for old_pipe in old:
                old_pipe.update()
        # get the edges of the birds hitbox
        edges = self.bird.get_edges()
        # check for a collision between the bird and the closest pipes
        pipe, pipet = self.bottom_pipes[0], self.top_pipes[0]
        # decides whether to check for collision with top or bottom pipe, if neither then dont check for collision
        if edges["y_max"] >= pipet.bottom + 10:
            pipe = pipet
        elif edges["y_min"] <= pipe.top + 8:
            pipe = pipe
        else:
            collision_check = False
        # check for collision with pipes, game over if bird collides
        if collision_check and check_collision(int(self.bird.x), pipe.x, 50, "x"):
            self.game_over()
        # if self.music_enabled and self.music.is_complete():
        #     self.play_music()

        # remove pipe from list and add 1 to score if the bird successfully passes through
        if self.bird.get_edges()["x_min"] > self.bottom_pipes[0].x + 50:
            self.score += 1
            self.old_pipes.append(self.bottom_pipes[0])
            self.old_pipes.append(self.top_pipes[0])
            self.bottom_pipes.pop(0)
            self.top_pipes.pop(0)
            arcade.play_sound(self.score_sound, self.SFX_VOLUME)

        if len(old) >= 2 and old[0].x <= -30:
            old.pop(0)
            old.pop(0)
        x = timeit.default_timer()
        self.processing_time = x - start_time
    # function which handles background music
    def play_music(self):
        if self.music.get_stream_position() != 0:
            self.music.stop()
        if len(self.tracklist) == 0:
            self.tracklist = self.tracks2.copy()
        self.music = random.choice(self.tracklist)
        self.tracklist.remove(self.music)
        self.music.play(self.MUSIC_VOLUME)
        # arcade.play_sound(self.music, self.MUSIC_VOLUME)




    def play_sound(self, sound):
        if sound.get_stream_position() == 0:
            sound.play(self.SFX_VOLUME)


    # handles keypresses
    def on_key_press(self, symbol: int, modifiers: int):
        # play flapping sound when bird moves
        # if self.flap.get_stream_position() > .6 or self.flap.get_stream_position() == 0:
        #     arcade.play_sound(self.flap, 0)
        # self.bird.tilt = -15
        # self.bird.y += self.bird_jump
        if symbol not in self.keys and not self.over:
            self.bird.y += self.bird_jump
            self.bird.tilt = -15
            # self.bird.dy *= .8
        elif symbol in self.keys:
            func = self.key_actions[symbol]
            if symbol in (49, 50, 51, 52):
                func(self.settings[symbol])
            else:
                func()




    def on_key_release(self, symbol: int, modifiers: int):
        self.key_pressed = False
        self.bird.tilt = 15
        self.bird.dy = self.bird_speed
        # if the current track finishes playing, start another

        pass

    def reset(self):
        # reset variables that were changed by the game over function
        self.difficulty = difficulties[self.diff]
        self.pipe_speed = self.difficulty['pipe_speed']
        self.bird_speed = self.difficulty['bird_speed']
        self.bird_jump = self.difficulty['bird_jump']
        self.pipes_distance = self.difficulty['pipes_distance']
        self.bird.dy, self.bird.y = self.bird_speed, 350
        self.score, self.over, self.death_vol = 0, False, 0.7
        # reset position of all pipes
        self.old_pipes = []
        # for each in self.old_pipes:
        #     self.old_pipes.remove(each)
        self.gen_pipes()

    def reset_high(self):
        self.high_score = 0
        self.scoring.set_high(0, self.diff)

    def toggle_music(self):
        if self.music.get_stream_position() != 0:
            arcade.stop_sound(self.music)
            self.music_enabled = False
        else:
            arcade.play_sound(self.music, self.MUSIC_VOLUME)
            self.music_enabled = True

    def toggle_sfx(self):
        if self.SFX_VOLUME != 0:
            self.SFX_VOLUME = 0
        else:
            self.SFX_VOLUME = 0.03

    def game_over(self):
        self.play_sound(self.death_sound)  # play death sound
        self.death_vol = 0  # sets vol to zero so sound doesnt keep playing
        self.bird.dy = 0  # stop bird from moving
        # set pipe movement to 0
        for bpipe, tpipe in zip(self.bottom_pipes, self.top_pipes):
            bpipe.dx = tpipe.dx = 0
        if self.score > self.high_score:
            self.scoring.set_high(self.score, self.diff)
            self.high_score = self.score
        self.over = True  # set game over variable to True

    def change_diff(self, diff):
        if diff in list(difficulties.keys()):
            self.score = 0
            self.diff = diff
            self.bird.y = 350
            self.top_pipes, self.bottom_pipes, self.old_pipes = [], [], []
            self.difficulty = difficulties[diff]
            self.pipe_speed = self.difficulty['pipe_speed']
            self.bird_speed = self.difficulty['bird_speed']
            self.bird_jump = self.difficulty['bird_jump']
            self.pipes_distance = self.difficulty['pipes_distance']
            self.bird.dy = self.bird_speed
            self.high_score = self.scoring.get_high(self.diff)
            self.gen_pipes()

    def gen_pipes(self):
        self.bottom_pipes, self.top_pipes = [], []
        self.bottom_pipes.append(BottomPipe(SW + 50, 100, self.pipe_speed))
        self.bottom_pipes.append(BottomPipe(SW + 300, 150, self.pipe_speed))
        self.top_pipes.append(TopPipe(SW + 50, 500, self.pipe_speed, 200))
        self.top_pipes.append(TopPipe(SW + 300, 550, self.pipe_speed, 200))



def main():
    win = Window(SW, SH, "Flutter Cube")
    arcade.run()


if __name__ == "__main__":
    main()
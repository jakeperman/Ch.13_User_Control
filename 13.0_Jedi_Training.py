'''
Sign your name:________________
 
Update the code in this chapter to do the following:
Open a 500px by 500px window.
Change the Ball class to a Box class.
Instantiate two 30px by 30px boxes. One red and one blue.
Make the blue box have a speed of 240 pixels/second
Make the red box have a speed of 180 pixels/second
Control the blue box with the arrow keys.
Control the red box with the WASD keys.
Do not let the boxes go off of the screen.
Incorporate different sounds when either box hits the edge of the screen.
Have two people play this TAG game at the same time.
The red box is always "it" and needs to try to catch the blue box.
When you're done demonstrate to your instructor!

'''
import arcade
import random
SW = 500
SH = 500
laser_tag = True

class Laser:
    def __init__(self, x, y, direction):
        self.directions = {"up": (0, 8), "left": (-8, 0), "down": (0, -8), "right": (8, 0)}
        self.dx, self.dy = self.directions[direction]
        self.x, self.y = x, y
        self.direction = direction
        self.sound = arcade.Sound("laser.mp3")
        self.sound.play(1, 0)
    def shoot(self):
        # print(f"laser x: {self.x} laser y :{self.y}")
        arcade.draw_rectangle_filled(self.x, self.y, 25, 25, arcade.color.YELLOW)

    def update(self):
        self.x += self.dx
        self.y += self.dy
        return self.x, self.y
    def play_sound(self):
        if self.sound.get_stream_position() == 0:
            self.sound.play(1, 0)


class Box:
    def __init__(self, x, y, width, height, color, speed, controls, sound):
        self.width, self.height, self.color, self.speed, self.controls = width, height, color, speed/60, controls
        self.rad, self.x, self.y = self.width/2, x, y
        self.speed_x = self.speed_y = 0
        self.sound = arcade.Sound(sound)
        self.sound.play(1, 0)
        self.last_key = None
        self.laser = Laser(self.x, self.y, "up")
        self.shoot = False

    def draw(self):
        if self.shoot:
            self.shoot_laser(self.last_key)
            self.shoot = False
        self.laser.shoot()
        return arcade.draw_rectangle_filled(self.x, self.y, self.width, self.height, self.color)

    def update(self):
        # set current x and y positions in accordance to speed and direction
        laser_pos = self.laser.update()
        self.x += self.speed_x
        self.y += self.speed_y
        # edges of box
        box_edges = [self.y + self.rad, self.x - self.rad, self.y - self.rad, self.x + self.rad]
        # bounds of window
        window_edges = [range(SH, SH+10), range(-10, 0), range(-10, 0), range(SW, SW+10)]
        # if edge of box tries to go past bounds of window, dont let it
        for i, (box_edge, window_edge) in enumerate(zip(box_edges, window_edges)):
            if box_edge in window_edge:
                self.play_sound()
                if i == 0 or i == 2:  # if direction is up or down
                    self.y = self.controls[list(self.controls)[i]][1]
                else:  # if direction is left or right
                    self.x = self.controls[list(self.controls)[i]][1]
        return laser_pos

    def play_sound(self):
        if self.sound.get_stream_position() >= .95 or self.sound.is_complete():
            self.sound.play(1, 0)

    def get_edges(self):
        return [self.y + self.rad, self.x - self.rad, self.y - self.rad, self.x + self.rad]

    def shoot_laser(self, direction):
        if direction is None:
            direction = 119
        w, a, s, d = 119, 97, 115, 100
        i, j, k, l = 105, 106, 107, 108
        o, k, l, x = 111, 107, 108, 59
        directions = {w: "up", a: "left", s: "down", d: "right",o: "up", k: "left", l: "down", x :"right"}
        self.laser = Laser(self.x, self.y, directions[direction])
        self.laser.play_sound()
        self.laser.shoot()
        return self.laser


    def set_speed(self, direction, speed=None):
        # if the shoot key is pressed,
        if direction == 65505 or direction == 65293:
            print(f"last key: {self.last_key}")
            self.shoot = True
            return
        if direction == self.get_keys()[0] or direction == self.get_keys()[2]:
            self.last_key = direction
            if speed is not None:
                self.speed_y = speed
                return
            self.speed_y = self.controls[direction][0]
        else:
            self.last_key = direction
            if speed is not None:
                self.speed_x = speed
                return
            self.speed_x = self.controls[direction][0]


    def get_keys(self):
        return list(self.controls.keys())

    def reset_pos(self):
        self.x, self.y = random.randint(25, 80), random.randint(25, 80)

    def reset_laser(self):
        self.laser.x, self.laser.y = -50, -50
        self.laser.dx, self.laser.dy = 0, 0



def check_collision(p1, p2, zone):
    p1_x, p1_y = p1
    p2_x, p2_y = range(p2[0] - zone, p2[0] + zone), range(p2[1] - zone, p2[1] + zone)
    if p1_x in p2_x and p1_y in p2_y:
        return True
    return False


class Window(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        # initialize red and blue boxes
        arcade.set_background_color(arcade.color.BLACK)
        w, a, s, d = 119, 97, 115, 100
        shoot = 65505
        if laser_tag:
            shoot2 = 65293
        else:
            shoot2 = None
        up, left, down, right = 65362, 65361, 65364, 65363
        i, j, k, l = 105, 106, 107, 108
        o, k, l ,x = 111, 107, 108, 59
        if laser_tag:
            speed_1 = 240
        else:
            speed_1 = 180
        speed_2 = 240
        key_speed = {w: (speed_1/60, SH-25), a: (-speed_1/60, 0+25), s: (-speed_1/60, 0+25), d: (speed_1/60, SW-25), shoot: 10}
        arrow_speed = {up: (180/60, SH-25), left: (-180/60, 0+25), down: (-180/60, 0+25), right: (180/60, SW-25)}
        key2_speed = {o: (speed_2/60, SH - 25), k: (-speed_2/60, 0 + 25), l: (-speed_2/60, 0 + 25), x: (speed_2/60, SW - 25), shoot2: 10}
        self.box_blue = Box(100, 250, 50, 50, arcade.color.BLUE, 180, key_speed, "blue.mp3")
        self.box_red = Box(400, 250, 50, 50, arcade.color.RED, 240, key2_speed, "red.mp3")
        self.keys_pressed = {w: False, a: False, s: False, d: False, o: False, k: False, l: False, x: False}
        self.recents = []
        self.sound = arcade.Sound("explosion.mp3")
        self.sound.play(1)
        self.lasa = None
        self.lasa2 = None
        self.score = [0, 0]

        self.explode = 0


    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(f"BLUE: {self.score[0]} RED: {self.score[1]}", 130, 450, arcade.color.WHITE, 25)
        # draw both boxes
        self.box_blue.draw()
        self.box_red.draw()

    def on_update(self, delta_time: float):
        # update positions of each box, and return positions of their lasers
        lasa_pos = self.box_blue.update()
        lasa_pos2 = self.box_red.update()

        # if the list of recent keys is too long, shorten it
        while len(self.recents) > 15:
            self.recents.pop()

        # set the relative speed for any key being pressed
        for key in reversed(self.recents):
            if self.keys_pressed[key]:
                if key in self.box_blue.get_keys():
                    self.box_blue.set_speed(key)
                elif key in self.box_red.get_keys():
                    self.box_red.set_speed(key)

        # get edges and coordinates for boxes
        red_edges, red_x, red_y = self.box_red.get_edges(), self.box_red.x, self.box_red.y
        blue_edges, blue_x, blue_y = self.box_blue.get_edges(), self.box_blue.x, self.box_blue.y
        # collision with blue for redsk
        # if check_collision((int(red_x), int(red_y)), (int(blue_x), int(blue_y)), 50):
        #     self.play_sound()
        #     self.box_blue.reset_pos()
        # if red is hit by laser
        if check_collision(lasa_pos, (int(red_x), int(red_y)), 50):
            self.play_sound()
            self.box_red.reset_pos()
            self.box_blue.reset_laser()
            self.score[0] += 1
        # if blue is hit by laser
        if check_collision(lasa_pos2, (int(blue_x), int(blue_y)), 50):
            self.play_sound()
            self.box_blue.reset_pos()
            self.score[1] += 1
            self.box_red.reset_laser()

    def play_sound(self):
        if self.sound.get_stream_position() >= .9 or self.sound.get_stream_position() == 0:
            self.sound.play(1, 0)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == 58:
            symbol = 59
        print(f"{chr(symbol)}: True")
        print(f"{symbol}: {chr(symbol)}")
        if symbol != 65293 and symbol != 65505:
            self.recents.insert(0, symbol)
        self.keys_pressed[symbol] = True

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == 58:
            symbol = 59
        self.keys_pressed[symbol] = False
        print(f"{chr(symbol)}: False")
        print("-"*10)
        if symbol != 65293 and symbol != 65505:
            self.recents.remove(symbol)
        if symbol in self.box_blue.get_keys():
            self.box_blue.set_speed(symbol, 0)
        elif symbol in self.box_red.get_keys():
            self.box_red.set_speed(symbol, 0)


def main():
    win = Window(SW, SH, "Laser Tag")
    arcade.run()


if __name__ == "__main__":
    main()

import board
import neopixel

class Expressions:
    def __init__(self):
        self.pin = board.D18
        self.num_leds = 44
        self.pixels = neopixel.NeoPixel(self.pin, self.num_leds, brightness=1)

        led_positions_full_eye = {
            "left":  [10, 9, 4, 11, 8, 5, 12, 7, 6],
            "right": [33, 34, 32, 39, 35, 31, 38, 36, 37]
        }

        led_positions_furrowed_up = {
            "left":  [0, 3, 4, 8, 12, 5, 7, 6],
            "right": [40, 43, 39, 35, 31, 38, 36, 37]
        }

        led_positions_furrowed_down = {
            "left":  [1, 2, 5, 8, 11, 12, 7, 6],
            "right": [41, 42, 32, 35, 31, 38, 36, 37]
        }

        led_positions_half_down = {
            "left":  [5, 12, 7, 6],
            "right": [31, 38, 36, 37]
        }

        led_positions_half_up = {
            "left":  [10, 9, 4, 11],
            "right": [33, 34, 32, 39]
        }

        led_positions_crossed = {
            "left":  [0, 3, 4, 8, 11, 14, 15, 1, 2, 5, 12, 13, 16],
            "right": [28, 29, 32, 35, 38, 39, 40, 43, 27, 30, 31, 41, 42]
        }

        led_positions_cute_closed = {
            "left":  [0, 3, 4, 8, 5, 2, 1],
            "right": [43, 40, 39, 35, 38, 41, 42]
        }

        led_positions_happy_mouth   =  [17, 19, 20, 21, 22, 23, 24, 26]

        led_positions_sad_mouth     =  [18, 19, 20, 21, 22, 23, 24, 25]

        led_positions_serious_mouth =  [19, 20, 21, 22, 23, 24]

    def full_eye(self, side, r, g, b):
        print(f"full eye {side}")
        if side in self.led_positions_full_eye:
            for index in self.led_positions_full_eye[side]:
                self.pixels[index] = (r, g, b)
        else:
            print(f"Side {side} not recognized")

    def furrowed_up(self, side, r, g, b):
        print(f"furrowed up eye {side}")
        if side in self.led_positions_furrowed_up:
            for index in self.led_positions_furrowed_up[side]:
                self.pixels[index] = (r, g, b)
        else:
            print(f"Side {side} not recognized")

    def furrowed_down(self, side, r, g, b):
        print(f"furrowed down eye {side}")
        if side in self.led_positions_furrowed_down:
            for index in self.led_positions_furrowed_down[side]:
                self.pixels[index] = (r, g, b)
        else:
            print(f"Side {side} not recognized")

    def half_down(self, side, r, g, b):
        print(f"half down {side} eye")
        if side in self.led_positions_half_down:
            for index in self.led_positions_half_down[side]:
                self.pixels[index] = (r, g, b)
        else:
            print(f"Side {side} not recognized")

    def half_up(self, side, r, g, b):
        print(f"half up {side} eye")
        if side in self.led_positions_half_up:
            for index in self.led_positions_half_up[side]:
                self.pixels[index] = (r, g, b)
        else:
            print(f"Side {side} not recognized")

    def crossed(self, side, r, g, b):
        print(f"crossed {side} eye")
        if side in self.led_positions_crossed:
            for index in self.led_positions_crossed[side]:
                self.pixels[index] = (r, g, b)
        else:
            print(f"Side {side} not recognized")

    def cute_closed(self, side, r, g, b):
        print(f"cute closed {side} eye")
        if side in self.selfled_positions_cute_closed:
            for index in self.led_positions_cute_closed[side]:
                self.pixels[index] = (r, g, b)
        else:
            print(f"Side {side} not recognized")


    #-------------------mouth------------
    def happy_mouth(self, r, g, b):
        print("happy mouth")
        for index in self.led_positions_happy_mouth:
            self.pixels[index] = (r, g, b)
        
    def sad_mouth(self, r, g, b):
        print("sad mouth")
        for index in self.led_positions_sad_mouth:
            self.pixels[index] = (r, g, b)

    def serious_mouth(self, r, g, b):
        print("serious mouth")
        for index in self.led_positions_serious_mouth:
            self.pixels[index] = (r, g, b)


    
    #-------------------face-------------
    #------------------------------------
    def happy(self, r,g,b):
        print("happy face")
        self.full_eye("left",r,g,b)
        self.full_eye("right",r,g,b)
        self.happy_mouth(r,g,b)

    def sad(self, r,g,b):
        print("sad")
        self.full_eye("left",r,g,b)
        self.full_eye("right",r,g,b)
        self.sad_mouth(r,g,b)

    def serious(self, r,g,b):
        print("pocker face")
        self.full_eye("left",r,g,b)
        self.full_eye("right",r,g,b)
        self.serious_mouth(r,g,b)

    def happy_evil(self, r,g,b):
        print("happy evil")
        self.furrowed_up("left",r,g,b)
        self.furrowed_up("right",r,g,b)
        self.happy_mouth(r,g,b)

    def disappointed_angry(self, r,g,b):
        print("disappointed_angry")
        self.furrowed_up("left",r,g,b)
        self.furrowed_up("right",r,g,b)
        self.sad_mouth(r,g,b)

    def angry(self, r,g,b):
        print("angry")
        self.furrowed_up("left",r,g,b)
        self.furrowed_up("right",r,g,b)
        self.serious_mouth(r,g,b)

    def peacefull(self, r,g,b):
        print("peacefull")
        self.furrowed_down("left",r,g,b)
        self.furrowed_down("right",r,g,b)
        self.happy_mouth(r,g,b)

    def really_sad(self, r,g,b):
        print("really sad")
        self.furrowed_down("left",r,g,b)
        self.furrowed_down("right",r,g,b)
        self.sad_mouth(r,g,b)

    def disappointed(self, r,g,b):
        print("disappointed")
        self.furrowed_down("left",r,g,b)
        self.furrowed_down("right",r,g,b)
        self.serious_mouth(r,g,b)

    def happy_spicy(self, r,g,b):
        print("happy spicy")
        self.half_down("left",r,g,b)
        self.half_down("right",r,g,b)
        self.happy_mouth(r,g,b)

    def bored(self, r,g,b):
        print("bored")
        self.half_down("left",r,g,b)
        self.half_down("right",r,g,b)
        self.sad_mouth(r,g,b)

    def stoic_disappointed(self, r,g,b):
        print("stoic disappointed")
        self.half_down("left",r,g,b)
        self.half_down("right",r,g,b)
        self.serious_mouth(r,g,b)

    def cute_happy(self, r,g,b):
        print("cute happy")
        self.half_up("left",r,g,b)
        self.half_up("right",r,g,b)
        self.happy_mouth(r,g,b)

    def surprised_sad(self, r,g,b):
        print("surprised sad")
        self.half_up("left",r,g,b)
        self.half_up("right",r,g,b)
        self.sad_mouth(r,g,b)

    def cute_stoic(self, r,g,b):
        print("cute stoic")
        self.half_up("left",r,g,b)
        self.half_up("right",r,g,b)
        self.serious_mouth(r,g,b)

    def happy_dead(self, r,g,b):
        print("happy dead")
        self.crossed("left",r,g,b)
        self.crossed("right",r,g,b)
        self.happy_mouth(r,g,b)

    def sad_dead(self, r,g,b):
        print("sad dead")
        self.crossed("left",r,g,b)
        self.crossed("right",r,g,b)
        self.sad_mouth(r,g,b)

    def stoic_dead(self, r,g,b):
        print("stoic dead")
        self.crossed("left",r,g,b)
        self.crossed("right",r,g,b)
        self.serious_mouth(r,g,b)

    def closed_eye_happy(self, r,g,b):
        print("closed eye happy")
        self.cute_closed("left",r,g,b)
        self.cute_closed("right",r,g,b)
        self.happy_mouth(r,g,b)

    def closed_eye_sad(self, r,g,b):
        print("closed eye sad")
        self.cute_closed("left",r,g,b)
        self.cute_closed("right",r,g,b)
        self.sad_mouth(r,g,b)

    def garu_face(self, r,g,b):
        print("garu face")
        self.cute_closed("left",r,g,b)
        self.cute_closed("right",r,g,b)
        self.serious_mouth(r,g,b)



face = Expressions()
face.happy(255, 0, 0)



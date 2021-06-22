class State:

    def __init__(self, brightness=0, red=0, green=0, blue=0, led1=True, led2=True, lcd1=True, lcd2=True, auto_led=False):
        self.brightness = brightness
        self.red = red
        self.green = green
        self.blue = blue
        self.led1 = led1
        self.led2 = led2
        self.leds = True if (self.led1 == self.led2 is True) else False
        self.lcd1 = lcd1
        self.lcd2 = lcd2
        self.lcds = True if (self.lcd1 == self.lcd2 is True) else False
        self.auto_led = auto_led

    # def __str__(self):


if __name__ == "__main__":
    state = State(255, 127, 127, 127, True, True, True, True)
    print(state.__dict__)

class GPIO:
    GPIO_RED = 17                               # GPIO pin for 12V red channel
    GPIO_GREEN = 22                             # GPIO pin for 12V green channel
    GPIO_BLUE = 27                              # GPIO pin for 12V blue channel
    GPIO_WS281B = 18                            # GPIO pin for WS281B addressable strip
    GPIO_IR_RX = 14                             # GPIO pin for IR reciving diode
    GPIO_IR_TX = 15                             # GPIO pin for IR transmitting diode
    GPIO_W1 = 4                                 # GPIO pin for 1-wire interface


class LEDSTRIP:
    LED_COUNT = 180                             # Number of LED pixels.
    LED_PIN = GPIO.GPIO_WS281B                  # GPIO pin connected to the pixels (18 uses PWM!).
    LED_FREQ_HZ = 800000                        # LED signal frequency in hertz (usually 800khz)
    LED_DMA = 10                                # DMA channel to use for generating signal (try 10)
    LED_BRIGHTNESS = 255                        # Set to 0 for darkest and 255 for brightest
    LED_INVERT = False                          # True to invert the signal (when using NPN transistor level shift)
    LED_CHANNEL = 0                             # set to '1' for GPIOs 13, 19, 41, 45 or 53


class INITIALS:
    LCD2_BACKLIGHT = True                       # lcd 2x16 backlight enabled
    LCD4_BACKLIGHT = True                       # lcd 4x20 backlight enabled
    LED12_ON = True                             # 12V strip enabled
    LED5_ON = True                              # 5V WS281B strip enabled
    LED_BRIGHTNESS = 255                        # LED strips brightness
    LED_RED = 255                               # red channel brightness
    LED_GREEN = 255                             # green channel brightness
    LED_BLUE = 255                              # blue channel brightness
    LED_STRIP_DIRECTION = 1                     # WS281B strip direction, 1 for forward, -1 for backward
    LED_STRIP_DISPLAY = LEDSTRIP.LED_COUNT      # number of WS281B strip lit counted from current direction start
    LED_CHANNEL_BRIGHTNESS = 'a'                # label for brightness channel
    LED_CHANNEL_RED = 'r'                       # label for red channel
    LED_CHANNEL_GREEN = 'g'                     # label for green channel
    LED_CHANNEL_BLUE = 'b'                      # label for blue channel
    LED_STRIP_PROP_DIR = 'dir'                  # label for WS281B strip direction
    LED_STRIP_PROP_DIS = 'dis'                  # label for WS281B strip display count
    FADE_AWAY_SPEED = 10


class LCD:
    ID_0 = 0x26
    ID_1 = 0x27
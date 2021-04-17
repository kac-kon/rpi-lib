import constants


class ButtonsVar:
    def __init__(self):
        self._button_one = False
        self._button_two = False
        self._button_three = False

        self._button_callbacks = []

    @property
    def button_one(self):
        return self._button_one

    @button_one.setter
    def button_one(self, new_state):
        button_number = 1
        self._button_one = new_state
        self._notify_button_observer(button_number, new_state)

    @property
    def button_two(self):
        return self._button_one

    @button_two.setter
    def button_two(self, new_state):
        button_number = 2
        self._button_two = new_state
        self._notify_button_observer(button_number, new_state)

    @property
    def button_three(self):
        return self._button_one

    @button_three.setter
    def button_three(self, new_state):
        button_number = 3
        self._button_three = new_state
        self._notify_button_observer(button_number, new_state)

    def _notify_button_observer(self, button_number, new_value):
        print("called")
        for callback in self._button_callbacks:
            callback(button_number, new_value)

    def register_button_callback(self, callback):
        self._button_callbacks.append(callback)


class LcdVar:
    def __init__(self):
        self._lcd2_backlight = constants.INITIALS.LCD2_BACKLIGHT
        self._lcd4_backlight = constants.INITIALS.LCD4_BACKLIGHT

        self._lcd_callbacks = []

    @property
    def lcd2_backlight(self):
        return self._lcd2_backlight

    @lcd2_backlight.setter
    def lcd2_backlight(self, new_state):
        lcd_id = constants.LCD.ID_0
        self._lcd2_backlight = new_state
        self._notify_lcd_observer(lcd_id, new_state)

    @property
    def lcd4_backlight(self):
        return self._lcd4_backlight

    @lcd4_backlight.setter
    def lcd4_backlight(self, new_state):
        lcd_id = constants.LCD.ID_1
        self._lcd4_backlight = new_state
        self._notify_lcd_observer(lcd_id, new_state)

    def _notify_lcd_observer(self, lcd_id, new_state):
        for callback in self._lcd_callbacks:
            callback(lcd_id, new_state)

    def register_lcd_callback(self, callback):
        self._lcd_callbacks.append(callback)


class LedVar:
    def __init__(self):
        self._led12_on = constants.INITIALS.LED12_ON
        self._led5_on = constants.INITIALS.LED5_ON
        self._led_brightness = constants.INITIALS.LED_BRIGHTNESS
        self._led_red = constants.INITIALS.LED_RED
        self._led_green = constants.INITIALS.LED_GREEN
        self._led_blue = constants.INITIALS.LED_BLUE
        self._led_strip_direction = constants.INITIALS.LED_STRIP_DIRECTION
        self._led_strip_display = constants.INITIALS.LED_STRIP_DISPLAY
        self._fade_away_speed = constants.INITIALS.FADE_AWAY_SPEED

        self._led_enable_callbacks = []
        self._led_color_callbacks = []
        self._led_strip_callbacks = []

    @property
    def fade_away_speed(self):
        return self._fade_away_speed

    @property
    def led12_on(self):
        return self._led12_on

    @led12_on.setter
    def led12_on(self, new_value):
        led_strip = 1
        self._led12_on = new_value
        self._notify_led_enable_observer(led_strip, new_value)

    @property
    def led5_on(self):
        return self._led5_on

    @led5_on.setter
    def led5_on(self, new_value):
        led_strip = 0
        self._led5_on = new_value
        self._notify_led_enable_observer(led_strip, new_value)

    @property
    def led_brightness(self):
        return self._led_brightness

    @led_brightness.setter
    def led_brightness(self, new_value):
        channel = constants.INITIALS.LED_CHANNEL_BRIGHTNESS
        self._led_brightness = new_value
        self._notify_led_color_observer(channel, new_value)

    @property
    def led_red(self):
        return self._led_red

    @led_red.setter
    def led_red(self, new_value):
        channel = constants.INITIALS.LED_CHANNEL_RED
        self._led_red = new_value
        self._notify_led_color_observer(channel, new_value)

    @property
    def led_green(self):
        return self._led_green

    @led_green.setter
    def led_green(self, new_value):
        channel = constants.INITIALS.LED_CHANNEL_GREEN
        self._led_green = new_value
        self._notify_led_color_observer(channel, new_value)

    @property
    def led_blue(self):
        return self._led_blue

    @led_blue.setter
    def led_blue(self, new_value):
        channel = constants.INITIALS.LED_CHANNEL_BLUE
        self._led_blue = new_value
        self._notify_led_color_observer(channel, new_value)

    @property
    def led_strip_direction(self):
        return self._led_strip_direction

    @led_strip_direction.setter
    def led_strip_direction(self, new_value):
        prop = constants.INITIALS.LED_STRIP_DIRECTION
        self._led_strip_direction = new_value
        self._notify_led_strip_properties_observer(prop, new_value)

    @property
    def led_strip_display(self):
        return self._led_strip_display

    @led_strip_display.setter
    def led_strip_display(self, new_value):
        prop = constants.INITIALS.LED_STRIP_DISPLAY
        self._led_strip_display = new_value
        self._notify_led_strip_properties_observer(prop, new_value)

    def _notify_led_enable_observer(self, strip, new_value):
        for callback in self._led_enable_callbacks:
            callback(strip, new_value)

    def register_led_enable_callback(self, callback):
        self._led_enable_callbacks.append(callback)

    def _notify_led_color_observer(self, channel, new_value):
        for callback in self._led_color_callbacks:
            callback(channel, new_value)

    def register_led_color_callback(self, callback):
        self._led_color_callbacks.append(callback)

    def _notify_led_strip_properties_observer(self, prop, new_value):
        # [callback(prop, new_value) for callback in self._led_strip_callbacks]
        for callback in self._led_strip_callbacks:
            callback(prop, new_value)

    def register_led_strip_callback(self, callback):
        self._led_strip_callbacks.append(callback)

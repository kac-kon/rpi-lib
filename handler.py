import constants
import drivers.lcd_driver
from button import ButtonsHandler
import time

class Buttons:
    def button_pressed(num, value):
        print("button {} is pressed? {}".format(num, value))

class LCDdisplay:
    def set_backlight(lcd_id, state):
        lcd = drivers.lcd_driver.lcd(constants.LCD.id(lcd_id))
        lcd.backlight(state)
        

if __name__ == "__main__":
    b = ButtonsHandler()
    b.register_button_callback(Buttons.button_pressed)
    b.start_loop()
    time.sleep(5)
    b.exit_loop()
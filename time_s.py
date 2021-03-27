import drivers.lcd_driver
import time
import datetime

LCD_BACKLIGHT = 0x08
LCD_NOBACKLIGHT = 0x00

def print_time_once():
    d = str(datetime.datetime.now().today())[:10]
    t = str(datetime.datetime.now().today())[11:19]
    lcd.lcd_display_string(d, 1)
    lcd.lcd_display_string(t, 2)

# ------------------------------
# INITIAL CONFIG
# ------------------------------

# lcd
lcd = drivers.lcd_driver.lcd(0x26, backlight=LCD_NOBACKLIGHT)



lcd.lcd_clear()
while True:
    print_time_once()
    time.sleep(.1)
    

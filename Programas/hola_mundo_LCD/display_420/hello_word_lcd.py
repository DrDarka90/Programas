# loading the class
import lcddriver
from time import *

# lcd start
lcd = lcddriver.lcd()

# this command clears the display (captain obvious)
lcd.lcd_clear()

# now we can display some characters (text, line)
lcd.lcd_display_string("Monitoreo y Control", 1)
lcd.lcd_display_string("  IEH electricidad  ", 2)
lcd.lcd_display_string(" Sistema OK", 3)
lcd.lcd_display_string("   2019   ", 4)

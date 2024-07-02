import RPi.GPIO as GPIO
from time import sleep
from RPLCD.gpio import CharLCD

lcd = CharLCD(pin_rs=22, pin_e=17, pin_rw=None, pins_data=[25, 24, 23, 18],
              numbering_mode=GPIO.BCM,
              cols=16, rows=2, dotsize=8)
lcd.clear()

number = 0
scode = ""
item_count = 0
end = False
items = []
i = 0

while (not end):
    lcd.clear()
    scode = str(input())
    
    if scode == "Q1":
        end = True
    else:
        lcd.write_string(scode)
        items.append(scode)
        lcd.cursor_pos = (1, 0)
        lcd.write_string("Item Added")
        sleep(1)
        
        lcd.clear()
        item_count = item_count + 1
        IC = str(item_count)
        lcd.write_string("Total Items: ")
        lcd.write_string(IC)
        sleep(1)

lcd.clear()
sleep(1)
while i < item_count :
    lcd.clear()
    lcd.write_string(items[i])
    test = input()
    if test == "" or test == 'd':
        i = i+1
    elif test == 'a' and i > 0:
        i = i-1

lcd.clear()
lcd.close()
GPIO.cleanup()
from machine import Pin, PWM
from light_utils import Indicator, Klaxon, stop_all, BackLight, FrontLight
from button_utils import Button, InterruptButton, AltInterruptButton, ModeButton
import time
from bluetooth import BLE


ble = BLE()

pwm_indicator_right = PWM(Pin(0, Pin.OUT))
pwm_indicator_right.freq(20000)

pwm_indicator_left = PWM(Pin(1, Pin.OUT))
pwm_indicator_left.freq(20000)

pwm_front_light = PWM(Pin(4, Pin.OUT))
pwm_front_light.freq(20000)

pwm_back_light = PWM(Pin(2, Pin.OUT))
pwm_back_light.freq(20000)

pwm_klaxon = PWM(Pin(3, Pin.OUT))
pwm_klaxon.freq(20000)

indicator_left = Indicator(pwm_indicator_left)
indicator_right = Indicator(pwm_indicator_right)
front_light = FrontLight(pwm_front_light)
back_light = BackLight(pwm_back_light)

klaxon = Klaxon([pwm_klaxon, pwm_indicator_left, pwm_indicator_right, pwm_front_light, pwm_back_light])

#pwm_functions = [indicator_left, indicator_right, klaxon]

events = {}

pin_button_left = 20
pin_button_right = 21
pin_button_light = 10
pin_klaxon = 9
button_left = AltInterruptButton(pin_button_left, events)
button_right = AltInterruptButton(pin_button_right, events)
button_klaxon = AltInterruptButton(pin_klaxon, events)
button_light = ModeButton(pin_button_light, events, 3)

while True:
    for key, value in events.items():
        if key == pin_klaxon:
            if value:
                klaxon()
                break
            else:
                klaxon.stop()

        elif key == pin_button_right :
            if value:
                indicator_right()
            else:
                indicator_right.stop()

        elif key == pin_button_left :
            if value:
                indicator_left()
            else:
                indicator_left.stop()

        elif key == pin_button_light :
            if value >= 0:
                back_light.set_mode(value)
                back_light()
                front_light.set_mode(value)
                front_light()
            elif back_light.is_started():
                back_light.stop()
                front_light.stop()


    time.sleep(0.01)

# while True:
#     if button_klaxon():
#         if not klaxon.is_started :
#             stop_all(pwm_functions)
#         klaxon()
#     else :
#         if klaxon.is_started :
#             klaxon.stop()
#         if button_left():
#             indicator_left()
#         elif indicator_left.is_started():
#             indicator_left.stop()
        
#         if button_right():
#             indicator_right()
#         elif indicator_right.is_started():
#             indicator_right.stop()

#         lightmode = button_light()
#         if lightmode >= 0:
#             back_light.set_mode(lightmode)
#             back_light()
#         elif back_light.is_started():
#             back_light.stop()

#     time.sleep(0.01)

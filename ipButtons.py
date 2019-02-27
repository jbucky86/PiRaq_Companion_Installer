
import RPi.GPIO as GPIO
import uinput
import os
from time import sleep

rot_a = 22
rot_b = 24
but_l = 26
but_r = 20
but_u = 21
but_d = 25
but_c = 23
counter = 0

# Pin Assignments FOR PiRaq
# backlight on screen
# BackLight = 27
# Center button         
# Center = 23
# Direction buttons
# Up = 21
# Down = 25
# Left = 26
# Right = 20
# Rot1 = 22
# Rot2 = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(rot_a, GPIO.IN)
GPIO.setup(rot_b, GPIO.IN)
GPIO.setup(but_l, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(but_r, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(but_u, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(but_d, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(but_c, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

device = uinput.Device([uinput.KEY_UP, uinput.KEY_DOWN,  uinput.KEY_LEFT,  uinput.KEY_RIGHT,  uinput.KEY_ENTER,  uinput.KEY_0,  uinput.KEY_1,  uinput.KEY_2,  uinput.KEY_3,  uinput.KEY_4,  uinput.KEY_5,  uinput.KEY_6,  uinput.KEY_7,  uinput.KEY_8,  uinput.KEY_9,  uinput.KEY_ESC])

seq_a = seq_b = 0

def on_rot(pin):
    global seq_a, seq_b
    a = GPIO.input(rot_a)
    b = GPIO.input(rot_b)
    seq_a = ((seq_a << 1) | a) & 0b1111
    seq_b = ((seq_b << 1) | b) & 0b1111
    if counter == -1:
        counter = 9
    if counter == 10:
        counter = 0
    if counter == 0:
        num = uinput.KEY_0
    if counter == 1:
        num = uinput.KEY_1
    if counter == 2:
        num = uinput.KEY_2
    if counter == 3:
        num = uinput.KEY_3
    if counter == 4:
        num = uinput.KEY_4
    if counter == 5:
        num = uinput.KEY_5
    if counter == 6:
        num = uinput.KEY_6
    if counter == 7:
        num = uinput.KEY_7
    if counter == 8:
        num = uinput.KEY_8
    if counter == 9:
        num = uinput.KEY_9

    if seq_a == 0b0011 and seq_b == 0b1001:
        device.emit_click(uinput.KEY_DEL)
        device.emit_click(num)
        counter = counter + 1
    
    if seq_a == 0b1001 and seq_b == 0b0011:
        device.emit_click(uinput.KEY_DEL)
        device.emit_click(num)
        counter = counter - 1

def on_but(pin):
    butl = GPIO.input(but_l)
    butr = GPIO.input(but_r)
    butu = GPIO.input(but_u)
    butd = GPIO.input(but_d)
    butc = GPIO.input(but_c)
    if (butl == 0):
          device.emit_click(uinput.KEY_LEFT)

    if (butr == 0):
          device.emit_click(uinput.KEY_RIGHT)

    if (butu == 0):
        device.emit_click(uinput.KEY_UP)

    if (butd == 0):
        device.emit_click(uinput.KEY_DOWN)

    if (butu == 0 and butd == 0):
        os.system('sudo reboot')

def on_cen(pin):
    butl = GPIO.input(but_l)
    butr = GPIO.input(but_r)
    butu = GPIO.input(but_u)
    butd = GPIO.input(but_d)
    butc = GPIO.input(but_c)
    
    if (butl == 0 and butc == 0):
        device.emit_click(uinput.KEY_ESC)
        print('Reseved butn1')
    
    if (butr == 0 and butc == 0):
        print('Reseved butn2')
    
    if (butu == 0 and butc == 0):
        print('Reseved butn3')

    if (butd == 0 and butc == 0):
        print('Reseved butn4')
    
    if (butc == 0 and butl == 1 and butr == 1 and butu == 1 and butd ==1):
        print('Center Push')
        device.emit_click(uinput.KEY_ENTER)

GPIO.add_event_detect(rot_a, GPIO.BOTH, callback=on_rot)
GPIO.add_event_detect(rot_b, GPIO.BOTH, callback=on_rot)
GPIO.add_event_detect(but_l, GPIO.BOTH, callback=on_but)
GPIO.add_event_detect(but_r, GPIO.BOTH, callback=on_but)
GPIO.add_event_detect(but_u, GPIO.BOTH, callback=on_but)
GPIO.add_event_detect(but_d, GPIO.BOTH, callback=on_but)
GPIO.add_event_detect(but_c, GPIO.BOTH, callback=on_cen)
try:
    while True:
        sleep(3600)
except KeyboardInterrupt:
    print("...DONE")
    GPIO.cleanup()

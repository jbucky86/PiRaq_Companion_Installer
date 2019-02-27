
import RPi.GPIO as GPIO
import uinput
import os
import socket
from time import sleep

UDP_IP = "127.0.0.1"
UDP_PORT = 51235
MESSAGE_push = "BANK-DOWN 99 12"
MESSAGE_rel = "BANK-UP 99 12"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

rot_a = 22
rot_b = 24
but_l = 26
but_r = 20
but_u = 21
but_d = 25
but_c = 23

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

device = uinput.Device([uinput.KEY_UP, uinput.KEY_DOWN,  uinput.KEY_HOME,  uinput.KEY_END, uinput.KEY_LEFTCTRL, uinput.KEY_KPPLUS, uinput.KEY_KPMINUS])

seq_a = seq_b = 0

def on_rot(pin):
    global seq_a, seq_b
    a = GPIO.input(rot_a)
    b = GPIO.input(rot_b)
    butd = GPIO.input(but_d)
    seq_a = ((seq_a << 1) | a) & 0b1111
    seq_b = ((seq_b << 1) | b) & 0b1111
    if seq_a == 0b0011 and seq_b == 0b1001 and butd == 1:
        device.emit_click(uinput.KEY_UP)
    
    if seq_a == 0b1001 and seq_b == 0b0011 and butd == 1:
        device.emit_click(uinput.KEY_DOWN)
    
    if seq_a == 0b0011 and seq_b == 0b1001 and butd == 0:
        device.emit_combo([uinput.KEY_LEFTCTRL, uinput.KEY_KPPLUS])

    if seq_a == 0b1001 and seq_b == 0b0011 and butd == 0:
        device.emit_combo([uinput.KEY_LEFTCTRL, uinput.KEY_KPMINUS])


def on_but(pin):
    butl = GPIO.input(but_l)
    butr = GPIO.input(but_r)
    butu = GPIO.input(but_u)
    butd = GPIO.input(but_d)
    butc = GPIO.input(but_c)
    if (butl == 0):
          device.emit_click(uinput.KEY_HOME)

    if (butr == 0):
          device.emit_click(uinput.KEY_END)

    if (butu == 0):
        device.emit_click(uinput.KEY_UP)
        device.emit_click(uinput.KEY_UP)
        device.emit_click(uinput.KEY_UP)
        device.emit_click(uinput.KEY_UP)
        device.emit_click(uinput.KEY_UP)
        device.emit_click(uinput.KEY_UP)
        device.emit_click(uinput.KEY_UP)
        device.emit_click(uinput.KEY_UP)
        device.emit_click(uinput.KEY_UP)
        device.emit_click(uinput.KEY_UP)

    if (butd == 0):
        device.emit_click(uinput.KEY_DOWN)
        device.emit_click(uinput.KEY_DOWN)
        device.emit_click(uinput.KEY_DOWN)
        device.emit_click(uinput.KEY_DOWN)
        device.emit_click(uinput.KEY_DOWN)
        device.emit_click(uinput.KEY_DOWN)
        device.emit_click(uinput.KEY_DOWN)
        device.emit_click(uinput.KEY_DOWN)
        device.emit_click(uinput.KEY_DOWN)
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
        print('Defalt IP')
        os.system('sudo cp /home/pi/companionipdhcp /etc/network/interfaces')
        os.system('sudo reboot')
    
    if (butr == 0 and butc == 0):
        print('DHCP IP')
        os.system('sudo cp /home/pi/companionipstatic /etc/network/interfaces')
        os.system('sudo reboot')
    
    if (butu == 0 and butc == 0):
        print('Reseved butn1')

    if (butd == 0 and butc == 0):
        print('Reseved butn2')
    
    if (butc == 0 and butl == 1 and butr == 1 and butu == 1 and butd ==1):
        print('Center Push')
        sock.sendto(MESSAGE_push, (UDP_IP, UDP_PORT))
    elif (butc == 1 and butl == 1 and butr == 1 and butu == 1 and butd == 1):
        print('Center Rel')
        sock.sendto(MESSAGE_rel, (UDP_IP, UDP_PORT))

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

import board
import digitalio
import time
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
import analogio
from adafruit_hid.mouse import Mouse
#set up the device as a human input device or (H.I.D) of type Mouse
m = Mouse(usb_hid.devices)
potentiometerY = analogio.AnalogIn(board.A1)
potentiometerX = analogio.AnalogIn(board.A0)
#set up the device as a human input device or (H.I.D) of type Keyboard
kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)
#Assigning each row a corresponding pin on the microcontroller
row1 = digitalio.DigitalInOut(board.GP1)
row2 = digitalio.DigitalInOut(board.GP2)
row3 = digitalio.DigitalInOut(board.GP3)
#Setting each row as an output
row1.direction = digitalio.Direction.OUTPUT
row2.direction = digitalio.Direction.OUTPUT
row3.direction = digitalio.Direction.OUTPUT
#switching each row off for now
row1.value = False
row2.value = False
row3.value = False

#Assigning each column a corresponding pin on the microcontroller
column1 = digitalio.DigitalInOut(board.GP4)
column2 = digitalio.DigitalInOut(board.GP5)
column3 = digitalio.DigitalInOut(board.GP6)
column4 = digitalio.DigitalInOut(board.GP7)
column5 = digitalio.DigitalInOut(board.GP8)
column6 = digitalio.DigitalInOut(board.GP9)
#Setting each column as an input
column1.switch_to_input(pull=digitalio.Pull.DOWN)
column2.switch_to_input(pull=digitalio.Pull.DOWN)
column3.switch_to_input(pull=digitalio.Pull.DOWN)
column4.switch_to_input(pull=digitalio.Pull.DOWN)
column5.switch_to_input(pull=digitalio.Pull.DOWN)
column6.switch_to_input(pull=digitalio.Pull.DOWN)
#Subroutines that use the current from the potentiometres to calculate an integer.
#which can be used as the velocity of the mouse pointer in the X and Y axis.
def get_voltageX(pin):
    valueX= ((pin.value * 3.3) / 65536-1.65)/1.6
    if -.02<valueX<.02:
        valueX=0
    valueX= int(round(valueX,1)*10)
    return valueX

def get_voltageY(pin):
    valueY=((pin.value * 3.3) / 65536-1.64)/1.6
    if -.02<valueY<.02:
        valueY=0
    valueY= int(round(valueY,1)*-10)
    return valueY
#test to check the script has set up properly
print(row1.value)
print(column1.value)
#Here I am creating a list of keys that have been pressed last cycle and are pressed in the current cycle
#to determine whether a key is held down or needs to be released
CurrentLST = []
PreviousLST = []
#I like to have fun with variable names and so the variable Lies can be either true of false...
Lies = True
while Lies == True:
    PreviousLST = CurrentLST
    CurrentLST = []
    #Here the first rail is electrified and a current is passed through it
    #allowing the code to see if any buttons are closed on that row.
    #if the switches are closed they are added to a list of keys to hold down.
    row1.value = True
    if (column1.value) == True:
        CurrentLST.append(41)#Escape
    if (column2.value) == True:
        CurrentLST.append(20)#Q
    if (column3.value) == True:
        CurrentLST.append(26)#W 
    if (column4.value) == True:
        CurrentLST.append(8)#E8
    if (column5.value) == True:
        CurrentLST.append(21)#R 
    if (column6.value) == True:
        CurrentLST.append(23)#T
    row1.value = False
    #Rail 1 is deactivated and row 2 is Activated and then repeated for the third rail
    row2.value = True
    if (column1.value) == True:
        CurrentLST.append(225)#Shift
    if (column2.value) == True:
        CurrentLST.append(4)#A
    if (column3.value) == True:
        CurrentLST.append(22)#S
    if (column4.value) == True:
        CurrentLST.append(7)#D
    if (column5.value) == True:
        CurrentLST.append(9)#F
    if (column6.value) == True:
        CurrentLST.append(10)#G
    row2.value = False
    row3.value = True
    if (column1.value) == True:
        CurrentLST.append(224)#CTRL
    if (column2.value) == True:
        m.press(Mouse.LEFT_BUTTON)#Left click
    if (column2.value) == False:
        m.release(Mouse.LEFT_BUTTON)
    if (column3.value) == True:
        CurrentLST.append(44)#SPACE
    if (column4.value) == True:
        CurrentLST.append(27)#X
    if (column5.value) == True:
        CurrentLST.append(6)#C
    if (column6.value) == True:
        CurrentLST.append(25)#V
    row3.value = False
    #each key is held down from the list.
    for each in CurrentLST:
        kbd.press(each)
    release = []
    #the list of keys is checked against the list from the previous cycle.
    #and then keys that are no longer in the list are released
    for Pre in PreviousLST:
        Check = False
        for Current in CurrentLST:
            if int(Current) == int(Pre):
                Check = True
        if Check == False:
            release.append(Pre)
    for each in release:
        kbd.release(each)
    #this section uses subroutines to calculate the velocity of the mouse
    Y=get_voltageY(potentiometerY)
    X=get_voltageX(potentiometerX)
    #and then send the mouse in that direction
    m.move(X,Y,0)
    #the program cycles every 100ths of a second so the approximate speed is 100Hz
    time.sleep(0.01)
        
Lies = False
#

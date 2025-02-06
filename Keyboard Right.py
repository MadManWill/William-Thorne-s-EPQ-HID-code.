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
row1 = digitalio.DigitalInOut(board.GP2)
row2 = digitalio.DigitalInOut(board.GP8)
row3 = digitalio.DigitalInOut(board.GP15)
#Setting each row as an output
row1.direction = digitalio.Direction.OUTPUT
row2.direction = digitalio.Direction.OUTPUT
row3.direction = digitalio.Direction.OUTPUT
#switching each row off for now
row1.value = False
row2.value = False
row3.value = False

#Assigning each column a corresponding pin on the microcontroller
column1 = digitalio.DigitalInOut(board.GP17)
column2 = digitalio.DigitalInOut(board.GP19)
column3 = digitalio.DigitalInOut(board.GP20)#w
column4 = digitalio.DigitalInOut(board.GP7)
column5 = digitalio.DigitalInOut(board.GP5)
column6 = digitalio.DigitalInOut(board.GP3)
#Setting each column as an input
column1.switch_to_input(pull=digitalio.Pull.DOWN)
column2.switch_to_input(pull=digitalio.Pull.DOWN)
column3.switch_to_input(pull=digitalio.Pull.DOWN)
column4.switch_to_input(pull=digitalio.Pull.DOWN)
column5.switch_to_input(pull=digitalio.Pull.DOWN)
column6.switch_to_input(pull=digitalio.Pull.DOWN)

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
    row2.value= True
    if column5.value == True:
        row2.value= False
        row1.value = True
        if (column1.value) == True:
            CurrentLST.append(30)#1
        if (column2.value) == True:
            CurrentLST.append(31)#2 
        if (column3.value) == True:
            CurrentLST.append(32)#3 
        if (column4.value) == True:
            CurrentLST.append(33)#4 
        if (column5.value) == True:
            CurrentLST.append(34)#5
        if (column6.value) == True:
            CurrentLST.append(35)#6
        row1.value = False
        #Rail 1 is deactivated and row 2 is Activated and then repeated for the third rail
        row2.value = True
        if (column1.value) == True:
            CurrentLST.append(36)#7
        if (column2.value) == True:
            CurrentLST.append(37)#8
        if (column3.value) == True:
            CurrentLST.append(38)#9
        if (column4.value) == True:
            CurrentLST.append(39)#0
        #Row 2 Column 5 is my special key to switch to punctuation mode
        if (column6.value) == True:
            CurrentLST.append(40)#Enter
        row2.value = False
        row3.value = True
        if (column1.value) == True:
            CurrentLST.append(51)#;
        if (column2.value) == True:
            CurrentLST.append(52)#'
        if (column3.value) == True:
            CurrentLST.append(50)##
        if (column4.value) == True:
            CurrentLST.append(56)#/
        if (column5.value) == True:
            CurrentLST.append(54)#Comma
        if (column6.value) == True:
            CurrentLST.append(55)#Full Stop
        row3.value = False
    else:
        row2.value= False
        row1.value = True
        if (column1.value) == True:
            CurrentLST.append(28)#Y 
        if (column2.value) == True:
            CurrentLST.append(24)#U 
        if (column3.value) == True:
            CurrentLST.append(12)#I 
        if (column4.value) == True:
            CurrentLST.append(18)#O 
        if (column5.value) == True:
            CurrentLST.append(19)#P
        if (column6.value) == True:
            CurrentLST.append(42)#Backspace
        row1.value = False
        #Rail 1 is deactivated and row 2 is Activated and then repeated for the third rail
        row2.value = True
        if (column1.value) == True:
            CurrentLST.append(11)#H
        if (column2.value) == True:
            CurrentLST.append(13)#J
        if (column3.value) == True:
            CurrentLST.append(14)#K
        if (column4.value) == True:
            CurrentLST.append(15)#L
        #Row 2 Column 5 is my special key to switch to punctuation mode
        if (column6.value) == True:
            CurrentLST.append(40)#Enter
        row2.value = False
        row3.value = True
        if (column1.value) == True:
            CurrentLST.append(25)#V
        if (column2.value) == True:
            CurrentLST.append(5)#B
        if (column3.value) == True:
            CurrentLST.append(17)#N
        if (column4.value) == True:
            CurrentLST.append(16)#M
        if (column5.value) == True:
            CurrentLST.append(54)#Comma
        if (column6.value) == True:
            CurrentLST.append(55)#Full Stop
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
    #the program cycles every 100ths of a second so the approximate speed is 100Hz
    time.sleep(0.01)
        
Lies = False
#

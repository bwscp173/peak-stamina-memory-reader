import pygetwindow as gw
import time
import keyboard
import tkinter as tk
from tkinter import messagebox
from pymem import Pymem,process


def getWindow(title:str) -> gw.Win32Window:
    win:gw.Win32Window

    for win in gw.getAllWindows():
        #print(type(win),win)
        if win.title == title:
            return win
        
    raise Exception("process is not open")


def pointer_chain(base_pointer:int, offsets:list) -> int:
    newListOffsets = offsets[ :- 1]
    lenght = len(newListOffsets)

    for i in newListOffsets:
        # print("starting to read to N",hex(base_pointer))
        base_pointer = pm.read_longlong(base_pointer + i)
        # print("basepointer -", hex(base_pointer))
        # print(f"i - {hex(i)} - {i}")
        # print("both - ", hex(base_pointer+i))

    #print(f"The base pointer is : {hex(base_pointer) }")
    #value = pm.read_longlong(base_pointer + offsets[-1])
    #print(f"The value of that address is: {value}")
    address = base_pointer + offsets[-1]
    #print(f"The address of that value is : {hex(address) }")
    return address


title = "PEAK" #Untitled - Notepad"
try:
    window = getWindow(title)
    print(type(window))
except Exception as E:
    messagebox.showerror(f"get '{title}' window error :(",E)
    exit(code=-1)

pm = Pymem('PEAK.exe')
print("got game")
print("base address: ",hex(pm.base_address))

unityplayer = process.module_from_name(pm.process_handle, "UnityPlayer.dll").lpBaseOfDll
print("UnityPlayer.dll base address:", hex(unityplayer))

player_base = pm.read_longlong(unityplayer + 0x01EEED90)#0x3000905A4D #0x1E190008740#pm.read_int(unityplayer + 0x01EEED90)
print("player_base:",hex(player_base))

#0x3000905A4D
#player_object_offsets = [0x60,0x0,0x040,0xEA0,0x88,0x30,0x0]
#print("player_object_offsets:",player_object_offsets)

player_sprint_offsets = [0x60,0x0,0x040,0xEA0,0x88,0x30,0x198]
print("player_sprint_offsets:",player_sprint_offsets)

sprint_addy = pointer_chain(player_base,player_sprint_offsets)
print("sprint_addy:",hex(sprint_addy))



hotkey = "g"
inital_sprint = None
final_sprint = None

running = True

while running:
    #print(f"waiting for '{hotkey}'")
    if keyboard.is_pressed(hotkey):
        print("was pressed")
        if inital_sprint is None:
            inital_sprint = pm.read_float(sprint_addy)
            print(inital_sprint,final_sprint)

        elif final_sprint is None:
            final_sprint = pm.read_float(sprint_addy)
            print(inital_sprint,final_sprint)

            print(100 - (final_sprint / inital_sprint) * 100)

            inital_sprint = None
            final_sprint = None

        print(f"waiting for '{hotkey}' again")

    if keyboard.is_pressed("esc"):
        running = False
    #time.sleep(0.1)

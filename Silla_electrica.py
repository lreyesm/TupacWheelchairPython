#!/usr/bin/env python3


import RPi.GPIO as GPIO
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pickle
import serial
import math
import threading
import time
import sys, os
from functools import partial

WINDOWWIDTH=800
WINDOWHEIGHT=480


# VARIABLES DE PUERTO SERIE ----------------------------------------------------------------------------------------

ser = serial.Serial('/dev/serial0',baudrate=115200,timeout = 9,bytesize = serial.EIGHTBITS,parity = serial.PARITY_NONE,stopbits = serial.STOPBITS_ONE,rtscts=False)

send_bytes = []
uart_busy = False
running_program=True
recibo_perfecto=False
valor_recibido = []

speed_indicator_names=['speeed_1.png','speeed_2.png','speeed_3.png','speeed_4.png','speeed_5.png']
speed_indicator_value=0

def N_function(z,xcor, ycor):



##     print('N_function')
     if xcor == 200 and ycor < 200:
          
          return True
     else:
          
          return False

def S_function(z,xcor, ycor):

##     print('S_function')


     if xcor == 200 and ycor > 200:
          
          return True
     else:
          
          return False

def E_function(z,xcor, ycor):
##     print('E_function')


     if ycor == 200 and xcor > 200:
          
          return True
     else:
          
          return False

def W_function(z,xcor, ycor):
##     print('W_function')


     if xcor < 200 and ycor == 200  :
          
          return True
     else:
          
          return False

def NE_function(z,xcor, ycor):


     if xcor > 200 and ycor == 400 - xcor  :
          
          return True
     else:
          
          return False
     
def NE7_function(z,xcor, ycor):

     if  xcor > 200 and ycor ==  xcor*(-4) + 1000 :
          
          return True
     else:
          
          return False

def NE6_function(z,xcor, ycor):
    # print('NE6_function **************************************************')


     if  xcor > 200 and ycor ==  xcor*(-2) + 600:
          
          return True
     else:
          
          return False

def NE5_function(z,xcor, ycor):
    # print('NE6_function **************************************************')


     if  xcor > 200 and 3*ycor ==  xcor*(-4) + 1400:
          
          return True
     else:
          
          return False

def NE3_function(z,xcor, ycor):
##     print('NE3_function **************************************************')


     if  xcor > 200 and 20*ycor ==  xcor*(-15) + 7000:
          
          return True
     else:
          
          return False

def NE2_function(z,xcor, ycor):
##     print('NE2_function **************************************************')


     if  xcor > 200 and 4*ycor ==  (-1)*xcor + 800:
          
          return True
     else:
          
          return False

def NE1_function(z,xcor, ycor):
##     print('NE2_function **************************************************')


     if  xcor > 200 and 4*ycor ==  (-1)*xcor + 1000:
          
          return True
     else:
          
          return False
     
def NW_function(z,xcor, ycor):


     if ycor == xcor and ycor < 200:
          
          return True
     else:
          
          return False

def SW_function(z,xcor, ycor):


     if  ycor > 200 and 400 - ycor == xcor :
          
          return True
     else:
          
          return False
     
def SE_function(z,xcor, ycor):


     if  ycor > 200 and ycor == xcor :
          
          return True
     else:
          
          return False
     
timon_position_ranges = []

timon_position_ranges.append({"cardinal": 'timon_N.png',"xmin": 175, "ymin": 0, "xmax": 225,"ymax": 200,"xcor": 124,"ycor": 167})
timon_position_ranges.append({"cardinal": 'timon_S.png',"xmin": 175, "ymin": 201, "xmax": 225,"ymax": 400,"xcor": 124,"ycor": 1})
timon_position_ranges.append({"cardinal": 'timon_E.png',"xmin": 226, "ymin": 175, "xmax": 400,"ymax": 225,"xcor": 168,"ycor": 123})
timon_position_ranges.append({"cardinal": 'timon_W.png',"xmin": 0, "ymin": 175, "xmax": 174,"ymax": 225,"xcor": 1,"ycor": 123})

timon_position_ranges.append({"cardinal": 'timon_NE.png',"xmin": 225, "ymin": 150, "xmax": 250,"ymax": 175,"xcor": 168,"ycor": 167})
timon_position_ranges.append({"cardinal": 'timon_NE.png',"xmin": 250, "ymin": 100, "xmax": 300,"ymax": 150,"xcor": 168,"ycor": 167})
timon_position_ranges.append({"cardinal": 'timon_NE.png',"xmin": 300, "ymin": 50, "xmax": 350,"ymax": 100,"xcor": 168,"ycor": 167})
timon_position_ranges.append({"cardinal": 'timon_NE.png',"xmin": 350, "ymin": 0, "xmax": 400,"ymax": 50,"xcor": 168,"ycor": 167})
timon_position_ranges.append({"cardinal": 'timon_NE6.png',"xmin": 225, "ymin": 50, "xmax": 300,"ymax": 100,"xcor": 146,"ycor": 167})
timon_position_ranges.append({"cardinal": 'timon_NE6.png',"xmin": 225, "ymin": 100, "xmax": 250,"ymax": 150,"xcor": 146,"ycor": 167})
timon_position_ranges.append({"cardinal": 'timon_NE6.png',"xmin": 225, "ymin": 0, "xmax": 350,"ymax": 50,"xcor": 146,"ycor": 167})
timon_position_ranges.append({"cardinal": 'timon_NE2.png',"xmin": 300, "ymin": 100, "xmax": 400,"ymax": 150,"xcor": 168,"ycor": 146})
timon_position_ranges.append({"cardinal": 'timon_NE2.png',"xmin": 350, "ymin": 50, "xmax": 400,"ymax": 100,"xcor": 168,"ycor": 146})
timon_position_ranges.append({"cardinal": 'timon_NE2.png',"xmin": 250, "ymin": 150, "xmax": 400,"ymax": 175,"xcor": 168,"ycor": 146})

timon_position_ranges.append({"cardinal": 'timon_NW.png',"xmin": 150, "ymin": 150, "xmax": 175,"ymax": 175,"xcor": 1,"ycor": 167})
timon_position_ranges.append({"cardinal": 'timon_NW.png',"xmin": 100, "ymin": 100, "xmax": 150,"ymax": 150,"xcor": 1,"ycor": 167})
timon_position_ranges.append({"cardinal": 'timon_NW.png',"xmin": 50, "ymin": 50, "xmax": 100,"ymax": 100,"xcor": 1,"ycor": 167})
timon_position_ranges.append({"cardinal": 'timon_NW.png',"xmin": 0, "ymin": 0, "xmax": 50,"ymax": 50,"xcor": 1,"ycor": 167})
timon_position_ranges.append({"cardinal": 'timon_NW2.png',"xmin": 0, "ymin": 150, "xmax": 150,"ymax": 175,"xcor": 61,"ycor": 167})
timon_position_ranges.append({"cardinal": 'timon_NW2.png',"xmin": 0, "ymin": 100, "xmax": 100,"ymax": 150,"xcor":61,"ycor": 167})
timon_position_ranges.append({"cardinal": 'timon_NW2.png',"xmin": 0, "ymin": 50, "xmax": 50,"ymax": 100,"xcor": 61,"ycor": 167})
timon_position_ranges.append({"cardinal": 'timon_NW6.png',"xmin": 50, "ymin": 0, "xmax": 175,"ymax": 50,"xcor": 1,"ycor": 146})
timon_position_ranges.append({"cardinal": 'timon_NW6.png',"xmin": 100, "ymin": 50, "xmax": 175,"ymax": 100,"xcor": 1,"ycor": 146})
timon_position_ranges.append({"cardinal": 'timon_NW6.png',"xmin": 150, "ymin": 100, "xmax": 175,"ymax": 150,"xcor": 1,"ycor": 146})

timon_position_ranges.append({"cardinal": 'timon_SE.png',"xmin": 350, "ymin": 350, "xmax": 400,"ymax": 400,"xcor": 168,"ycor": 1,})
timon_position_ranges.append({"cardinal": 'timon_SE.png',"xmin": 225, "ymin": 225, "xmax": 250,"ymax": 250,"xcor": 168,"ycor": 1,})
timon_position_ranges.append({"cardinal": 'timon_SE.png',"xmin": 250, "ymin": 250, "xmax": 300,"ymax": 300,"xcor": 168,"ycor": 1,})
timon_position_ranges.append({"cardinal": 'timon_SE.png',"xmin": 300, "ymin": 300, "xmax": 350,"ymax": 350,"xcor": 168,"ycor": 1,})
timon_position_ranges.append({"cardinal": 'timon_SE6.png',"xmin": 225, "ymin": 225, "xmax": 400,"ymax": 250,"xcor": 146,"ycor": 1,})
timon_position_ranges.append({"cardinal": 'timon_SE6.png',"xmin": 300, "ymin": 250, "xmax": 400,"ymax": 300,"xcor": 146,"ycor": 1,})
timon_position_ranges.append({"cardinal": 'timon_SE6.png',"xmin": 350, "ymin": 300, "xmax": 400,"ymax": 350,"xcor": 146,"ycor": 1,})
timon_position_ranges.append({"cardinal": 'timon_SE2.png',"xmin": 225, "ymin": 250, "xmax": 250,"ymax": 400,"xcor": 168,"ycor": 61,})
timon_position_ranges.append({"cardinal": 'timon_SE2.png',"xmin": 250, "ymin": 300, "xmax": 300,"ymax": 400,"xcor": 168,"ycor": 61,})
timon_position_ranges.append({"cardinal": 'timon_SE2.png',"xmin": 300, "ymin": 350, "xmax": 350,"ymax": 400,"xcor": 168,"ycor": 61,})

timon_position_ranges.append({"cardinal": 'timon_SW.png',"xmin": 150, "ymin": 225, "xmax": 175,"ymax": 250,"xcor": 1,"ycor": 1})
timon_position_ranges.append({"cardinal": 'timon_SW.png',"xmin": 100, "ymin": 250, "xmax": 150,"ymax": 300,"xcor": 1,"ycor": 1})
timon_position_ranges.append({"cardinal": 'timon_SW.png',"xmin": 50, "ymin": 300, "xmax": 100,"ymax": 350,"xcor": 1,"ycor": 1})
timon_position_ranges.append({"cardinal": 'timon_SW.png',"xmin": 0, "ymin": 350, "xmax": 50,"ymax": 400,"xcor": 1,"ycor": 1})
timon_position_ranges.append({"cardinal": 'timon_SW2.png',"xmin": 0, "ymin": 225, "xmax": 150,"ymax": 250,"xcor": 1,"ycor": 61})
timon_position_ranges.append({"cardinal": 'timon_SW2.png',"xmin": 0, "ymin": 250, "xmax": 100,"ymax": 300,"xcor": 1,"ycor": 61})
timon_position_ranges.append({"cardinal": 'timon_SW2.png',"xmin": 0, "ymin": 300, "xmax": 50,"ymax": 350,"xcor": 1,"ycor": 61})
timon_position_ranges.append({"cardinal": 'timon_SW6.png',"xmin": 150, "ymin": 250, "xmax": 175,"ymax": 400,"xcor": 61,"ycor": 1})
timon_position_ranges.append({"cardinal": 'timon_SW6.png',"xmin": 100, "ymin": 300, "xmax": 175,"ymax": 350,"xcor": 61,"ycor": 1})
timon_position_ranges.append({"cardinal": 'timon_SW6.png',"xmin": 50, "ymin": 175, "xmax": 350,"ymax": 400,"xcor": 61,"ycor": 1})

"""
timon_position_ranges.append({"cardinal": 'timon_N.png',"xmin": 150, "ymin": 0, "xmax": 250,"ymax": 200,"xcor": 124,"ycor": 167,"function": partial(N_function,2)})
timon_position_ranges.append({"cardinal": 'timon_S.png',"xmin": 150, "ymin": 201, "xmax": 250,"ymax": 400,"xcor": 124,"ycor": 1,"function": partial(S_function,2)})
timon_position_ranges.append({"cardinal": 'timon_E.png',"xmin": 201, "ymin": 150, "xmax": 400,"ymax": 250,"xcor": 168,"ycor": 123,"function": partial(E_function,2)})

timon_position_ranges.append({"cardinal": 'timon_W.png',"xmin": 0, "ymin": 150, "xmax": 200,"ymax": 250,"xcor": 1,"ycor": 123,"function": partial(W_function,2)})

timon_position_ranges.append({"cardinal": 'timon_NE.png',"xmin": 250, "ymin": 0, "xmax": 400,"ymax": 150,"xcor": 168,"ycor": 167,"function": partial(NE_function,2)})
timon_position_ranges.append({"cardinal": 'timon_NE7.png',"xmin": 250, "ymin": 0, "xmax": 400,"ymax": 150,"xcor": 168,"ycor": 167,"function": partial(NE7_function,2)})
timon_position_ranges.append({"cardinal": 'timon_NE6.png',"xmin": 250, "ymin": 0, "xmax": 400,"ymax": 150,"xcor": 168,"ycor": 167,"function": partial(NE6_function,2)})
timon_position_ranges.append({"cardinal": 'timon_NE5.png',"xmin": 250, "ymin": 0, "xmax": 400,"ymax": 150,"xcor": 168,"ycor": 167,"function": partial(NE5_function,2)})
timon_position_ranges.append({"cardinal": 'timon_NE3.png',"xmin": 250, "ymin": 0, "xmax": 400,"ymax": 150,"xcor": 168,"ycor": 167,"function": partial(NE3_function,2)})
timon_position_ranges.append({"cardinal": 'timon_NE2.png',"xmin": 250, "ymin": 0, "xmax": 400,"ymax": 150,"xcor": 168,"ycor": 167,"function": partial(NE2_function,2)})
timon_position_ranges.append({"cardinal": 'timon_NE1.png',"xmin": 250, "ymin": 0, "xmax": 400,"ymax": 150,"xcor": 168,"ycor": 167,"function": partial(NE1_function,2)})

timon_position_ranges.append({"cardinal": 'timon_NW.png',"xmin": 0, "ymin": 0, "xmax": 150,"ymax": 150,"xcor": 1,"ycor": 167,"function": partial(NW_function,2)})

timon_position_ranges.append({"cardinal": 'timon_SE.png',"xmin": 250, "ymin": 250, "xmax": 400,"ymax": 400,"xcor": 168,"ycor": 1,"function": partial(SE_function,2)})

timon_position_ranges.append({"cardinal": 'timon_SW.png',"xmin": 0, "ymin": 250, "xmax": 150,"ymax": 400,"xcor": 1,"ycor": 1,"function": partial(SW_function,2)})
"""

class Audiometro:
     def __init__(self,master):

        self.style=ttk.Style()
        self.style.theme_use('clam')
        self.style.configure( 'TFrame',background = '#ffffff')
        self.style.configure( 'TLabelFrame',background = '#ffffff')
        self.style.configure( 'TButton',background = '#ffffff')
        self.style.configure( 'TLabel',background = '#494949')
        self.style.configure( 'TCheckbutton',background = '#ffffff',font = ('Droid Naskh Shift Alt',12,'bold'), foreground = 'green')
             
        self.main_frame = ttk.Frame(master)
        self.main_frame.pack()
        self.main_frame.config(width = WINDOWWIDTH, height=WINDOWHEIGHT)
        #self.photo_fondo=PhotoImage(file = 'photos_silla/fondo.png') 
        #self.main_frame.config(image=self.photo_fondo)
        self.main_frame.bind('<ButtonPress-1>', self.on_timon_pressed)
        self.main_frame.bind('<ButtonPress-2>', self.on_B2_pressed_emergency)
        self.main_frame.bind('<ButtonPress-3>', self.on_mouse_B3_pressed)
        self.main_frame.bind('<B3-Motion>', self.on_mouse_movement_B3_hold)
        self.main_frame.bind('<ButtonRelease-3>', self.on_mouse_movement_B3_release)

        self.global_y_pos=0
        self.global_y_pos_init=0
        self.global_x_pos=0
        self.global_x_pos_init=0
        self.indicator_actual_pos_x=0.56
        self.indicator_actual_pos_y=0.38
        self.state=False
        self.first_move = True
        self.binding_state = True
        self.actual_timon_image = 'photos_silla/timon_480.png'
        self.last_timon_image = 'photos_silla/timon_480.png'
        self.actual_timon_image_pos=0
        self.first_x=200
        self.first_y=200
        
        self.label_quit_button=ttk.Label(self.main_frame)  # label edad value
        self.label_quit_button.place(relx=0.93,rely=0.9)
        self.label_quit_button.config(background = 'white', width = 5)
        self.photo_quit=PhotoImage(file = 'photos_silla/salir_red.png') 
        self.label_quit_button.config(compound = 'center', image=self.photo_quit)
        self.label_quit_button.bind('<ButtonPress-2>', self.on_B2_pressed_emergency)
        self.label_quit_button.bind('<ButtonPress-1>', lambda e: self.on_quit(master))

        self.label_led_button=ttk.Label(self.main_frame)  # label edad value
        self.label_led_button.place(relx=0.85,rely=0.9)
        self.label_led_button.config(background = 'white', width = 5)
        self.photo_led=PhotoImage(file = 'photos_silla/led_off.png') 
        self.label_led_button.config(compound = 'center', image=self.photo_led)
        self.label_led_button.bind('<ButtonPress-2>', self.on_B2_pressed_emergency)
        self.label_led_button.bind('<ButtonPress-1>', self.on_led_button)
        self.label_led_button.bind('<ButtonRelease-1>', self.on_led_release)

                
        self.label_off_button=ttk.Label(self.main_frame)  # label edad value
        self.label_off_button.place(relx=0.1,rely=0.45)
        self.label_off_button.config(foreground = 'white',background = 'white')
        self.photo_off=PhotoImage(file = 'photos_silla/speeed.png') 
        self.label_off_button.config(compound = 'center', image=self.photo_off)
        self.label_off_button.bind('<ButtonPress-2>', self.on_B2_pressed_emergency)     
        self.label_off_button.bind('<ButtonPress-1>', self.on_on_button)

        self.label_claxon_button=ttk.Label(self.main_frame)  # label edad value
        self.label_claxon_button.place(relx=0.169,rely=0.31)
        self.label_claxon_button.config(foreground = 'white',background = 'white')
        self.photo_claxon=PhotoImage(file = 'photos_silla/claxon.png')  #my_icons/off.png
        self.label_claxon_button.config(compound = 'center', image=self.photo_claxon)
        self.label_claxon_button.bind('<ButtonPress-1>', self.on_claxon_button)
        self.label_claxon_button.bind('<ButtonPress-2>', self.on_B2_pressed_emergency)         
        self.label_claxon_button.bind('<ButtonRelease-1>', self.on_claxon_release)


        self.label_logo=ttk.Label(self.main_frame)  # label edad value
        self.label_logo.place(relx=0.01,rely=0.01)
        self.label_logo.config(foreground = 'white',background = 'white')
        self.photo_logo=PhotoImage(file = 'photos_silla/logo.png')  #my_icons/off.png
        self.label_logo.bind('<ButtonPress-2>', self.on_B2_pressed_emergency)  
        self.label_logo.config(compound = 'center', image=self.photo_logo)

        self.label_higher_button=ttk.Label(self.main_frame)  # label edad value
        self.label_higher_button.place(relx=0.39,rely=0.525)
        self.label_higher_button.config(foreground = 'white',background = 'white')
        self.photo_aumentar=PhotoImage(file = 'photos_silla/up.png')  #my_icons/off.png
        self.label_higher_button.config(compound = 'center', image=self.photo_aumentar)
        self.label_higher_button.bind('<ButtonPress-1>', self.on_higher)
        self.label_higher_button.bind('<ButtonPress-2>', self.on_B2_pressed_emergency)
        self.label_higher_button.bind('<ButtonRelease-1>', self.on_higher_release)

        self.label_lower_button=ttk.Label(self.main_frame)  # label edad value
        self.label_lower_button.place(relx=0.005,rely=0.53)
        self.label_lower_button.config(foreground = 'white',background = 'white')
        self.photo_disminuir=PhotoImage(file = 'photos_silla/down.png')  
        self.label_lower_button.config(compound = 'center', image=self.photo_disminuir)
        self.label_lower_button.bind('<ButtonPress-1>', self.on_lower)
        self.label_lower_button.bind('<ButtonPress-2>', self.on_B2_pressed_emergency)
        self.label_lower_button.bind('<ButtonRelease-1>', self.on_lower_release)

        self.label_dial=Canvas(self.main_frame)  # label edad value
        self.label_dial.config(width= 400, height = 400, background = 'white')
        self.label_dial.place(relx=0.49,rely=0.00)
        #self.label_dial.config(foreground= 'white')
        self.photo_dial=PhotoImage(file = 'photos_silla/timon_480.png')  #my_icons/off.png
        #self.label_dial.config(image=self.photo_dial)
        self.label_dial.create_image(200,200, image = self.photo_dial)
        self.label_dial.bind('<ButtonPress-1>', self.on_timon_pressed)
        self.label_dial.bind('<ButtonPress-3>', self.on_mouse_B3_pressed)
        self.label_dial.bind('<B3-Motion>', self.on_mouse_movement_B3_hold)
        self.label_dial.bind('<ButtonPress-2>', self.on_B2_pressed_emergency)
        self.label_dial.bind('<ButtonRelease-3>', self.on_mouse_movement_B3_release)

        self.label_indicator=ttk.Label(self.main_frame)  # label edad value
        self.label_indicator.place(relx=0.719, rely= 0.415)
        #self.label_indicator.config(background = '#494949')
        self.photo_indice=PhotoImage(file = 'photos_silla/move.png')  #my_icons/off.png
        self.label_indicator.config(compound = 'center', image=self.photo_indice)
        self.label_indicator.bind('<ButtonPress-1>', self.on_timon_pressed)
        self.label_indicator.bind('<ButtonPress-3>', self.on_mouse_B3_pressed)
        self.label_indicator.bind('<B3-Motion>', self.on_mouse_movement_B3_hold)
        self.label_indicator.bind('<ButtonPress-2>', self.on_B2_pressed_emergency)
        self.label_indicator.bind('<ButtonRelease-3>', self.on_mouse_movement_B3_release)

        """
        self.label_indicator=Canvas(self.main_frame)  # label edad value
        self.label_indicator.place(relx=0.72, rely=0.42)
        self.label_indicator.config(background = '#494949', width= 50, height = 50)
        self.photo_indice=PhotoImage(file = 'photos_silla/move.png')  #my_icons/off.png
        self.label_indicator.create_image(25,25,image=self.photo_indice)
        self.label_indicator.bind('<ButtonPress-1>', self.on_mouse_B3_pressed)
        self.label_indicator.bind('<B1-Motion>', self.on_mouse_movement_B3_hold)
        self.label_indicator.bind('<ButtonRelease-1>', self.on_mouse_movement_B3_release)
        """

        
        self.label_battery=ttk.Label(self.main_frame)  # label edad value
        self.label_battery.place(relx=0.63,rely=0.79)
        self.label_battery.config(foreground = 'white',background = 'white')
        self.photo_battery=PhotoImage(file = 'photos_silla/battery.png')  #my_icons/off.png
        self.label_battery.config(compound = 'center', image=self.photo_battery)

        self.label_chage_controls_button=ttk.Label(self.main_frame)  # label edad value
        self.label_chage_controls_button.place(relx=0.889,rely=0.0)
        self.photo_chage_controls=PhotoImage(file = 'photos_silla/mode_1.png')
        self.label_chage_controls_button.config(background = 'white', image = self.photo_chage_controls)
        self.label_chage_controls_button.bind('<ButtonPress-1>', self.on_change_controls_button)
        self.label_chage_controls_button.bind('<ButtonPress-2>', self.on_B2_pressed_emergency)

        """self.label_speed_indicator=ttk.Label(self.main_frame)  # label edad value
        self.label_speed_indicator.place(relx=0.2,rely=0.5)
        self.label_speed_indicator.config(foreground = 'white')
        self.photo_speed_indicator=PhotoImage(file = 'photos_silla/'+speed_indicator_names[1])  #my_icons/off.png
        self.label_speed_indicator.config(compound = 'center', image=self.photo_speed_indicator)
        #self.label_speed_indicator.bind('<ButtonPress-1>', lambda e: self.on_quit(master))"""

        
        """self.label_pos_indicator=ttk.Label(self.main_frame)  # label edad value
        self.label_pos_indicator.place(relx=0.1,rely=0.0)
        self.label_pos_indicator.config(foreground = 'red', text='posicion', font=('Droid Naskh Shift Alt',16,'bold'))
        
        self.label_pos_init_indicator=ttk.Label(self.main_frame)  # label edad value
        self.label_pos_init_indicator.place(relx=0.1,rely=0.1)
        self.label_pos_init_indicator.config(foreground = 'red', text='posicion inicial', font=('Droid Naskh Shift Alt',16,'bold'))
        """
        """self.label_pos_movement_indicator=ttk.Label(self.main_frame)  # label edad value
        self.label_pos_movement_indicator.place(relx=0.1,rely=0.2)
        self.label_pos_movement_indicator.config(foreground = 'red', text='movimiento '+str(math.asin(0.5)), font=('Droid Naskh Shift Alt',16,'bold'))
        """
        
        print('hola')

     """def on_indicador(self,event):

          self.label_pos_indicator.config(foreground = 'red', text='y: '+str(event.y)+'\n'+'x: '+str(event.x))
     """

     def on_B2_pressed_emergency(self, event):

          global send_bytes

          self.first_move=True

          if(self.binding_state == True):
              self.label_indicator.place(relx=0.719, rely= 0.415)

          uart_busy = True

          send_bytes = []

          send_bytes.append(77)
          send_bytes.append(77)
          send_bytes.append(0)
          send_bytes.append(0)


          values= bytearray(send_bytes)

          ser.write(values)

          uart_busy = False
          
     def on_change_controls_button(self, event):
          
          if (self.binding_state==True):
               
               
               self.binding_state=False
               self.change_binding()

               self.photo_chage_controls=PhotoImage(file = 'photos_silla/mode_2.png')
               self.label_chage_controls_button.config(background = 'white', image = self.photo_chage_controls)
               self.photo_dial=PhotoImage(file = 'photos_silla/timon.png')
               self.label_dial.create_image(200,200, image = self.photo_dial)
               self.label_indicator.place_forget()
               
          else:
               self.binding_state=True  
               self.change_binding()
               self.photo_chage_controls=PhotoImage(file = 'photos_silla/mode_1.png')
               self.label_chage_controls_button.config(background = 'white', image = self.photo_chage_controls)
              
          """self.label_S_button=ttk.Label(self.main_frame)  # label edad value
          self.label_S_button.place(relx=0.725,rely=0.64)
          self.label_S_button.config(background = 'blue', width = 3)
          self.label_S_button.bind('<ButtonPress-1>', self.on_change_controls_button)
          
          self.label_N_button=ttk.Label(self.main_frame)  # label edad value
          self.label_N_button.place(relx=0.725,rely=0.22)
          self.label_N_button.config(background = 'blue', width = 3)
          self.label_N_button.bind('<ButtonPress-1>', self.on_change_controls_button)

          self.label_E_button=ttk.Label(self.main_frame)  # label edad value
          self.label_E_button.place(relx=0.84,rely=0.435)
          self.label_E_button.config(background = 'blue', width = 3)
          self.label_E_button.bind('<ButtonPress-1>', self.on_change_controls_button)
          
          self.label_W_button=ttk.Label(self.main_frame)  # label edad value
          self.label_W_button.place(relx=0.6,rely=0.435)
          self.label_W_button.config(background = 'blue', width = 3)
          self.label_W_button.bind('<ButtonPress-1>', self.on_change_controls_button)
          
          self.label_NW_button=ttk.Label(self.main_frame)  # label edad value
          self.label_NW_button.place(relx=0.6625,rely=0.3275)
          self.label_NW_button.config(background = 'blue', width = 3)
          self.label_NW_button.bind('<ButtonPress-1>', self.on_change_controls_button)

          self.label_NE_button=ttk.Label(self.main_frame)  # label edad value
          self.label_NE_button.place(relx=0.7825,rely=0.3275)
          self.label_NE_button.config(background = 'blue', width = 3)
          self.label_NE_button.bind('<ButtonPress-1>', self.on_change_controls_button)

          self.label_SW_button=ttk.Label(self.main_frame)  # label edad value
          self.label_SW_button.place(relx=0.6625,rely=0.5425)
          self.label_SW_button.config(background = 'blue', width = 3)
          self.label_SW_button.bind('<ButtonPress-1>', self.on_change_controls_button)

          self.label_SE_button=ttk.Label(self.main_frame)  # label edad value
          self.label_SE_button.place(relx=0.7825,rely=0.5425)
          self.label_SE_button.config(background = 'blue', width = 3)
          self.label_SE_button.bind('<ButtonPress-1>', self.on_change_controls_button)
          """

     def on_quit(self,master):

          global running_program

          running_program = False

          ser.flushInput()
          ser.flushOutput()
          ser.close()
          time.sleep(0.1)
          master.destroy()
          #sys.exit()
          os._exit(1)
          

     def do_nothing(self,event):
          
          pass

     def change_binding(self):

          if(self.binding_state == True): #true es el estado inicial
               
               self.label_indicator.bind('<ButtonPress-1>', self.on_timon_pressed)
               self.label_indicator.bind('<ButtonPress-3>', self.on_mouse_B3_pressed)
               self.label_indicator.bind('<B3-Motion>', self.on_mouse_movement_B3_hold)
               self.label_indicator.bind('<ButtonRelease-3>', self.on_mouse_movement_B3_release)

               self.main_frame.bind('<ButtonPress-1>', self.on_timon_pressed)
               self.main_frame.bind('<ButtonPress-3>', self.on_mouse_B3_pressed)
               self.main_frame.bind('<B3-Motion>', self.on_mouse_movement_B3_hold)
               self.main_frame.bind('<ButtonRelease-3>', self.on_mouse_movement_B3_release)

               self.label_dial.bind('<ButtonPress-1>', self.on_timon_pressed)
               self.label_dial.bind('<ButtonPress-3>', self.on_mouse_B3_pressed)
               self.label_dial.bind('<B3-Motion>', self.on_mouse_movement_B3_hold)
               self.label_dial.bind('<Motion>', self.do_nothing)
               self.label_dial.bind('<ButtonRelease-3>', self.on_mouse_movement_B3_release)

               self.photo_dial=PhotoImage(file = 'photos_silla/timon_480.png')
               self.label_dial.create_image(200,200, image = self.photo_dial)
               self.label_indicator.place(relx=0.719, rely= 0.415)

          else:

               self.label_indicator.bind('<ButtonPress-1>', self.do_nothing)
               self.label_indicator.bind('<ButtonPress-3>', self.do_nothing)
               self.label_indicator.bind('<B3-Motion>', self.do_nothing)
               self.label_indicator.bind('<ButtonRelease-3>', self.do_nothing)

               self.main_frame.bind('<ButtonPress-1>', self.do_nothing)
               self.main_frame.bind('<ButtonPress-3>', self.do_nothing)
               self.main_frame.bind('<B3-Motion>', self.do_nothing)
               self.main_frame.bind('<ButtonRelease-3>', self.do_nothing)

               #self.label_dial.bind('<ButtonPress-1>', self.do_nothing)
               self.label_dial.bind('<B3-Motion>', self.do_nothing)
               #self.label_dial.bind('<ButtonRelease-3>', self.do_nothing)
               self.label_dial.bind('<Motion>', self.area_timon)
               self.label_dial.bind('<ButtonPress-3>', self.alternative_timon_B3_pressed)
                      

     def area_timon(self, event):

          #print('Enter in timon area')
          if self.state == False:  #estado del boton on
               return

          """if((abs(self.first_x - event.x)) > 2 or (abs(self.first_y - event.y)) > 2):
               
               self.first_x=event.x
               self.first_y=event.y

          else:
               
               return
          """
          x_suma=0
          y_suma=0
          #self.label_pos_init_indicator.config(text='y: '+str(event.y)+'\n'+'x: '+str(event.x))

          #self.label_indicator.place_forget()
          if(event.x > 200 and event.y < 200 and event.x < 280 and event.y > 120 ): # correccionNE
               x_suma=80
               y_suma=-80

          if(event.x > 200 and event.y > 200 and event.x < 280 and event.y < 280 ):# correccion SE
               x_suma=80
               y_suma=80
               
          if(event.x < 200 and event.y > 200 and event.x > 120 and event.y < 280 ):# correccion SW
               x_suma=-80
               y_suma= 80
               
          if(event.x < 200 and event.y < 200 and event.x > 120 and event.y > 120 ):# correccion NW
               x_suma=-80
               y_suma=-80

          for i in range(len(timon_position_ranges)):

               #print(timon_position_ranges[i]["cardinal"])

               #if (timon_position_ranges[i]["function"](event.x, event.y)):
                    
               if ((timon_position_ranges[i]["xmin"] < event.x + x_suma) and (timon_position_ranges[i]["xmax"] > event.x + x_suma) and (timon_position_ranges[i]["ymin"] < event.y + y_suma) and (timon_position_ranges[i]["ymax"] > y_suma +event.y)):

                    self.actual_timon_image = timon_position_ranges[i]["cardinal"]
                    self.actual_timon_image_pos = i
                    break

          if self.actual_timon_image != self.last_timon_image:

               self.last_timon_image = self.actual_timon_image
               self.photo_dial=PhotoImage(file = 'photos_silla/'+self.actual_timon_image)
               self.label_dial.create_image(200,200, image = self.photo_dial)


     def alternative_timon_B3_pressed(self, event):

          if self.state == False:  #estado del boton on
               return

          global send_bytes

          

          #self.last_timon_image = self.actual_timon_image
          
          self.photo_dial=PhotoImage(file = 'photos_silla/red_'+self.actual_timon_image)
          self.label_dial.create_image(200,200, image = self.photo_dial)

          if(self.first_move == True):

               uart_busy = True
               
               send_bytes=[]

               send_bytes.append(77)#M
               send_bytes.append(79)#O
               send_bytes.append(86)#V
               send_bytes.append(69)#E
               
               values= bytearray(send_bytes)
               ser.write(values)

               uart_busy = False

          self.first_move = False

          time.sleep(0.1)

          uart_busy = True

          send_bytes=[]

          send_bytes.append(1)#X COORDENADES
          send_bytes.append(timon_position_ranges[self.actual_timon_image_pos]["xcor"])# VALOR DE XCOORDENADES
          send_bytes.append(2)#Y COORDENADES
          send_bytes.append(timon_position_ranges[self.actual_timon_image_pos]["ycor"])#VALOR DE YCOORDENADES
               
          values= bytearray(send_bytes)
          ser.write(values)

          uart_busy = False


     def on_timon_pressed(self, event):

         if self.state == False:  #estado del boton on
               return

         global send_bytes

         
         if(self.first_move == False):

             uart_busy = True

             send_bytes=[]
             
             send_bytes.append(75) # ASCII K
             send_bytes.append(69) # ASCII E
             send_bytes.append(69) # ASCII E
             send_bytes.append(80) # ASCII P

             values= bytearray(send_bytes)

             ser.write(values)

             uart_busy = False

     def on_claxon_button(self,event):


         global send_bytes

         send_bytes=[]
         
         self.photo_claxon=PhotoImage(file = 'photos_silla/claxon_on.png')  #my_icons/off.png
         self.label_claxon_button.config(compound = 'center', image=self.photo_claxon)
         self.label_claxon_button.place(relx=0.169,rely=0.29)

         uart_busy = True

         send_bytes.append(67) # ASCII C de aumentar
         send_bytes.append(97) # ASCII a de activar
         send_bytes.append(0)
         send_bytes.append(0)

         values= bytearray(send_bytes)

         ser.write(values)

         uart_busy = False

     def on_claxon_release(self,event):

          global send_bytes

          send_bytes = []
          
          self.photo_claxon=PhotoImage(file = 'photos_silla/claxon.png')  #my_icons/off.png
          self.label_claxon_button.config(compound = 'center', image=self.photo_claxon)
          self.label_claxon_button.place(relx=0.169,rely=0.31)
         
          uart_busy = True

          send_bytes.append(67) # ASCII C de claxon
          send_bytes.append(100) # ASCII d de desactivar
          send_bytes.append(0)
          send_bytes.append(0)

          values= bytearray(send_bytes)

          ser.write(values)

          uart_busy = False

     def on_led_button(self, event):

          global send_bytes

          self.label_led_button.place(relx=0.84, rely = 0.89)

          send_bytes = []
          
          uart_busy = True
                    
          send_bytes.append(84)# ASCII T  para pulso y apagar silla con error
          send_bytes.append(0)
          send_bytes.append(0) 
          send_bytes.append(0) 


          values= bytearray(send_bytes)

          ser.write(values)

          uart_busy = False


     def on_led_release(self, event):

          self.label_led_button.place(relx=0.85, rely = 0.9)
         
     def on_on_button(self,event):

          global send_bytes#, valor_recibido

          """print(valor_recibido)

          string_send_bytes = ""

          for digit in send_bytes:
              string_send_bytes += str(digit)

          string_receive_bytes = ""

          for digit in valor_recibido:
              string_receive_bytes += str(digit)

          self.label_pos_movement_indicator.config(text='recibido '+string_receive_bytes+'envio '+string_send_bytes)
          """

          if(recibo_perfecto == False):
               self.photo_quit=PhotoImage(file = 'photos_silla/salir_red.png') 
               self.label_quit_button.config(compound = 'center', image=self.photo_quit)

          else:
               self.photo_quit=PhotoImage(file = 'photos_silla/salir_green.png') 
               self.label_quit_button.config(compound = 'center', image=self.photo_quit)


          send_bytes = []

          if self.state == True:
               self.state = False
               self.photo_off=PhotoImage(file = 'photos_silla/speeed.png')
               self.label_off_button.config(compound = 'center', image=self.photo_off)

               uart_busy = True
               
               send_bytes.append(84) # ASCII T de turn
               send_bytes.append(79)# ASCII O 
               send_bytes.append(70)# ASCII F de off
               send_bytes.append(70)# ASCII F de off
               values= bytearray(send_bytes)

               ser.write(values)

               uart_busy = False
               
          else:
               if self.state == False:
                    self.state = True
                    self.photo_off=PhotoImage(file = 'photos_silla/'+speed_indicator_names[speed_indicator_value]) 
                    self.label_off_button.config(compound = 'center', image=self.photo_off)

                    uart_busy = True
                    
                    send_bytes.append(84)# ASCII T de turn
                    send_bytes.append(0)
                    send_bytes.append(79) # ASCII O de turn
                    send_bytes.append(78) # ASCII N de on


                    values= bytearray(send_bytes)

                    ser.write(values)

                    uart_busy = False

          time.sleep(0.1)

     def on_lower(self,event):

          if self.state == False:  #estado del boton on
               return

          if(recibo_perfecto == False):#si no pincha comunicacion debe estar en rojo el boton salir
               self.photo_quit=PhotoImage(file = 'photos_silla/salir_red.png') 
               self.label_quit_button.config(compound = 'center', image=self.photo_quit)

          else: #si pincha comunicacion debe estar en verde el boton salir
               self.photo_quit=PhotoImage(file = 'photos_silla/salir_green.png') 
               self.label_quit_button.config(compound = 'center', image=self.photo_quit)


          global speed_indicator_value, send_bytes

          send_bytes = []

          self.photo_disminuir=PhotoImage(file = 'photos_silla/down_on.png')  
          self.label_lower_button.config(compound = 'center', image=self.photo_disminuir)
          self.label_lower_button.place(relx = 0.004, rely = 0.526)

          if speed_indicator_value > 0:
               speed_indicator_value=speed_indicator_value-1
               self.photo_speed_indicator=PhotoImage(file = 'photos_silla/'+speed_indicator_names[speed_indicator_value])  #my_icons/off.png
               self.label_off_button.config(image=self.photo_speed_indicator)

          uart_busy = True

          send_bytes.append(76) # ASCII L de lower disminuir
          send_bytes.append(speed_indicator_value+1)
          send_bytes.append(0)
          send_bytes.append(0)


          values= bytearray(send_bytes)
          
          
          ser.write(values)
          
          uart_busy = False

      
     def on_lower_release(self,event):

          if self.state == False:  #estado del boton on
               return
          
          if(recibo_perfecto == False):#si no pincha comunicacion debe estar en rojo el boton salir
               self.photo_quit=PhotoImage(file = 'photos_silla/salir_red.png') 
               self.label_quit_button.config(compound = 'center', image=self.photo_quit)

          else: #si pincha comunicacion debe estar en verde el boton salir
               self.photo_quit=PhotoImage(file = 'photos_silla/salir_green.png') 
               self.label_quit_button.config(compound = 'center', image=self.photo_quit)


          self.photo_disminuir=PhotoImage(file = 'photos_silla/down.png')  
          self.label_lower_button.config(compound = 'center', image=self.photo_disminuir)
          self.label_lower_button.place(relx = 0.005, rely = 0.53)

     def on_higher(self,event):

          if self.state == False:
               return

          if(recibo_perfecto == False):#si no pincha comunicacion debe estar en rojo el boton salir
               self.photo_quit=PhotoImage(file = 'photos_silla/salir_red.png') 
               self.label_quit_button.config(compound = 'center', image=self.photo_quit)

          else: #si pincha comunicacion debe estar en verde el boton salir
               self.photo_quit=PhotoImage(file = 'photos_silla/salir_green.png') 
               self.label_quit_button.config(compound = 'center', image=self.photo_quit)


          global speed_indicator_value, send_bytes
          
          send_bytes = []

          self.photo_aumentar=PhotoImage(file = 'photos_silla/up_on.png')  #my_icons/off.png
          self.label_higher_button.config(compound = 'center', image=self.photo_aumentar)

          if speed_indicator_value < 4:
               speed_indicator_value=speed_indicator_value+1
               self.photo_speed_indicator=PhotoImage(file = 'photos_silla/'+speed_indicator_names[speed_indicator_value])  #my_icons/off.png
               self.label_off_button.config(image=self.photo_speed_indicator)

          uart_busy = True

          send_bytes.append(72) # ASCII H de higher aumentar
          send_bytes.append(speed_indicator_value+1)
          send_bytes.append(0)
          send_bytes.append(0)


          values= bytearray(send_bytes)

          ser.write(values)

          uart_busy = False

          

     def on_higher_release(self,event):

          if self.state == False:
               return
 
          if(recibo_perfecto == False):#si no pincha comunicacion debe estar en rojo el boton salir
               self.photo_quit=PhotoImage(file = 'photos_silla/salir_red.png') 
               self.label_quit_button.config(compound = 'center', image=self.photo_quit)

          else: #si pincha comunicacion debe estar en verde el boton salir
               self.photo_quit=PhotoImage(file = 'photos_silla/salir_green.png') 
               self.label_quit_button.config(compound = 'center', image=self.photo_quit)

          self.photo_aumentar=PhotoImage(file = 'photos_silla/up.png')  #my_icons/off.png
          self.label_higher_button.config(compound = 'center', image=self.photo_aumentar)


     def on_mouse_B3_pressed(self,event):

          if self.state == False:  #estado del boton on
               return


          #centro indicador x=0.72  y=0.42  r= 0.18  rx= 0.18*0.6
          global send_bytes

          send_bytes = []
          
          self.global_y_pos_init=event.y_root
          self.global_x_pos_init=event.x_root

          #self.label_pos_init_indicator.config(text='y: '+str(self.global_y_pos_init)+'\n'+'x: '+str(self.global_x_pos_init))
          if(self.first_move == True):

               uart_busy = True
               
               send_bytes.append(77)#M
               send_bytes.append(79)#O
               send_bytes.append(86)#V
               send_bytes.append(69)#E
               values= bytearray(send_bytes)
               ser.write(values)

               uart_busy = False

          self.first_move = False
          time.sleep(0.1)
          
          """self.global_y_pos_init=event.y
          self.global_x_pos_init=event.x
          """

          #self.label_indicator.place(relx=0.612, rely=0.42)
       

     def on_mouse_movement_B3_hold(self,event):

          if self.state == False:  #estado del boton on
               return

          #centro indicador x=0.72  y=0.42     r= 0.18 (60 pix)    rx= 0.18*0.6 (36 pix)

          global send_bytes

          send_bytes = []
          
          self.global_y_pos=event.y_root
          self.global_x_pos=event.x_root

          if (self.global_x_pos - self.global_x_pos_init) == 0:
               
               if (self.global_y_pos - self.global_y_pos_init) < 0:
                    alpha=math.asin(-1)
               
               if (self.global_y_pos - self.global_y_pos_init) > 0:
                         alpha=math.asin(1)
               else:
                         alpha=0
               
               

          else:
               alpha = math.atan( (self.global_y_pos - self.global_y_pos_init) / (self.global_x_pos - self.global_x_pos_init) )

          factor = 1 
          if (self.global_x_pos - self.global_x_pos_init) < 0:
               
               factor = (-1)

          dx = 70 * (math.cos(alpha))*(factor)
          dy = 70 * (math.sin(alpha))*(factor)
               
          xf = 570  + dx
          yf = 200  + dy

          
          uart_busy = True
          
          send_bytes.append(1)
          send_bytes.append(int((int(dx)+70)*1.8214))
          send_bytes.append(2)
          send_bytes.append(int((255-(int(dy)+70)*1.8214)))
          values= bytearray(send_bytes)
          ser.write(values)

          uart_busy = False

          self.indicator_actual_pos_x = xf/800
          self.indicator_actual_pos_y = yf/480

          self.label_indicator.place(relx= self.indicator_actual_pos_x, rely= self.indicator_actual_pos_y)

          #self.label_pos_movement_indicator.config(foreground = 'red', text=str(alpha))
        
          
          """self.global_y_pos=event.y
          self.global_x_pos=event.x

          self.label_pos_indicator.config(text='y: '+str(self.global_y_pos)+'\n'+'x: '+str(self.global_x_pos))

          move_x = (self.global_x_pos - self.global_x_pos_init)/1000
          move_y = (self.global_y_pos - self.global_y_pos_init)/1000
          
          self.label_pos_movement_indicator.config(text='y: '+str(move_y)+'\n'+'x: '+str(move_x))



          self.indicator_actual_pos_x = self.indicator_actual_pos_x + move_x
          self.indicator_actual_pos_y = self.indicator_actual_pos_y + move_y

          if self.indicator_actual_pos_y > 0.48:
               self.indicator_actual_pos_y = 0.48
               
          if self.indicator_actual_pos_x > 0.66:
               self.indicator_actual_pos_x = 0.66
               
               
          if self.indicator_actual_pos_y < 0.28:
               self.indicator_actual_pos_y = 0.28
               
          if self.indicator_actual_pos_x < 0.46:
               self.indicator_actual_pos_x = 0.46
               
          
          self.label_indicator.place(relx= self.indicator_actual_pos_x, rely= self.indicator_actual_pos_y)
          """
          
          
             
     def on_mouse_movement_B3_release(self, event):

          if self.state == False:  #estado del boton on
               return
          

          global send_bytes

          send_bytes = []

          self.first_move=True

          if(self.binding_state == True):
              self.label_indicator.place(relx=0.719, rely= 0.415)

          uart_busy = True

          send_bytes.append(77)
          send_bytes.append(77)
          send_bytes.append(0)
          send_bytes.append(0)


          values= bytearray(send_bytes)

          ser.write(values)

          uart_busy = False
          
          """
          self.global_y_pos=0
          self.global_x_pos=0
          self.label_pos_indicator.config(text='y: '+str(self.global_y_pos)+'\n'+'x: '+str(self.global_x_pos))
          """
          #centro - x: 0.56   y: 0.38     radiox=0.1 radioy=0.1
          

def function_TKInter_Thread():

   root =Tk()
   root.overrideredirect(1)
   w,h = root.winfo_screenwidth() ,root.winfo_screenheight()
   root.geometry('%dx%d+0+0'%(WINDOWWIDTH,WINDOWHEIGHT))
   audiometro=Audiometro(root)
   root.mainloop()


def function_UART_Read():

     global running_program, valor_recibido,recibo_perfecto

     time.sleep(3)
     
     while running_program == True:
          comando_recibido=ser.readline(4)
          
          if(comando_recibido != ''):
               
               valor_recibido = comando_recibido
               
               print(valor_recibido)
               #print(valor_recibido)
          if(valor_recibido == bytearray([221,221,221,221])):

               print('valor recibido fin *****************************************')

               """ser.flushInput()
               ser.flushOutput()
               
               ser.close()

               time.sleep(0.5)
               """ 
               os._exit(1)
               
          if(valor_recibido == bytearray(send_bytes) or valor_recibido == bytearray([170,170,170,170]) or valor_recibido == bytearray([204,204,204,204])): #debe ser igual el ultimo enviado y el recibido

               recibo_perfecto=True

               print('valor recibido perfecto ')
          else:
               
               recibo_perfecto=False
               
               print('valor recibido error ')


          """print('send_bytes: ')
          print(bytearray(send_bytes))
          print('valor_recibido: ')
          print(valor_recibido)
          print(recibo_perfecto)
          """
          
def function_check_connection():

     global running_program, uart_busy

     send_bytes_check_connection = []

     send_bytes_check_connection.append(204) # CC para inicio de aplicacion
     send_bytes_check_connection.append(204)
     send_bytes_check_connection.append(204)
     send_bytes_check_connection.append(204)


     values= bytearray(send_bytes_check_connection)

     ser.write(values)
     time.sleep(2)

     while running_program == True:      
          print('enviando check connection')

          while (uart_busy == True):
               pass

          uart_busy = True
          
          send_bytes_check_connection = []

          send_bytes_check_connection.append(170)
          send_bytes_check_connection.append(170)
          send_bytes_check_connection.append(170)
          send_bytes_check_connection.append(170)


          values= bytearray(send_bytes_check_connection)

          ser.write(values)

          uart_busy = False
          
          time.sleep(2)
    
          
def main():

     thread_TK = threading.Thread( target = function_TKInter_Thread )
     thread_check_connection = threading.Thread( target = function_check_connection )
     thread_UART_Read = threading.Thread( target = function_UART_Read )
     
     thread_TK.daemon = True
     thread_check_connection.daemon = True
     thread_UART_Read.daemon = True
     
     
     thread_TK.start()
     thread_check_connection.start()
     thread_UART_Read.start()
     
     thread_UART_Read.join()
     thread_check_connection.join()
     thread_TK.join()
     print('program finished')
     
if __name__ == "__main__": main()


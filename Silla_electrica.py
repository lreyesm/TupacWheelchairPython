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
##import pyautogui //hay que descargarla

WINDOWWIDTH=800
WINDOWHEIGHT=480


# VARIABLES DE PUERTO SERIE ----------------------------------------------------------------------------------------

x_correction_movement = 20
y_correction_movement = 15

delta_y_max = 90
delta_x_max = 150

is_straight_button_pressed = False

ser = serial.Serial('/dev/serial0',baudrate=115200,timeout = 9,bytesize = serial.EIGHTBITS,parity = serial.PARITY_NONE,stopbits = serial.STOPBITS_ONE,rtscts=False)


timer_event_started = False
timeout = True
timer_buttons_delay = 1.3

timer_delay_correct_direction = 1.2
timer_correct_dir_event_started = False
timeout_correct_dir = False
center_of_correction  = 128
correction_range = 72
xcoord_max_correction = center_of_correction + correction_range
xcoord_min_correction = center_of_correction - correction_range

dont_move = False

uart_counter = 0;
send_bytes = []
send_bytes_header = [160, 160, 160, 160]
send_bytes_check = [160, 160, 160, 160]
uart_busy = False
running_program=True
recibo_perfecto=False
valor_recibido = []
first_move=True
first_correction = True

speed_indicator_names=['speeed_1.png','speeed_2.png','speeed_3.png','speeed_4.png','speeed_5.png']
speed_indicator_value=0
initspeed=3

Start_Moving_Button = '<ButtonPress-1>'
Start_Moving_Motion ='<B1-Motion>'
Start_Moving_Release = '<ButtonRelease-1>'
Keep_Moving_Button = '<ButtonPress-3>'
Stop_Moving_Button = '<Double-Button-3>'
Stop_Moving_Button_emergency = '<ButtonPress-3>'
without_click_motion = '<Motion>'

sig_x_0_por   = 80 
sig_x_25_por  = 102
sig_x_50_por  = 124
sig_x_75_por  = 146
sig_x_100_por = 168

sig_y_0_por   = 1
sig_y_25_por  = 102
sig_y_50_por  = 124
sig_y_75_por  = 146
sig_y_100_por = 167

timon_position_ranges = []

timon_position_ranges.append({"cardinal": 'timon_N.png',"xmin": 160, "ymin": 0, "xmax": 240,"ymax": 200,"xcor": sig_x_50_por,"ycor": sig_y_100_por}) ##*****************************************
timon_position_ranges.append({"cardinal": 'timon_S.png',"xmin": 165, "ymin": 201, "xmax": 235,"ymax": 400,"xcor": sig_x_50_por,"ycor": sig_y_0_por})
timon_position_ranges.append({"cardinal": 'timon_E.png',"xmin": 226, "ymin": 175, "xmax": 400,"ymax": 225,"xcor": sig_x_100_por,"ycor": sig_y_50_por})
timon_position_ranges.append({"cardinal": 'timon_W.png',"xmin": 0, "ymin": 175, "xmax": 174,"ymax": 225,"xcor": sig_x_0_por,"ycor": sig_y_50_por})

timon_position_ranges.append({"cardinal": 'timon_NE.png',"xmin": 225, "ymin": 150, "xmax": 250,"ymax": 175,"xcor": sig_x_100_por,"ycor": sig_y_100_por})
timon_position_ranges.append({"cardinal": 'timon_NE.png',"xmin": 250, "ymin": 100, "xmax": 300,"ymax": 150,"xcor": sig_x_100_por,"ycor": sig_y_100_por})
timon_position_ranges.append({"cardinal": 'timon_NE.png',"xmin": 300, "ymin": 50, "xmax": 350,"ymax": 100,"xcor": sig_x_100_por,"ycor": sig_y_100_por})
timon_position_ranges.append({"cardinal": 'timon_NE.png',"xmin": 350, "ymin": 0, "xmax": 400,"ymax": 50,"xcor": sig_x_100_por,"ycor": sig_y_100_por})
timon_position_ranges.append({"cardinal": 'timon_NE6.png',"xmin": 225, "ymin": 50, "xmax": 300,"ymax": 100,"xcor": sig_x_75_por,"ycor": sig_y_100_por})
timon_position_ranges.append({"cardinal": 'timon_NE6.png',"xmin": 225, "ymin": 100, "xmax": 250,"ymax": 150,"xcor": sig_x_75_por,"ycor": sig_y_100_por})
timon_position_ranges.append({"cardinal": 'timon_NE6.png',"xmin": 225, "ymin": 0, "xmax": 350,"ymax": 50,"xcor": sig_x_75_por,"ycor": sig_y_100_por})
timon_position_ranges.append({"cardinal": 'timon_NE2.png',"xmin": 300, "ymin": 100, "xmax": 400,"ymax": 150,"xcor": sig_x_100_por,"ycor": sig_y_75_por})
timon_position_ranges.append({"cardinal": 'timon_NE2.png',"xmin": 350, "ymin": 50, "xmax": 400,"ymax": 100,"xcor": sig_x_100_por,"ycor": sig_y_75_por})
timon_position_ranges.append({"cardinal": 'timon_NE2.png',"xmin": 250, "ymin": 150, "xmax": 400,"ymax": 175,"xcor": sig_x_100_por,"ycor": sig_y_75_por})

timon_position_ranges.append({"cardinal": 'timon_NW.png',"xmin": 150, "ymin": 150, "xmax": 175,"ymax": 175,"xcor": sig_x_0_por,"ycor": sig_y_100_por})
timon_position_ranges.append({"cardinal": 'timon_NW.png',"xmin": 100, "ymin": 100, "xmax": 150,"ymax": 150,"xcor": sig_x_0_por,"ycor": sig_y_100_por})
timon_position_ranges.append({"cardinal": 'timon_NW.png',"xmin": 50, "ymin": 50, "xmax": 100,"ymax": 100,"xcor": sig_x_0_por,"ycor": sig_y_100_por})
timon_position_ranges.append({"cardinal": 'timon_NW.png',"xmin": 0, "ymin": 0, "xmax": 50,"ymax": 50,"xcor": sig_x_0_por,"ycor": sig_y_100_por})
timon_position_ranges.append({"cardinal": 'timon_NW2.png',"xmin": 0, "ymin": 150, "xmax": 150,"ymax": 175,"xcor": sig_x_0_por,"ycor": sig_y_75_por})
timon_position_ranges.append({"cardinal": 'timon_NW2.png',"xmin": 0, "ymin": 100, "xmax": 100,"ymax": 150,"xcor": sig_x_0_por,"ycor": sig_y_75_por})
timon_position_ranges.append({"cardinal": 'timon_NW2.png',"xmin": 0, "ymin": 50, "xmax": 50,"ymax": 100,"xcor": sig_x_0_por,"ycor": sig_y_75_por})
timon_position_ranges.append({"cardinal": 'timon_NW6.png',"xmin": 50, "ymin": 0, "xmax": 175,"ymax": 50,"xcor": sig_x_25_por,"ycor": sig_y_100_por})
timon_position_ranges.append({"cardinal": 'timon_NW6.png',"xmin": 100, "ymin": 50, "xmax": 175,"ymax": 100,"xcor": sig_x_25_por,"ycor": sig_y_100_por})
timon_position_ranges.append({"cardinal": 'timon_NW6.png',"xmin": 150, "ymin": 100, "xmax": 175,"ymax": 150,"xcor": sig_x_25_por,"ycor": sig_y_100_por})

timon_position_ranges.append({"cardinal": 'timon_SE.png',"xmin": 350, "ymin": 350, "xmax": 400,"ymax": 400,"xcor": sig_x_100_por,"ycor": sig_y_0_por})
timon_position_ranges.append({"cardinal": 'timon_SE.png',"xmin": 225, "ymin": 225, "xmax": 250,"ymax": 250,"xcor": sig_x_100_por,"ycor": sig_y_0_por})
timon_position_ranges.append({"cardinal": 'timon_SE.png',"xmin": 250, "ymin": 250, "xmax": 300,"ymax": 300,"xcor": sig_x_100_por,"ycor": sig_y_0_por})
timon_position_ranges.append({"cardinal": 'timon_SE.png',"xmin": 300, "ymin": 300, "xmax": 350,"ymax": 350,"xcor": sig_x_100_por,"ycor": sig_y_0_por})
timon_position_ranges.append({"cardinal": 'timon_SE6.png',"xmin": 225, "ymin": 225, "xmax": 400,"ymax": 250,"xcor": sig_x_100_por,"ycor": sig_y_25_por})
timon_position_ranges.append({"cardinal": 'timon_SE6.png',"xmin": 300, "ymin": 250, "xmax": 400,"ymax": 300,"xcor": sig_x_100_por,"ycor": sig_y_25_por})
timon_position_ranges.append({"cardinal": 'timon_SE6.png',"xmin": 350, "ymin": 300, "xmax": 400,"ymax": 350,"xcor": sig_x_100_por,"ycor": sig_y_25_por})
timon_position_ranges.append({"cardinal": 'timon_SE2.png',"xmin": 225, "ymin": 250, "xmax": 250,"ymax": 400,"xcor": sig_x_75_por,"ycor": sig_y_0_por})
timon_position_ranges.append({"cardinal": 'timon_SE2.png',"xmin": 250, "ymin": 300, "xmax": 300,"ymax": 400,"xcor": sig_x_75_por,"ycor": sig_y_0_por})
timon_position_ranges.append({"cardinal": 'timon_SE2.png',"xmin": 300, "ymin": 350, "xmax": 350,"ymax": 400,"xcor": sig_x_75_por,"ycor": sig_y_0_por})

timon_position_ranges.append({"cardinal": 'timon_SW.png',"xmin": 150, "ymin": 225, "xmax": 175,"ymax": 250,"xcor": sig_x_0_por,"ycor": sig_y_0_por})
timon_position_ranges.append({"cardinal": 'timon_SW.png',"xmin": 100, "ymin": 250, "xmax": 150,"ymax": 300,"xcor": sig_x_0_por,"ycor": sig_y_0_por})
timon_position_ranges.append({"cardinal": 'timon_SW.png',"xmin": 50, "ymin": 300, "xmax": 100,"ymax": 350,"xcor": sig_x_0_por,"ycor": sig_y_0_por})
timon_position_ranges.append({"cardinal": 'timon_SW.png',"xmin": 0, "ymin": 350, "xmax": 50,"ymax": 400,"xcor": sig_x_0_por,"ycor": sig_y_0_por})
timon_position_ranges.append({"cardinal": 'timon_SW2.png',"xmin": 0, "ymin": 225, "xmax": 150,"ymax": 250,"xcor": sig_x_0_por,"ycor": sig_y_25_por})
timon_position_ranges.append({"cardinal": 'timon_SW2.png',"xmin": 0, "ymin": 250, "xmax": 100,"ymax": 300,"xcor": sig_x_0_por,"ycor": sig_y_25_por})
timon_position_ranges.append({"cardinal": 'timon_SW2.png',"xmin": 0, "ymin": 300, "xmax": 50,"ymax": 350,"xcor": sig_x_0_por,"ycor": sig_y_25_por})
timon_position_ranges.append({"cardinal": 'timon_SW6.png',"xmin": 150, "ymin": 250, "xmax": 175,"ymax": 400,"xcor": sig_x_25_por,"ycor": sig_y_0_por})
timon_position_ranges.append({"cardinal": 'timon_SW6.png',"xmin": 100, "ymin": 300, "xmax": 175,"ymax": 350,"xcor": sig_x_25_por,"ycor": sig_y_0_por})
timon_position_ranges.append({"cardinal": 'timon_SW6.png',"xmin": 50, "ymin": 175, "xmax": 350,"ymax": 400,"xcor": sig_x_25_por,"ycor": sig_y_0_por})


def send_uart_data( dat1 = 0,  dat2 = 0, dat3 = 0,  dat4 = 0):
    
    global send_bytes, uart_busy , uart_counter     

    send_bytes = []

    send_bytes.extend(send_bytes_header)
    send_bytes.append(dat1)
    send_bytes.append(dat2)
    send_bytes.append(dat3)
    send_bytes.append(dat4)
    send_bytes.append(uart_counter)
    send_bytes.extend(send_bytes_check)
    
    if(uart_counter >= 255):
        uart_counter=0
    
    uart_counter = uart_counter +1


    values= bytearray(send_bytes)

    uart_busy = True
    
    ser.write(values)

    uart_busy = False
    
    
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
        self.main_frame.bind(Keep_Moving_Button, self.on_timon_pressed)
        self.main_frame.bind(Stop_Moving_Button, self.on_B2_pressed_emergency)
        self.main_frame.bind(Stop_Moving_Button_emergency, self.on_B2_pressed_emergency)
        self.main_frame.bind(Start_Moving_Button, self.on_mouse_B1_pressed_init_movement)
        self.main_frame.bind(Start_Moving_Motion, self.on_mouse_movement_B3_hold)
        self.main_frame.bind(Start_Moving_Release, self.on_mouse_movement_B3_release)
        ##self.main_frame.bind('<B3-Motion>', self.on_mouse_movement_B3_hold)
        ##self.main_frame.bind('<ButtonRelease-3>', self.on_mouse_movement_B3_release)

        self.global_y_pos=0
        self.global_y_pos_init=0
        self.global_x_pos=0
        self.global_x_pos_init=0
        self.indicator_actual_pos_x=0.56
        self.indicator_actual_pos_y=0.38
        self.state=False
        ##first_move = True**************************************************************
        self.binding_state = True
        self.actual_timon_image = 'photos_silla/timon_480.png'
        self.last_timon_image = 'photos_silla/timon_480.png'
        self.actual_timon_image_pos=0
        self.first_x=200
        self.first_y=200
        self.correction_x=0
        self.correction_y=0
        
        self.label_quit_button=ttk.Label(self.main_frame)  # label edad value
        self.label_quit_button.place(relx=0.93,rely=0.9)
        self.label_quit_button.config(background = 'white', width = 5)
        self.photo_quit=PhotoImage(file = 'photos_silla/salir_red.png') 
        self.label_quit_button.config(compound = 'center', image=self.photo_quit)
        self.label_quit_button.bind(Stop_Moving_Button, self.on_B2_pressed_emergency)
        self.label_quit_button.bind(Stop_Moving_Button_emergency, self.on_B2_pressed_emergency)
        self.label_quit_button.bind(Start_Moving_Button, lambda e: self.on_quit(master))

        self.label_led_button=ttk.Label(self.main_frame)  # label edad value
        self.label_led_button.place(relx=0.85,rely=0.9)
        self.label_led_button.config(background = 'white', width = 5)
        self.photo_led=PhotoImage(file = 'photos_silla/led_off.png') 
        self.label_led_button.config(compound = 'center', image=self.photo_led)
        self.label_led_button.bind(Stop_Moving_Button, self.on_B2_pressed_emergency)
        self.label_led_button.bind(Stop_Moving_Button_emergency, self.on_B2_pressed_emergency)
        self.label_led_button.bind(Start_Moving_Button, self.on_led_button)
        self.label_led_button.bind('<ButtonRelease-1>', self.on_led_release)

                
        self.label_off_button=ttk.Label(self.main_frame)  # label edad value
        self.label_off_button.place(relx=0.1,rely=0.45)
        self.label_off_button.config(foreground = 'white',background = 'white')
        self.photo_off=PhotoImage(file = 'photos_silla/speeed.png') 
        self.label_off_button.config(compound = 'center', image=self.photo_off)
        self.label_off_button.bind(Stop_Moving_Button, self.on_B2_pressed_emergency)
        self.label_off_button.bind(Stop_Moving_Button_emergency, self.on_B2_pressed_emergency) 
        self.label_off_button.bind(Start_Moving_Button, self.on_on_button)

        self.label_claxon_button=ttk.Label(self.main_frame)  # label edad value
        self.label_claxon_button.place(relx=0.169,rely=0.31)
        self.label_claxon_button.config(foreground = 'white',background = 'white')
        self.photo_claxon=PhotoImage(file = 'photos_silla/claxon.png')  #my_icons/off.png
        self.label_claxon_button.config(compound = 'center', image=self.photo_claxon)
        self.label_claxon_button.bind(Start_Moving_Button, self.on_claxon_button)
        self.label_claxon_button.bind(Stop_Moving_Button, self.on_B2_pressed_emergency)
        self.label_claxon_button.bind(Stop_Moving_Button_emergency, self.on_B2_pressed_emergency)
        self.label_claxon_button.bind('<ButtonRelease-1>', self.on_claxon_release)


        self.label_logo=ttk.Label(self.main_frame)  # label edad value
        self.label_logo.place(relx=0.01,rely=0.01)
        self.label_logo.config(foreground = 'white',background = 'white')
        self.photo_logo=PhotoImage(file = 'photos_silla/logo.png')  #my_icons/off.png
        self.label_logo.bind(Stop_Moving_Button, self.on_B2_pressed_emergency)
        self.label_logo.bind(Stop_Moving_Button_emergency, self.on_B2_pressed_emergency)  
        self.label_logo.config(compound = 'center', image=self.photo_logo)

        self.label_higher_button=ttk.Label(self.main_frame)  # label edad value
        self.label_higher_button.place(relx=0.39,rely=0.525)
        self.label_higher_button.config(foreground = 'white',background = 'white')
        self.photo_aumentar=PhotoImage(file = 'photos_silla/up.png')  #my_icons/off.png
        self.label_higher_button.config(compound = 'center', image=self.photo_aumentar)
        self.label_higher_button.bind(Start_Moving_Button, self.on_higher)
        self.label_higher_button.bind(Stop_Moving_Button, self.on_B2_pressed_emergency)
        self.label_higher_button.bind(Stop_Moving_Button_emergency, self.on_B2_pressed_emergency)
        self.label_higher_button.bind('<ButtonRelease-1>', self.on_higher_release)

        self.label_lower_button=ttk.Label(self.main_frame)  # label edad value
        self.label_lower_button.place(relx=0.005,rely=0.53)
        self.label_lower_button.config(foreground = 'white',background = 'white')
        self.photo_disminuir=PhotoImage(file = 'photos_silla/down.png')  
        self.label_lower_button.config(compound = 'center', image=self.photo_disminuir)
        self.label_lower_button.bind(Start_Moving_Button, self.on_lower)
        self.label_lower_button.bind(Stop_Moving_Button, self.on_B2_pressed_emergency)
        self.label_lower_button.bind(Stop_Moving_Button_emergency, self.on_B2_pressed_emergency)
        self.label_lower_button.bind(Start_Moving_Release, self.on_lower_release)

        self.label_dial=Canvas(self.main_frame)  # label edad value
        self.label_dial.config(width= 400, height = 400, background = 'white')
        self.label_dial.place(relx=0.49,rely=0.00)
        #self.label_dial.config(foreground= 'white')
        self.photo_dial=PhotoImage(file = 'photos_silla/timon_480.png')  #my_icons/off.png
        #self.label_dial.config(image=self.photo_dial)
        self.label_dial.create_image(200,200, image = self.photo_dial)
        self.label_dial.bind(Keep_Moving_Button, self.on_timon_pressed)
        self.label_dial.bind(Start_Moving_Button, self.on_mouse_B1_pressed_init_movement)
        self.label_dial.bind(Start_Moving_Motion, self.on_mouse_movement_B3_hold)
        self.label_dial.bind(Stop_Moving_Button, self.on_B2_pressed_emergency)
        self.label_dial.bind(Stop_Moving_Button_emergency, self.on_B2_pressed_emergency)
        self.label_dial.bind(Start_Moving_Release, self.on_mouse_movement_B3_release)

        self.label_indicator=ttk.Label(self.main_frame)  # label edad value
        self.label_indicator.place(relx=0.719, rely= 0.415)
        #self.label_indicator.config(background = '#494949')
        self.photo_indice=PhotoImage(file = 'photos_silla/move.png')  #my_icons/off.png
        self.label_indicator.config(compound = 'center', image=self.photo_indice)
        self.label_indicator.bind(Keep_Moving_Button, self.on_timon_pressed)
        self.label_indicator.bind(Start_Moving_Button, self.on_mouse_B1_pressed_init_movement)
        self.label_indicator.bind(Start_Moving_Motion, self.on_mouse_movement_B3_hold)
        self.label_indicator.bind(Stop_Moving_Button, self.on_B2_pressed_emergency)
        self.label_indicator.bind(Stop_Moving_Button_emergency, self.on_B2_pressed_emergency)
        self.label_indicator.bind(Start_Moving_Release, self.on_mouse_movement_B3_release)

        
        self.label_battery=ttk.Label(self.main_frame)  # label edad value
        self.label_battery.place(relx=0.63,rely=0.79)
        self.label_battery.config(foreground = 'white',background = 'white')
        self.photo_battery=PhotoImage(file = 'photos_silla/battery.png')  #my_icons/off.png
        self.label_battery.config(compound = 'center', image=self.photo_battery)

        self.label_chage_controls_button=ttk.Label(self.main_frame)  # label edad value
        self.label_chage_controls_button.place(relx=0.889,rely=0.0)
        self.photo_chage_controls=PhotoImage(file = 'photos_silla/mode_1.png')
        self.label_chage_controls_button.config(background = 'white', image = self.photo_chage_controls)
        ##self.label_chage_controls_button.bind(Keep_Moving_Button, self.on_change_controls_button)
        self.label_chage_controls_button.bind(Stop_Moving_Button, self.on_B2_pressed_emergency)
        self.label_chage_controls_button.bind(Stop_Moving_Button_emergency, self.on_B2_pressed_emergency)

        """self.label_speed_indicator=ttk.Label(self.main_frame)  # label edad value
        self.label_speed_indicator.place(relx=0.2,rely=0.5)
        self.label_speed_indicator.config(foreground = 'white')
        self.photo_speed_indicator=PhotoImage(file = 'photos_silla/'+speed_indicator_names[1])  #my_icons/off.png
        self.label_speed_indicator.config(compound = 'center', image=self.photo_speed_indicator)
        #self.label_speed_indicator.bind(Start_Moving_Button, lambda e: self.on_quit(master))"""

        """
        self.label_pos_indicator=ttk.Label(self.main_frame)  # label edad value
        self.label_pos_indicator.place(relx=0.1,rely=0.0)
        self.label_pos_indicator.config(foreground = 'red', text='correccion en x : '+ str(self.correction_x), font=('Droid Naskh Shift Alt',16,'bold'))
        
        self.label_pos_init_indicator=ttk.Label(self.main_frame)  # label edad value
        self.label_pos_init_indicator.place(relx=0.1,rely=0.1)
        self.label_pos_init_indicator.config(foreground = 'red', text='correccion en y : '+ str(self.correction_y), font=('Droid Naskh Shift Alt',16,'bold'))
        """
        """self.label_pos_movement_indicator=ttk.Label(self.main_frame)  # label edad value
        self.label_pos_movement_indicator.place(relx=0.1,rely=0.2)
        self.label_pos_movement_indicator.config(foreground = 'red', text='movimiento '+str(math.asin(0.5)), font=('Droid Naskh Shift Alt',16,'bold'))
        """
        
        """self.entry_correccion_x = ttk.Entry(self.main_frame)
        self.entry_correccion_x.place(relx=0.05,rely=0.2)
        #self.entry_correccion_x.pack()
        self.entry_correccion_x.state(['!disabled'])
        #self.entry_correccion_x.insert(0,'x')
        
        self.entry_correccion_y = ttk.Entry(self.main_frame)
        self.entry_correccion_y.place(relx=0.28,rely=0.2)
        """
        """self.label_up_x_button=ttk.Label(self.main_frame)  # label edad value
        self.label_up_x_button.place(relx=0.1,rely=0.25)
        #self.photo_up_x_button=PhotoImage(file = 'photos_silla/mode_1.png')
        #self.label_up_x_button.config(background = 'white', image = self.photo_up_x_button)
        self.label_up_x_button.config(background = 'red',  width = 3)
        self.label_up_x_button.bind(Start_Moving_Button, self.on_label_up_x_button)
        #self.label_up_x_button.bind(Stop_Moving_Button, self.on_B2_pressed_emergency)
        
        self.label_down_x_button=ttk.Label(self.main_frame)  # label edad value
        self.label_down_x_button.place(relx=0.15,rely=0.25)
        #self.photo_down_x_button=PhotoImage(file = 'photos_silla/mode_1.png')
        #self.label_down_x_button.config(background = 'white', image = self.photo_down_x_button)
        self.label_down_x_button.config(background = 'blue', width = 3)
        self.label_down_x_button.bind(Start_Moving_Button, self.on_label_down_x_button)
        #self.label_chage_controls_button.bind(Stop_Moving_Button, self.on_B2_pressed_emergency)
        
        self.label_up_y_button=ttk.Label(self.main_frame)  # label edad value
        self.label_up_y_button.place(relx=0.32,rely=0.25)
        #self.photo_up_y_button=PhotoImage(file = 'photos_silla/mode_1.png')
        #self.label_up_y_button.config(background = 'white', image = self.photo_up_y_button)
        self.label_up_y_button.config(background = 'red',width = 3)
        self.label_up_y_button.bind(Start_Moving_Button, self.on_label_up_y_button)
        """
        self.label_straight_button=ttk.Label(self.main_frame)  # label edad value
        self.label_straight_button.place(relx=0.605,rely=0.005)
        self.photo_straight_button_off=PhotoImage(file = 'photos_silla/front_button_off.png')
        self.photo_straight_button_on=PhotoImage(file = 'photos_silla/front_button_on.png')
        self.label_straight_button.config(background = 'white',image = self.photo_straight_button_off)
        ##self.label_straight_button.config(background = 'blue', width = 5)
        self.label_straight_button.bind(Start_Moving_Button, self.on_label_straight_button)
        self.label_straight_button.bind(Stop_Moving_Button, self.on_B2_pressed_emergency)
        self.label_straight_button.bind(Stop_Moving_Button_emergency, self.on_B2_pressed_emergency)
        
        print('wheel chair aplication running')

     """def on_indicador(self,event):

          self.label_pos_indicator.config(foreground = 'red', text='y: '+str(event.y)+'\n'+'x: '+str(event.x))
     """
     
     def on_label_up_x_button(self, event):
         
         self.correction_x = self.correction_x +1
         self.label_pos_indicator.config(text='correccion en x : '+ str(self.correction_x))
         
    
     def on_label_down_x_button(self, event):
         
         self.correction_x = self.correction_x -1
         self.label_pos_indicator.config(text='correccion en x : '+ str(self.correction_x))
        
     def on_label_up_y_button(self, event):
         
         self.correction_y = self.correction_y +1
         self.label_pos_init_indicator.config(text='correccion en y : '+ str(self.correction_y))
        
     def on_label_straight_button(self, event):
         
         if self.state == False:  #estado del boton on
               return
         
         global is_straight_button_pressed
         if(is_straight_button_pressed):
             
               is_straight_button_pressed = False
               self.label_indicator.bind(Keep_Moving_Button, self.on_timon_pressed)
               self.label_indicator.bind(Start_Moving_Button, self.on_mouse_B1_pressed_init_movement)
               self.label_indicator.bind(Start_Moving_Motion, self.on_mouse_movement_B3_hold)
               self.label_indicator.bind(Start_Moving_Release, self.on_mouse_movement_B3_release)

               self.main_frame.bind(Keep_Moving_Button, self.on_timon_pressed)
               self.main_frame.bind(Start_Moving_Button, self.on_mouse_B1_pressed_init_movement)
               self.main_frame.bind(Start_Moving_Motion, self.on_mouse_movement_B3_hold)
               self.main_frame.bind(Start_Moving_Release, self.on_mouse_movement_B3_release)

               self.label_dial.bind(Keep_Moving_Button, self.on_timon_pressed)
               self.label_dial.bind(Start_Moving_Button, self.on_mouse_B1_pressed_init_movement)
               self.label_dial.bind(Start_Moving_Motion, self.on_mouse_movement_B3_hold)
               self.label_dial.bind('<Motion>', self.do_nothing)
               self.label_dial.bind(Start_Moving_Release, self.on_mouse_movement_B3_release)

               self.photo_dial=PhotoImage(file = 'photos_silla/timon_480.png')
               self.label_dial.create_image(200,200, image = self.photo_dial)
               self.label_indicator.place(relx=0.719, rely= 0.415)
         else:
             
               is_straight_button_pressed = True
               
               os.system("DISPLAY=:0 xdotool mousemove 585 210")
               
               self.label_straight_button.config(background = 'white',image = self.photo_straight_button_on)
               self.label_straight_button.bind(Start_Moving_Button, self.on_B2_pressed_emergency)
          
               global first_move          
          
               self.global_y_pos_init=event.y_root
               self.global_x_pos_init=event.x_root
              
               if(first_move == True):
              
                    send_uart_data(77,79,86,69)#Move
               
               first_move = False
               
               send_uart_data(1, 127, 2, 254)
                              
               self.label_indicator.bind(Stop_Moving_Button_emergency, self.on_B2_pressed_emergency)
               self.label_indicator.bind(Start_Moving_Button, self.on_B2_pressed_emergency)
               self.label_indicator.bind(Start_Moving_Motion, self.do_nothing)
               self.label_indicator.bind(Start_Moving_Release, self.do_nothing)
               self.label_indicator.bind(without_click_motion, self.on_mouse_movement_in_straight)

               self.main_frame.bind(Stop_Moving_Button_emergency, self.on_B2_pressed_emergency)
               self.main_frame.bind(Start_Moving_Motion, self.do_nothing)
               self.main_frame.bind(Start_Moving_Release, self.do_nothing)
               self.main_frame.bind(Start_Moving_Button, self.on_B2_pressed_emergency)
               self.main_frame.bind(without_click_motion, self.on_mouse_movement_in_straight)

               #self.label_dial.bind(Start_Moving_Button, self.do_nothing)
               self.label_dial.bind(Start_Moving_Motion, self.do_nothing)
               self.label_dial.bind(Start_Moving_Button, self.on_B2_pressed_emergency)
               self.label_dial.bind(Start_Moving_Release, self.do_nothing)
               self.label_dial.bind(without_click_motion, self.on_mouse_movement_in_straight)
               self.label_dial.bind(Stop_Moving_Button_emergency, self.on_B2_pressed_emergency)
             
    
     def on_B2_pressed_emergency(self, event):

          send_uart_data(77,77,0,0)                 
          global first_move
         
          first_move=True
          first_correction = True
          
          os.system("DISPLAY=:0 xdotool mousemove 585 210")
          self.label_straight_button.config(background = 'white',image = self.photo_straight_button_off)
          self.label_straight_button.bind(Start_Moving_Button, self.on_label_straight_button)
        
##########        self.label_straight_button.bind(Stop_Moving_Button, self.on_B2_pressed_emergency)
        
          print('emergency click ****************************')

          if(self.binding_state == True):
              self.label_indicator.place(relx=0.719, rely= 0.415)
              
          
          self.label_indicator.bind(Start_Moving_Motion, self.do_nothing)
          self.main_frame.bind(Start_Moving_Motion, self.do_nothing)
          self.label_dial.bind(Start_Moving_Motion, self.do_nothing)
          
          global is_straight_button_pressed
          if(is_straight_button_pressed):
             
               is_straight_button_pressed = False
               self.label_indicator.bind(Keep_Moving_Button, self.on_timon_pressed)
               self.label_indicator.bind(Start_Moving_Button, self.on_mouse_B1_pressed_init_movement)
               self.label_indicator.bind(Start_Moving_Motion, self.on_mouse_movement_B3_hold)
               self.label_indicator.bind(Start_Moving_Release, self.on_mouse_movement_B3_release)
               self.label_indicator.bind(without_click_motion, self.do_nothing)
               
               self.main_frame.bind(Keep_Moving_Button, self.on_timon_pressed)
               self.main_frame.bind(Start_Moving_Button, self.on_mouse_B1_pressed_init_movement)
               self.main_frame.bind(Start_Moving_Motion, self.on_mouse_movement_B3_hold)
               self.main_frame.bind(Start_Moving_Release, self.on_mouse_movement_B3_release)
               self.main_frame.bind(without_click_motion, self.do_nothing)


               self.label_dial.bind(Keep_Moving_Button, self.on_timon_pressed)
               self.label_dial.bind(Start_Moving_Button, self.on_mouse_B1_pressed_init_movement)
               self.label_dial.bind(Start_Moving_Motion, self.on_mouse_movement_B3_hold)
               self.label_dial.bind('<Motion>', self.do_nothing)
               self.label_dial.bind(Start_Moving_Release, self.on_mouse_movement_B3_release)
               

               self.photo_dial=PhotoImage(file = 'photos_silla/timon_480.png')
               self.label_dial.create_image(200,200, image = self.photo_dial)
               self.label_indicator.place(relx=0.719, rely= 0.415)
          
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
          self.label_S_button.bind(Start_Moving_Button, self.on_change_controls_button)
          
          self.label_N_button=ttk.Label(self.main_frame)  # label edad value
          self.label_N_button.place(relx=0.725,rely=0.22)
          self.label_N_button.config(background = 'blue', width = 3)
          self.label_N_button.bind(Start_Moving_Button, self.on_change_controls_button)

          self.label_E_button=ttk.Label(self.main_frame)  # label edad value
          self.label_E_button.place(relx=0.84,rely=0.435)
          self.label_E_button.config(background = 'blue', width = 3)
          self.label_E_button.bind(Start_Moving_Button, self.on_change_controls_button)
          
          self.label_W_button=ttk.Label(self.main_frame)  # label edad value
          self.label_W_button.place(relx=0.6,rely=0.435)
          self.label_W_button.config(background = 'blue', width = 3)
          self.label_W_button.bind(Start_Moving_Button, self.on_change_controls_button)
          
          self.label_NW_button=ttk.Label(self.main_frame)  # label edad value
          self.label_NW_button.place(relx=0.6625,rely=0.3275)
          self.label_NW_button.config(background = 'blue', width = 3)
          self.label_NW_button.bind(Start_Moving_Button, self.on_change_controls_button)

          self.label_NE_button=ttk.Label(self.main_frame)  # label edad value
          self.label_NE_button.place(relx=0.7825,rely=0.3275)
          self.label_NE_button.config(background = 'blue', width = 3)
          self.label_NE_button.bind(Start_Moving_Button, self.on_change_controls_button)

          self.label_SW_button=ttk.Label(self.main_frame)  # label edad value
          self.label_SW_button.place(relx=0.6625,rely=0.5425)
          self.label_SW_button.config(background = 'blue', width = 3)
          self.label_SW_button.bind(Start_Moving_Button, self.on_change_controls_button)

          self.label_SE_button=ttk.Label(self.main_frame)  # label edad value
          self.label_SE_button.place(relx=0.7825,rely=0.5425)
          self.label_SE_button.config(background = 'blue', width = 3)
          self.label_SE_button.bind(Start_Moving_Button, self.on_change_controls_button)
          """

     def on_quit(self,master):

          global running_program

          
          send_uart_data(69, 69, 69, 69) # EEEE
               
          running_program = False

          ser.flushInput()
          ser.flushOutput()
          ser.close()
          time.sleep(1)
          master.destroy()
          #sys.exit()
          os.system("sudo ./hub-ctrl -h 0 -P 2 -p 0")#Power off USB
          os.system("sudo ./hub-ctrl -h 0 -P 3 -p 0")
          print("Empieza")
          time.sleep(0.5)
          print("Termina")
          os.system("sudo ./hub-ctrl -h 0 -P 2 -p 1")
          os.system("sudo ./hub-ctrl -h 0 -P 3 -p 1")               
          os._exit(1)
          

     def do_nothing(self,event):
          
          pass

     def change_binding(self):

          if(self.binding_state == True): #true es el estado inicial
               
               self.label_indicator.bind(Keep_Moving_Button, self.on_timon_pressed)
               self.label_indicator.bind(Start_Moving_Button, self.on_mouse_B1_pressed_init_movement)
               self.label_indicator.bind(Start_Moving_Motion, self.on_mouse_movement_B3_hold)
               self.label_indicator.bind(without_click_motion, self.do_nothing)
               self.label_indicator.bind(Start_Moving_Release, self.on_mouse_movement_B3_release)

               self.main_frame.bind(Keep_Moving_Button, self.on_timon_pressed)
               self.main_frame.bind(Start_Moving_Button, self.on_mouse_B1_pressed_init_movement)
               self.main_frame.bind(Start_Moving_Motion, self.on_mouse_movement_B3_hold)
               self.main_frame.bind(without_click_motion, self.do_nothing)
               self.main_frame.bind(Start_Moving_Release, self.on_mouse_movement_B3_release)

               self.label_dial.bind(Keep_Moving_Button, self.on_timon_pressed)
               self.label_dial.bind(Start_Moving_Button, self.on_mouse_B1_pressed_init_movement)
               self.label_dial.bind(Start_Moving_Motion, self.on_mouse_movement_B3_hold)
               self.label_dial.bind('<Motion>', self.do_nothing)
               self.label_dial.bind(Start_Moving_Release, self.on_mouse_movement_B3_release)

               self.photo_dial=PhotoImage(file = 'photos_silla/timon_480.png')
               self.label_dial.create_image(200,200, image = self.photo_dial)
               self.label_indicator.place(relx=0.719, rely= 0.415)

          else:

               self.label_indicator.bind(Start_Moving_Button, self.do_nothing)
               self.label_indicator.bind(Start_Moving_Button, self.do_nothing)
               self.label_indicator.bind(Start_Moving_Motion, self.do_nothing)
               self.label_indicator.bind(Start_Moving_Release, self.do_nothing)

               self.main_frame.bind(Start_Moving_Button, self.do_nothing)
               self.main_frame.bind(Start_Moving_Button, self.do_nothing)
               self.main_frame.bind(Start_Moving_Motion, self.do_nothing)
               self.main_frame.bind(Start_Moving_Release, self.do_nothing)

               #self.label_dial.bind(Start_Moving_Button, self.do_nothing)
               self.label_dial.bind(Start_Moving_Motion, self.do_nothing)
               self.label_dial.bind(Start_Moving_Release, self.do_nothing)
               self.label_dial.bind('<Motion>', self.area_timon)
               self.label_dial.bind(Start_Moving_Button, self.alternative_timon_B1_pressed_init_movement)
                      

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
               

     def alternative_timon_B1_pressed_init_movement(self, event):

          if self.state == False:  #estado del boton on
               return

          global  first_move, speed_indicator_value

          

          #self.last_timon_image = self.actual_timon_image
          
          self.photo_dial=PhotoImage(file = 'photos_silla/red_'+self.actual_timon_image)
          print("foto --- "  +self.actual_timon_image)
          self.label_dial.create_image(200,200, image = self.photo_dial)
          
          if(self.actual_timon_image == 'timon_S.png'):
                   
                   ##print('corrigiendo timon_S.png ********************************')
                   
                   if(speed_indicator_value + 1 == 1):
                       
                       self.correction_x = 25
                       
                   if(speed_indicator_value + 1 == 2 ):
                       
                       self.correction_x = 15
                   
                   if(speed_indicator_value + 1 == 3):
                       
                       self.correction_x = 10
                    
                   if(speed_indicator_value + 1 == 4):
                       
                       self.correction_x = 5
                       
                   if(speed_indicator_value + 1 == 5):
                       
                       self.correction_x = 3
                       
                   print('corrigiendo timon_S.png ********************************'+ str(self.correction_x))
                   
                   
          if(self.actual_timon_image == 'timon_N.png'):
                   
                   ##print('corrigiendo timon_N.png ********************************')
                   
                   if(speed_indicator_value + 1 == 5):
                       
                       self.correction_x = -15
                       
                   if(speed_indicator_value + 1 == 4):
                       
                       self.correction_x = -18 
                       
                   if(speed_indicator_value + 1 == 1 or speed_indicator_value + 1 == 2 or speed_indicator_value + 1 == 3):
                       
                       self.correction_x = -20
                       
                   print('corrigiendo timon_N.png ********************************'+ str(self.correction_x)) 
                   
          if(self.actual_timon_image == 'timon_NW.png' or self.actual_timon_image == 'timon_NW2.png' or self.actual_timon_image == 'timon_NW6.png'):
                   
                   ##print('corrigiendo timon_NW.png ********************************')
                   
                   if(speed_indicator_value + 1 == 3):
                       
                       self.correction_x = -15
                       
                   if(speed_indicator_value + 1 == 1 or speed_indicator_value + 1 == 2 or speed_indicator_value + 1 == 4 or speed_indicator_value + 1 == 5):
                       
                       self.correction_x = -10
                       
                   print('corrigiendo timon_NW.png ********************************'+ str(self.correction_x))
          
          if(first_move == True):

      
               send_uart_data(77,79,86,69)


               

          first_move = False

          #time.sleep(0.1)

          


          send_uart_data(1,timon_position_ranges[self.actual_timon_image_pos]["xcor"] + self.correction_x, 2,timon_position_ranges[self.actual_timon_image_pos]["ycor"] + self.correction_y)
          
               
          self.correction_x = 0
          


     def on_timon_pressed(self, event):

         if self.state == False:  #estado del boton on
               return

         global  first_move

         
         if(first_move == False):

             uart_busy = True

             send_uart_data(75,69,69,80)#MOVE
             
             

     def on_claxon_button(self,event):


         global  timer_event_started, timeout#, valor_recibido
          
         if (timeout == False):
              return
         else:
              timeout = False
            
          
         timer_event_started = True 

         
         self.photo_claxon=PhotoImage(file = 'photos_silla/claxon_on.png')  #my_icons/off.png
         self.label_claxon_button.config(compound = 'center', image=self.photo_claxon)
         self.label_claxon_button.place(relx=0.169,rely=0.29)

         
         send_uart_data(67,97,0,0)# ASCII C de aumentar      # ASCII a de activar
         

     def on_claxon_release(self,event):

          

          
          self.photo_claxon=PhotoImage(file = 'photos_silla/claxon.png')  #my_icons/off.png
          self.label_claxon_button.config(compound = 'center', image=self.photo_claxon)
          self.label_claxon_button.place(relx=0.169,rely=0.31)
         
          send_uart_data(67,100,0,0) # ASCII C de claxon      # ASCII d de desactivar
          

     def on_led_button(self, event):

          global timer_event_started, timeout#, valor_recibido
          
          if (timeout == False):
              return
          else:
              timeout = False
                    
          timer_event_started = True
          

          self.label_led_button.place(relx=0.84, rely = 0.89)

          send_uart_data(84,0,0,0)# ASCII T  para pulso y apagar silla con error
          


     def on_led_release(self, event):

          self.label_led_button.place(relx=0.85, rely = 0.9)
         
     def on_on_button(self,event):

          global speed_indicator_value, timer_event_started, timeout#, valor_recibido
          
          if timeout == False:
              return
          else:
              timeout = False
            
          
          timer_event_started = True 
          
    

          if(recibo_perfecto == False):
               self.photo_quit=PhotoImage(file = 'photos_silla/salir_red.png') 
               self.label_quit_button.config(compound = 'center', image=self.photo_quit)

          else:
               self.photo_quit=PhotoImage(file = 'photos_silla/salir_green.png') 
               self.label_quit_button.config(compound = 'center', image=self.photo_quit)



          if self.state == True:
               self.state = False
               self.photo_off=PhotoImage(file = 'photos_silla/speeed.png')
               self.label_off_button.config(compound = 'center', image=self.photo_off)

               
               send_uart_data(84,79,70,70)
            
               
          else:
               if self.state == False:
                   
                    self.state = True
                    speed_indicator_value=initspeed-1
                    self.photo_off=PhotoImage(file = 'photos_silla/'+speed_indicator_names[speed_indicator_value]) 
                    self.label_off_button.config(compound = 'center', image=self.photo_off)

                    send_uart_data(84,0,79,78)
                    
                    

          #time.sleep(0.1)

     def on_lower(self,event):

          global speed_indicator_value, timer_event_started, timeout#, valor_recibido
          
          if timeout == False:
              return
          else:
              timeout = False
            
          
          timer_event_started = True
          
          
          if self.state == False:  #estado del boton on
               return

          if(recibo_perfecto == False):#si no pincha comunicacion debe estar en rojo el boton salir
               self.photo_quit=PhotoImage(file = 'photos_silla/salir_red.png') 
               self.label_quit_button.config(compound = 'center', image=self.photo_quit)

          else: #si pincha comunicacion debe estar en verde el boton salir
               self.photo_quit=PhotoImage(file = 'photos_silla/salir_green.png') 
               self.label_quit_button.config(compound = 'center', image=self.photo_quit)

          

          self.photo_disminuir=PhotoImage(file = 'photos_silla/down_on.png')  
          self.label_lower_button.config(compound = 'center', image=self.photo_disminuir)
          self.label_lower_button.place(relx = 0.004, rely = 0.526)

          if speed_indicator_value > 0:
               speed_indicator_value=speed_indicator_value-1
               self.photo_speed_indicator=PhotoImage(file = 'photos_silla/'+speed_indicator_names[speed_indicator_value])  #my_icons/off.png
               self.label_off_button.config(image=self.photo_speed_indicator)

          
          send_uart_data(76, speed_indicator_value+1, 76, 76)  # ASCII L de lower disminuir
          

      
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
         
          global speed_indicator_value, timer_event_started, timeout#, valor_recibido
          
          if timeout == False:
              return
          else:
              timeout = False           
          
          timer_event_started = True
          

          if self.state == False:
               return

          if(recibo_perfecto == False):#si no pincha comunicacion debe estar en rojo el boton salir
               self.photo_quit=PhotoImage(file = 'photos_silla/salir_red.png') 
               self.label_quit_button.config(compound = 'center', image=self.photo_quit)

          else: #si pincha comunicacion debe estar en verde el boton salir
               self.photo_quit=PhotoImage(file = 'photos_silla/salir_green.png') 
               self.label_quit_button.config(compound = 'center', image=self.photo_quit)


              

          self.photo_aumentar=PhotoImage(file = 'photos_silla/up_on.png')  #my_icons/off.png
          self.label_higher_button.config(compound = 'center', image=self.photo_aumentar)

          if speed_indicator_value < 4:
               speed_indicator_value=speed_indicator_value+1
               self.photo_speed_indicator=PhotoImage(file = 'photos_silla/'+speed_indicator_names[speed_indicator_value])  #my_icons/off.png
               self.label_off_button.config(image=self.photo_speed_indicator)

    
          send_uart_data(72, speed_indicator_value+1, 72, 72) # ASCII H de higher aumentar
          

          

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


     def on_mouse_B1_pressed_init_movement(self,event):

          ##print("Se ejecuto")
          if self.state == False:  #estado del boton on
               return


          #centro indicador x=0.72  y=0.42  r= 0.18  rx= 0.18*0.6
          global first_move

          
          
          self.global_y_pos_init=event.y_root
          self.global_x_pos_init=event.x_root

          #self.label_pos_init_indicator.config(text='y: '+str(self.global_y_pos_init)+'\n'+'x: '+str(self.global_x_pos_init))
          if(first_move == True):

              
               send_uart_data(77,79,86,69)#Move
               

          first_move = False
          #time.sleep(0.1)
          
          """self.global_y_pos_init=event.y
          self.global_x_pos_init=event.x
          """

          #self.label_indicator.place(relx=0.1022, rely=0.42)
       
##------------------------------------------------------------------------------------------------------------------------------revisar esto
     def on_mouse_movement_in_straight(self,event):
         
         self.global_x_pos=event.x_root
         delta_x = self.global_x_pos - self.global_x_pos_init
         
         if self.global_x_pos < 440:
             os.system("DISPLAY=:0 xdotool mousemove 440 "+str(event.y_root))
         if(abs(delta_x) > delta_x_max):
             if(delta_x < 0):
                 delta_x = (-1)*delta_x_max
             else:
                 delta_x = delta_x_max
              
         dx = int(70 * delta_x/delta_x_max)
         xf = 570  + dx
                  
         xcoord = int(((int((int(dx)+70)*1.8214) - 127)/2)+127)
         
         send_uart_data(1, xcoord, 2, 254)
          
         self.indicator_actual_pos_x = xf/800        
          
         self.label_indicator.place(relx= self.indicator_actual_pos_x, rely= 0.415)
         pass
         
         
     def on_mouse_movement_B3_hold(self,event):    

          global first_correction,timeout_correct_dir,timer_correct_dir_event_started, dont_move
##          if dont_move == True:
##              dont_move = False
##              return
          
          if self.state == False:  #estado del boton on
               return

          #centro indicador x=0.72  y=0.42     r= 0.18 (60 pix)    rx= 0.18*0.6 (36 pix)
    
          if self.global_x_pos < 440:
             os.system("DISPLAY=:0 xdotool mousemove 440 "+str(event.y_root))
             
          if(abs(self.global_y_pos- event.y_root))< y_correction_movement  and (abs(self.global_x_pos- event.x_root))< y_correction_movement:
              return
          
          self.global_y_pos=event.y_root
          self.global_x_pos=event.x_root                  
          
          delta_x = 1
          delta_y = 1
          
          if (self.global_x_pos - self.global_x_pos_init) == 0:
               
               if (self.global_y_pos - self.global_y_pos_init) < 0:
                    alpha=math.asin(-1)
               
               if (self.global_y_pos - self.global_y_pos_init) > 0:
                         alpha=math.asin(1)
               else:
                         alpha=0
               
               

          else:
               delta_y = self.global_y_pos - self.global_y_pos_init
               delta_x = self.global_x_pos - self.global_x_pos_init
                                    
               alpha = math.atan( (delta_y) / (delta_x) )
               
               delta_x = abs(delta_x)
               delta_y = abs(delta_y)

          if(delta_y > delta_y_max):
              delta_y = delta_y_max
              
          if(delta_x > delta_x_max):
              delta_x = delta_x_max
          
          factor = 1
          
          if (self.global_x_pos - self.global_x_pos_init) < 0:
               
               factor = (-1)

          dx = 70* (delta_x/delta_x_max) * (math.cos(alpha))*(factor)
          dy = 70* (delta_y/delta_y_max) * (math.sin(alpha))*(factor)
          
                        
          xf = 570  + dx
          yf = 200  + dy

          xcoord = int((int(dx)+70)*1.8214)
          if(abs(xcoord - 127) < 100):
              xcoord = int((xcoord -127)/2)+127
              
          ycoord = int((255-(int(dy)+70)*1.8214))
          if(abs(ycoord - 127) < 100):
              ycoord = int((ycoord -127)/2)+127
          print(" xcoord ---------------------")
          print(xcoord)
          print(" ycoord ---------------------")
          print(ycoord)
          
          """correct_optimization = False
          
          if  first_correction == True and (xcoord < xcoord_max_correction and xcoord > xcoord_min_correction):##**********************************************************************************************
              timer_correct_dir_event_started = True
              first_correction = False
              timeout_correct_dir = True
              
          if timeout_correct_dir == True:
              if xcoord < xcoord_max_correction and xcoord > xcoord_min_correction and ycoord > 127:
                 
                  correct_optimization = True
                  xcoord = center_of_correction
                  
                  ##self.label_indicator.event_generate('<Motion>', warp=True, x=570, y=130)
          """
                     
          send_uart_data(1, xcoord, 2, ycoord)
          
          self.indicator_actual_pos_x = xf/800
          self.indicator_actual_pos_y = yf/480
          
          self.label_indicator.place(relx= self.indicator_actual_pos_x, rely= self.indicator_actual_pos_y)
          """
          if correct_optimization == True:
              self.label_indicator.place(relx= 0.7136, rely= 0.2708)
              os.system("DISPLAY=:0 xdotool mousemove 585 145")
              
          else:   
              self.label_indicator.place(relx= self.indicator_actual_pos_x, rely= self.indicator_actual_pos_y)
##              os.system("DISPLAY=:0 xdotool mousemove "+str(xf+18)+" "+str(yf+18))
##              dont_move = True

          #self.label_pos_movement_indicator.config(foreground = 'red', text=str(alpha)
          """
          
          
             
     def on_mouse_movement_B3_release(self, event):

          send_uart_data(77,77,0,0)
          
          if self.state == False:  #estado del boton on
               return
          
      
          global first_move, first_correction

          print(' Movimiento detenido **************************************************')

          first_move=True
          first_correction = True

          
          
          if(self.binding_state == True):
              self.label_indicator.place(relx=0.719, rely= 0.415)
              os.system("DISPLAY=:0 xdotool mousemove 585 200")
        
          self.label_indicator.bind(Start_Moving_Motion, self.on_mouse_movement_B3_hold)
          self.main_frame.bind(Start_Moving_Motion, self.on_mouse_movement_B3_hold)
          self.label_indicator.bind(Start_Moving_Motion, self.on_mouse_movement_B3_hold)
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

     global running_program, valor_recibido,recibo_perfecto, first_move, uart_counter

     time.sleep(3)
     
     while running_program == True:
          comando_recibido=ser.readline(13)
          
          if(comando_recibido != ''):
               
               valor_recibido = comando_recibido
               
               ##print('recibido: ')
               ##print(uart_counter)
               ##print(valor_recibido)
          if(valor_recibido == bytearray([160,160,160,160,111,111,111,111,111,160,160,160,160])):
               print('valor recibido fin por error*****************************************')
               os.system("sudo ./hub-ctrl -h 0 -P 2 -p 0") #power off USB
               os.system("sudo ./hub-ctrl -h 0 -P 3 -p 0")
               
               time.sleep(0.5)
               
               os.system("sudo ./hub-ctrl -h 0 -P 2 -p 1")
               os.system("sudo ./hub-ctrl -h 0 -P 3 -p 1")
               
          if(valor_recibido == bytearray([160,160,160,160,221,221,221,221,221,160,160,160,160])):

               print('valor recibido fin *****************************************')
               os.system("sudo ./hub-ctrl -h 0 -P 2 -p 0") #power off USB
               os.system("sudo ./hub-ctrl -h 0 -P 3 -p 0")
               
               time.sleep(0.5)
               
               os.system("sudo ./hub-ctrl -h 0 -P 2 -p 1")
               os.system("sudo ./hub-ctrl -h 0 -P 3 -p 1")

               os._exit(1)
            
        
          send_bytes_copy = []
          send_bytes_copy.extend(send_bytes)
          send_bytes_copy[8]=0
          
          if(valor_recibido == bytearray([160,160,160,160,83,83,83,83,0,160,160,160,160]) or valor_recibido == bytearray(send_bytes_copy) or valor_recibido == bytearray([160,160,160,160,170,170,170,170,0,160,160,160,160]) or valor_recibido == bytearray([160,160,160,160,204,204,204,204,0,160,160,160,160])): #debe ser igual el ultimo enviado y el recibido

               recibo_perfecto=True
               
               
               
               if(valor_recibido == bytearray([160,160,160,160,83,83,83,83,0,160,160,160,160])):
                   
                   first_move = True

                   ##print('valor recibido stop********')
          else:
               
               recibo_perfecto=False
               
               ##print('valor recibido error ')

          
def function_check_connection():

     global running_program, uart_busy

    
     send_uart_data(204, 204, 204, 204)# CC para inicio de aplicacion
     
     time.sleep(2)

     while running_program == True:      
##          print('enviando check connection')

          while (uart_busy == True):
               pass
          
          send_uart_data(170, 170, 170, 170)        
          
          time.sleep(2)
    
    
def function_timer():
    
    global timer_event_started, timeout
    
    while running_program == True:
        
        time_init = time.time()

        while timer_event_started == True:
            
            if(time.time()-time_init >= timer_buttons_delay):
                
                timeout = True
                timer_event_started = False
                ##print('paso el tiempo')
                time.sleep(0.05)
            
            
def function_timer_correct_dir():
    
    global timer_correct_dir_event_started, timeout_correct_dir, function_timer_correct_dir
    
    first_capture = True
    ##print('Hilo de tiempo de correcion')
    time_init = time.time()
    
    while running_program == True:      
        
        
        while timer_correct_dir_event_started == True:
            
            if(first_capture == True):
                
                time_init = time.time()
                first_capture = False
                
                
            
            if(time.time()-time_init >= timer_delay_correct_direction):
                
                timeout_correct_dir = False
                timer_correct_dir_event_started = False
                
                first_capture = True
                
                  
    
def main():

     thread_TK = threading.Thread( target = function_TKInter_Thread )
     thread_check_connection = threading.Thread( target = function_check_connection )
     thread_UART_Read = threading.Thread( target = function_UART_Read )
     thread_timer = threading.Thread( target = function_timer )
     ##thread_timer_correct_dir = threading.Thread( target = function_timer_correct_dir )
     
     thread_TK.daemon = True
     thread_check_connection.daemon = True
     thread_UART_Read.daemon = True
     thread_timer.daemon = True
     ##thread_timer_correct_dir.daemon = True
     
     
     thread_TK.start()
     thread_check_connection.start()
     thread_UART_Read.start()
     thread_timer.start()
     ##thread_timer_correct_dir.start()
     
     thread_UART_Read.join()
     thread_check_connection.join()
     thread_TK.join()
     thread_timer.join()
     ##thread_timer_correct_dir.join()
     
     print('program finished')
     
if __name__ == "__main__": main()


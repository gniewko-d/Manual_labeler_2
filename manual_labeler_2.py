
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  1 17:28:58 2022

@author: malgo
"""

import math
import keyboard
import vlc
from time import sleep
import tkinter as tk
import requests
from PIL import Image, ImageTk
from io import BytesIO
from tkinter import messagebox
import easygui

import pyttsx3
import random
from pandastable import Table
import cv2
import pandas as pd
import numpy as np
import csv
from datetime import date
def advert():
    root_v1 = tk.Tk()
    root_v1.title("Ad")
    url = "https://i.postimg.cc/hjpLn1gY/image-v1-1.png"

    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img = ImageTk.PhotoImage(img)
    label1 = tk.Label(root_v1,image= img, bg = "black")
    label1.pack()
    root_v1.after(3000, lambda: root_v1.destroy())
    root_v1.mainloop()

df3 = None
df4 = None
label_name = [f"{None}",f"{None}",f"{None}",f"{None}",f"{None}",f"{None}",f"{None}",f"{None}",f"{None}"]
configruation_title = f"{None}"
video_file = None
available_formats = ["flv", "avi", "amv", "mp4"]
length_movie = False
df_checker = False
current_label = "starter"
start_frame_bool = False
label_list = None
time_jump = 0
video_rate = 1.0
start_frame_bool_v2 = False
class Application:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Manual Labeler")
        self.root.protocol("WM_DELETE_WINDOW", disable_event)
    
        self.first_frame = tk.Frame(self.root, background="#116562", width=400, height = 30)
        self.first_frame.pack(expand=True, fill='both')
        self.first_frame.pack_propagate(0)
        
        self.open_file = tk.Button(self.first_frame, text = "Load video", command = self.easy_open, background="black", foreground="green", width = 26)
        self.open_file.pack(side= tk.LEFT, padx=1, pady=1, expand=True, fill='both')
        self.text = f"Video: {None}"
        self.current_video = tk.Text(self.first_frame, height = 1, width = 16, background="black", foreground="green", insertbackground = "white")
        self.current_video.insert(tk.INSERT, self.text)
        self.desired_font = tk.font.Font(size = 14)
        self.current_video.configure(font = self.desired_font)
        self.current_video.pack(side=tk.RIGHT, padx=1, pady=1, expand=True, fill='both')
        
        self.second_frame = tk.Frame(self.root, background="#116562", width=400, height = 30)
        self.second_frame.pack(side = tk.TOP, expand=True, fill='both')
        self.second_frame.pack_propagate(0)
        
        self.keyboard = tk.Button(self.second_frame, text="Keyboard settings", command = self.keyboard_settings, background="black", foreground="green", width = 13)
        self.keyboard.pack(side=tk.LEFT, padx=1, pady=1, expand=True, fill='both')
        
        self.label_1_9 = tk.Button(self.second_frame, text="Labels settings", command = self.label_settings, background="black", foreground="green")
        self.label_1_9.pack(side=tk.RIGHT, padx=1, pady=1, expand=True, fill='both')
        
        self.third_frame_v1 = tk.Frame(self.root, background="#116562", width=400, height = 30)
        self.third_frame_v1.pack(side = tk.TOP, expand=True, fill='both')
        self.third_frame_v1.pack_propagate(0)
        
        self.start_labeling = tk.Button(self.third_frame_v1, text="Start labeling", command = self.bridge_start_video, background="black", foreground="green", width = 15)
        self.start_labeling.pack(side=tk.LEFT, padx=1, pady=1, expand=True, fill='both')
        
        self.show_df = tk.Button(self.third_frame_v1, text="Show data frame", command = self.draw_table, background="black", foreground="green")
        self.show_df.pack(side=tk.LEFT, padx=1, pady=1, expand=True, fill='both')
        
    
        self.fifth_frame_v1 = tk.Frame(self.root, background="#116562", width=400, height = 30)
        self.fifth_frame_v1.pack(side = tk.TOP, expand=True, fill='both')
        self.fifth_frame_v1.pack_propagate(0)
    
        self.save_machine_state = tk.Button(self.fifth_frame_v1, text = "Save current state", command = run_save_machine_state, background="black", foreground="green", width = 17)
        self.save_machine_state.pack(side=tk.LEFT, padx=1, pady=1, expand=True, fill='both')
        
        self.load_machine_state = tk.Button(self.fifth_frame_v1, text = "Load state from file", command = lambda:[load_machine_state_fun(), self.label_changer_2()], background="black", foreground="green")
        self.load_machine_state.pack(side=tk.LEFT, padx=1, pady=1, expand=True, fill='both')
        
        self.sixth_frame = tk.Frame(self.root, background="#116562", width=400, height = 30)
        self.sixth_frame.pack(side = tk.TOP, expand=True, fill='both')
        self.sixth_frame.pack_propagate(0)
        
        self.create_configuration = tk.Button(self.sixth_frame, text = "Create configuration", command = self.creat_configuration_fun, background="black", foreground="green", width = 19)
        self.create_configuration.pack(side=tk.LEFT, padx=1, pady=1, expand=True, fill='both')
        
        self.load_configuration = tk.Button(self.sixth_frame, text = "Load configuration", command = lambda:[load_configuration_fun(), self.label_changer_2()], background="black", foreground="green", width = 17)
        self.load_configuration.pack(side=tk.LEFT, padx=1, pady=1, expand=True, fill='both')
        
        self.fourth_frame_v1 = tk.Frame(self.root, background="#116562", width=400, height = 30)
        self.fourth_frame_v1.pack(side = tk.TOP, expand=True, fill='both')
        self.fourth_frame_v1.pack_propagate(0)
        
        self.save_labeled_video = tk.Button(self.fourth_frame_v1, text= "Save data", command = start_vido3, background="black", foreground="green", width = 5)
        self.save_labeled_video.pack(side=tk.LEFT, padx=1, pady=1, expand=True, fill='both')
        
        self.close_gui = tk.Button(self.fourth_frame_v1, text= "Exit", command = self.close_gate, background="black", foreground="green", activebackground = "white")
        self.close_gui.pack(side=tk.LEFT, padx=1, pady=1, expand=True, fill='both')
        
        self.engine = pyttsx3.init()
        self.list_of_voices = ['Hello World', "welcome to the Labeling world", "hello friend", "I wish you fruitful work", "hello user", "I will try my best to help you work", "What a nice day to label something", "Thank your for your contribution", "Verifying ID"]
        self.list_of_voices_2 = ["Have a nice day", "Have a pleasant journey", "Time to say goodbye ", "It was nice to see you again", "Peace"]
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)
        self.engine.say(random.choice(self.list_of_voices))
        self.engine.runAndWait()


    def close_gate(self):
        msgbox = tk.messagebox.askquestion ('Exit Application','Are you sure you want to exit the application? Unsaved data will be lost',icon = 'warning')
        if msgbox == "yes":
            self.engine.say(random.choice(self.list_of_voices_2))
            self.engine.runAndWait()
            self.root.destroy()
        else:
            pass
    def close_gate2(self):
        msgbox = tk.messagebox.askquestion ('Exit Application','Are you sure you want to exit the support window? Unsaved data will be lost',icon = 'warning')
        if msgbox == "yes":
            self.root_support.destroy()
        else:
            pass
    def easy_open(self):
        global video_file, available_formats, player
        video_file = easygui.fileopenbox(title="Select An Video", filetypes= ["*.gif", "*.flv", "*.avi", "*.amv", "*.mp4"])
        if video_file != None:
            video_title = video_file.split("\\")
            video_format = video_title[-1].split(".")
            video_format = video_format[-1].lower()
            if video_format in available_formats:
                self.current_video.delete("1.0","end")
                self.text = f"Video: {video_title[-1]}"
                self.current_video.configure(width = len(self.text))
                self.current_video.insert(tk.INSERT, self.text)
                messagebox.showinfo("Information box", "Video uploaded")
                vlc_instance = vlc.Instance()
                player = vlc_instance.media_player_new()
                media = vlc_instance.media_new(video_file)
                player.set_media(media)
            else:
                messagebox.showerror("Error box", "Wrong format of video!")
                messagebox.showinfo("Information box", f'Currently available formats: .flv, .avi, .amv, .mp4, \nformat of your video : {video_format}')
        else:
            self.current_video.delete("1.0","end")
            self.text = "Video: None"
            self.current_video.configure(width = len(self.text))
            self.current_video.insert(tk.INSERT, self.text)
            messagebox.showerror("Error box", "Video was not loaded")
        
    def keyboard_settings(self):
        global fps
        self.new_root = tk.Toplevel(self.root)
        self.new_root.title("Keyboard_settings")
        
        self.first_frame_v1 = tk.Frame(self.new_root, background="black")
        self.first_frame_v1.pack(expand=True, fill='both')
        self.instruction = tk.Text(self.first_frame_v1, height = 23, width = 70)
        self.text_v1 = "Press on your keyboard:\n a = move one frame backward\n d = move one frame forward\n space = pause/resume the video\n z = slow down the video\n c = speed up the video\n x = video speed back to normal\n e = frame to which (without it) all the preceding ones will\n\t be appropriately marked (depends on labels name set by user).\n\t Start point is set by key 1-9\n key 1-9 = label current frame and jumpt to next one or\n\t set the beginning of the range.\n\t Next you can move to whatever frame (backward or forward)\n\t and there set the end of the range by key e.\n\t All frames within that range will be labeled\n g = delete last used label (Check active label) from current frame\n h = removes the last labelled range\n"
        conteiner = ["~"*70, "~"*70, self.text_v1, "="*70, "="*70]
        
        for i in range(len(conteiner)):
            self.instruction.insert(tk.INSERT, conteiner[i])
            self.instruction.pack(side=tk.TOP, expand=True, fill='both')
            self.instruction.configure(foreground="green", background= "black")

    def label_settings(self):
        global label_name
        self.new_root_2 = tk.Toplevel(self.root, background= "black")
        self.new_root_2.title("Label_settings")
        
        self.first_frame_v2 = tk.Frame(self.new_root_2, background="black")
        self.first_frame_v2.pack()
        
        self.label_1 = tk.Label(self.first_frame_v2, text = "key_1 label:", foreground="green", background= "black")
        self.label_1.pack(side=tk.LEFT)
        
        self.label_1_text_box = tk.Text(self.first_frame_v2, height = 1, width = 20, foreground="green", background= "black", insertbackground = "white")
        self.label_1_text_box.insert(tk.INSERT, label_name[0])
        self.label_1_text_box.pack(side=tk.LEFT)
        
        self.second_frame_v1 = tk.Frame(self.new_root_2, background= "black")
        self.second_frame_v1.pack(side = tk.TOP)
        
        self.label_2 = tk.Label(self.second_frame_v1, text = "key_2 label:", foreground="green", background= "black")
        self.label_2.pack(side=tk.LEFT)
        
        self.label_2_text_box = tk.Text(self.second_frame_v1, height = 1, width = 20, foreground="green", background= "black",insertbackground = "white")
        self.label_2_text_box.insert(tk.INSERT, label_name[1])
        self.label_2_text_box.pack(side=tk.LEFT)
        
        self.third_frame = tk.Frame(self.new_root_2, background= "black")
        self.third_frame.pack(side = tk.TOP)
        
        self.label_3 = tk.Label(self.third_frame, text = "key_3 label:", foreground="green", background= "black")
        self.label_3.pack(side=tk.LEFT)
        
        self.label_3_text_box = tk.Text(self.third_frame, height = 1, width = 20, foreground="green", background= "black", insertbackground = "white")
        self.label_3_text_box.insert(tk.INSERT, label_name[2])
        self.label_3_text_box.pack(side=tk.LEFT)
        
        self.fourth_frame = tk.Frame(self.new_root_2, background= "black")
        self.fourth_frame.pack(side = tk.TOP)
        
        self.label_4 = tk.Label(self.fourth_frame, text = "key_4 label:", foreground="green", background= "black")
        self.label_4.pack(side=tk.LEFT)
        
        self.label_4_text_box = tk.Text(self.fourth_frame, height = 1, width = 20, foreground="green", background= "black", insertbackground = "white")
        self.label_4_text_box.insert(tk.INSERT, label_name[3])
        self.label_4_text_box.pack(side=tk.LEFT)
        
        self.fifth_frame = tk.Frame(self.new_root_2, background= "black")
        self.fifth_frame.pack(side = tk.TOP)
        
        self.label_5 = tk.Label(self.fifth_frame, text = "key_5 label:", foreground="green", background= "black")
        self.label_5.pack(side=tk.LEFT)
        
        self.label_5_text_box = tk.Text(self.fifth_frame, height = 1, width = 20, foreground="green", background= "black", insertbackground = "white")
        self.label_5_text_box.insert(tk.INSERT, label_name[4])
        self.label_5_text_box.pack(side=tk.LEFT)
        
        self.sixth_frame = tk.Frame(self.new_root_2, background= "black")
        self.sixth_frame.pack(side = tk.TOP)
        
        self.label_6 = tk.Label(self.sixth_frame, text = "key_6 label:", foreground="green", background= "black")
        self.label_6.pack(side=tk.LEFT)
        
        self.label_6_text_box = tk.Text(self.sixth_frame, height = 1, width = 20, foreground="green", background= "black", insertbackground = "white")
        self.label_6_text_box.insert(tk.INSERT, label_name[5])
        self.label_6_text_box.pack(side=tk.LEFT)
        
        self.seventh_frame = tk.Frame(self.new_root_2, background= "black")
        self.seventh_frame.pack(side = tk.TOP)
        
        self.label_7 = tk.Label(self.seventh_frame, text = "key_7 label:", foreground="green", background= "black")
        self.label_7.pack(side=tk.LEFT)
        
        self.label_7_text_box = tk.Text(self.seventh_frame, height = 1, width = 20, foreground="green", background= "black", insertbackground = "white")
        self.label_7_text_box.insert(tk.INSERT, label_name[6])
        self.label_7_text_box.pack(side=tk.LEFT)
        
        
        self.eighth_frame = tk.Frame(self.new_root_2, background= "black")
        self.eighth_frame.pack(side = tk.TOP)
        
        self.label_8 = tk.Label(self.eighth_frame, text = "key_8 label:", foreground="green", background= "black")
        self.label_8.pack(side=tk.LEFT)
        
        self.label_8_text_box = tk.Text(self.eighth_frame, height = 1, width = 20, foreground="green", background= "black", insertbackground = "white")
        self.label_8_text_box.insert(tk.INSERT, label_name[7])
        self.label_8_text_box.pack(side=tk.LEFT)
        
        self.ninth_frame = tk.Frame(self.new_root_2, background= "black")
        self.ninth_frame.pack(side = tk.TOP)
        
        self.label_9 = tk.Label(self.ninth_frame, text = "key_9 label:", foreground="green", background= "black")
        self.label_9.pack(side=tk.LEFT)
        
        self.label_9_text_box = tk.Text(self.ninth_frame, height = 1, width = 20, foreground="green", background= "black", insertbackground = "white")
        self.label_9_text_box.insert(tk.INSERT, label_name[8])
        self.label_9_text_box.pack(side=tk.LEFT)
        
        self.submit_frame = tk.Frame(self.new_root_2, background= "black")
        self.submit_frame.pack(side = tk.TOP)
        
        self.submit = tk.Button(self.submit_frame, text = "Submit", command = self.label_changer, foreground="green", background= "black")
        self.submit.pack(side = tk.BOTTOM)
        
    
    def creat_configuration_fun(self):
        global label_name, configruation_title
        self.new_root_4 = tk.Toplevel(self.root, background= "black")
        self.new_root_4.title("Label_configuration")
        
        self.first_frame_v3 = tk.Frame(self.new_root_4, background="black")
        self.first_frame_v3.pack()
        
        self.label_1_v1 = tk.Label(self.first_frame_v3, text = "key_1 label:", foreground="green", background= "black")
        self.label_1_v1.pack(side=tk.LEFT)
        
        self.label_1_v1_text_box = tk.Text(self.first_frame_v3, height = 1, width = 20, foreground="green", background= "black", insertbackground = "white")
        self.label_1_v1_text_box.insert(tk.INSERT, label_name[0])
        self.label_1_v1_text_box.pack(side=tk.LEFT)
        
        self.second_frame_v2 = tk.Frame(self.new_root_4, background= "black")
        self.second_frame_v2.pack(side = tk.TOP)
        
        self.label_2_v1 = tk.Label(self.second_frame_v2, text = "key_2 label:", foreground="green", background= "black")
        self.label_2_v1.pack(side=tk.LEFT)
        
        self.label_2_v1_text_box = tk.Text(self.second_frame_v2, height = 1, width = 20, foreground="green", background= "black",insertbackground = "white")
        self.label_2_v1_text_box.insert(tk.INSERT, label_name[1])
        self.label_2_v1_text_box.pack(side=tk.LEFT)
        
        self.third_frame_v1 = tk.Frame(self.new_root_4, background= "black")
        self.third_frame_v1.pack(side = tk.TOP)
        
        self.label_3_v1 = tk.Label(self.third_frame_v1, text = "key_3 label:", foreground="green", background= "black")
        self.label_3_v1.pack(side=tk.LEFT)
        
        self.label_3_v1_text_box = tk.Text(self.third_frame_v1, height = 1, width = 20, foreground="green", background= "black", insertbackground = "white")
        self.label_3_v1_text_box.insert(tk.INSERT, label_name[2])
        self.label_3_v1_text_box.pack(side=tk.LEFT)
        
        self.fourth_frame_v1 = tk.Frame(self.new_root_4, background= "black")
        self.fourth_frame_v1.pack(side = tk.TOP)
        
        self.label_4_v1 = tk.Label(self.fourth_frame_v1, text = "key_4 label:", foreground="green", background= "black")
        self.label_4_v1.pack(side=tk.LEFT)
        
        self.label_4_v1_text_box = tk.Text(self.fourth_frame_v1, height = 1, width = 20, foreground="green", background= "black", insertbackground = "white")
        self.label_4_v1_text_box.insert(tk.INSERT, label_name[3])
        self.label_4_v1_text_box.pack(side=tk.LEFT)
        
        self.fifth_frame_v1 = tk.Frame(self.new_root_4, background= "black")
        self.fifth_frame_v1.pack(side = tk.TOP)
        
        self.label_5_v1 = tk.Label(self.fifth_frame_v1, text = "key_5 label:", foreground="green", background= "black")
        self.label_5_v1.pack(side=tk.LEFT)
        
        self.label_5_v1_text_box = tk.Text(self.fifth_frame_v1, height = 1, width = 20, foreground="green", background= "black", insertbackground = "white")
        self.label_5_v1_text_box.insert(tk.INSERT, label_name[4])
        self.label_5_v1_text_box.pack(side=tk.LEFT)
        
        self.sixth_frame_v1 = tk.Frame(self.new_root_4, background= "black")
        self.sixth_frame_v1.pack(side = tk.TOP)
        
        self.label_6_v1 = tk.Label(self.sixth_frame_v1, text = "key_6 label:", foreground="green", background= "black")
        self.label_6_v1.pack(side=tk.LEFT)
        
        self.label_6_v1_text_box = tk.Text(self.sixth_frame_v1, height = 1, width = 20, foreground="green", background= "black", insertbackground = "white")
        self.label_6_v1_text_box.insert(tk.INSERT, label_name[5])
        self.label_6_v1_text_box.pack(side=tk.LEFT)
        
        self.seventh_frame_v1 = tk.Frame(self.new_root_4, background= "black")
        self.seventh_frame_v1.pack(side = tk.TOP)
        
        self.label_7_v1 = tk.Label(self.seventh_frame_v1, text = "key_7 label:", foreground="green", background= "black")
        self.label_7_v1.pack(side=tk.LEFT)
        
        self.label_7_v1_text_box = tk.Text(self.seventh_frame_v1, height = 1, width = 20, foreground="green", background= "black", insertbackground = "white")
        self.label_7_v1_text_box.insert(tk.INSERT, label_name[6])
        self.label_7_v1_text_box.pack(side=tk.LEFT)
        
        
        self.eighth_frame_v1 = tk.Frame(self.new_root_4, background= "black")
        self.eighth_frame_v1.pack(side = tk.TOP)
        
        self.label_8_v1 = tk.Label(self.eighth_frame_v1, text = "key_8 label:", foreground="green", background= "black")
        self.label_8_v1.pack(side=tk.LEFT)
        
        self.label_8_v1_text_box = tk.Text(self.eighth_frame_v1, height = 1, width = 20, foreground="green", background= "black", insertbackground = "white")
        self.label_8_v1_text_box.insert(tk.INSERT, label_name[7])
        self.label_8_v1_text_box.pack(side=tk.LEFT)
        
        self.ninth_frame_v1 = tk.Frame(self.new_root_4, background= "black")
        self.ninth_frame_v1.pack(side = tk.TOP)
        
        self.label_9_v1 = tk.Label(self.ninth_frame_v1, text = "key_9 label:", foreground="green", background= "black")
        self.label_9_v1.pack(side=tk.LEFT)
        
        self.label_9_v1_text_box = tk.Text(self.ninth_frame_v1, height = 1, width = 20, foreground="green", background= "black", insertbackground = "white")
        self.label_9_v1_text_box.insert(tk.INSERT, label_name[8])
        self.label_9_v1_text_box.pack(side=tk.LEFT)
        
        self.tenth_frame = tk.Frame(self.new_root_4, background= "black")
        self.tenth_frame.pack(side = tk.TOP)
        
        self.label_10 = tk.Label(self.tenth_frame, text = "Configuration title:", foreground="green", background= "black")
        self.label_10.pack(side=tk.LEFT, pady=10)
        
        self.label_10_text_box = tk.Text(self.tenth_frame, height = 1, width = 20, foreground="green", background= "black", insertbackground = "white")
        self.label_10_text_box.insert(tk.INSERT, configruation_title)
        self.label_10_text_box.pack(side=tk.LEFT, pady=15)
        
        self.save_v1_frame = tk.Frame(self.new_root_4, background= "black")
        self.save_v1_frame.pack(side = tk.TOP)
        
        self.submit = tk.Button(self.save_v1_frame, text = "Save", command = self.label_configurator_save, foreground="green", background= "black")
        self.submit.pack(side = tk.BOTTOM)

    def label_changer(self):
        global label_name, label_list, key_unlocker, video_file, length_movie
        if video_file:
            label_name[0] = self.label_1_text_box.get("1.0", "end-1c")
            label_name[1] = self.label_2_text_box.get("1.0", "end-1c")
            label_name[2] = self.label_3_text_box.get("1.0", "end-1c")
            label_name[3] = self.label_4_text_box.get("1.0", "end-1c")
            label_name[4] = self.label_5_text_box.get("1.0", "end-1c")
            label_name[5] = self.label_6_text_box.get("1.0", "end-1c")
            label_name[6] = self.label_7_text_box.get("1.0", "end-1c")
            label_name[7] = self.label_8_text_box.get("1.0", "end-1c")
            label_name[8] = self.label_9_text_box.get("1.0", "end-1c")
        
            label_list = label_name
            messagebox.showinfo("Information box", "Labels updated")
            player.play()
            sleep(0.2)
            length_movie = player.get_length()
            player.stop()
        else:
            messagebox.showerror("Error box", "Before you submit labels, upload the video first")
    
    def label_changer_2(self):
        global label_name, label_list, length_movie
        
        self.label_1_text_box.insert(tk.INSERT, label_name[0])
        self.label_2_text_box.insert(tk.INSERT, label_name[1])
        self.label_3_text_box.insert(tk.INSERT, label_name[2])
        self.label_4_text_box.insert(tk.INSERT, label_name[3])
        self.label_5_text_box.insert(tk.INSERT, label_name[4])
        self.label_6_text_box.insert(tk.INSERT, label_name[5])
        self.label_7_text_box.insert(tk.INSERT, label_name[6])
        self.label_8_text_box.insert(tk.INSERT, label_name[7])
        self.label_9_text_box.insert(tk.INSERT, label_name[8])
        label_list = label_name
        
        
        
    def label_configurator_save(self):
        
        list_configuration = []
        list_configuration.append(self.label_1_v1_text_box.get("1.0", "end-1c"))
        list_configuration.append(self.label_2_v1_text_box.get("1.0", "end-1c"))
        list_configuration.append(self.label_3_v1_text_box.get("1.0", "end-1c"))
        list_configuration.append(self.label_4_v1_text_box.get("1.0", "end-1c"))
        list_configuration.append(self.label_5_v1_text_box.get("1.0", "end-1c"))
        list_configuration.append(self.label_6_v1_text_box.get("1.0", "end-1c"))
        
        list_configuration.append(self.label_7_v1_text_box.get("1.0", "end-1c"))
        list_configuration.append(self.label_8_v1_text_box.get("1.0", "end-1c"))
        list_configuration.append(self.label_9_v1_text_box.get("1.0", "end-1c"))
        list_configuration.append(self.label_10_text_box.get("1.0", "end-1c"))
        save_file2 = None
        save_file2 = easygui.diropenbox(msg = "Select folder for a save location", title = "Typical window")
        if save_file2 == None:
            messagebox.showerror("Error box", "Folder was not selected, data unsaved")
        else:
            save_file2 = save_file2 + "\\" + list_configuration[9] + ".txt"
            text_for_conf = open(save_file2, "w")
            for i in list_configuration:
                text_for_conf.write(i + "\n")
            text_for_conf.close()
            messagebox.showinfo("Information box", "Configuration saved :):):)")
            messagebox.showinfo("Information box", "Do not change the content of created files")

    def draw_table(self):
        global df, df_checker
        
        if df_checker == False:
            messagebox.showerror("Error box", "To see your data frame first press start labeling")
        names_columns = df.columns.tolist()
        names_columns[0:9]= label_list
        df.columns = names_columns
        self.new_root_3 = tk.Toplevel(self.root)
        self.new_root_3.title("Labeled frames")
        self.tabel_frame = tk.Frame(self.new_root_3)
        self.tabel_frame.pack(fill='both', expand=True)
        pt = Table(self.tabel_frame, dataframe=df)
        pt.show()
        
    def bridge_start_video(self):
        global df_checker, df, frame_duration
        if video_file == None:
            messagebox.showerror("Error box", "Upload the video first")
        elif label_list == None:
            messagebox.showerror("Error box", "Before you start labeling you have to submit any label first")
        else:
            cap = cv2.VideoCapture(video_file)
            tots = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            frame_duration = length_movie / tots
            if df_checker == False:
                if len(np.arange(0, length_movie, frame_duration)) == tots:
                    df = pd.DataFrame(columns = label_list, index = range(1, int(tots) + 2))
                    df.index.name="Frame No."
                    df["Frame time [ms]."] = np.arange(0, length_movie+frame_duration, frame_duration)
                    df_checker = True
                else:
                    df = pd.DataFrame(columns = label_list, index = range(1, int(tots) + 2))
                    df.index.name="Frame No."
                    df["Frame time [ms]."] = np.arange(0, length_movie, frame_duration)
                    df_checker = True
            else:
                messagebox.showinfo("Information box", "Labels uploaded")
                names_columns = df.columns.tolist()
                names_columns[0:9]= label_list
                df.columns = names_columns
            self.newwindow = tk.Toplevel(self.root)
            self.app = Start_video(self.newwindow)
def disable_event():
    pass

def delete_mode(data, label, column_name):
    try:
        timestamp_v1 = player.get_time()
        closest_timestamp_stop_v1 = min(list_of_times, key=lambda x:abs(x-timestamp_v1))
        
        df.loc[df["Frame time [ms]."] == closest_timestamp_stop_v1, column_name] = label
        messagebox.showinfo("Information box", "Label deleted")
        player.pause()
    except ValueError:
        messagebox.showerror("Error box", f"Frame unlabeled or wrong label to delet (current label :{current_label})")
        
def ctrl_alt_delet(data):
    global stop_frame, start_frame_freezed, current_label_list, column
    try:
        if stop_frame >= start_frame_freezed:
            data.iloc[start_frame_freezed-2:stop_frame, column] = np.nan
            z = [current_label_list.remove(i) for i in range(start_frame_freezed-1, stop_frame) if i in current_label_list]
            cv2.waitKey(-1)
        elif stop_frame < start_frame_freezed:
            data.iloc[stop_frame:start_frame_freezed, column] = np.nan
            cv2.waitKey(-1)
    except TypeError:
        messagebox.showerror("Error box", "First, set the beginning (key 1-9) and the end (key e) of the range")

def save_machine_state_fun(mother_list, *args):
    
    mother_list = []
    zz = [mother_list.append(i) for i in args]
    xx = [i.append("exist") for i in mother_list if len(i) == 0]
    return mother_list

def run_save_machine_state():
    global df, video_file, label_list
    if video_file == None or label_list == None or df_checker == False:
        messagebox.showerror("Error box", "Before save current state:\n 1. Upload the video \n 2. Submit any label \n 3. Label something")
    else:
        mother_df = df
        mother_list = []
        save_file1 = None
        save_file1 = easygui.diropenbox(msg = "Select folder for a save location", title = "Typical window")
        if save_file1 == None:
            messagebox.showerror("Error box", "Folder was not selected, data unsaved")
        else:
            messagebox.showinfo("Information box", "Folder added :):):)")
            messagebox.showinfo("Information box", "Do not change the content of created files")
            today = str(date.today()).replace("-", "_")
            video_title = video_file.split("\\")
            video_title = video_title[-1].split(".")
            save_mother_df = save_file1 + "\\" + video_title[0] + "_" + today + ".xlsx"
            mother_df.to_excel(save_mother_df)
            
def load_machine_state_fun():
    global df, df_checker, label_list, label_name, df2, df3, df4
    if video_file == None:
        messagebox.showerror("Error box", "Before you load state from file: Upload the video first")
    else:
        video_title = video_file.split("\\")
        video_title = video_title[-1].split(".")
        video_title_first, format_type = video_title
        messagebox.showinfo("Information box", f"Load file for video named: {video_title[0]}")
        df_loaded = easygui.fileopenbox(title="Select a file", filetypes= ["*.gif", "*.flv", "*.avi", "*.amv", "*.mp4"])
        df_loaded_checker = df_loaded.split("\\")
        df_loaded_checker, _ = df_loaded_checker[-1].split(".")
        if video_title_first in df_loaded_checker:
            df_loaded = pd.read_excel(df_loaded)
            df_loaded = df_loaded.set_index("Frame No.")
            df = df_loaded
            list_of_columns = list(df.columns)
            list_of_columns = ["None" if "None" in i else i for i in list_of_columns]
            list_of_columns = ["Frame No." if "Frame No" in i else i for i in list_of_columns]
            df.columns = list_of_columns
            list_of_columns = list(df.columns)
            df_checker = True
            label_name = list_of_columns[0:9]
            label_list=label_name
            df = dtype_checker(df, label_name)
            messagebox.showinfo("Information box", "Data and labels loaded. Continue labeling")
        else:
            messagebox.showerror("Error box", "Wrong file uploaded. Try again")

def dtype_checker(data, list_of_columns):
    
    name_checker = [x for x in list_of_columns if x != "None"]
    dict_convert = {item: str for item in name_checker if not data[item].dtypes.name == "object"}
    if dict_convert:
        data = data.astype(dict_convert)
        for i in dict_convert:
            data.loc[data[i] != "nan", i] = i
            data.loc[data[i] == "nan", i] = np.nan
    return data


def start_vido3():
    global df, df_checker, video_title
    if video_file == None or label_list == None or df_checker == False:
        messagebox.showerror("Error box", "Before save current state:\n 1. Upload the video \n 2. Submit any label \n 3. Label something")
    else:
        video_title = video_file.split("\\")
        video_title = video_title[-1].split(".")
        save_file = None
        save_file = easygui.diropenbox(msg = "Select folder for a save location", title = "Typical window")
        if save_file == None:
            messagebox.showerror("Error box", "Folder was not selected")
        else:
            messagebox.showinfo("Information box", "Folder added :):):)")
        save_file_excel = save_file + "\\" + video_title[0] + ".xlsx"
        df.to_excel(save_file_excel)
        messagebox.showinfo("Information box", "Data saved successfully :):):)")


def load_configuration_fun():
    global df, df_checker,label_list 
    configuration_labels_v1 = []
    configuration_loaded = None
    messagebox.showinfo("Information box", "Load configuration file (.txt)")
    configuration_loaded = easygui.fileopenbox(title="Select a file", filetypes= ["*.txt"])
    if configuration_loaded == None:
            messagebox.showerror("Error box", "Configuration not loaded")
    else:
        with open (configuration_loaded) as content:
            configuration_labels_v1 = content.readlines()
            for i, j in enumerate(configuration_labels_v1):
                configuration_labels_v1[i] = j.replace("\n", "")
        
        if configuration_labels_v1[0] != "None":
            label_name[0] = configuration_labels_v1[0]
        if configuration_labels_v1[1] != "None":
            label_name[1] = configuration_labels_v1[1]
        if configuration_labels_v1[2] != "None":
            label_name[2] = configuration_labels_v1[2]
        if configuration_labels_v1[3] != "None":
            label_name[3] = configuration_labels_v1[3]
        if configuration_labels_v1[4] != "None":
            label_name[4] = configuration_labels_v1[4]
        if configuration_labels_v1[5] != "None":
            label_name[5] = configuration_labels_v1[5]
        if configuration_labels_v1[6] != "None":
            label_name[6] = configuration_labels_v1[6]
        if configuration_labels_v1[7] != "None":
            label_name[7] = configuration_labels_v1[7]
        if configuration_labels_v1[8] != "None":
            label_name[8] = configuration_labels_v1[8]
        label_list = label_name
        messagebox.showinfo("Information box", "Labels updated, before start labeling you have to submit them (go to labels settings window)")

class Start_video:

    def __init__(self, master):
        global video_file, list_of_times, first_time, current_label, text, track_bar_panel, trackbar_name, label_panel_v1_text, label_panel_v2_text, length_movie, label_panel_v3_text, label_panel_v4_text, label_panel_v5_text, label_panel_v6_text, label_panel_v7_text, label_panel_v8_text, label_panel_v9_text, df
        self.master = master
        track_bar_panel = "Track bar"
        trackbar_name = "Time [ms]"
        cv2.namedWindow(track_bar_panel, cv2.WINDOW_NORMAL)
        if not length_movie:
            length_movie = int(df.iloc[-1, 9])
        cv2.createTrackbar(trackbar_name, track_bar_panel, 0, length_movie, self.slider_fun)
        self.bindings_on()
        
        self.block_bindings = False
        self.labelspanel = tk.Frame(self.master, background="#116562")
        self.labelspanel.pack(side= tk.LEFT, fill=tk.BOTH, expand=1)
        
        self.videopanel = tk.Frame(self.master, background="#116562") # for video
        self.canvas = tk.Canvas(self.videopanel).pack(fill=tk.BOTH, expand=1)
        self.videopanel.pack(fill=tk.BOTH, expand=1, side = tk.TOP)
        
        self.main_frame_v2 = tk.Frame(self.master, background="#116562") #for controls
        self.main_frame_v2.pack(side= tk.BOTTOM, fill=tk.BOTH, expand=1)
        
        self.button_pause = tk.Button(self.main_frame_v2, text = "Pause/PLay", background="black", foreground="green", width = 17)
        self.button_pause.bind("<Button-1>", self.button_pause_fun)
        self.button_pause.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        
        self.button_next = tk.Button(self.main_frame_v2, text = "Next Frame", background="black", foreground="green", width = 17)
        self.button_next.bind("<Button-1>", self.next_frame)
        self.button_next.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        
        self.button_previous = tk.Button(self.main_frame_v2, text = "Prev. Frame", background="black", foreground="green", width = 17)
        self.button_previous.bind("<Button-1>", self.previous_frame)
        self.button_previous.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        
        self.button_calibration = tk.Button(self.main_frame_v2, text = "Calibration", background="black", foreground="green", width = 17)
        self.button_calibration.bind("<Button-1>", self.calibration)
        self.button_calibration.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        
        label_panel_v1_text = tk.StringVar()
        label_panel_v1_text.set("Label 1: None")
        self.label_panel_v1 = tk.Label( self.labelspanel, textvariable = label_panel_v1_text, background="black", foreground="green", width = 17, height = 7, bd = 0)
        self.label_panel_v1.grid(row = 0, column = 0, padx=1, pady=1)
        
        label_panel_v2_text = tk.StringVar()
        label_panel_v2_text.set("Label 2: None")
        self.label_panel_v2 = tk.Label( self.labelspanel, textvariable = label_panel_v2_text, background="black", foreground="green", width = 17, height = 7, bd = 0)
        self.label_panel_v2.grid(row = 0, column = 1, padx=1, pady=1, sticky = tk.NE)
        
        label_panel_v3_text = tk.StringVar()
        label_panel_v3_text.set("Label 3: None")
        self.label_panel_v3 = tk.Label( self.labelspanel, textvariable = label_panel_v3_text, background="black", foreground="green", width = 17, height = 7, bd = 0)
        self.label_panel_v3.grid(row = 0, column = 2, padx=1, pady=1)
        
        label_panel_v4_text = tk.StringVar()
        label_panel_v4_text.set("Label 4: None")
        self.label_panel_v4 = tk.Label( self.labelspanel, textvariable = label_panel_v4_text, background="black", foreground="green", width = 17, height = 7, bd = 0)
        self.label_panel_v4.grid(row = 1, column = 0, padx=1, pady=1)
        
        label_panel_v5_text = tk.StringVar()
        label_panel_v5_text.set("Label 5: None")
        self.label_panel_v5 = tk.Label( self.labelspanel, textvariable = label_panel_v5_text, background="black", foreground="green", width = 17, height = 7, bd = 0)
        self.label_panel_v5.grid(row = 1, column = 1, padx=1, pady=1)
        
        label_panel_v6_text = tk.StringVar()
        label_panel_v6_text.set("Label 6: None")
        self.label_panel_v6 = tk.Label( self.labelspanel, textvariable = label_panel_v6_text, background="black", foreground="green", width = 17, height = 7, bd = 0)
        self.label_panel_v6.grid(row = 1, column = 2, padx=1, pady=1)
        
        label_panel_v7_text = tk.StringVar()
        label_panel_v7_text.set("Label 7: None")
        self.label_panel_v7 = tk.Label( self.labelspanel, textvariable = label_panel_v7_text, background="black", foreground="green", width = 17, height = 7, bd = 0)
        self.label_panel_v7.grid(row = 2, column = 0, padx=1, pady=1)
        
        label_panel_v8_text = tk.StringVar()
        label_panel_v8_text.set("Label 8: None")
        self.label_panel_v8 = tk.Label( self.labelspanel, textvariable = label_panel_v8_text, background="black", foreground="green", width = 17, height = 7, bd = 0)
        self.label_panel_v8.grid(row = 2, column = 1, padx=1, pady=1)
        
        label_panel_v9_text = tk.StringVar()
        label_panel_v9_text.set("Label 9: None")
        self.label_panel_v9 = tk.Label( self.labelspanel, textvariable = label_panel_v9_text, background="black", foreground="green", width = 17, height = 7, bd = 0)
        self.label_panel_v9.grid(row = 2, column = 2, padx=1, pady=1)
        
        text = tk.StringVar()
        text.set(f"Active label: {current_label}")
        self.current_label_widget = tk.Label(self.main_frame_v2, textvariable = text, background="black", foreground="green", width = 17)
        self.current_label_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        
        self.button_set_time = tk.Button(self.main_frame_v2, text = "Set time [click me] of video [ms]:", background="black", foreground="green", width = 24)
        self.button_set_time.bind("<Button-1>", self.set_time_manually)
        self.button_set_time.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        
        self.box_for_time = tk.Entry(self.main_frame_v2,  width = 16, background="black", foreground="green", insertbackground = "green")
        self.box_for_time.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.box_for_time.bind("<Enter>", self.bindings_off)
        self.box_for_time.bind("<Leave>", lambda event: self.bindings_on_2())
        self.Instance = vlc.Instance()
        self.player = self.Instance.media_player_new()
        media = self.Instance.media_new(video_file)
        self.player.set_media(media)
        self.player.set_hwnd(self.videopanel.winfo_id())
        messagebox.showinfo("Information box", "Before you start press Calibration button")
        self.player.play()
        list_of_times = df["Frame time [ms]."].tolist()
        
    def button_pause_fun(self, event):
        return self.player.pause()
    
    def next_frame(self, event):
        return self.player.next_frame()
    
    def set_time_manually(self, event):
        try:
            answer_int = int(self.box_for_time.get())
            self.player.set_time(answer_int)
            cv2.setTrackbarPos(trackbar_name, track_bar_panel, answer_int)
            current_state = str(self.player.get_state())
            self.bindings_on()
            if current_state == "State.Playing":
                self.player.pause()
            else:
                pass
        except ValueError:
            messagebox.showerror("Error box", "You inserted wrong value try using integers")
    
    def previous_frame(self, event):
        global frame_duration, time_jump
        
        if not time_jump:
            messagebox.showinfo("Information box", "I have to calibrate my self. Now you can use this option normally. Thank your for your contribution")
            back_up = self.player.get_time()
            self.player.next_frame()
            sleep(0.2)
            self.player.next_frame()
            sleep(0.2)
            self.player.next_frame()
            sleep(0.2)
            first_time = self.player.get_time()
            sleep(0.2)
            self.player.next_frame()
            sleep(0.2)
            second_time = self.player.get_time()
            time_jump = second_time - first_time
            self.player.set_time(back_up)
        else:
            back_one_frame = self.player.get_time()
            time_12 = back_one_frame - round(time_jump)
            current_state = str(self.player.get_state())
            if current_state == "State.Playing":
                self.player.set_time(time_12)
                self.player.pause()
            else:
                self.player.set_time(time_12)
    
    def step_mode(self, index):
        global start_frame_bool, closest_timestamp, current_label, text
        current_label = label_name[index]
        if current_label != "None":
            timestamp = self.player.get_time()
            closest_timestamp = min(list_of_times, key=lambda x:abs(x-timestamp))
            df.loc[df["Frame time [ms]."] == closest_timestamp, current_label,] = current_label
            self.player.next_frame()
            start_frame_bool = True
            text.set(f"Active label: {current_label}")
        else:
            messagebox.showinfo("Information box", "This key is disable, change label name If you want to use it")
    def end_key(self, data):
        global start_frame_bool, current_label, index_timestamp, index_timestamp_stop, closest_timestamp_stop, start_frame_bool_v2
        if start_frame_bool:
            timestamp_stop = self.player.get_time()
            closest_timestamp_stop = min(list_of_times, key=lambda x:abs(x-timestamp_stop))
            range_timestamp = abs(closest_timestamp - closest_timestamp_stop)
            
            index_timestamp = data.index[df["Frame time [ms]."] == closest_timestamp].tolist()
            index_timestamp_stop = data.index[df["Frame time [ms]."] == closest_timestamp_stop].tolist()
            
            if range_timestamp < 10:
                messagebox.showerror("Error box", "Your range is too short (at least 3 frames). Use step method")
                start_frame_bool = False
            elif closest_timestamp_stop >= closest_timestamp:
                data.loc[index_timestamp[0]:index_timestamp_stop[0]-1, current_label] = current_label
                start_frame_bool = False
                start_frame_bool_v2 = True
                current_state = str(self.player.get_state())
                if current_state == "State.Playing":
                    self.player.pause()
                else:
                    pass
                messagebox.showinfo("Information box", f"Frames from {index_timestamp[0]} to {index_timestamp_stop[0]-1} were labeled")
                
            elif closest_timestamp_stop < closest_timestamp:
                data.loc[index_timestamp_stop[0]+1:index_timestamp[0], current_label] = current_label
                start_frame_bool = False
                start_frame_bool_v2 = True
                current_state = str(self.player.get_state())
                if current_state == "State.Playing":
                    self.player.pause()
                else:
                    pass
                messagebox.showinfo("Information box", f"Frames from {index_timestamp[0]+1} to {index_timestamp[0]} were labeled")
        else:
            root_v2 = tk.Tk()
            current_state = str(self.player.get_state())
            if current_state == "State.Playing":
                self.player.pause()
            else:
                pass
            messagebox.showerror("Error box", "First, set the beginning of range", parent= root_v2)
            root_v2.destroy()
    
    def delete_mode(self, data, label):
        global current_label
        timestamp_v1 = self.player.get_time()
        closest_timestamp_stop_v1 = min(list_of_times, key=lambda x:abs(x-timestamp_v1))
        checker = data.loc[df["Frame time [ms]."] == closest_timestamp_stop_v1, current_label].tolist()
        if str(checker[0]) == "nan":
            current_state = str(self.player.get_state())
            if current_state == "State.Playing":
                self.player.pause()
            else:
                pass
            messagebox.showerror("Error box", f"Frame unlabeled or wrong label to delet (current label :{current_label})")
        
        else:
            data.loc[df["Frame time [ms]."] == closest_timestamp_stop_v1, current_label] = label
            current_state = str(self.player.get_state())
            if current_state == "State.Playing":
                self.player.pause()
            else:
                pass
            messagebox.showinfo("Information box", "Label deleted")
    def bindings_on(self):
        
        self.bindings_space = self.master.bind("<space>", self.button_pause_fun)
        self.bindings_a = self.master.bind("<a>", self.previous_frame)
        self.bindings_d = self.master.bind("<d>", self.next_frame)
        self.bindings_1 = self.master.bind("1", lambda event, index = 0: self.step_mode(index))
        self.bindings_2 = self.master.bind("2", lambda event, index = 1: self.step_mode(index))
        self.bindings_3 = self.master.bind("3", lambda event, index = 2: self.step_mode(index))
        self.bindings_4 = self.master.bind("4", lambda event, index = 3: self.step_mode(index))
        self.bindings_5 = self.master.bind("5", lambda event, index = 4: self.step_mode(index))
        self.bindings_6 = self.master.bind("6", lambda event, index = 5: self.step_mode(index))
        self.bindings_7 = self.master.bind("7", lambda event, index = 6: self.step_mode(index))
        self.bindings_8 = self.master.bind("8", lambda event, index = 7: self.step_mode(index))
        self.bindings_9 = self.master.bind("9", lambda event, index = 8: self.step_mode(index))
        self.bindings_e = self.master.bind("e", lambda event, data = df: self.end_key(data))
        self.bindings_g = self.master.bind("g", lambda event, data = df, label = np.nan: self.delete_mode(data, label))
        self.bindings_h = self.master.bind("h", lambda event, data = df: self.ctrl_alt_delet(data))
        self.bindings_c = self.master.bind("c", lambda event: self.speed_up())
        self.bindings_z = self.master.bind("z", lambda event: self.slow_down())
        self.bindings_x = self.master.bind("x", lambda event: self.normal_speed())
        self.bindings_all = self.master.bind_all("<1>", lambda event:event.widget.focus_set())
        
    def bindings_off(self, event):
        
        self.master.unbind("<space>", self.bindings_space)
        self.master.unbind("<a>", self.bindings_a)
        self.master.unbind("<d>", self.bindings_d)
        self.master.unbind("1", self.bindings_1)
        self.master.unbind("2", self.bindings_2)
        self.master.unbind("3", self.bindings_3)
        self.master.unbind("4", self.bindings_4)
        self.master.unbind("5", self.bindings_5)
        self.master.unbind("6", self.bindings_6)
        self.master.unbind("7", self.bindings_7)
        self.master.unbind("8", self.bindings_8)
        self.master.unbind("9", self.bindings_9)
        self.master.unbind("e", self.bindings_e)
        self.master.unbind("g", self.bindings_g)
        self.master.unbind("h", self.bindings_h)
        self.master.unbind("c", self.bindings_c)
        self.master.unbind("z", self.bindings_z)
        self.master.unbind("x",self.bindings_x)
        self.box_for_time.focus_set()
        #messagebox.showinfo("Information box", "Entering insert zone. Labeling off")
    def bindings_on_2(self):
        self.bindings_space = self.master.bind("<space>", self.button_pause_fun)
        self.bindings_a = self.master.bind("<a>", self.previous_frame)
        self.bindings_d = self.master.bind("<d>", self.next_frame)
        self.bindings_1 = self.master.bind("1", lambda event, index = 0: self.step_mode(index))
        self.bindings_2 = self.master.bind("2", lambda event, index = 1: self.step_mode(index))
        self.bindings_3 = self.master.bind("3", lambda event, index = 2: self.step_mode(index))
        self.bindings_4 = self.master.bind("4", lambda event, index = 3: self.step_mode(index))
        self.bindings_5 = self.master.bind("5", lambda event, index = 4: self.step_mode(index))
        self.bindings_6 = self.master.bind("6", lambda event, index = 5: self.step_mode(index))
        self.bindings_7 = self.master.bind("7", lambda event, index = 6: self.step_mode(index))
        self.bindings_8 = self.master.bind("8", lambda event, index = 7: self.step_mode(index))
        self.bindings_9 = self.master.bind("9", lambda event, index = 8: self.step_mode(index))
        self.bindings_e = self.master.bind("e", lambda event, data = df: self.end_key(data))
        self.bindings_g = self.master.bind("g", lambda event, data = df, label = np.nan: self.delete_mode(data, label))
        self.bindings_h = self.master.bind("h", lambda event, data = df: self.ctrl_alt_delet(data))
        self.bindings_c = self.master.bind("c", lambda event: self.speed_up())
        self.bindings_z = self.master.bind("z", lambda event: self.slow_down())
        self.bindings_x = self.master.bind("x", lambda event: self.normal_speed())
        self.label_panel_v2.focus_set()
        #messagebox.showinfo("Information box", "Leaving insert zone. Labeling on")
    def speed_up(self):
        global video_rate
        video_rate = 2.5
        messagebox.showinfo("Information box", "The video sped up")
        return self.player.set_rate(video_rate)
    
    def slow_down(self):
        global video_rate
        video_rate = 0.2
        messagebox.showinfo("Information box", "The video has slowed down")
        return self.player.set_rate(video_rate)
    
    def normal_speed(self):
        global video_rate
        video_rate = 1.0
        messagebox.showinfo("Information box", "Video speed, back to normal")
        return self.player.set_rate(video_rate)
    
    def ctrl_alt_delet(self, data):
        
        if start_frame_bool_v2:
            if closest_timestamp_stop >= closest_timestamp:
                data.loc[index_timestamp[0]:index_timestamp_stop[0]-1, current_label] = np.nan
                messagebox.showinfo("Information box", f"Labels from {index_timestamp[0]} to {index_timestamp_stop[0]} were deleted")
            elif closest_timestamp_stop < closest_timestamp:
                data.loc[index_timestamp_stop[0]+1:index_timestamp[0], current_label] = current_label
                messagebox.showinfo("Information box", f"Labels from {index_timestamp_stop[0]} to {index_timestamp[0]} were deleted")
        else:
            messagebox.showerror("Error box", "First, set the beginning (key 1-9) and the end (key e) of the range")
    
    def calibration(self, event):
        back_up_v2 = self.player.get_time()
        self.player.next_frame()
        sleep(0.2)
        self.player.next_frame()
        sleep(0.2)
        self.player.next_frame()
        sleep(0.2)
        self.player.next_frame()
        sleep(0.2)
        self.player.next_frame()
        sleep(0.2)
        self.player.next_frame()
        sleep(0.2)
        self.player.set_time(back_up_v2)
        self.button_calibration["state"] = tk.DISABLED
        self.button_calibration.update()
        messagebox.showinfo("Information box", "Thank you for your contribution")
    
    def slider_fun(self, unused):
        global df
        timestamp_track = cv2.getTrackbarPos(trackbar_name, track_bar_panel)
        closest_timestamp = min(list_of_times, key=lambda x:abs(x-timestamp_track))
        

        if label_list[0] == "None":
            label_panel_v1_text.set("Label 1: unused")
        else:
            checker = df.loc[df["Frame time [ms]."] == closest_timestamp, label_list[0]].tolist()
            if checker[0] == label_list[0]:
                label_panel_v1_text.set(f"Label 1: {label_list[0]}")
                self.label_panel_v1.config(bg = "blue")
            else:
                label_panel_v1_text.set("Label 1: unlabel")
                self.label_panel_v1.config(bg = "black")
        
        if label_list[1] == "None":
            label_panel_v2_text.set("Label 2: unused")
        else:
            checker = df.loc[df["Frame time [ms]."] == closest_timestamp, label_list[1]].tolist()
            if checker[0] == label_list[1]:
                label_panel_v2_text.set(f"Label 2: {label_list[1]}")
                self.label_panel_v2.config(bg = "red")
            else:
                label_panel_v2_text.set("Label 2: unlabel")
                self.label_panel_v2.config(bg = "black")
        
        if label_list[2] == "None":
            label_panel_v3_text.set("Label 3: unused")
        else:
            checker = df.loc[df["Frame time [ms]."] == closest_timestamp, label_list[2]].tolist()
            if checker[0] == label_list[2]:
                label_panel_v3_text.set(f"Label 3: {label_list[2]}")
                self.label_panel_v3.config(bg = "cyan")
            else:
                label_panel_v3_text.set("Label 3: unlabel")
                self.label_panel_v3.config(bg = "black")
        
        if label_list[3] == "None":
            label_panel_v4_text.set("Label 4: unused")
        else:
            checker = df.loc[df["Frame time [ms]."] == closest_timestamp, label_list[3]].tolist()
            if checker[0] == label_list[3]:
                label_panel_v4_text.set(f"Label 4: {label_list[3]}")
                self.label_panel_v4.config(bg = "yellow")
            else:
                label_panel_v4_text.set("Label 4: unlabel")
                self.label_panel_v4.config(bg = "black")
        
        if label_list[4] == "None":
            label_panel_v5_text.set("Label 5: unused")
        else:
            checker = df.loc[df["Frame time [ms]."] == closest_timestamp, label_list[4]].tolist()
            if checker[0] == label_list[4]:
                label_panel_v5_text.set(f"Label 5: {label_list[4]}")
                self.label_panel_v5.config(bg = "magenta")
            else:
                label_panel_v5_text.set("Label 5: unlabel")
                self.label_panel_v5.config(bg = "black")
        
        if label_list[5] == "None":
            label_panel_v6_text.set("Label 6: unused")
        else:
            checker = df.loc[df["Frame time [ms]."] == closest_timestamp, label_list[5]].tolist()
            if checker[0] == label_list[5]:
                label_panel_v6_text.set(f"Label 6: {label_list[5]}")
                self.label_panel_v6.config(bg = "#8B8B23")
            else:
                label_panel_v6_text.set("Label 6: unlabel")
                self.label_panel_v6.config(bg = "black")
        
        if label_list[6] == "None":
            label_panel_v7_text.set("Label 7: unused")
        else:
            checker = df.loc[df["Frame time [ms]."] == closest_timestamp, label_list[6]].tolist()
            if checker[0] == label_list[6]:
                label_panel_v7_text.set(f"Label 7: {label_list[6]}")
                self.label_panel_v7.config(bg = "#BCBC8F")
            else:
                label_panel_v7_text.set("Label 7: unlabel")
                self.label_panel_v7.config(bg = "black")
        
        if label_list[7] == "None":
            label_panel_v8_text.set("Label 8: unused")
        else:
            checker = df.loc[df["Frame time [ms]."] == closest_timestamp, label_list[7]].tolist()
            if checker[0] == label_list[7]:
                label_panel_v8_text.set(f"Label 8: {label_list[7]}")
                self.label_panel_v8.config(bg = "#3A3A5F")
            else:
                label_panel_v8_text.set("Label 8: unlabel")
                self.label_panel_v8.config(bg = "black")
        
        if label_list[8] == "None":
            label_panel_v9_text.set("Label 9: unused")
        else:
            checker = df.loc[df["Frame time [ms]."] == closest_timestamp, label_list[8]].tolist()
            if checker[0] == label_list[8]:
                label_panel_v9_text.set(f"Label 9: {label_list[8]}")
                self.label_panel_v9.config(bg = "#CDCDB3")
            else:
                label_panel_v9_text.set("Label 9: unlabel")
                self.label_panel_v9.config(bg = "black")
        self.player.set_time(timestamp_track)
advert()
video_object = Application()
video_object.root.mainloop()
    
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  1 17:28:58 2022

@author: malgo
"""

import keyboard
import vlc
from time import sleep
import tkinter as tk
import requests
from PIL import Image, ImageTk
from io import BytesIO




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
advert()

class Application:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Manual Labeler")
        self.root.protocol("WM_DELETE_WINDOW", disable_event)
    
        self.first_frame = tk.Frame(self.root, background="#116562", width=400, height = 30)
        self.first_frame.pack()
        self.first_frame.pack_propagate(0)
        
        self.open_file = tk.Button(self.first_frame, text = "Load video", command = self.easy_open, background="black", foreground="green", width = 26)
        self.open_file.pack(side= tk.LEFT, padx=1, pady=1, expand=True, fill='both')
        self.text = f"Current video: {None}"
        self.current_video = tk.Text(self.first_frame, height = 1, width = 16, background="black", foreground="green", insertbackground = "white")
        self.current_video.insert(tk.INSERT, self.text)
        self.desired_font = tk.font.Font(size = 14)
        self.current_video.configure(font = self.desired_font)
        self.current_video.pack(side=tk.RIGHT, padx=1, pady=1, expand=True, fill='both')
        
        self.second_frame = tk.Frame(self.root, background="#116562", width=400, height = 30)
        self.second_frame.pack(side = tk.TOP)
        self.second_frame.pack_propagate(0)
        
        self.keyboard = tk.Button(self.second_frame, text="Keyboard settings", command = self.keyboard_settings, background="black", foreground="green", width = 13)
        self.keyboard.pack(side=tk.LEFT, padx=1, pady=1, expand=True, fill='both')
        
        self.label_1_9 = tk.Button(self.second_frame, text="Labels settings", command = self.label_settings, background="black", foreground="green")
        self.label_1_9.pack(side=tk.RIGHT, padx=1, pady=1, expand=True, fill='both')
        
        self.third_frame_v1 = tk.Frame(self.root, background="#116562", width=400, height = 30)
        self.third_frame_v1.pack(side = tk.TOP)
        self.third_frame_v1.pack_propagate(0)
        
        self.start_labeling = tk.Button(self.third_frame_v1, text="Start labeling", command = start_vido1, background="black", foreground="green", width = 15)
        self.start_labeling.pack(side=tk.LEFT, padx=1, pady=1, expand=True, fill='both')
        
        self.show_df = tk.Button(self.third_frame_v1, text="Show data frame", command = self.draw_table, background="black", foreground="green")
        self.show_df.pack(side=tk.LEFT, padx=1, pady=1, expand=True, fill='both')
        
    
        self.fifth_frame_v1 = tk.Frame(self.root, background="#116562", width=400, height = 30)
        self.fifth_frame_v1.pack(side = tk.TOP)
        self.fifth_frame_v1.pack_propagate(0)
    
        self.save_machine_state = tk.Button(self.fifth_frame_v1, text = "Save current state", command = run_save_machine_state, background="black", foreground="green", width = 17)
        self.save_machine_state.pack(side=tk.LEFT, padx=1, pady=1, expand=True, fill='both')
        
        self.load_machine_state = tk.Button(self.fifth_frame_v1, text = "Load state from file", command = load_machine_state_fun, background="black", foreground="green")
        self.load_machine_state.pack(side=tk.LEFT, padx=1, pady=1, expand=True, fill='both')
        
        self.sixth_frame = tk.Frame(self.root, background="#116562", width=400, height = 30)
        self.sixth_frame.pack(side = tk.TOP)
        self.sixth_frame.pack_propagate(0)
        
        self.create_configuration = tk.Button(self.sixth_frame, text = "Create configuration", command = self.creat_configuration_fun, background="black", foreground="green", width = 19)
        self.create_configuration.pack(side=tk.LEFT, padx=1, pady=1, expand=True, fill='both')
        
        self.load_configuration = tk.Button(self.sixth_frame, text = "Load configuration", command = lambda:[load_configuration_fun(), self.label_changer()], background="black", foreground="green", width = 17)
        self.load_configuration.pack(side=tk.LEFT, padx=1, pady=1, expand=True, fill='both')
        
        self.fourth_frame_v1 = tk.Frame(self.root, background="#116562", width=400, height = 30)
        self.fourth_frame_v1.pack(side = tk.TOP)
        self.fourth_frame_v1.pack_propagate(0)
        
        self.save_labeled_video = tk.Button(self.fourth_frame_v1, text= "Save data", command = start_vido3, background="black", foreground="green", width = 5)
        self.save_labeled_video.pack(side=tk.LEFT, padx=1, pady=1, expand=True, fill='both')
        
        self.close_gui = tk.Button(self.fourth_frame_v1, text= "Exit", command = self.close_gate, background="black", foreground="green", activebackground = "white")
        self.close_gui.pack(side=tk.LEFT, padx=1, pady=1, expand=True, fill='both')
        
        self.engine = pyttsx3.init()
        self.list_of_voices = ['Hello World', "welcome to the Labeling world", "hello friend", "I wish you fruitful work", "hello user", "I will try my best to help you work", "What a nice day to label something"]
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)
        self.engine.say(random.choice(self.list_of_voices))
        self.engine.runAndWait()




vlc_instance = vlc.Instance()
player = vlc_instance.media_player_new()
media = vlc_instance.media_new("D:\\Zw_1_exp_Trim.mp4")
player.set_media(media)
player.play()
#sleep(1)
fps = player.get_fps()
length_movie = player.get_length()


while True:
    if keyboard.read_key() == "1":
        player.play()
        length_movie = player.get_length()
    if keyboard.read_key() == "2":
        player.pause()
        
    if keyboard.read_key() == "3":
        player.next_frame()    
    if keyboard.read_key() == "4":
        player.stop()
        break
    if keyboard.read_key() == "5":
        x = player.get_time()
        
player.get_fps()
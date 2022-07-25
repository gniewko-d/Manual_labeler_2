# -*- coding: utf-8 -*-
"""
Created on Sat Jul 23 15:24:57 2022

@author: malgo
"""
import tkinter as tk
import vlc
video_file = None

class Start_video:

    def __init__(self, master):
        self.master = master
        self.videopanel = tk.Frame(self.master, background="#116562") # for video
        self.canvas = tk.Canvas(self.videopanel).pack(fill=tk.BOTH, expand=1)
        self.videopanel.pack(fill=tk.BOTH, expand=1)
        
        self.main_frame_v2 # może tu bedą opcje przechowywane narazie se zostaiwam
        
        self.Instance = vlc.Instance()
        self.player = self.Instance.media_player_new()
        media = self.Instance.media_new(video_file)
        self.player.set_media(media)
        self.player.set_hwnd(self.videopanel.winfo_id())
        self.player.play()
        list_of_times = df["Frame time [ms]."].tolist()
        stoper = True
        self.player.play()
        while stoper:
            x = self.player.get_time()
            print(x)
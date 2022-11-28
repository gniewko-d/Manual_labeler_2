import threading
import vlc
from time import sleep
import tkinter as tk
import requests
from PIL import Image, ImageTk
from io import BytesIO
import matplotlib.pyplot as plt
from tkinter import messagebox
import easygui
from matplotlib.figure import Figure
import pyttsx3
import random
from pandastable import Table
import cv2
import pandas as pd
import numpy as np
import csv
from datetime import date
from sklearn.metrics import matthews_corrcoef
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from RangeSlider.RangeSlider import RangeSliderH


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

back_current_label = False
label_name = [f"{None}",f"{None}",f"{None}",f"{None}",f"{None}",f"{None}",f"{None}",f"{None}",f"{None}"]
configruation_title = f"{None}"
video_file = None
available_formats = ["flv", "avi", "amv", "mp4"]
length_movie = False
df_checker = False
current_label = "Nought"
start_frame_bool = False
label_list = None
time_jump = 0
video_rate = 1.0
start_frame_bool_v2 = False
window_checker = 0
radio_variable = "off"
t = None
player_first = 0
player_second = 0
save_mother_df_automatic = None
controler_slider = True
class Application:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Manual Labeler")
        self.root.protocol("WM_DELETE_WINDOW", disable_event)
        self.root.geometry("600x600")
        
        self.var1 = tk.StringVar()
        self.var1.set("off")
        self.var2 = tk.StringVar()
        self.var2.set("off")
        self.var1_controller = False
        self.var2_controller = False
        
        self.reupload_controler = 0
        self.desired_font = tk.font.Font(size = 16)
        
        self.first_frame = tk.Frame(self.root, background="#116562", width=200, height = 60)
        self.first_frame.pack(expand=True, fill='both')
        self.first_frame.pack_propagate(0)
        
        self.open_file = tk.Button(self.first_frame, text = "Load video", command = self.easy_open, background="black", foreground="green", width=25, relief = tk.RAISED)
        self.open_file["font"] = self.desired_font
        self.open_file.pack(side= tk.LEFT, padx=1, pady=1, expand=True, fill='both')
        
        self.text = f"Video: {None}"
        self.current_video = tk.Label(self.first_frame, height = 1, width=25, background="black", foreground="#FFFF00", anchor = tk.CENTER, relief = tk.RAISED)
        self.current_video.config(text = self.text)
        
        self.current_video.configure(font = self.desired_font)
        self.current_video.pack(side=tk.RIGHT, padx=1, pady=1, expand=True, fill='both')
        
        self.second_frame = tk.Frame(self.root, background="#116562", width=200, height = 60)
        self.second_frame.pack(side = tk.TOP, expand=True, fill='both')
        self.second_frame.pack_propagate(0)
        
        self.keyboard = tk.Button(self.second_frame, text="Settings", command = self.keyboard_settings, background="black", foreground="green", width=25)
        self.keyboard["font"] = self.desired_font
        self.keyboard.pack(side=tk.LEFT, padx=1, pady=1, expand=True, fill='both')
        
        self.label_1_9 = tk.Button(self.second_frame, text="Labels settings", command = self.label_settings, background="black", foreground="green", width=25)
        self.label_1_9["font"] = self.desired_font
        self.label_1_9.pack(side=tk.RIGHT, padx=1, pady=1, expand=True, fill='both')
        
        self.third_frame_v1 = tk.Frame(self.root, background="#116562", width=200, height = 60)
        self.third_frame_v1.pack(side = tk.TOP, expand=True, fill='both')
        self.third_frame_v1.pack_propagate(0)
        
        self.start_labeling = tk.Button(self.third_frame_v1, text="Start labeling", command = self.bridge_start_video, background="black", foreground="green", width=25)
        self.start_labeling["font"] = self.desired_font
        self.start_labeling.pack(side=tk.LEFT, padx=1, pady=1, expand=True, fill='both')
        
        self.show_df = tk.Button(self.third_frame_v1, text="Show data frame", command = self.draw_table, background="black", foreground="green", width=25)
        self.show_df["font"] = self.desired_font
        self.show_df.pack(side=tk.LEFT, padx=1, pady=1, expand=True, fill='both')
        
        self.fifth_frame_v1 = tk.Frame(self.root, background="#116562", width=200, height = 60)
        self.fifth_frame_v1.pack(side = tk.TOP, expand=True, fill='both')
        self.fifth_frame_v1.pack_propagate(0)
    
        self.data_comparison = tk.Button(self.fifth_frame_v1, text = "Compare data", command = self.compare_main, background="black", foreground="green", width=25)
        self.data_comparison["font"] = self.desired_font
        self.data_comparison.pack(side=tk.LEFT, padx=1, pady=1, expand=True, fill='both')
        
        self.load_machine_state = tk.Button(self.fifth_frame_v1, text = "Load file", command = lambda:[load_machine_state_fun(), self.label_changer_2()], background="black", foreground="green", width=25)
        self.load_machine_state["font"] = self.desired_font
        self.load_machine_state.pack(side=tk.LEFT, padx=1, pady=1, expand=True, fill='both')
        
        self.sixth_frame = tk.Frame(self.root, background="#116562", width=200, height = 60)
        self.sixth_frame.pack(side = tk.TOP, expand=True, fill='both')
        self.sixth_frame.pack_propagate(0)
        
        self.create_configuration = tk.Button(self.sixth_frame, text = "Create configuration", command = self.creat_configuration_fun, background="black", foreground="green", width=25)
        self.create_configuration["font"] = self.desired_font
        self.create_configuration.pack(side=tk.LEFT, padx=1, pady=1, expand=True, fill='both')
        
        self.load_configuration = tk.Button(self.sixth_frame, text = "Load configuration", command = lambda:[load_configuration_fun(), self.label_changer_2()], background="black", foreground="green", width=25)
        self.load_configuration["font"] = self.desired_font
        self.load_configuration.pack(side=tk.LEFT, padx=1, pady=1, expand=True, fill='both')
        
        self.seventh_frame = tk.Frame(self.root, background="#116562", width= 200, height = 60)
        self.seventh_frame.pack(side = tk.TOP, expand=True, fill='both')
        self.seventh_frame.pack_propagate(0)
        
        self.play_labeled_frames = tk.Button(self.seventh_frame, text = "Play labeled frames", background="black", command = self.play_labeled_fun, foreground="green", width=25)
        self.play_labeled_frames["font"] = self.desired_font
        self.play_labeled_frames.pack(side=tk.LEFT, padx=1, pady=1, expand=True, fill='both')
        
        self.save_labeled_frames = tk.Button(self.seventh_frame, text = "Save labeled frames", background="black", foreground="green", width=25)
        self.save_labeled_frames["font"] = self.desired_font
        self.save_labeled_frames.pack(side=tk.LEFT, padx=1, pady=1, expand=True, fill='both')
        
        self.fourth_frame_v1 = tk.Frame(self.root, background="#116562", width=400, height = 60)
        self.fourth_frame_v1.pack(side = tk.TOP, expand=True, fill='both')
        self.fourth_frame_v1.pack_propagate(0)
        
        self.save_labeled_video = tk.Button(self.fourth_frame_v1, text= "Save data", command = start_vido3, background="black", foreground="green", width=25)
        self.save_labeled_video["font"] = self.desired_font
        self.save_labeled_video.pack(side=tk.LEFT, padx=1, pady=1, expand=True, fill='both')
        
        self.close_gui = tk.Button(self.fourth_frame_v1, text= "Exit", command = self.close_gate, background="black", foreground="green", activebackground = "white", width=25)
        self.close_gui["font"] = self.desired_font
        self.close_gui.pack(side=tk.LEFT, padx=1, pady=1, expand=True, fill='both')
        
        self.engine = pyttsx3.init()
        self.list_of_voices = ['Hello World', "welcome to the Labeling world", "hello friend", "I wish you fruitful work", "hello user", "I will try my best to help you work", "What a nice day to label something", "Thank your for your contribution", "Verifying ID"]
        self.list_of_voices_2 = ["Have a nice day", "Have a pleasant journey", "Time to say goodbye ", "It was nice to see you again", "Peace"]
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)
        self.engine.say(random.choice(self.list_of_voices))
        self.engine.runAndWait()
    
      
    def active_window(self, window):
        window.after(1, lambda: window.focus_force())
    
    def compare_main(self):
        self.new_root_v2 = tk.Toplevel(self.root, background= "black")
        self.new_root_v2.title("Data_comparator")
    
        self.first_frame_v1 = tk.Frame(self.new_root_v2, background="black")
        self.first_frame_v1.pack(expand=True, fill='both', pady=10)
    
        self.label_info = tk.Label(self.first_frame_v1, text = "Add files to compare", foreground="#FFFF00", background= "black")
        self.label_info["font"] = self.desired_font
        self.label_info.pack(side=tk.TOP, padx=1, pady=1)
    
        self.first_frame_v2 = tk.Frame(self.new_root_v2, background="black")
        self.first_frame_v2.pack(expand=True, fill='both', pady=10)
    
        self.b_first = tk.Button(self.first_frame_v2, text = "Add first file", foreground="green", background= "black")
        self.b_first["font"] = self.desired_font
        self.b_first.bind("<Button-1>", lambda event, optional_video = True: self.open_first(optional_video))
        self.b_first.pack(side=tk.TOP, padx=1, pady=1)
    
        self.first_frame_v3 = tk.Frame(self.new_root_v2, background="black")
        self.first_frame_v3.pack(expand=True, fill='both', pady=10)
    
        self.text_first = f"File: {None}"
        self.current_video_first = tk.Label(self.first_frame_v3, height = 1, width=25, background="black", foreground="#FFFF00", anchor = tk.CENTER, relief = tk.RAISED)
        self.current_video_first.config(text = self.text_first)
        
        self.current_video_first.configure(font = self.desired_font)
        self.current_video_first.pack(side=tk.TOP, padx=1, pady=1, expand=True, fill='both')
    
        self.first_frame_v4 = tk.Frame(self.new_root_v2, background="black")
        self.first_frame_v4.pack(expand=True, fill='both', pady=10)
    
        self.b_second = tk.Button(self.first_frame_v4, text = "Add second file", foreground="green", background= "black")
        self.b_second["font"] = self.desired_font
        self.b_second.bind("<Button-1>", lambda event, optional_video = False: self.open_first(optional_video))
        self.b_second.pack(side=tk.TOP, padx=1, pady=1)
    
        self.first_frame_v5 = tk.Frame(self.new_root_v2, background="black")
        self.first_frame_v5.pack(expand=True, fill='both', pady=10)
    
        self.text_second = f"File: {None}"
        self.current_video_second = tk.Label(self.first_frame_v5, height = 1, width=25, background="black", foreground="#FFFF00", anchor = tk.CENTER, relief = tk.RAISED)
        self.current_video_second.config(text = self.text_second)
        
        self.current_video_second.configure(font = self.desired_font)
        self.current_video_second.pack(side=tk.TOP, padx=1, pady=1, expand=True, fill='both')
    
        self.first_frame_v6 = tk.Frame(self.new_root_v2, background="black")
        self.first_frame_v6.pack(expand=True, fill='both', pady=10)
    
        self.comper_submit = tk.Button(self.first_frame_v6, text = "Save", command = self.compare_option, foreground="green", background= "black")
        self.comper_submit["font"] = self.desired_font
        self.comper_submit.pack(side = tk.TOP, expand=True, fill='both')
                
    
    def open_first(self, optional_video):
        global df_loaded_first, df_loaded_second, player_first, player_second
        if video_file == None:
            messagebox.showerror("Error box", "Before you load file: Upload the video first")
        else:
            video_title = video_file.split("\\")
            video_title = video_title[-1].split(".")
            video_title_first, format_type = video_title
            if optional_video:
                messagebox.showinfo("Information box", f"Load first file for video named: {video_title[0]}")
                df_loaded_first = easygui.fileopenbox(title="Select a file", filetypes= ["*.xlsx", ".xlsm", ".xlsb"])
                df_loaded_checker_first = df_loaded_first.split("\\")
                df_loaded_checker_first, _ = df_loaded_checker_first[-1].split(".")
                if video_title_first in df_loaded_checker_first:
                    df_loaded_first = pd.read_excel(df_loaded_first)
                    df_loaded_first = df_loaded_first.set_index("Frame No.")
                    self.text_first = f"File: {df_loaded_checker_first}"
                    self.current_video_first.config(text = self.text_first)
                    messagebox.showinfo("Information box", "Data loaded.")
                    self.active_window(self.new_root_v2)
                    player_first = str(easygui.enterbox("Enter author's nick", "Message Box", "Enter here.."))
                else:
                    messagebox.showerror("Error box", "Wrong file uploaded. Try again")
            elif not optional_video:
                messagebox.showinfo("Information box", f"Load second file for video named: {video_title[0]}")
                df_loaded_second = easygui.fileopenbox(title="Select a file", filetypes= ["*.xlsx", ".xlsm", ".xlsb"])
                df_loaded_checker_second = df_loaded_second.split("\\")
                df_loaded_checker_second, _ = df_loaded_checker_second[-1].split(".")
                if video_title_first in df_loaded_checker_second:
                    df_loaded_second = pd.read_excel(df_loaded_second)
                    df_loaded_second = df_loaded_second.set_index("Frame No.")
                    self.text_second = f"File: {df_loaded_checker_second}"
                    self.current_video_second.config(text = self.text_second)
                    messagebox.showinfo("Information box", "Data loaded.")
                    self.active_window(self.new_root_v2)
                    player_second = str(easygui.enterbox("Enter author's nick", "Message Box", "Enter here.."))
                else:
                    messagebox.showerror("Error box", "Wrong file uploaded. Try again")
    def compare_option(self):
        
        self.new_root_v2.destroy()
        try:
            assert len(df_loaded_first) == len(df_loaded_second)
            self.new_root_v3 = tk.Toplevel(self.root, background= "black")
            self.new_root_v3.title("Data_comparator")
    
            self.first_frame_v1 = tk.Frame(self.new_root_v3, background="black")
            self.first_frame_v1.pack(expand=True, fill='both', pady=10)
    
            self.b_first = tk.Button(self.first_frame_v1, text = "Real-time comparison", foreground="green", background= "black")
            self.b_first["font"] = self.desired_font
            self.b_first.bind("<Button-1>", lambda event : self.real_time_fun())
            self.b_first.pack(side=tk.TOP, padx=1, pady=1)
    
            self.first_frame_v2 = tk.Frame(self.new_root_v3, background="black")
            self.first_frame_v2.pack(expand=True, fill='both', pady=10)
    
            self.b_second = tk.Button(self.first_frame_v2, text = "Paired labels comparison", foreground="green", background= "black")
            self.b_second["font"] = self.desired_font
            self.b_second.bind("<Button-1>", lambda event : self.paired())
            self.b_second.pack(side=tk.TOP, padx=1, pady=1)
    
            self.first_frame_v3 = tk.Frame(self.new_root_v3, background="black")
            self.first_frame_v3.pack(expand=True, fill='both', pady=10)
    
            self.b_thrid = tk.Button(self.first_frame_v3, text = "Select the labels to compare", foreground="green", background= "black")
            self.b_thrid["font"] = self.desired_font
            self.b_thrid.bind("<Button-1>", lambda event, optional_video = True: self.open_first(optional_video))
            self.b_thrid.pack(side=tk.TOP, padx=1, pady=1)
        except AssertionError:
            messagebox.showerror("Error box", "The size of the uploaded files does not match")
        
    def paired(self):
        global df_loaded_first, df_loaded_second, join_index_list_g, join_index_list, df_loaded_first_copy, df_result
        
        self.new_root_v3.destroy()
        self.new_root_v4 = tk.Toplevel(self.root, background= "black")
        self.new_root_v4.title("Paired labels comparison")
        self.new_root_v5 = tk.Toplevel(self.root, background= "black")
        self.new_root_v5.title("Plot")
        df_loaded_first = df_loaded_first.fillna("989_12478")
        df_loaded_second = df_loaded_second.fillna("989_12478")
        list_column_1 = list(df_loaded_first.columns)
        index_list_column_1 = [i for i in range(len(list_column_1)) if "None" not in list_column_1[i]]
        list_column_2 = list(df_loaded_second.columns)
        index_list_column_2 = [i for i in range(len(list_column_2)) if "None" not in list_column_2[i]]
        join_index_list = list(set(index_list_column_1 + index_list_column_2))
        join_index_list.remove(9)
        result_column_list = ["General_fidelity_[%]", "Labeling_fidelity_[%]", "Unlabeling_fidelity_[%]", "Labeled_by_both_[n]", "Unlabeled_by_both_[n]", "Labeled_by_one_[n]", "Phi_coefficient"]
        
        
        join_index_list_g = (i for i in join_index_list)
        df_loaded_first_copy = df_loaded_first.copy(deep=True)
        g_paried_gen = self.paried_gen()
        len_df, _ = df_loaded_first.shape
        for i in range(len(join_index_list)):
            next(g_paried_gen)
        result_count = [df_loaded_first_copy.iloc[:,i].sum() for i in range(10, 10+2*len(join_index_list))]
        row_n = [f"Key_{i+1}" for i in range(len(join_index_list))]
        df_result = pd.DataFrame(columns = result_column_list, index = row_n)
        df_loaded_first.iloc[:, 0:9] = df_loaded_first.iloc[:, 0:9] != "989_12478"
        df_loaded_second.iloc[:, 0:9] = df_loaded_second.iloc[:, 0:9] != "989_12478"
        
        x = 0
        for i,j in enumerate(result_count):
            if i% 2 == 0:
                print(i,j)
                res = round((j + result_count[i+1]) / len_df * 100)
                
                res_1 = round(j/ (j + (len_df - (j + result_count[i+1]))) * 100) if j != 0 else 0
                res_2 =  round(result_count[i+1]/ (result_count[i+1] + (len_df - (j + result_count[i+1]))) * 100)
                res_3 = j
                res_4 = result_count[i+1]
                res_5 = len_df - (j + result_count[i+1])
                first_np = np.asarray(df_loaded_first.iloc[:, x])
                first_np = first_np * 1
                second_np = np.asarray(df_loaded_second.iloc[:, x])
                second_np = second_np * 1
                res_6 = round(matthews_corrcoef(first_np, second_np),2)
                df_result.iloc[x,:] = [res, res_1, res_2, res_3, res_4, res_5, res_6]
                
                x +=1
        
        df_result.insert(0, "Key" ,row_n)
        
        #Tabel 
        self.tabel_frame_v1 = tk.Frame(self.new_root_v4)
        self.tabel_frame_v1.pack(fill='both', expand=True)
        pt = Table(self.tabel_frame_v1, dataframe=df_result)
        pt.show()
        
        
        # Figure Matplotlib
        plt.style.use("ggplot")
        barWidth = 0.25
        fig = Figure(figsize = (5, 5), dpi = 100)
        plot1 = fig.add_subplot(111)
        
        br1 = np.arange(len(row_n))
        br2= [x + barWidth for x in br1]
        br3 = [x + barWidth for x in br2]
        plot1.bar(br1, list(df_result["General_fidelity_[%]"]), color = "tomato", width = barWidth, edgecolor ='black', label = "General fidelity")
        plot1.bar(br2, list(df_result["Labeling_fidelity_[%]"]), color = "limegreen", width = barWidth, edgecolor ='black', label = "Labeling fidelity")
        plot1.bar(br3, list(df_result["Unlabeling_fidelity_[%]"]), color = "lightskyblue", width = barWidth, edgecolor ='black', label = "Unlabeling fidelity")
        plot1.set_ylabel("Fidelity [%]", fontweight = "bold", fontsize  = 15)
        plot1.set_xlabel("Key number", fontweight = "bold", fontsize  = 15)
        plot1.set_xticks(br2)
        plot1.set_xticklabels(row_n)
        plot1.legend()
        tk_plot = FigureCanvasTkAgg(fig, self.new_root_v5)
        tk_plot.get_tk_widget().pack(fill=tk.BOTH)
        
    
    def paried_gen(self):
        global join_index_list_g, join_index_list
        for j in range(len(join_index_list)):
            i = next(join_index_list_g)
            df_loaded_first_copy[f"Key_{i+1}_label"] = np.where((df_loaded_first.iloc[:, i] != "989_12478") & (df_loaded_second.iloc[:,i] != "989_12478"), True, False)
            df_loaded_first_copy[f"Key_{i+1}_unlabel"] = np.where((df_loaded_first.iloc[:, i] == "989_12478") & (df_loaded_second.iloc[:,i] == "989_12478"), True, False)
            
            yield df_loaded_first_copy
    
    def real_time_fun(self):
        app_v2 = Real_time()

    
    def close_gate(self):
        msgbox = tk.messagebox.askquestion ('Exit Application','Are you sure you want to exit the application? Unsaved data will be lost',icon = 'warning')
        if msgbox == "yes":
            self.engine.say(random.choice(self.list_of_voices_2))
            self.engine.runAndWait()
            self.root.destroy()
            cv2.destroyAllWindows()
        else:
            pass
    
    def close_gate2(self):
        msgbox = tk.messagebox.askquestion ('Exit Application','Are you sure you want to exit the support window? Unsaved data will be lost',icon = 'warning')
        if msgbox == "yes":
            self.root_support.destroy()
        else:
            pass
    def play_labeled_fun(self):
        if video_file == None or label_list == None or df_checker == False:
            messagebox.showerror("Error box", "Video unlabeled")
        else:
            messagebox.showinfo("Information box", "Choose labels you interested to see")
            self.new_root_5 = tk.Toplevel(self.root, background= "black")
            self.new_root_5.title("Choose your labels")
            filter_labels = [i for i in label_list if i != "None"]
            self.list_of_choosen = []
            if not filter_labels:
                messagebox.showerror("Error box", "Labels were not set")
            else:
                if label_list[0] != "None":
                    self.frames_labeled_v1 = tk.Frame(self.new_root_5, background="black", width = 20)
                    self.frames_labeled_v1.pack(side = tk.TOP, expand=True, fill='both')
                    var1 = tk.StringVar()
                    var1.set("None")
                    self.label_check_box_v1 = tk.Checkbutton(self.frames_labeled_v1, text = '1. ' + str(label_list[0]), variable=var1, onvalue=label_list[0], offvalue= "None", background="black", foreground="green", highlightcolor = "black")
                    self.label_check_box_v1.pack(side= tk.LEFT)
                    self.list_of_choosen.append(var1)
                
                if label_list[1] != "None":
                    self.frames_labeled_v2 = tk.Frame(self.new_root_5, background="black", width = 20)
                    self.frames_labeled_v2.pack(side = tk.TOP, expand=True, fill='both')
                    var2 = tk.StringVar()
                    var2.set("None")
                    self.label_check_box_v2 = tk.Checkbutton(self.frames_labeled_v2, text = '2. ' + str(label_list[1]), variable=var2, onvalue=label_list[1], offvalue="None", background="black", foreground="green")
                    self.label_check_box_v2.pack(side= tk.LEFT)
                    self.list_of_choosen.append(var2)
                    
                if label_list[2] != "None":
                    self.frames_labeled_v3 = tk.Frame(self.new_root_5, background="black", width = 20)
                    self.frames_labeled_v3.pack(side = tk.TOP, expand=True, fill='both')
                    var3 = tk.StringVar()
                    var3.set("None")
                    self.label_check_box_v3 = tk.Checkbutton(self.frames_labeled_v3, text = '3. ' + str(label_list[2]), variable=var3, onvalue=label_list[2], offvalue="None", background="black", foreground="green")
                    self.label_check_box_v3.pack(side= tk.LEFT)
                    self.list_of_choosen.append(var3)
                
                if label_list[3] != "None":
                    self.frames_labeled_v4 = tk.Frame(self.new_root_5, background="black", width = 20)
                    self.frames_labeled_v4.pack(side = tk.TOP, expand=True, fill='both')
                    var4 = tk.StringVar()
                    var4.set("None")
                    self.label_check_box_v4 = tk.Checkbutton(self.frames_labeled_v4, text = '4. ' + str(label_list[3]), variable=var4, onvalue=label_list[3], offvalue="None", background="black", foreground="green")
                    self.label_check_box_v4.pack(side= tk.LEFT)
                    self.list_of_choosen.append(var4)
                
                if label_list[4] != "None":
                    self.frames_labeled_v5 = tk.Frame(self.new_root_5, background="black", width = 20)
                    self.frames_labeled_v5.pack(side = tk.TOP, expand=True, fill='both')
                    var5 = tk.StringVar()
                    var5.set("None")
                    self.label_check_box_v5 = tk.Checkbutton(self.frames_labeled_v5, text = '5. ' + str(label_list[4]), variable=var5, onvalue=label_list[4], offvalue="None", background="black", foreground="green")
                    self.label_check_box_v5.pack(side= tk.LEFT)
                    self.list_of_choosen.append(var5)
                    
                if label_list[5] != "None":
                    self.frames_labeled_v6 = tk.Frame(self.new_root_5, background="black", width = 20)
                    self.frames_labeled_v6.pack(side = tk.TOP, expand=True, fill='both')
                    var6 = tk.StringVar()
                    var6.set("None")
                    self.label_check_box_v6 = tk.Checkbutton(self.frames_labeled_v6, text = '6. ' + str(label_list[5]), variable=var6, onvalue=label_list[5], offvalue="None", background="black", foreground="green")
                    self.label_check_box_v6.pack(side= tk.LEFT)
                    self.list_of_choosen.append(var6)
                    
                if label_list[6] != "None":
                    self.frames_labeled_v7 = tk.Frame(self.new_root_5, background="black", width = 20)
                    self.frames_labeled_v7.pack(side = tk.TOP, expand=True, fill='both')
                    var7 = tk.StringVar()
                    var7.set("None")
                    self.label_check_box_v7 = tk.Checkbutton(self.frames_labeled_v7, text = '7. ' + str(label_list[6]), variable=var7, onvalue=label_list[6], offvalue="None", background="black", foreground="green")
                    self.label_check_box_v7.pack(side= tk.LEFT)
                    self.list_of_choosen.append(var7)
                    
                if label_list[7] != "None":
                    self.frames_labeled_v8 = tk.Frame(self.new_root_5, background="black", width = 20)
                    self.frames_labeled_v8.pack(side = tk.TOP, expand=True, fill='both')
                    var8 = tk.StringVar()
                    var8.set("None")
                    self.label_check_box_v8 = tk.Checkbutton(self.frames_labeled_v8, text = '8. ' + str(label_list[7]), variable=var8, onvalue=label_list[7], offvalue="None", background="black", foreground="green")
                    self.label_check_box_v8.pack(side= tk.LEFT)
                    self.list_of_choosen.append(var8)
                    
                if label_list[8] != "None":
                    self.frames_labeled_v9 = tk.Frame(self.new_root_5, background="black", width = 20)
                    self.frames_labeled_v9.pack(side = tk.TOP, expand=True, fill='both')
                    var9 = tk.StringVar()
                    var9.set("None")
                    self.label_check_box_v9 = tk.Checkbutton(self.frames_labeled_v9, text = '9. ' + str(label_list[8]), variable=var9, onvalue=label_list[8], offvalue="None", background="black", foreground="green")
                    self.label_check_box_v9.pack(side= tk.LEFT)
                    self.list_of_choosen.append(var9)
                
                self.frames_v10 = tk.Frame(self.new_root_5, background="black")
                self.frames_v10.pack(side = tk.TOP, expand=True, fill='both')
                
                self.label_time_box = tk.Label(self.frames_v10, text = "Minimal time of videos [s]:", background="black", foreground="green")
                self.label_time_box.pack(side = tk.LEFT, expand=True, fill='both')
                
                self.box_for_time_v1 = tk.Entry(self.frames_v10, width = 16, background="black", foreground="green", insertbackground = "green", )
                self.box_for_time_v1.insert(tk.INSERT, "1")
                self.box_for_time_v1.pack(side = tk.LEFT, expand=True, fill='both')
                
                self.frames_v11 = tk.Frame(self.new_root_5, background="black")
                self.frames_v11.pack(side = tk.TOP, expand=True, fill='both')
                
                self.frames_labeled_submit = tk.Button(self.frames_v11, text = "Save", command = self.get_play_labeled, foreground="green", background= "black")
                self.frames_labeled_submit.pack(side = tk.TOP, expand=True, fill='both')

    def get_play_labeled(self):
        try:    
            self.time_filter = float(self.box_for_time_v1.get()) * 1000
            self.new_root_5.destroy()
            self.new_root_6 = tk.Toplevel(self.root, background= "black")
            self.new_root_6.title("Video screen")
            self.on_value = [i.get() for i in self.list_of_choosen if i.get() != "None"]
            self.start_frame = 0
            self.stop_frame = 0
            self.videopanel_v1 = tk.Frame(self.new_root_6, background="#116562") # for video
            self.canvas = tk.Canvas(self.videopanel_v1).pack(fill=tk.BOTH, expand=1)
            self.videopanel_v1.pack(fill=tk.BOTH, expand=1, side = tk.TOP)
            
            self.Instance = vlc.Instance()
            self.player_v1 = self.Instance.media_player_new()
            self.media = self.Instance.media_new(video_file)
            self.player_v1.set_media(self.media)
            self.player_v1.set_hwnd(self.videopanel_v1.winfo_id())
            self.changer = 0
            
            self.screen_width = int(self.new_root_6.winfo_screenwidth())
            self.screen_height = int(self.new_root_6.winfo_screenheight()/2)
            
            self.frame_otpions = tk.Frame(self.new_root_6, background="#116562")
            self.frame_otpions.pack(fill=tk.BOTH, expand=0, side = tk.BOTTOM)
            
            self.on_value = [i.get() for i in self.list_of_choosen if i.get() != "None"]
            self.filter_time_dict = {i: df.loc[df[i] == i, "Frame time [ms]."].tolist() for i in self.on_value}
            
            variable = tk.StringVar()
            variable.set("Choose your label")
            
            self.dropdown_menu = tk.OptionMenu(self.frame_otpions, variable, *self.on_value, command = self.option_menu)
            self.dropdown_menu["menu"].config(bg = "black")
            self.dropdown_menu["menu"].config(fg = "green")
            self.dropdown_menu.config(bg = "black")
            self.dropdown_menu.config(fg = "green")
            self.dropdown_menu.pack(fill=tk.BOTH, expand=0, side = tk.LEFT)
            self.dropdown_menu["font"] = self.desired_font
            self.dropdown_menu["menu"]["font"] = self.desired_font
            
            self.text_third = f"Frames from {self.start_frame} to {self.stop_frame}"
            self.current_frames = tk.Label(self.frame_otpions, height = 1, width=25, background="black", foreground="#FFFF00", anchor = tk.CENTER, relief = tk.RAISED)
            self.current_frames["font"] = self.desired_font
            self.current_frames.config(text = self.text_third)
            self.current_frames.pack(fill=tk.BOTH, expand=0, side = tk.LEFT)
            
            self.delete_range = tk.Button(self.frame_otpions, text = "Unlabel", foreground="green", background= "black", command = self.delete_range) 
            self.delete_range["font"] = self.desired_font
            self.delete_range.pack(fill=tk.BOTH, expand=0, side = tk.LEFT)
            
            self.frame_next_button= tk.Frame(self.new_root_6, background="#116562")
            self.frame_next_button.pack(fill=tk.BOTH, expand=0, side = tk.TOP)
            
            self.next_button = tk.Button(self.frame_next_button, text = "Play", foreground="green", background= "black", command = self.generator_controler) 
            self.next_button["font"] = self.desired_font
            self.next_button.pack(fill=tk.BOTH, expand=0, side = tk.LEFT)
            
            self.sync_video = tk.Button(self.frame_next_button, text = "Synchronize", foreground="green", background= "black", command = self.video_synchronizer)
            self.sync_video["font"] = self.desired_font
            self.sync_video.pack(fill=tk.BOTH, expand=0, side = tk.LEFT)
            
            self.pause_button_v1 = tk.Button(self.frame_next_button, text = "Pause", foreground="green", background= "black") 
            self.pause_button_v1.bind("<Button-1>", lambda event, player = self.player_v1: app.button_pause_fun(player))
            self.pause_button_v1["font"] = self.desired_font
            self.pause_button_v1.pack(fill=tk.BOTH, expand=0, side = tk.LEFT)
            
            self.button_next_frame = tk.Button(self.frame_next_button, text = "Next Frame", background="black", foreground="green", width = 17)
            self.button_next_frame.bind("<Button-1>", lambda event, player = self.player_v1: app.next_frame(player))
            self.button_next_frame["font"] = self.desired_font
            self.button_next_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=0)
            
            self.button_previous = tk.Button(self.frame_next_button, text = "Prev. Frame", background="black", foreground="green", width = 17)
            self.button_previous["font"] = self.desired_font
            self.button_previous.bind("<Button-1>", lambda event, player = self.player_v1, master = self.new_root_6: app.previous_frame(player, master))
            self.button_previous.pack(side=tk.LEFT, fill=tk.BOTH, expand=0)
            
            self.bindings_previous = self.new_root_6.bind("<a>", lambda event, player = self.player_v1, master = self.new_root_6: app.previous_frame(player, master))
            self.bindings_next = self.new_root_6.bind("<d>", lambda event, player = self.player_v1: app.next_frame(player))
            self.bindings_space = self.new_root_6.bind("<space>", lambda event, player = self.player_v1: app.button_pause_fun(player))
            
        except ValueError:
            messagebox.showerror("Error box", "You inserted wrong value try using integers")
    
    def next_video_controler(self):
        self.break_point = 1
    
    def delete_range(self):
        global df
        msgbox = tk.messagebox.askquestion ('Typical window','Do you want to specify range? If "no" will be clicked whole range will be unlabeled.',icon = 'warning')
        if msgbox == "yes":
            self.new_root_7 = tk.Toplevel(self.new_root_6, background= "black")
            
            self.vVar1 = tk.DoubleVar()   #bottom handle variable
            self.vVar2 = tk.DoubleVar()
            
            self.vVar1.set(self.start_frame)
            self.vVar2.set(self.stop_frame)
            
            self.panel_v2 = tk.Frame(self.new_root_7, background="#116562")
            self.panel_v2 .pack(fill=tk.BOTH, expand=1, side = tk.TOP)
            
            rs1 = RangeSliderH(self.panel_v2, [self.vVar1, self.vVar2], padX=50, min_val = self.start_frame, max_val= self.stop_frame, digit_precision = ".0f")
            rs1.pack()
            
        elif msgbox == "no":
            try:
                assert self.start_frame + self.stop_frame > 0
                df.loc[self.start_frame:self.stop_frame, self.selection] = np.nan
                messagebox.showinfo("Information box", "Range unlabeled")
            except AssertionError:
                messagebox.showerror("Error box", "No frame to delete")
                
    def option_menu(self, selection):
        self.value = self.filter_time_dict.get(selection)
        self.value.append(self.value[-1] + 20000)
        self.generator_instance = self.generator_labels()
        self.selection = selection 
    def generator_controler(self):
     global answer_scale, length_movie, df
     try:
            self.start_time, self.stop_time_v1 = next(self.generator_instance)
            list_of_times = df["Frame time [ms]."].tolist()
            closest_timestamp_start = min(list_of_times, key=lambda x:abs(x-self.start_time))
            closest_timestamp_stop = min(list_of_times, key=lambda x:abs(x-self.stop_time_v1))
            self.start_frame = list_of_times.index(closest_timestamp_start) + 1
            self.stop_frame = list_of_times.index(closest_timestamp_stop) + 1
            self.stop_time_v1 /= 1000
            self.text_third = f"Frames from {self.start_frame} to {self.stop_frame}"
            self.current_frames.config(text = self.text_third)
            
            if self.var2_controller:
                 self.start_time = 0 if self.start_time - answer_scale * 1000 <= 0 else self.start_time - answer_scale * 1000
                 self.stop_time_v1 = length_movie / 1000 if self.stop_time_v1 * 1000 + answer_scale * 1000 >= length_movie else self.stop_time_v1 + answer_scale 
            
            if self.changer == 0 :
                self.media.add_option(f"stop-time={self.stop_time_v1}")
                self.changer = 1
                self.player_v1.set_time(0)
                self.player_v1.play()
                sleep(0.1)
                self.player_v1.play()
                self.player_v1.set_time(round(self.start_time))
            elif self.changer == 1:
                self.media = self.Instance.media_new(video_file)
                self.player_v1.set_media(self.media)
                self.player_v1.set_hwnd(self.videopanel_v1.winfo_id())
                self.media.add_option(f"stop-time={self.stop_time_v1}")
                self.player_v1.play()
                self.player_v1.set_time(round(self.start_time))
                self.player_v1.play()
                self.pause_button_v1.focus_set()
     except StopIteration:
            messagebox.showinfo("Information box", "All labeled video been played. If you want to watch them again, click Next button")
            self.generator_instance = self.generator_labels()
            
            self.changer = 1
     except AttributeError:
            messagebox.showerror("Error box", "First, choose label you want to watch!")
    
    def generator_labels(self):
            initial = 0
            n = 0
            for i, j in enumerate(self.value):
                if n == 0:
                    start_point = j
                    n += 1
                    initial = j
                elif j - initial < 60:
                    initial = j
                elif j - initial > 60 and n == 1:
                    stop_point = initial
                    if stop_point - start_point > self.time_filter:
                        #duration = stop_point - start_point
                        yield start_point, stop_point
                        initial = j
                        start_point = j
                    else:
                        n += 1
                        initial = j
                        start_point = j
                elif j - initial > 60: 
                    stop_point = initial
                    if stop_point - start_point > self.time_filter:
                        #duration = stop_point - start_point
                        yield start_point, stop_point
                        initial = j
                        start_point = j
                    else:
                        initial = j
                        start_point = j
    
    def video_synchronizer(self):
        global window_checker, app
        if window_checker == 0:
            current_state = str(self.player_v1.get_state())
            if current_state == "State.Playing":
                self.player_v1.pause()
            self.bridge_start_video()
            time_to_set = self.player_v1.get_time()
            Start_video.set_time_automatically(self, time_set = time_to_set)
            self.new_root_6.geometry(f'{self.screen_width}x{self.screen_height-50}+0-34')
            app.set_video_postion()
            self.pause_button_v1.focus_set()
            cv2.setTrackbarPos(trackbar_name, track_bar_panel, time_to_set)
        else:
            current_state = str(self.player_v1.get_state())
            if current_state == "State.Playing":
                self.player_v1.pause()
            time_to_set = self.player_v1.get_time()
            Start_video.set_time_automatically(self, time_set = time_to_set)
            self.new_root_6.geometry(f'{self.screen_width}x{self.screen_height-50}+0-34')
            self.pause_button_v1.focus_set()
            cv2.setTrackbarPos(trackbar_name, track_bar_panel, time_to_set)
            
    def easy_open(self):
        global video_file, available_formats, player, media
        video_file = easygui.fileopenbox(title="Select An Video", filetypes= ["*.gif", "*.flv", "*.avi", "*.amv", "*.mp4"])
        if video_file != None:
            video_title = video_file.split("\\")
            video_format = video_title[-1].split(".")
            video_format = video_format[-1].lower()
            if self.reupload_controler == 1 and video_format in available_formats:
                msgbox = tk.messagebox.askquestion ('Exit Application','Are you sure you want to re-upload video? Unsaved data will be lost?',icon = 'warning')
                if msgbox == "yes":
                    self.restart_systems()
                    self.text = f"Video: {video_title[-1]}"
                    self.current_video.configure(width = len(self.text))
                    self.current_video.config(text = self.text)
                    messagebox.showinfo("Information box", "Video re-uploaded")
                    vlc_instance = vlc.Instance()
                    player = vlc_instance.media_player_new()
                    media = vlc_instance.media_new(video_file)
                    player.set_media(media)
                else:
                    pass
            elif video_format in available_formats:
                self.text = f"Video: {video_title[-1]}"
                self.current_video.configure(width = len(self.text))
                self.current_video.config(text = self.text)
                messagebox.showinfo("Information box", "Video uploaded")
                vlc_instance = vlc.Instance()
                player = vlc_instance.media_player_new()
                media = vlc_instance.media_new(video_file)
                player.set_media(media)
                self.reupload_controler += 1
            else:
                messagebox.showerror("Error box", "Wrong format of video!")
                messagebox.showinfo("Information box", f'Currently available formats: .flv, .avi, .amv, .mp4, \nformat of your video : {video_format}')
        else:
            self.text = "Video: None"
            self.current_video.configure(width = len(self.text))
            self.current_video.config(text = self.text)
            messagebox.showerror("Error box", "Video was not loaded")
    
    def restart_systems(self):
        global df_checker, label_list, label_name, radio_variable
        df_checker = False
        label_list = None
        label_name = [f"{None}",f"{None}",f"{None}",f"{None}",f"{None}",f"{None}",f"{None}",f"{None}",f"{None}"]
        self.var1_controller = False
        radio_variable = "off"
        if t != None:
            t.cancel()
    def keyboard_settings(self):
        global fps
        self.new_root = tk.Toplevel(self.root)
        self.new_root.title("Keyboard_settings")
        self.var_checker()
        self.first_frame_v1 = tk.Frame(self.new_root, background="black")
        self.first_frame_v1.pack(expand=True, fill='both')
        
        self.second_frame_v2 = tk.Frame(self.new_root, background="black")
        self.second_frame_v2.pack(expand=True, fill='both')
        
        self.third_frame_v2 = tk.Frame(self.new_root, background="black")
        self.third_frame_v2.pack(expand=True, fill='both')
        
        self.third_frame_v3 = tk.Frame(self.new_root, background="black")
        self.third_frame_v3.pack(expand=True, fill='both')
        
        self.fourth_frame_v2 = tk.Frame(self.new_root, background="black")
        self.fourth_frame_v2.pack(expand=True, fill='both')
        
        self.instruction = tk.Text(self.first_frame_v1, height = 23, width = 70)
        self.text_v1 = "Press on your keyboard:\n a = move one frame backward\n d = move one frame forward\n space = pause/resume the video\n z = slow down the video\n c = speed up the video\n x = video speed back to normal\n e = frame to which (without it) all the preceding ones will\n\t be appropriately marked (depends on labels name set by user).\n\t Start point is set by key 1-9\n key 1-9 = label current frame and jumpt to next one or\n\t set the beginning of the range.\n\t Next you can move to whatever frame (backward or forward)\n\t and there set the end of the range by key e.\n\t All frames within that range will be labeled\n g = delete last used label (Check active label) from current frame\n h = removes the last labelled range\n Extra seconds = If turn on, adds extra labelled frames (1s-10s), at the \n\t beginning, and end of labeled range but only during playback \n\t (Play labeled frames).\n" 

        conteiner = ["~"*70, "~"*70, self.text_v1, "="*70, "="*70]
        
        for i in range(len(conteiner)):
            self.instruction.insert(tk.INSERT, conteiner[i])
            self.instruction.pack(side=tk.TOP, expand=True, fill='both')
            self.instruction.configure(foreground="green", background= "black")
            
        self.label_saving = tk.Label(self.second_frame_v2, text = "Auto Save:", foreground="green", background= "black")
        self.label_saving["font"] = self.desired_font
        self.label_saving.pack(side=tk.LEFT, padx=1, pady=1)
        
        self.radio_BTN_saving_on = tk.Radiobutton(self.second_frame_v2, fg = "green" ,bg = "black", text = "on", variable =self.var1, value = "on", selectcolor = "black", tristatevalue= "on")
        self.radio_BTN_saving_on["font"] = self.desired_font
        self.radio_BTN_saving_on.pack(side=tk.LEFT, padx=1, pady=1)
        
        self.radio_BTN_saving_off = tk.Radiobutton(self.second_frame_v2, bg = "black", fg = "green", text = "off", variable = self.var1, value = "off", highlightbackground = "black", selectcolor = "black", tristatevalue= "off")
        self.radio_BTN_saving_off["font"] = self.desired_font
        self.radio_BTN_saving_off.pack(side=tk.LEFT, padx=1, pady=1)
        
        self.label_saving = tk.Label(self.third_frame_v2, text = "Extra seconds:", foreground="green", background= "black")
        self.label_saving["font"] = self.desired_font
        self.label_saving.pack(side=tk.LEFT, padx=1, pady=1)
        
        self.radio_BTN_saving_on_v1 = tk.Radiobutton(self.third_frame_v2, bg = "black", fg = "green", text = "on", variable = self.var2, value = "on", highlightbackground = "black", selectcolor = "black")
        self.radio_BTN_saving_on_v1["font"] = self.desired_font
        self.radio_BTN_saving_on_v1.pack(side=tk.LEFT, padx=1, pady=1)
        
        self.radio_BTN_saving_off_v1 = tk.Radiobutton(self.third_frame_v2, bg = "black", fg = "green", text = "off", variable = self.var2, value = "off", selectcolor = "black")
        self.radio_BTN_saving_off_v1["font"] = self.desired_font
        self.radio_BTN_saving_off_v1.pack(side=tk.LEFT, padx=1, pady=1)
              
        self.submit = tk.Button(self.fourth_frame_v2, text = "Submit", command = self.get_k_settings, foreground="green", background= "black")
        self.submit["font"] = self.desired_font
        self.submit.pack(side = tk.TOP, expand=True, fill='both', padx=1, pady=1)

    def get_k_settings(self):
        global save_file3, radio_variable, save_mother_df_automatic, t
        if self.var1.get() == "on":
            if video_file == None:
                messagebox.showerror("Error box", "Upload the video first")
            else:
                radio_variable = "on"
                save_file3 = None
                save_file3 = easygui.diropenbox(msg = "Select a folder for auto save", title = "Typical window")
                if save_file3 == None:
                    messagebox.showerror("Error box", "Folder was not selected, the data will not be saved automatically")
                    self.var1.set("off")
                    radio_variable = "off"
                else:
                    today = str(date.today()).replace("-", "_")
                    video_title = video_file.split("\\")
                    video_title = video_title[-1].split(".")
                    save_mother_df_automatic = save_file3 + "\\" + video_title[0] + "_auto" + ".xlsx"
                    messagebox.showinfo("Information box", "Auto save ON")
                    self.var1_controller = True
        elif self.var1.get() == "off":
            radio_variable = "off"
            self.var1_controller = False
            if t != None:
                t.cancel()
                messagebox.showinfo("Information box", "Auto save OFF")
        if self.var2.get() == "on":
            
            self.new_root_v1 = tk.Toplevel(self.new_root)
            self.first_frame_v4 = tk.Frame(self.new_root_v1, background="black")
            self.first_frame_v4.pack(expand=True, fill='both')
            
            self.label_to_scale = tk.Label(self.first_frame_v4, text = "How many seconds do you want to add?", foreground="green", background= "black")
            self.label_to_scale["font"] = self.desired_font
            self.label_to_scale.pack(side=tk.TOP, padx=1, pady=1)
            
            self.submit = tk.Button(self.first_frame_v4, text = "Submit", command = self.get_scale_val, foreground="green", background= "black")
            self.submit["font"] = self.desired_font
            self.submit.pack(side=tk.BOTTOM, expand=True, fill='both', padx=1, pady=1)
            
            self.scale_widget = tk.Scale(self.first_frame_v4, bg = "black", fg = "green", borderwidth=0  , from_=1, to=10, orient=tk.HORIZONTAL, length=400, troughcolor = 'green', activebackground = "black", highlightthickness = 1, highlightbackground = "green")
            self.scale_widget["font"] = self.desired_font
            self.scale_widget.pack(side=tk.BOTTOM, padx=1, pady=1)
        if self.var2.get() == "off":
            self.var2_controller = False
            messagebox.showinfo("Information box", "Extra time OFF")
            
    def get_scale_val(self):
        global answer_scale
        answer_scale = self.scale_widget.get()
        self.new_root_v1.destroy()
        self.var2_controller = True
        messagebox.showinfo("Information box", f"Extra time : {answer_scale}")
        
    def var_checker(self):
        if self.var1_controller:
            self.var1.set("on")
        else:
            self.var1.set("off")
        
        if self.var2_controller:
            self.var2.set("on")
        else:
            self.var2.set("off")
    def label_settings(self):
        global label_name
        self.new_root_2 = tk.Toplevel(self.root, background= "black")
        self.new_root_2.title("Label_settings")
        self.new_root_2.bind("<FocusIn>", lambda event, color = "#DCDC14": self.handle_focus(event, color))
        self.new_root_2.bind("<FocusOut>", self.handle_focus_out)
        
        self.first_frame_v2 = tk.Frame(self.new_root_2, background="black")
        self.first_frame_v2.pack(expand=True, fill='both')
        
        self.label_1 = tk.Label(self.first_frame_v2, text = "key_1 label:", foreground="green", background= "black")
        self.label_1["font"] = self.desired_font
        self.label_1.pack(side=tk.LEFT, expand=True, fill='both', padx=1, pady=1)
        
        self.label_1_text_box = tk.Text(self.first_frame_v2, height = 1, width = 20, foreground="green", background= "black", insertbackground = "white")
        self.label_1_text_box.insert(tk.INSERT, label_name[0])
        self.label_1_text_box["font"] = self.desired_font
        self.label_1_text_box.pack(side=tk.LEFT, expand=True,
                                   fill='both', padx=1, pady=1)
        
        self.second_frame_v1 = tk.Frame(self.new_root_2, background= "black")
        self.second_frame_v1.pack(side = tk.TOP,expand=True, fill='both')
        
        self.label_2 = tk.Label(self.second_frame_v1, text = "key_2 label:", foreground="green", background= "black")
        self.label_2["font"] = self.desired_font
        self.label_2.pack(side=tk.LEFT, expand=True, fill='both', padx=1, pady=1)
        
        self.label_2_text_box = tk.Text(self.second_frame_v1, height = 1, width = 20, foreground="green", background= "black",insertbackground = "white")
        self.label_2_text_box.insert(tk.INSERT, label_name[1])
        self.label_2_text_box["font"] = self.desired_font
        self.label_2_text_box.pack(side=tk.LEFT, expand=True, fill='both', padx=1, pady=1)
        
        self.third_frame = tk.Frame(self.new_root_2, background= "black")
        self.third_frame.pack(side = tk.TOP, expand=True, fill='both')
        
        self.label_3 = tk.Label(self.third_frame, text = "key_3 label:", foreground="green", background= "black")
        self.label_3["font"] = self.desired_font
        self.label_3.pack(side=tk.LEFT, expand=True, fill='both', padx=1, pady=1)
        
        self.label_3_text_box = tk.Text(self.third_frame, height = 1, width = 20, foreground="green", background= "black", insertbackground = "white")
        self.label_3_text_box.insert(tk.INSERT, label_name[2])
        self.label_3_text_box["font"] = self.desired_font
        self.label_3_text_box.pack(side=tk.LEFT, expand=True, fill='both', padx=1, pady=1)
        
        self.fourth_frame = tk.Frame(self.new_root_2, background= "black")
        self.fourth_frame.pack(side = tk.TOP, expand=True, fill='both')
        
        self.label_4 = tk.Label(self.fourth_frame, text = "key_4 label:", foreground="green", background= "black")
        self.label_4["font"] = self.desired_font
        self.label_4.pack(side=tk.LEFT, expand=True, fill='both')
        
        self.label_4_text_box = tk.Text(self.fourth_frame, height = 1, width = 20, foreground="green", background= "black", insertbackground = "white")
        self.label_4_text_box.insert(tk.INSERT, label_name[3])
        self.label_4_text_box["font"] = self.desired_font
        self.label_4_text_box.pack(side=tk.LEFT, expand=True, fill='both', padx=1, pady=1)
        
        self.fifth_frame = tk.Frame(self.new_root_2, background= "black")
        self.fifth_frame.pack(side = tk.TOP, expand=True, fill='both')
        
        self.label_5 = tk.Label(self.fifth_frame, text = "key_5 label:", foreground="green", background= "black")
        self.label_5["font"] = self.desired_font
        self.label_5.pack(side=tk.LEFT, expand=True, fill='both', padx=1, pady=1)
        
        self.label_5_text_box = tk.Text(self.fifth_frame, height = 1, width = 20, foreground="green", background= "black", insertbackground = "white")
        self.label_5_text_box.insert(tk.INSERT, label_name[4])
        self.label_5_text_box["font"] = self.desired_font
        self.label_5_text_box.pack(side=tk.LEFT, expand=True, fill='both', padx=1, pady=1)
        
        self.sixth_frame = tk.Frame(self.new_root_2, background= "black")
        self.sixth_frame.pack(side = tk.TOP,expand=True, fill='both')
        
        self.label_6 = tk.Label(self.sixth_frame, text = "key_6 label:", foreground="green", background= "black")
        self.label_6["font"] = self.desired_font
        self.label_6.pack(side=tk.LEFT, expand=True, fill='both', padx=1, pady=1)
        
        self.label_6_text_box = tk.Text(self.sixth_frame, height = 1, width = 20, foreground="green", background= "black", insertbackground = "white")
        self.label_6_text_box.insert(tk.INSERT, label_name[5])
        self.label_6_text_box["font"] = self.desired_font
        self.label_6_text_box.pack(side=tk.LEFT, expand=True, fill='both', padx=1, pady=1)
        
        self.seventh_frame = tk.Frame(self.new_root_2, background= "black")
        self.seventh_frame.pack(side = tk.TOP, expand=True, fill='both')
        
        self.label_7 = tk.Label(self.seventh_frame, text = "key_7 label:", foreground="green", background= "black")
        self.label_7["font"] = self.desired_font
        self.label_7.pack(side=tk.LEFT, expand=True, fill='both', padx=1, pady=1)
        
        self.label_7_text_box = tk.Text(self.seventh_frame, height = 1, width = 20, foreground="green", background= "black", insertbackground = "white")
        self.label_7_text_box.insert(tk.INSERT, label_name[6])
        self.label_7_text_box["font"] = self.desired_font
        self.label_7_text_box.pack(side=tk.LEFT, expand=True, fill='both', padx=1, pady=1)
        
        self.eighth_frame = tk.Frame(self.new_root_2, background= "black")
        self.eighth_frame.pack(side = tk.TOP, expand=True, fill='both')
        
        self.label_8 = tk.Label(self.eighth_frame, text = "key_8 label:", foreground="green", background= "black")
        self.label_8["font"] = self.desired_font
        self.label_8.pack(side=tk.LEFT, expand=True, fill='both', padx=1, pady=1)
        
        self.label_8_text_box = tk.Text(self.eighth_frame, height = 1, width = 20, foreground="green", background= "black", insertbackground = "white")
        self.label_8_text_box.insert(tk.INSERT, label_name[7])
        self.label_8_text_box["font"] = self.desired_font
        self.label_8_text_box.pack(side=tk.LEFT, expand=True, fill='both', padx=1, pady=1)
        
        self.ninth_frame = tk.Frame(self.new_root_2, background= "black")
        self.ninth_frame.pack(side = tk.TOP, expand=True, fill='both')
        
        self.label_9 = tk.Label(self.ninth_frame, text = "key_9 label:", foreground="green", background= "black")
        self.label_9["font"] = self.desired_font
        self.label_9.pack(side=tk.LEFT, expand=True, fill='both', padx=1, pady=1)
        
        self.label_9_text_box = tk.Text(self.ninth_frame, height = 1, width = 20, foreground="green", background= "black", insertbackground = "white")
        self.label_9_text_box.insert(tk.INSERT, label_name[8])
        self.label_9_text_box["font"] = self.desired_font
        self.label_9_text_box.pack(side=tk.LEFT, expand=True, fill='both', padx=1, pady=1)
        
        self.submit_frame = tk.Frame(self.new_root_2, background= "black")
        self.submit_frame.pack(side = tk.TOP, expand=True, fill='both')
        
        self.submit = tk.Button(self.submit_frame, text = "Submit", command = self.label_changer, foreground="green", background= "black")
        self.submit["font"] = self.desired_font
        self.submit.pack(side = tk.BOTTOM, expand=True, fill='both', padx=1, pady=1)
        
    
    def creat_configuration_fun(self):
        global label_name, configruation_title
        self.new_root_4 = tk.Toplevel(self.root, background= "black")
        self.new_root_4.title("Label_configuration")
        self.new_root_4.bind("<FocusIn>", lambda event, color = "#00008B": self.handle_focus(event, color))
        self.new_root_4.bind("<FocusOut>", self.handle_focus_out)
        
        self.first_frame_v3 = tk.Frame(self.new_root_4, background="black")
        self.first_frame_v3.pack()
        
        self.label_1_v1 = tk.Label(self.first_frame_v3, text = "key_1 label:", foreground="green", background= "black")
        self.label_1_v1["font"] = self.desired_font
        self.label_1_v1.pack(side=tk.LEFT, padx=1, pady=1)
        
        self.label_1_v1_text_box = tk.Text(self.first_frame_v3, height = 1, width = 20, foreground="green", background= "black", insertbackground = "white")
        self.label_1_v1_text_box.insert(tk.INSERT, label_name[0])
        self.label_1_v1_text_box["font"] = self.desired_font
        self.label_1_v1_text_box.pack(side=tk.LEFT, padx=1, pady=1)
        
        self.second_frame_v2 = tk.Frame(self.new_root_4, background= "black")
        self.second_frame_v2.pack(side = tk.TOP)
        
        self.label_2_v1 = tk.Label(self.second_frame_v2, text = "key_2 label:", foreground="green", background= "black")
        self.label_2_v1["font"] = self.desired_font
        self.label_2_v1.pack(side=tk.LEFT, padx=1, pady=1)
        
        self.label_2_v1_text_box = tk.Text(self.second_frame_v2, height = 1, width = 20, foreground="green", background= "black",insertbackground = "white")
        self.label_2_v1_text_box.insert(tk.INSERT, label_name[1])
        self.label_2_v1_text_box["font"] = self.desired_font
        self.label_2_v1_text_box.pack(side=tk.LEFT, padx=1, pady=1)
        
        self.third_frame_v1 = tk.Frame(self.new_root_4, background= "black")
        self.third_frame_v1.pack(side = tk.TOP)
        
        self.label_3_v1 = tk.Label(self.third_frame_v1, text = "key_3 label:", foreground="green", background= "black")
        self.label_3_v1["font"] = self.desired_font
        self.label_3_v1.pack(side=tk.LEFT, padx=1, pady=1)
        
        self.label_3_v1_text_box = tk.Text(self.third_frame_v1, height = 1, width = 20, foreground="green", background= "black", insertbackground = "white")
        self.label_3_v1_text_box.insert(tk.INSERT, label_name[2])
        self.label_3_v1_text_box["font"] = self.desired_font
        self.label_3_v1_text_box.pack(side=tk.LEFT, padx=1, pady=1)
        
        self.fourth_frame_v1 = tk.Frame(self.new_root_4, background= "black")
        self.fourth_frame_v1.pack(side = tk.TOP)
        
        self.label_4_v1 = tk.Label(self.fourth_frame_v1, text = "key_4 label:", foreground="green", background= "black")
        self.label_4_v1["font"] = self.desired_font
        self.label_4_v1.pack(side=tk.LEFT, padx=1, pady=1)
        
        self.label_4_v1_text_box = tk.Text(self.fourth_frame_v1, height = 1, width = 20, foreground="green", background= "black", insertbackground = "white")
        self.label_4_v1_text_box.insert(tk.INSERT, label_name[3])
        self.label_4_v1_text_box["font"] = self.desired_font
        self.label_4_v1_text_box.pack(side=tk.LEFT, padx=1, pady=1)
        
        self.fifth_frame_v1 = tk.Frame(self.new_root_4, background= "black")
        self.fifth_frame_v1.pack(side = tk.TOP)
        
        self.label_5_v1 = tk.Label(self.fifth_frame_v1, text = "key_5 label:", foreground="green", background= "black")
        self.label_5_v1["font"] = self.desired_font
        self.label_5_v1.pack(side=tk.LEFT, padx=1, pady=1)
        
        self.label_5_v1_text_box = tk.Text(self.fifth_frame_v1, height = 1, width = 20, foreground="green", background= "black", insertbackground = "white")
        self.label_5_v1_text_box.insert(tk.INSERT, label_name[4])
        self.label_5_v1_text_box["font"] = self.desired_font
        self.label_5_v1_text_box.pack(side=tk.LEFT, padx=1, pady=1)
        
        self.sixth_frame_v1 = tk.Frame(self.new_root_4, background= "black")
        self.sixth_frame_v1.pack(side = tk.TOP)
        
        self.label_6_v1 = tk.Label(self.sixth_frame_v1, text = "key_6 label:", foreground="green", background= "black")
        self.label_6_v1["font"] = self.desired_font
        self.label_6_v1.pack(side=tk.LEFT, padx=1, pady=1)
        
        self.label_6_v1_text_box = tk.Text(self.sixth_frame_v1, height = 1, width = 20, foreground="green", background= "black", insertbackground = "white")
        self.label_6_v1_text_box.insert(tk.INSERT, label_name[5])
        self.label_6_v1_text_box["font"] = self.desired_font
        self.label_6_v1_text_box.pack(side=tk.LEFT, padx=1, pady=1)
        
        self.seventh_frame_v1 = tk.Frame(self.new_root_4, background= "black")
        self.seventh_frame_v1.pack(side = tk.TOP)
        
        self.label_7_v1 = tk.Label(self.seventh_frame_v1, text = "key_7 label:", foreground="green", background= "black")
        self.label_7_v1["font"] = self.desired_font
        self.label_7_v1.pack(side=tk.LEFT, padx=1, pady=1)
        
        self.label_7_v1_text_box = tk.Text(self.seventh_frame_v1, height = 1, width = 20, foreground="green", background= "black", insertbackground = "white")
        self.label_7_v1_text_box.insert(tk.INSERT, label_name[6])
        self.label_7_v1_text_box["font"] = self.desired_font
        self.label_7_v1_text_box.pack(side=tk.LEFT, padx=1, pady=1)
        
        
        self.eighth_frame_v1 = tk.Frame(self.new_root_4, background= "black")
        self.eighth_frame_v1.pack(side = tk.TOP)
        
        self.label_8_v1 = tk.Label(self.eighth_frame_v1, text = "key_8 label:", foreground="green", background= "black")
        self.label_8_v1["font"] = self.desired_font
        self.label_8_v1.pack(side=tk.LEFT, padx=1, pady=1)
        
        self.label_8_v1_text_box = tk.Text(self.eighth_frame_v1, height = 1, width = 20, foreground="green", background= "black", insertbackground = "white")
        self.label_8_v1_text_box.insert(tk.INSERT, label_name[7])
        self.label_8_v1_text_box["font"] = self.desired_font
        self.label_8_v1_text_box.pack(side=tk.LEFT, padx=1, pady=1)
        
        self.ninth_frame_v1 = tk.Frame(self.new_root_4, background= "black")
        self.ninth_frame_v1.pack(side = tk.TOP)
        
        self.label_9_v1 = tk.Label(self.ninth_frame_v1, text = "key_9 label:", foreground="green", background= "black")
        self.label_9_v1["font"] = self.desired_font
        self.label_9_v1.pack(side=tk.LEFT, padx=1, pady=1)
        
        self.label_9_v1_text_box = tk.Text(self.ninth_frame_v1, height = 1, width = 20, foreground="green", background= "black", insertbackground = "white")
        self.label_9_v1_text_box.insert(tk.INSERT, label_name[8])
        self.label_9_v1_text_box["font"] = self.desired_font
        self.label_9_v1_text_box.pack(side=tk.LEFT, padx=1, pady=1)
        
        self.tenth_frame = tk.Frame(self.new_root_4, background= "black")
        self.tenth_frame.pack(side = tk.TOP)
        
        self.label_10 = tk.Label(self.tenth_frame, text = "Configuration title:", foreground="green", background= "black")
        self.label_10["font"] = self.desired_font
        self.label_10.pack(side=tk.LEFT, pady=10)
        
        self.label_10_text_box = tk.Text(self.tenth_frame, height = 1, width = 20, foreground="green", background= "black", insertbackground = "white")
        self.label_10_text_box.insert(tk.INSERT, configruation_title)
        self.label_10_text_box["font"] = self.desired_font
        self.label_10_text_box.pack(side=tk.LEFT, pady=15)
        
        self.save_v1_frame = tk.Frame(self.new_root_4, background= "black")
        self.save_v1_frame.pack(side = tk.TOP)
        
        self.submit = tk.Button(self.save_v1_frame, text = "Save", command = self.label_configurator_save, foreground="green", background= "black")
        self.submit["font"] = self.desired_font
        self.submit.pack(side = tk.BOTTOM, padx=1, pady=1)
    
    def handle_focus(self, event, color: str):
        x = event.widget.get("1.0", "end-1c")
        
        if x == "None":
            event.widget.delete("1.0","end")
            event.widget.config(fg = color)
        else:
            event.widget.config(fg = color)
    
    def handle_focus_out(self, event):
        x = event.widget.get("1.0", "end-1c")
        if len(x) == 0:
            event.widget.insert(tk.INSERT, "None")
            event.widget.config(fg = "green")
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
            self.new_root_2.destroy()
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
        global df_checker, df, frame_duration, app
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
                    df = pd.DataFrame(columns = label_list, index = range(1, len(np.arange(0, length_movie + frame_duration, frame_duration)) + 1))
                    df.index.name="Frame No."
                    df["Frame time [ms]."] = np.arange(0, length_movie + frame_duration, frame_duration)
                    df_checker = True
                    if not df.iloc[-1,9] == length_movie:
                        df.drop(df.index[-1], inplace=True)
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
            self.root.state(newstate='iconic')
            self.Instance = vlc.Instance()
            self.player_v2 = self.Instance.media_player_new()
            media = self.Instance.media_new(video_file)
            self.player_v2.set_media(media)
            #self.player_v2.set_hwnd(self.videopanel.winfo_id())
            self.newwindow = tk.Toplevel(self.root)
            app = Start_video(self.newwindow, self.player_v2)

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
    

def run_save_machine_state(logic_gate):
    global df, video_file, label_list, t
    if video_file == None or label_list == None or df_checker == False:
        messagebox.showerror("Error box", "Before save current state:\n 1. Upload the video \n 2. Submit any label \n 3. Label something")
    elif logic_gate:
        mother_df = df
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
    elif radio_variable == "on":
        autosave()

def autosave():
    global t, df
    mother_df = df
    mother_df.to_excel(save_mother_df_automatic)
    t = threading.Timer(120, autosave)
    t.start()

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
        today = str(date.today()).replace("-", "_")
        save_file_excel = save_file + "\\" + video_title[0] + "_" + today + '.xlsx'
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

    def __init__(self, newwindow, player_v2):
        global video_file, list_of_times, first_time, current_label, text, track_bar_panel, trackbar_name, label_panel_v1_text, label_panel_v2_text, length_movie, label_panel_v3_text, label_panel_v4_text, label_panel_v5_text, label_panel_v6_text, label_panel_v7_text, label_panel_v8_text, label_panel_v9_text, df, window_checker
        self.master = newwindow
        self.master.configure(background='black')
        self.master.protocol("WM_DELETE_WINDOW", disable_event)
        self.player = player_v2
        self.desired_font = tk.font.Font(size = 14)
        track_bar_panel = "Track bar"
        trackbar_name = "Time [ms]"
        window_checker = 1
        cv2.namedWindow(track_bar_panel, cv2.WINDOW_NORMAL)
        if not length_movie:
            length_movie = int(df.iloc[-1, 9])
        cv2.createTrackbar(trackbar_name, track_bar_panel, 0, length_movie, self.slider_fun)
        self.set_video_postion()
        run_save_machine_state(logic_gate= False)
        
        self.video_rate_gen = (2.5 * num for num in range(1,4))
        self.bindings_on()
        self.img = self.audio_icon()
        
        self.labelspanel = tk.Frame(self.master, background="#116562")
        self.labelspanel.pack(side= tk.LEFT, fill=tk.NONE, expand=0)
        
        self.videopanel = tk.Frame(self.master, background="#116562") # for video
        self.canvas = tk.Canvas(self.videopanel).pack(fill=tk.BOTH, expand=1)
        self.videopanel.pack(fill=tk.BOTH, expand=1, side = tk.TOP)
        
        self.main_frame_v3 = tk.Frame(self.master, background="#116562") #for controls
        self.main_frame_v3.pack(side= tk.BOTTOM, fill=tk.NONE, expand=0)
        
        self.main_frame_v2 = tk.Frame(self.master, background="#116562") #for controls
        self.main_frame_v2.pack(side= tk.BOTTOM, fill=tk.NONE, expand=0)
        
        self.button_pause = tk.Button(self.main_frame_v2, text = "Pause/PLay", background="black", foreground="green", width = 17)
        self.button_pause["font"] = self.desired_font
        self.button_pause.bind("<Button-1>", lambda event, player = self.player: self.button_pause_fun(player))
        self.button_pause.pack(side=tk.LEFT, fill=tk.BOTH, expand=0)
        
        self.button_next = tk.Button(self.main_frame_v2, text = "Next Frame", background="black", foreground="green", width = 17)
        self.button_next["font"] = self.desired_font
        self.button_next.bind("<Button-1>", lambda event, player = self.player: self.next_frame(player))
        self.button_next.pack(side=tk.LEFT, fill=tk.BOTH, expand=0)
        
        self.button_previous = tk.Button(self.main_frame_v2, text = "Prev. Frame", background="black", foreground="green", width = 17)
        self.button_previous["font"] = self.desired_font
        self.button_previous.bind("<Button-1>", lambda event, player = self.player, master = self.master: self.previous_frame(player, master))
        self.button_previous.pack(side=tk.LEFT, fill=tk.BOTH, expand=0)
        
        label_panel_v1_text = tk.StringVar()
        label_panel_v1_text.set("Label 1: None")
        self.label_panel_v1 = tk.Label( self.labelspanel, textvariable = label_panel_v1_text, background="black", foreground="green", width = 18, height = 7, bd = 0)
        self.label_panel_v1["font"] = self.desired_font
        self.label_panel_v1.grid(row = 0, column = 0, padx=1, pady=1, sticky = tk.EW)
        
        label_panel_v2_text = tk.StringVar()
        label_panel_v2_text.set("Label 2: None")
        self.label_panel_v2 = tk.Label( self.labelspanel, textvariable = label_panel_v2_text, background="black", foreground="green", width = 18, height = 7, bd = 0)
        self.label_panel_v2["font"] = self.desired_font
        self.label_panel_v2.grid(row = 0, column = 1, padx=1, pady=1, sticky = tk.EW)
        
        label_panel_v3_text = tk.StringVar()
        label_panel_v3_text.set("Label 3: None")
        self.label_panel_v3 = tk.Label( self.labelspanel, textvariable = label_panel_v3_text, background="black", foreground="green", width = 18, height = 7, bd = 0)
        self.label_panel_v3["font"] = self.desired_font
        self.label_panel_v3.grid(row = 0, column = 2, padx=1, pady=1, sticky = tk.EW)
        
        label_panel_v4_text = tk.StringVar()
        label_panel_v4_text.set("Label 4: None")
        self.label_panel_v4 = tk.Label( self.labelspanel, textvariable = label_panel_v4_text, background="black", foreground="green", width = 18, height = 7, bd = 0)
        self.label_panel_v4["font"] = self.desired_font
        self.label_panel_v4.grid(row = 1, column = 0, padx=1, pady=1)
        
        label_panel_v5_text = tk.StringVar()
        label_panel_v5_text.set("Label 5: None")
        self.label_panel_v5 = tk.Label( self.labelspanel, textvariable = label_panel_v5_text, background="black", foreground="green", width = 18, height = 7, bd = 0)
        self.label_panel_v5["font"] = self.desired_font
        self.label_panel_v5.grid(row = 1, column = 1, padx=1, pady=1)
        
        label_panel_v6_text = tk.StringVar()
        label_panel_v6_text.set("Label 6: None")
        self.label_panel_v6 = tk.Label( self.labelspanel, textvariable = label_panel_v6_text, background="black", foreground="green", width = 18, height = 7, bd = 0)
        self.label_panel_v6["font"] = self.desired_font
        self.label_panel_v6.grid(row = 1, column = 2, padx=1, pady=1)
        
        label_panel_v7_text = tk.StringVar()
        label_panel_v7_text.set("Label 7: None")
        self.label_panel_v7 = tk.Label( self.labelspanel, textvariable = label_panel_v7_text, background="black", foreground="green", width = 18, height = 7, bd = 0)
        self.label_panel_v7["font"] = self.desired_font
        self.label_panel_v7.grid(row = 2, column = 0, padx=1, pady=1)
        
        label_panel_v8_text = tk.StringVar()
        label_panel_v8_text.set("Label 8: None")
        self.label_panel_v8 = tk.Label( self.labelspanel, textvariable = label_panel_v8_text, background="black", foreground="green", width = 18, height = 7, bd = 0)
        self.label_panel_v8["font"] = self.desired_font
        self.label_panel_v8.grid(row = 2, column = 1, padx=1, pady=1)
        
        label_panel_v9_text = tk.StringVar()
        label_panel_v9_text.set("Label 9: None")
        self.label_panel_v9 = tk.Label( self.labelspanel, textvariable = label_panel_v9_text, background="black", foreground="green", width = 18, height = 7, bd = 0)
        self.label_panel_v9["font"] = self.desired_font
        self.label_panel_v9.grid(row = 2, column = 2, padx=1, pady=1)
        
        self.button_set_time = tk.Button(self.main_frame_v2, text = "Set time [click me] of video [ms]:", background="black", foreground="green", width = 24)
        self.button_set_time["font"] = self.desired_font
        self.button_set_time.bind("<Button-1>", self.set_time_manually)
        self.button_set_time.pack(side=tk.LEFT, fill=tk.BOTH, expand=0)
        
        self.box_for_time = tk.Entry(self.main_frame_v2, width = 16, background="black", foreground="green", insertbackground = "green", relief = tk.RAISED)
        self.box_for_time.pack(side=tk.LEFT, fill=tk.BOTH, expand=0)
        self.box_for_time["font"] = self.desired_font
        self.box_for_time.bind("<Enter>", self.bindings_off)
        self.box_for_time.bind("<Leave>", lambda event: self.bindings_on_2())
        
        text = tk.StringVar()
        text.set(f"Active label: {current_label}")
        self.current_label_widget = tk.Label(self.main_frame_v3, textvariable = text, background="black", foreground="#FFFF00", width = 17, relief = tk.RAISED)
        self.current_label_widget["font"] = self.desired_font
        self.current_label_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=0)
        
        self.button_check_v1 = tk.Button(self.main_frame_v3, text = "Check_labeling", background="black", foreground="green", width = 17)
        self.button_check_v1["font"] = self.desired_font
        self.button_check_v1.bind("<Button-1>", lambda event: self.slider_fun_2())
        self.button_check_v1.pack(side=tk.LEFT, fill=tk.NONE, expand=0)
        self.button_check_v1_binding = self.master.bind("<s>", lambda event: self.slider_fun_2())
        
        self.button_calibration = tk.Button(self.main_frame_v3, text = "Calibration", background="black", foreground="green", width = 17)
        self.button_calibration["font"] = self.desired_font
        self.button_calibration.bind("<Button-1>", self.calibration)
        self.button_calibration.pack(side=tk.LEFT, fill=tk.BOTH, expand=0)
        
        self.audio_label = tk.Label(self.main_frame_v3,image= self.img, bg = "green", relief = tk.SUNKEN)
        self.audio_label["font"] = self.desired_font
        self.audio_label.pack(side=tk.LEFT, fill=tk.BOTH, expand=0)
        self.audio_label.configure(foreground="green")
    
        self.var = tk.IntVar()
        self.scale_audio = tk.Scale(self.main_frame_v3, from_ = 0, to=100, length=200, orient=tk.HORIZONTAL, command = self.audio_volume, variable=self.var, bg = "black", fg = "green", troughcolor = "green", bd = 0 , highlightthickness = 0, relief = tk.RAISED)
        self.scale_audio["font"] = self.desired_font
        self.scale_audio.set(100)
        self.scale_audio.pack(side=tk.LEFT, fill=tk.BOTH, expand=0)
        
        self.exit_v1 = tk.Button(self.main_frame_v3, text = "Exit", background="black", foreground="green", width = 24, command = self.close_gate_v2)
        self.exit_v1["font"] = self.desired_font
        self.exit_v1.pack(side=tk.LEFT, fill=tk.BOTH, expand=0)
        self.player.set_hwnd(self.videopanel.winfo_id())
        
        messagebox.showinfo("Information box", "Before you start press Calibration button")
        self.player.play()
        sleep(0.2)
        self.player.pause()
        self.player.set_time(0)
        list_of_times = df["Frame time [ms]."].tolist()
        self.active_window(self.master)
    
    def set_video_postion(self):
    
        self.screen_width_v1 = int(self.master.winfo_screenwidth())
        self.screen_height_v1 = int(self.master.winfo_screenheight()/2)
        self.master.geometry(f'{self.screen_width_v1}x{self.screen_height_v1-50}+0+0')
    
    def active_window(self, window):
        window.after(1, lambda: window.focus_force())
    
    def button_pause_fun(self, player):
        return player.pause()
    
    def audio_volume(self,val):
        self.player.audio_set_volume(self.var.get())
    
    def close_gate_v2(self):
        global window_checker
        self.master.destroy()
        window_checker = 0
        cv2.destroyAllWindows()
    
    def next_frame(self, player):
        return player.next_frame()
    def set_time_automatically(self, time_set):
        app.player.set_time(time_set)
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
    
    def previous_frame(self, player, master):
        global frame_duration, time_jump
        
        if not time_jump:
            messagebox.showinfo("Information box", "I have to calibrate my self. Now you can use this option normally. Thank your for your contribution")
            back_up = player.get_time()
            player.next_frame()
            sleep(0.2)
            player.next_frame()
            sleep(0.2)
            player.next_frame()
            sleep(0.2)
            first_time = player.get_time()
            sleep(0.2)
            player.next_frame()
            sleep(0.2)
            second_time = player.get_time()
            time_jump = second_time - first_time
            player.set_time(back_up)
            self.button_calibration["state"] = tk.DISABLED
            self.button_calibration.update()
            self.active_window(master)
        else:
            back_one_frame = player.get_time()
            time_12 = back_one_frame - round(time_jump)
            current_state = str(player.get_state())
            if current_state == "State.Playing":
                player.set_time(time_12)
                player.pause()
            else:
                player.set_time(time_12)
    def audio_icon(self):
        url = "https://i.postimg.cc/MZVj1n3f/audio.png"
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        img = img.resize((20, 15))
        img = ImageTk.PhotoImage(img)
        return img
    
    def step_mode(self, index):
        global start_frame_bool, closest_timestamp, current_label, text, time_jump, back_current_label 
        current_label = label_name[index]
        if not time_jump:
            current_state = str(self.player.get_state())
            if current_state == "State.Playing":
                self.player.pause()
            else:
                pass
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
            self.button_calibration["state"] = tk.DISABLED
            self.button_calibration.update()
            self.active_window(self.master)
        elif current_label != "None":
            current_state = str(self.player.get_state())
            self.bindings_on()
            if current_state == "State.Playing":
                self.player.pause()
            else:
                pass
            back_current_label = current_label
            timestamp = self.player.get_time()
            closest_timestamp = min(list_of_times, key=lambda x:abs(x-timestamp))
            df.loc[df["Frame time [ms]."] == closest_timestamp, current_label,] = current_label
            time_12 = timestamp + round(time_jump)
            self.player.set_time(time_12)
            start_frame_bool = True
            text.set(f"Active label: {current_label}")
        else:
            messagebox.showinfo("Information box", "This key is disable, change label name If you want to use it")
    
    def end_key(self, data):
        global start_frame_bool, current_label, index_timestamp, index_timestamp_stop, closest_timestamp_stop, start_frame_bool_v2, text, back_current_label
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
                back_current_label = current_label
                current_label = "Nought"
                text.set(f"Active label: {current_label}")
                if current_state == "State.Playing":
                    self.player.pause()
                else:
                    pass
                messagebox.showinfo("Information box", f"Frames from {index_timestamp[0]} to {index_timestamp_stop[0]-1} were labeled")
                self.active_window(self.master)
                
            elif closest_timestamp_stop < closest_timestamp:
                data.loc[index_timestamp_stop[0]+1:index_timestamp[0], current_label] = current_label
                start_frame_bool = False
                start_frame_bool_v2 = True
                current_state = str(self.player.get_state())
                back_current_label = current_label
                current_label = "Nought"
                text.set(f"Active label: {current_label}")
                if current_state == "State.Playing":
                    self.player.pause()
                else:
                    pass
                messagebox.showinfo("Information box", f"Frames from {index_timestamp_stop[0]+1} to {index_timestamp[0]} were labeled")
                self.active_window(self.master)
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
        if not back_current_label:
            messagebox.showerror("Error box", "Data unlabeled")
            self.active_window(self.master)
        else:
            timestamp_v1 = self.player.get_time()
            if current_label != "Nought":
                closest_timestamp_stop_v1 = min(list_of_times, key=lambda x:abs(x-timestamp_v1))
                checker = data.loc[df["Frame time [ms]."] == closest_timestamp_stop_v1, current_label].tolist()
                if str(checker[0]) == "nan":
                    current_state = str(self.player.get_state())
                    if current_state == "State.Playing":
                        self.player.pause()
                    else:
                        pass
                    messagebox.showerror("Error box", f"Frame unlabeled or wrong label to delet (current label :{current_label})")
                    self.active_window(self.master)
                else:
                    data.loc[df["Frame time [ms]."] == closest_timestamp_stop_v1, current_label] = label
                    current_state = str(self.player.get_state())
                    if current_state == "State.Playing":
                        self.player.pause()
                    else:
                        pass
                    messagebox.showinfo("Information box", "Label deleted")
                    self.active_window(self.master)
            else:
                msgbox = tk.messagebox.askquestion ('Information box','Label inactive. Do you want to activate the key with the last used label?',icon = 'warning')
                if msgbox == "yes":
                    current_label = back_current_label
                    text.set(f"Active label: {current_label}")
                    self.active_window(self.master)

    
    def bindings_on(self):
        
        self.bindings_space = self.master.bind("<space>", lambda event, player = self.player: self.button_pause_fun(player))
        self.bindings_a = self.master.bind("<a>", lambda event, player = self.player, master = self.master: self.previous_frame(player, master))
        self.bindings_d = self.master.bind("<d>", lambda event, player = self.player: self.next_frame(player))
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
        
    def bindings_on_2(self):

        self.bindings_space = self.master.bind("<space>", lambda event, player = self.player: self.button_pause_fun(player))
        self.bindings_a = self.master.bind("<a>", lambda event, player = self.player, master = self.master: self.previous_frame(player, master))
        self.bindings_d = self.master.bind("<d>", lambda event, player = self.player: self.next_frame(player))
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

    def speed_up(self):
        try:
            messagebox.showinfo("Information box", "The video sped up")
            self.active_window(self.master)
            return self.player.set_rate(next(self.video_rate_gen))
        except StopIteration:
            self.video_rate_gen = (2.5 * num for num in range(1,4))
            self.active_window(self.master)
            return self.player.set_rate(next(self.video_rate_gen))
    def slow_down(self):
        global video_rate
        video_rate = 0.2
        messagebox.showinfo("Information box", "The video has slowed down")
        self.active_window(self.master)
        return self.player.set_rate(video_rate)
    
    def normal_speed(self):
        global video_rate
        video_rate = 1.0
        messagebox.showinfo("Information box", "Video speed, back to normal")
        self.active_window(self.master)
        return self.player.set_rate(video_rate)
    
    def ctrl_alt_delet(self, data):
        global label_name
        if start_frame_bool_v2:
            if closest_timestamp_stop >= closest_timestamp:
                data.iloc[index_timestamp[0]-1:index_timestamp_stop[0], label_name.index(back_current_label)] = np.nan
                current_state = str(self.player.get_state())
                if current_state == "State.Playing":
                        self.player.pause()
                else:
                        pass
                messagebox.showinfo("Information box", f"Labels from {index_timestamp[0]} to {index_timestamp_stop[0]-1} were deleted")
            elif closest_timestamp_stop < closest_timestamp:
                data.iloc[index_timestamp_stop[0]-1:index_timestamp[0]-1, label_name.index(back_current_label)] = np.nan
                current_state = str(self.player.get_state())
                if current_state == "State.Playing":
                        self.player.pause()
                else:
                        pass
                messagebox.showinfo("Information box", f"Labels from {index_timestamp_stop[0]+1} to {index_timestamp[0]} were deleted")
        else:
            messagebox.showerror("Error box", "First, set the beginning (key 1-9) and the end (key e) of the range")
    
    def calibration(self, event):
        global time_jump
        if self.button_calibration['state'] != "disabled":
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
            self.button_calibration["state"] = tk.DISABLED
            self.button_calibration.update()
            messagebox.showinfo("Information box", "Thank you for your contribution")
            self.active_window(self.master)
        else:
            pass
    
    def slider_fun_2(self):
        global df
        time_frame = int(self.player.get_time())
        closest_timestamp_v2 = min(list_of_times, key=lambda x:abs(x-time_frame))
        

        if label_list[0] == "None":
            label_panel_v1_text.set("Label 1: unused")
        else:
            checker = df.loc[df["Frame time [ms]."] == closest_timestamp_v2, label_list[0]].tolist()
            if checker[0] == label_list[0]:
                label_panel_v1_text.set(f"Label 1: {label_list[0]}")
                self.label_panel_v1.config(bg = "blue")
            else:
                label_panel_v1_text.set("Label 1: unlabel")
                self.label_panel_v1.config(bg = "black")
        
        if label_list[1] == "None":
            label_panel_v2_text.set("Label 2: unused")
        else:
            checker = df.loc[df["Frame time [ms]."] == closest_timestamp_v2, label_list[1]].tolist()
            if checker[0] == label_list[1]:
                label_panel_v2_text.set(f"Label 2: {label_list[1]}")
                self.label_panel_v2.config(bg = "red")
            else:
                label_panel_v2_text.set("Label 2: unlabel")
                self.label_panel_v2.config(bg = "black")
        
        if label_list[2] == "None":
            label_panel_v3_text.set("Label 3: unused")
        else:
            checker = df.loc[df["Frame time [ms]."] == closest_timestamp_v2, label_list[2]].tolist()
            if checker[0] == label_list[2]:
                label_panel_v3_text.set(f"Label 3: {label_list[2]}")
                self.label_panel_v3.config(bg = "cyan")
            else:
                label_panel_v3_text.set("Label 3: unlabel")
                self.label_panel_v3.config(bg = "black")
        
        if label_list[3] == "None":
            label_panel_v4_text.set("Label 4: unused")
        else:
            checker = df.loc[df["Frame time [ms]."] == closest_timestamp_v2, label_list[3]].tolist()
            if checker[0] == label_list[3]:
                label_panel_v4_text.set(f"Label 4: {label_list[3]}")
                self.label_panel_v4.config(bg = "yellow")
            else:
                label_panel_v4_text.set("Label 4: unlabel")
                self.label_panel_v4.config(bg = "black")
        
        if label_list[4] == "None":
            label_panel_v5_text.set("Label 5: unused")
        else:
            checker = df.loc[df["Frame time [ms]."] == closest_timestamp_v2, label_list[4]].tolist()
            if checker[0] == label_list[4]:
                label_panel_v5_text.set(f"Label 5: {label_list[4]}")
                self.label_panel_v5.config(bg = "magenta")
            else:
                label_panel_v5_text.set("Label 5: unlabel")
                self.label_panel_v5.config(bg = "black")
        
        if label_list[5] == "None":
            label_panel_v6_text.set("Label 6: unused")
        else:
            checker = df.loc[df["Frame time [ms]."] == closest_timestamp_v2, label_list[5]].tolist()
            if checker[0] == label_list[5]:
                label_panel_v6_text.set(f"Label 6: {label_list[5]}")
                self.label_panel_v6.config(bg = "#8B8B23")
            else:
                label_panel_v6_text.set("Label 6: unlabel")
                self.label_panel_v6.config(bg = "black")
        
        if label_list[6] == "None":
            label_panel_v7_text.set("Label 7: unused")
        else:
            checker = df.loc[df["Frame time [ms]."] == closest_timestamp_v2, label_list[6]].tolist()
            if checker[0] == label_list[6]:
                label_panel_v7_text.set(f"Label 7: {label_list[6]}")
                self.label_panel_v7.config(bg = "#BCBC8F")
            else:
                label_panel_v7_text.set("Label 7: unlabel")
                self.label_panel_v7.config(bg = "black")
        
        if label_list[7] == "None":
            label_panel_v8_text.set("Label 8: unused")
        else:
            checker = df.loc[df["Frame time [ms]."] == closest_timestamp_v2, label_list[7]].tolist()
            if checker[0] == label_list[7]:
                label_panel_v8_text.set(f"Label 8: {label_list[7]}")
                self.label_panel_v8.config(bg = "#3A3A5F")
            else:
                label_panel_v8_text.set("Label 8: unlabel")
                self.label_panel_v8.config(bg = "black")
        
        if label_list[8] == "None":
            label_panel_v9_text.set("Label 9: unused")
        else:
            checker = df.loc[df["Frame time [ms]."] == closest_timestamp_v2, label_list[8]].tolist()
            if checker[0] == label_list[8]:
                label_panel_v9_text.set(f"Label 9: {label_list[8]}")
                self.label_panel_v9.config(bg = "#CDCDB3")
            else:
                label_panel_v9_text.set("Label 9: unlabel")
                self.label_panel_v9.config(bg = "black")
        cv2.setTrackbarPos(trackbar_name, track_bar_panel, int(closest_timestamp_v2))
        self.active_window(self.master)
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


class Real_time:
    
    def __init__(self):
        global video_file, label_panel_v1_text_v1, trackbar_name, track_bar_panel
        self.newwindow_v2 = tk.Tk()
        self.newwindow_v2.protocol("WM_DELETE_WINDOW", disable_event)
        self.newwindow_v3 = tk.Tk()
        self.Instance = vlc.Instance()
        self.player_v3 = self.Instance.media_player_new()
        media = self.Instance.media_new(video_file)
        self.player_v3.set_media(media)
        self.len_df, _ = df_loaded_first.shape
        self.desired_font = tk.font.Font(size = 16)
        
        track_bar_panel = "Track bar"
        trackbar_name = "Frame"
        cv2.namedWindow(track_bar_panel, cv2.WINDOW_NORMAL)
        cv2.createTrackbar(trackbar_name, track_bar_panel, 1, self.len_df, self.slider_operator)
        
        
        self.videopanel_v1 = tk.Frame(self.newwindow_v2, background="#116562") # for video
        self.canvas = tk.Canvas(self.videopanel_v1).pack(fill=tk.BOTH, expand=1)
        self.videopanel_v1.pack(fill=tk.BOTH, expand=1, side = tk.TOP)
        
        self.labelspanel = tk.Frame(self.newwindow_v3, background="#116562")
        self.labelspanel.pack(side= tk.TOP, fill=tk.BOTH, expand=1)
        
        
        self.keypanel = tk.Frame(self.newwindow_v2, background="#116562")
        self.keypanel.pack(side= tk.TOP, fill=tk.NONE, expand=0)
        
        self.player_v3.set_hwnd(self.videopanel_v1.winfo_id())
        
        self.label_panel_v1 = tk.Label( self.labelspanel, text = "Label 1: None", background="black", foreground="green", width = 22, height = 12, bd = 0)
        self.label_panel_v1["font"] = self.desired_font
        self.label_panel_v1.grid(row = 0, column = 0, padx=1, pady=1, sticky = tk.EW)
        
        self.label_panel_v2 = tk.Label( self.labelspanel, text = "Label 2: None", background="black", foreground="green", width = 22, height = 12, bd = 0)
        self.label_panel_v2["font"] = self.desired_font
        self.label_panel_v2.grid(row = 0, column = 1, padx=1, pady=1, sticky = tk.EW)
        
        self.label_panel_v3 = tk.Label( self.labelspanel, text = "Label 3: None", background="black", foreground="green", width = 22, height = 12, bd = 0)
        self.label_panel_v3["font"] = self.desired_font
        self.label_panel_v3.grid(row = 0, column = 2, padx=1, pady=1, sticky = tk.EW)
        
        self.label_panel_v4 = tk.Label( self.labelspanel, text = "Label 4: None", background="black", foreground="green", width = 22, height = 12, bd = 0)
        self.label_panel_v4["font"] = self.desired_font
        self.label_panel_v4.grid(row = 1, column = 0, padx=1, pady=1)
        
        self.label_panel_v5 = tk.Label( self.labelspanel, text = "Label 5: None", background="black", foreground="green", width = 22, height = 12, bd = 0)
        self.label_panel_v5["font"] = self.desired_font
        self.label_panel_v5.grid(row = 1, column = 1, padx=1, pady=1)
        
        self.label_panel_v6 = tk.Label( self.labelspanel, text = "Label 6: None", background="black", foreground="green", width = 22, height = 12, bd = 0)
        self.label_panel_v6["font"] = self.desired_font
        self.label_panel_v6.grid(row = 1, column = 2, padx=1, pady=1)
        
        self.label_panel_v7 = tk.Label( self.labelspanel, text = "Label 7: None", background="black", foreground="green", width = 22, height = 12, bd = 0)
        self.label_panel_v7["font"] = self.desired_font
        self.label_panel_v7.grid(row = 2, column = 0, padx=1, pady=1)
        
        self.label_panel_v8 = tk.Label( self.labelspanel, text = "Label 8: None", background="black", foreground="green", width = 22, height = 12, bd = 0)
        self.label_panel_v8["font"] = self.desired_font
        self.label_panel_v8.grid(row = 2, column = 1, padx=1, pady=1)
        
        self.label_panel_v9 = tk.Label( self.labelspanel, text = "Label 9: None", background="black", foreground="green", width = 22, height = 12, bd = 0)
        self.label_panel_v9["font"] = self.desired_font
        self.label_panel_v9.grid(row = 2, column = 2, padx=1, pady=1)
        
        self.pause_button_v1 = tk.Button(self.keypanel, text = "Pause", foreground="green", background= "black", width = 17) 
        self.pause_button_v1["font"] = self.desired_font
        self.pause_button_v1.bind("<Button-1>", lambda event: self.pause())
        self.pause_button_v1.pack(side=tk.LEFT, fill=tk.NONE, expand=0)
        self.bindings_space = self.newwindow_v2.bind("<space>", lambda event: self.pause())
        
        self.next_button_v1 = tk.Button(self.keypanel, text = "Next Frame", foreground="green", background= "black", width = 17) 
        self.next_button_v1["font"] = self.desired_font
        self.next_button_v1.bind("<Button-1>", lambda event: self.next_frame())
        self.next_button_v1.pack(side=tk.LEFT, fill=tk.NONE, expand=0)
        self.next_binding = self.newwindow_v2.bind("<d>", lambda event: self.next_frame())
            
        self.button_previous_v1 = tk.Button(self.keypanel, text = "Prev. Frame", background="black", foreground="green", width = 17)
        self.button_previous_v1["font"] = self.desired_font
        self.button_previous_v1.bind("<Button-1>", lambda event, player = self.player_v3, master = self.newwindow_v2: self.previous_frame(player, master))
        self.button_previous_v1.pack(side=tk.LEFT, fill=tk.NONE, expand=0)
        self.prev_binding = self.newwindow_v2.bind("<a>", lambda event, player = self.player_v3, master = self.newwindow_v2: self.previous_frame(player, master))
        
        self.button_check_v1 = tk.Button(self.keypanel, text = "Check_labeling", background="black", foreground="green", width = 17)
        self.button_check_v1["font"] = self.desired_font
        self.button_check_v1.bind("<Button-1>", lambda event: self.check_labeling())
        self.button_check_v1.pack(side=tk.LEFT, fill=tk.NONE, expand=0)
        self.button_check_v1_binding = self.newwindow_v2.bind("<s>", lambda event: self.check_labeling())
        
        self.button_set_time_v1 = tk.Button(self.keypanel, text = "Set frame [click me] of video:", background="black", foreground="green", width = 24)
        self.button_set_time_v1["font"] = self.desired_font
        self.button_set_time_v1.bind("<Button-1>", self.set_time_manually)
        self.button_set_time_v1.pack(side=tk.LEFT, fill=tk.NONE, expand=0)
        
        self.box_for_time_v1 = tk.Entry(self.keypanel, width = 17, background="black", foreground="green", insertbackground = "green", relief = tk.RAISED)
        self.box_for_time_v1["font"] = self.desired_font
        self.box_for_time_v1.pack(side=tk.LEFT, fill=tk.NONE, expand=0)
        self.box_for_time_v1.bind("<Enter>", self.bindings_off)
        self.box_for_time_v1.bind("<Leave>", lambda event, master = self.newwindow_v2: self.active_window(master))
        
        
        
        self.exit_v2 = tk.Button(self.keypanel, text = "Exit", background="black", foreground="green", width = 24, command = self.close_gate_v2)
        self.exit_v2["font"] = self.desired_font
        self.exit_v2.pack(side=tk.LEFT, fill=tk.BOTH, expand=0)
        
        self.player_v3.play()
        sleep(0.2)
        self.player_v3.pause()
        self.player_v3.set_time(0)
            
    def bindings_off(self, event):

        self.box_for_time_v1.focus_set()
    
    def bindings_on_2(self):

        self.label_panel_v2.focus_set()
    
    def check_labeling(self):
        global controler_slider
        controler_slider = False
        self.slider_operator_v2()
    
    def pause(self):
        global controler_slider
        controler_slider = False
        self.player_v3.pause()
        self.slider_operator_v2()
    def next_frame(self):
        global controler_slider
        controler_slider = False
        self.player_v3.next_frame()
        self.slider_operator_v2()
    
    def previous_frame(self, player, master):
        global frame_duration, time_jump, controler_slider
        
        controler_slider = False
        if not time_jump:
            messagebox.showinfo("Information box", "I have to calibrate my self. Now you can use this option normally. Thank your for your contribution")
            back_up = player.get_time()
            player.next_frame()
            sleep(0.2)
            player.next_frame()
            sleep(0.2)
            player.next_frame()
            sleep(0.2)
            first_time = player.get_time()
            sleep(0.2)
            player.next_frame()
            sleep(0.2)
            second_time = player.get_time()
            time_jump = second_time - first_time
            player.set_time(back_up)
            self.active_window(master)
        else:
            back_one_frame = player.get_time()
            time_12 = back_one_frame - round(time_jump)
            current_state = str(player.get_state())
            self.slider_operator_v2()
            if current_state == "State.Playing":
                player.set_time(time_12)
                player.pause()
            else:
                player.set_time(time_12)
    def set_time_manually(self, event):
        try:
            answer_int = int(self.box_for_time_v1.get())
            self.player_v3.set_time(answer_int)
            cv2.setTrackbarPos(trackbar_name, track_bar_panel, answer_int)
            current_state = str(self.player_v3.get_state())
            if current_state == "State.Playing":
                self.player_v3.pause()
            else:
                pass
        except ValueError:
            messagebox.showerror("Error box", "You inserted wrong value try using integers")
    
    def close_gate_v2(self):
        global window_checker
        self.newwindow_v2.destroy()
        self.newwindow_v3.destroy()
        cv2.destroyAllWindows()
    
    def active_window(self, window):
        window.after(1, lambda: window.focus_force())
    
    def slider_operator_v2(self):
            global trackbar_name, track_bar_panel
            
            time_frame = int(self.player_v3.get_time())
            list_of_times = df_loaded_first["Frame time [ms]."].tolist()
            closest_timestamp = min(list_of_times, key=lambda x:abs(x-time_frame))
            list_of_times.index(closest_timestamp)
            
            list_column_1 = list(df_loaded_first.columns)
            list_column_2 = list(df_loaded_second.columns)
            
            if "None" in list_column_1[0] and "None" in list_column_2[0]:
                self.label_panel_v1.config(text = "Unused")
                self.label_panel_v1.config(bg = "#8B8B83")
                
            elif df_loaded_first.iloc[list_of_times.index(closest_timestamp), 0] == list_column_1[0] and df_loaded_second.iloc[list_of_times.index(closest_timestamp), 0] == list_column_1[0]:
                self.label_panel_v1.config(text = "Key_1: Labeled by both")
                self.label_panel_v1.config(bg = "green")
                self.label_panel_v1.config(foreground="white")
            
            elif df_loaded_first.iloc[list_of_times.index(closest_timestamp), 0] == list_column_1[0] and df_loaded_second.iloc[list_of_times.index(closest_timestamp), 0] != list_column_1[0]:
                self.label_panel_v1.config(text = f"Key_1: Labeled by {player_first}")
                self.label_panel_v1.config(bg = "red")
                self.label_panel_v1.config(foreground="black")
                
            elif df_loaded_first.iloc[list_of_times.index(closest_timestamp), 0] != list_column_1[0] and df_loaded_second.iloc[list_of_times.index(closest_timestamp), 0] == list_column_1[0]:
                self.label_panel_v1.config(text = f"Key_1: {player_second}")
                self.label_panel_v1.config(bg = "red")
                self.label_panel_v1.config(foreground="black")
                
            elif df_loaded_first.iloc[list_of_times.index(closest_timestamp), 0] != list_column_1[0] and df_loaded_second.iloc[list_of_times.index(closest_timestamp), 0] != list_column_1[0]:
                self.label_panel_v1.config(text = "Key_1: Unlabeled by both")
                self.label_panel_v1.config(bg = "blue")
                self.label_panel_v1.config(foreground="white")
            
            if "None" in list_column_1[1] and "None" in list_column_2[1]:
                self.label_panel_v2.config(text = "Unused")
                self.label_panel_v2.config(bg = "#8B8B83")
            
            elif df_loaded_first.iloc[list_of_times.index(closest_timestamp), 1] == list_column_1[1] and df_loaded_second.iloc[list_of_times.index(closest_timestamp), 1] == list_column_1[1]:
                self.label_panel_v2.config(text = "Key_2: Labeled by both")
                self.label_panel_v2.config(bg = "green")
                self.label_panel_v2.config(foreground="white")
            
            elif df_loaded_first.iloc[list_of_times.index(closest_timestamp), 1] == list_column_1[1] and df_loaded_second.iloc[list_of_times.index(closest_timestamp), 1] != list_column_1[1]:
                self.label_panel_v2.config(text = f"Key_2: Labeled by {player_first}")
                self.label_panel_v2.config(bg = "red")
                self.label_panel_v2.config(foreground="black")
                
            elif df_loaded_first.iloc[list_of_times.index(closest_timestamp), 1] != list_column_1[1] and df_loaded_second.iloc[list_of_times.index(closest_timestamp), 1] == list_column_1[1]:
                self.label_panel_v2.config(text = f"Key_2: Labeled by {player_second}")
                self.label_panel_v2.config(bg = "red")
                self.label_panel_v2.config(foreground="black")
            
            elif df_loaded_first.iloc[list_of_times.index(closest_timestamp), 1] != list_column_1[1] and df_loaded_second.iloc[list_of_times.index(closest_timestamp), 1] != list_column_1[1]:
                self.label_panel_v2.config(text = "Key_2: Unlabeled by both")
                self.label_panel_v2.config(bg = "blue")
                self.label_panel_v2.config(foreground="white")
                
            if "None" in list_column_1[2] and "None" in list_column_2[2]:
                self.label_panel_v3.config(text = "Unused")
                self.label_panel_v3.config(bg = "#8B8B83")
            
            elif df_loaded_first.iloc[list_of_times.index(closest_timestamp), 2] == list_column_1[2] and df_loaded_second.iloc[list_of_times.index(closest_timestamp), 2] == list_column_1[2]:
                self.label_panel_v3.config(text = "Key_3: Labeled by both")
                self.label_panel_v3.config(bg = "green")
                self.label_panel_v3.config(foreground="white")
            
            elif df_loaded_first.iloc[list_of_times.index(closest_timestamp), 2] == list_column_1[2] and df_loaded_second.iloc[list_of_times.index(closest_timestamp), 2] != list_column_1[2]:
                self.label_panel_v3.config(text = f"Key_3: Labeled by {player_first}")
                self.label_panel_v3.config(bg = "red")
                self.label_panel_v3.config(foreground="black")
                
            elif df_loaded_first.iloc[list_of_times.index(closest_timestamp), 2] != list_column_1[2] and df_loaded_second.iloc[list_of_times.index(closest_timestamp), 2] == list_column_1[2]:
                self.label_panel_v3.config(text = f"Key_3: Labeled by {player_second}")
                self.label_panel_v3.config(bg = "red")
                self.label_panel_v3.config(foreground="black")
            
            elif df_loaded_first.iloc[list_of_times.index(closest_timestamp), 2] != list_column_1[2] and df_loaded_second.iloc[list_of_times.index(closest_timestamp), 2] != list_column_1[2]:
                self.label_panel_v3.config(text = "Key_3: Unlabeled by both")
                self.label_panel_v3.config(bg = "blue")
                self.label_panel_v3.config(foreground="white")    
            
            if "None" in list_column_1[3] and "None" in list_column_2[3]:
                self.label_panel_v4.config(text = "Unused")
                self.label_panel_v4.config(bg = "#8B8B83")
            
            elif df_loaded_first.iloc[list_of_times.index(closest_timestamp), 3] == list_column_1[3] and df_loaded_second.iloc[list_of_times.index(closest_timestamp), 3] == list_column_1[3]:
                self.label_panel_v4.config(text = "Key_4: Labeled by both")
                self.label_panel_v4.config(bg = "green")
                self.label_panel_v4.config(foreground="white")
            
            elif df_loaded_first.iloc[list_of_times.index(closest_timestamp), 3] == list_column_1[3] and df_loaded_second.iloc[list_of_times.index(closest_timestamp), 3] != list_column_1[3]:
                self.label_panel_v4.config(text = f"Key_4: Labeled by {player_first}")
                self.label_panel_v4.config(bg = "red")
                self.label_panel_v4.config(foreground="black")
                
            elif df_loaded_first.iloc[list_of_times.index(closest_timestamp), 3] != list_column_1[3] and df_loaded_second.iloc[list_of_times.index(closest_timestamp), 3] == list_column_1[3]:
                self.label_panel_v4.config(text = f"Key_4: Labeled by {player_second}")
                self.label_panel_v4.config(bg = "red")
                self.label_panel_v4.config(foreground="black")
            
            elif df_loaded_first.iloc[list_of_times.index(closest_timestamp), 3] != list_column_1[3] and df_loaded_second.iloc[list_of_times.index(closest_timestamp), 3] != list_column_1[3]:
                self.label_panel_v4.config(text = "Key_4: Unlabeled by both")
                self.label_panel_v4.config(bg = "blue")
                self.label_panel_v4.config(foreground="white")
            
            if "None" in list_column_1[4] and "None" in list_column_2[4]:
                self.label_panel_v5.config(text = "Unused")
                self.label_panel_v5.config(bg = "#8B8B83")
            
            elif df_loaded_first.iloc[list_of_times.index(closest_timestamp), 4] == list_column_1[4] and df_loaded_second.iloc[list_of_times.index(closest_timestamp), 4] == list_column_1[4]:
                self.label_panel_v5.config(text = "Key_5: Labeled by both")
                self.label_panel_v5.config(bg = "green")
                self.label_panel_v5.config(foreground="white")
            
            elif df_loaded_first.iloc[list_of_times.index(closest_timestamp), 4] == list_column_1[4] and df_loaded_second.iloc[list_of_times.index(closest_timestamp), 4] != list_column_1[4]:
                self.label_panel_v5.config(text = f"Key_5: Labeled by {player_first}")
                self.label_panel_v5.config(bg = "red")
                self.label_panel_v5.config(foreground="black")
                
            elif df_loaded_first.iloc[list_of_times.index(closest_timestamp), 4] != list_column_1[4] and df_loaded_second.iloc[list_of_times.index(closest_timestamp), 4] == list_column_1[4]:
                self.label_panel_v5.config(text = f"Key_5: Labeled by {player_second}")
                self.label_panel_v5.config(bg = "red")
                self.label_panel_v5.config(foreground="black")
            
            elif df_loaded_first.iloc[list_of_times.index(closest_timestamp), 4] != list_column_1[4] and df_loaded_second.iloc[list_of_times.index(closest_timestamp), 4] != list_column_1[4]:
                self.label_panel_v5.config(text = "Key_5: Unlabeled by both")
                self.label_panel_v5.config(bg = "blue")
                self.label_panel_v5.config(foreground="white")
            
            if "None" in list_column_1[5] and "None" in list_column_2[5]:
                self.label_panel_v6.config(text = "Unused")
                self.label_panel_v6.config(bg = "#8B8B83")
            
            elif df_loaded_first.iloc[list_of_times.index(closest_timestamp), 5] == list_column_1[2] and df_loaded_second.iloc[list_of_times.index(closest_timestamp), 5] == list_column_1[5]:
                self.label_panel_v6.config(text = "Key_6: Labeled by both")
                self.label_panel_v6.config(bg = "green")
                self.label_panel_v6.config(foreground="white")
            
            elif df_loaded_first.iloc[list_of_times.index(closest_timestamp), 5] == list_column_1[5] and df_loaded_second.iloc[list_of_times.index(closest_timestamp), 5] != list_column_1[5]:
                self.label_panel_v6.config(text = f"Key_6: Labeled by {player_first}")
                self.label_panel_v6.config(bg = "red")
                self.label_panel_v6.config(foreground="black")
                
            elif df_loaded_first.iloc[list_of_times.index(closest_timestamp), 5] != list_column_1[5] and df_loaded_second.iloc[list_of_times.index(closest_timestamp), 5] == list_column_1[5]:
                self.label_panel_v6.config(text = f"Key_6: Labeled by {player_second}")
                self.label_panel_v6.config(bg = "red")
                self.label_panel_v6.config(foreground="black")
            
            elif df_loaded_first.iloc[list_of_times.index(closest_timestamp), 5] != list_column_1[5] and df_loaded_second.iloc[list_of_times.index(closest_timestamp), 5] != list_column_1[5]:
                self.label_panel_v6.config(text = "Key_6: Unlabeled by both")
                self.label_panel_v6.config(bg = "blue")
                self.label_panel_v6.config(foreground="white")
                
            if "None" in list_column_1[6] and "None" in list_column_2[6]:
                self.label_panel_v7.config(text = "Unused")
                self.label_panel_v7.config(bg = "#8B8B83")
            
            elif df_loaded_first.iloc[list_of_times.index(closest_timestamp), 6] == list_column_1[6] and df_loaded_second.iloc[list_of_times.index(closest_timestamp), 6] == list_column_1[6]:
                self.label_panel_v7.config(text = "Key_7: Labeled by both")
                self.label_panel_v7.config(bg = "green")
                self.label_panel_v7.config(foreground="white")
            
            elif df_loaded_first.iloc[list_of_times.index(closest_timestamp), 6] == list_column_1[6] and df_loaded_second.iloc[list_of_times.index(closest_timestamp), 6] != list_column_1[6]:
                self.label_panel_v7.config(text = f"Key_7: Labeled by {player_first}")
                self.label_panel_v7.config(bg = "red")
                self.label_panel_v7.config(foreground="black")
                
            elif df_loaded_first.iloc[list_of_times.index(closest_timestamp), 6] != list_column_1[6] and df_loaded_second.iloc[list_of_times.index(closest_timestamp), 6] == list_column_1[6]:
                self.label_panel_v7.config(text = f"Key_7: Labeled by {player_second}")
                self.label_panel_v7.config(bg = "red")
                self.label_panel_v7.config(foreground="black")
            
            elif df_loaded_first.iloc[list_of_times.index(closest_timestamp), 6] != list_column_1[6] and df_loaded_second.iloc[list_of_times.index(closest_timestamp), 6] != list_column_1[6]:
                self.label_panel_v7.config(text = "Key_7: Unlabeled by both")
                self.label_panel_v7.config(bg = "blue")
                self.label_panel_v7.config(foreground="white")
            
            if "None" in list_column_1[7] and "None" in list_column_2[7]:
                self.label_panel_v8.config(text = "Unused")
                self.label_panel_v8.config(bg = "#8B8B83")
            
            elif df_loaded_first.iloc[list_of_times.index(closest_timestamp), 7] == list_column_1[7] and df_loaded_second.iloc[list_of_times.index(closest_timestamp), 7] == list_column_1[7]:
                self.label_panel_v8.config(text = "Key_8: Labeled by both")
                self.label_panel_v8.config(bg = "green")
                self.label_panel_v8.config(foreground="white")
            
            elif df_loaded_first.iloc[list_of_times.index(closest_timestamp), 7] == list_column_1[7] and df_loaded_second.iloc[list_of_times.index(closest_timestamp), 7] != list_column_1[7]:
                self.label_panel_v8.config(text = f"Key_8: Labeled by {player_first}")
                self.label_panel_v8.config(bg = "red")
                self.label_panel_v8.config(foreground="black")
                
            elif df_loaded_first.iloc[list_of_times.index(closest_timestamp), 7] != list_column_1[7] and df_loaded_second.iloc[list_of_times.index(closest_timestamp), 7] == list_column_1[7]:
                self.label_panel_v8.config(text = f"Key_8: Labeled by {player_second}")
                self.label_panel_v8.config(bg = "red")
                self.label_panel_v8.config(foreground="black")
            
            elif df_loaded_first.iloc[list_of_times.index(closest_timestamp), 7] != list_column_1[7] and df_loaded_second.iloc[list_of_times.index(closest_timestamp), 7] != list_column_1[7]:
                self.label_panel_v8.config(text = "Key_8: Unlabeled by both")
                self.label_panel_v8.config(bg = "blue")
                self.label_panel_v8.config(foreground="white")
            
            if "None" in list_column_1[8] and "None" in list_column_2[8]:
                self.label_panel_v9.config(text = "Unused")
                self.label_panel_v9.config(bg = "#8B8B83")
            
            elif df_loaded_first.iloc[list_of_times.index(closest_timestamp), 8] == list_column_1[8] and df_loaded_second.iloc[list_of_times.index(closest_timestamp), 8] == list_column_1[8]:
                self.label_panel_v9.config(text = "Key_9: Labeled by both")
                self.label_panel_v9.config(bg = "green")
                self.label_panel_v9.config(foreground="white")
            
            elif df_loaded_first.iloc[list_of_times.index(closest_timestamp), 8] == list_column_1[8] and df_loaded_second.iloc[list_of_times.index(closest_timestamp), 8] != list_column_1[8]:
                self.label_panel_v9.config(text = f"Key_9: Labeled by {player_first}")
                self.label_panel_v9.config(bg = "red")
                self.label_panel_v9.config(foreground="black")
                
            elif df_loaded_first.iloc[list_of_times.index(closest_timestamp), 8] != list_column_1[8] and df_loaded_second.iloc[list_of_times.index(closest_timestamp), 8] == list_column_1[8]:
                self.label_panel_v9.config(text = f"Key_9: Labeled by {player_second}")
                self.label_panel_v9.config(bg = "red")
                self.label_panel_v9.config(foreground="black")
            
            elif df_loaded_first.iloc[list_of_times.index(closest_timestamp), 8] != list_column_1[8] and df_loaded_second.iloc[list_of_times.index(closest_timestamp), 8] != list_column_1[8]:
                self.label_panel_v9.config(text = "Key_9: Unlabeled by both")
                self.label_panel_v9.config(bg = "blue")
                self.label_panel_v9.config(foreground="white")
            
            cv2.setTrackbarPos(trackbar_name, track_bar_panel, list_of_times.index(closest_timestamp) + 1)
            
    
    def slider_operator(self, unused):
            global trackbar_name, track_bar_panel, controler_slider
            timestamp_track = int(cv2.getTrackbarPos(trackbar_name, track_bar_panel))
            list_column_1 = list(df_loaded_first.columns)
            list_column_2 = list(df_loaded_second.columns)
            
            if "None" in list_column_1[0] and "None" in list_column_2[0]:
                self.label_panel_v1.config(text = "Unused")
                self.label_panel_v1.config(bg = "#8B8B83")
                
            elif df_loaded_first.iloc[timestamp_track-1, 0] == list_column_1[0] and df_loaded_second.iloc[timestamp_track-1, 0] == list_column_1[0]:
                self.label_panel_v1.config(text = "Key_1: Labeled by both")
                self.label_panel_v1.config(bg = "green")
                self.label_panel_v1.config(foreground="white")
            
            elif df_loaded_first.iloc[timestamp_track-1, 0] == list_column_1[0] and df_loaded_second.iloc[timestamp_track-1, 0] != list_column_1[0]:
                self.label_panel_v1.config(text = f"Key_1: Labeled by {player_first}")
                self.label_panel_v1.config(bg = "red")
                self.label_panel_v1.config(foreground="black")
                
            elif df_loaded_first.iloc[timestamp_track-1, 0] != list_column_1[0] and df_loaded_second.iloc[timestamp_track-1, 0] == list_column_1[0]:
                self.label_panel_v1.config(text = f"Key_1: Labeled by {player_second}")
                self.label_panel_v1.config(bg = "red")
                self.label_panel_v1.config(foreground="black")
                
            elif df_loaded_first.iloc[timestamp_track-1, 0] != list_column_1[0] and df_loaded_second.iloc[timestamp_track-1, 0] != list_column_1[0]:
                self.label_panel_v1.config(text = "Key_1: Unlabeled by both")
                self.label_panel_v1.config(bg = "blue")
                self.label_panel_v1.config(foreground="white")
            
            if "None" in list_column_1[1] and "None" in list_column_2[1]:
                self.label_panel_v2.config(text = "Unused")
                self.label_panel_v2.config(bg = "#8B8B83")
            
            elif df_loaded_first.iloc[timestamp_track-1, 1] == list_column_1[1] and df_loaded_second.iloc[timestamp_track-1, 1] == list_column_1[1]:
                self.label_panel_v2.config(text = "Key_2: Labeled by both")
                self.label_panel_v2.config(bg = "green")
                self.label_panel_v2.config(foreground="white")
            
            elif df_loaded_first.iloc[timestamp_track-1, 1] == list_column_1[1] and df_loaded_second.iloc[timestamp_track-1, 1] != list_column_1[1]:
                self.label_panel_v2.config(text = f"Key_2: Labeled by {player_first}")
                self.label_panel_v2.config(bg = "red")
                self.label_panel_v2.config(foreground="black")
                
            elif df_loaded_first.iloc[timestamp_track-1, 1] != list_column_1[1] and df_loaded_second.iloc[timestamp_track-1, 1] == list_column_1[1]:
                self.label_panel_v2.config(text = f"Key_2: Labeled by {player_second}")
                self.label_panel_v2.config(bg = "red")
                self.label_panel_v2.config(foreground="black")
            
            elif df_loaded_first.iloc[timestamp_track-1, 1] != list_column_1[1] and df_loaded_second.iloc[timestamp_track-1, 1] != list_column_1[1]:
                self.label_panel_v2.config(text = "Key_2: Unlabeled by both")
                self.label_panel_v2.config(bg = "blue")
                self.label_panel_v2.config(foreground="white")
                
            if "None" in list_column_1[2] and "None" in list_column_2[2]:
                self.label_panel_v3.config(text = "Unused")
                self.label_panel_v3.config(bg = "#8B8B83")
            
            elif df_loaded_first.iloc[timestamp_track-1, 2] == list_column_1[2] and df_loaded_second.iloc[timestamp_track-1, 2] == list_column_1[2]:
                self.label_panel_v3.config(text = "Key_3: Labeled by both")
                self.label_panel_v3.config(bg = "green")
                self.label_panel_v3.config(foreground="white")
            
            elif df_loaded_first.iloc[timestamp_track-1, 2] == list_column_1[2] and df_loaded_second.iloc[timestamp_track-1, 2] != list_column_1[2]:
                self.label_panel_v3.config(text = f"Key_3: Labeled by {player_first}")
                self.label_panel_v3.config(bg = "red")
                self.label_panel_v3.config(foreground="black")
                
            elif df_loaded_first.iloc[timestamp_track-1, 2] != list_column_1[2] and df_loaded_second.iloc[timestamp_track-1, 2] == list_column_1[2]:
                self.label_panel_v3.config(text = f"Key_3: Labeled by {player_second}")
                self.label_panel_v3.config(bg = "red")
                self.label_panel_v3.config(foreground="black")
            
            elif df_loaded_first.iloc[timestamp_track-1, 2] != list_column_1[2] and df_loaded_second.iloc[timestamp_track-1, 2] != list_column_1[2]:
                self.label_panel_v3.config(text = "Key_3: Unlabeled by both")
                self.label_panel_v3.config(bg = "blue")
                self.label_panel_v3.config(foreground="white")    
            
            if "None" in list_column_1[3] and "None" in list_column_2[3]:
                self.label_panel_v4.config(text = "Unused")
                self.label_panel_v4.config(bg = "#8B8B83")
            
            elif df_loaded_first.iloc[timestamp_track-1, 3] == list_column_1[3] and df_loaded_second.iloc[timestamp_track-1, 3] == list_column_1[3]:
                self.label_panel_v4.config(text = "Key_4: Labeled by both")
                self.label_panel_v4.config(bg = "green")
                self.label_panel_v4.config(foreground="white")
            
            elif df_loaded_first.iloc[timestamp_track-1, 3] == list_column_1[3] and df_loaded_second.iloc[timestamp_track-1, 3] != list_column_1[3]:
                self.label_panel_v4.config(text = f"Key_4: Labeled by {player_first}")
                self.label_panel_v4.config(bg = "red")
                self.label_panel_v4.config(foreground="black")
                
            elif df_loaded_first.iloc[timestamp_track-1, 3] != list_column_1[3] and df_loaded_second.iloc[timestamp_track-1, 3] == list_column_1[3]:
                self.label_panel_v4.config(text = f"Key_4: Labeled by {player_second}")
                self.label_panel_v4.config(bg = "red")
                self.label_panel_v4.config(foreground="black")
            
            elif df_loaded_first.iloc[timestamp_track-1, 3] != list_column_1[3] and df_loaded_second.iloc[timestamp_track-1, 3] != list_column_1[3]:
                self.label_panel_v4.config(text = "Key_4: Unlabeled by both")
                self.label_panel_v4.config(bg = "blue")
                self.label_panel_v4.config(foreground="white")
            
            if "None" in list_column_1[4] and "None" in list_column_2[4]:
                self.label_panel_v5.config(text = "Unused")
                self.label_panel_v5.config(bg = "#8B8B83")
            
            elif df_loaded_first.iloc[timestamp_track-1, 4] == list_column_1[4] and df_loaded_second.iloc[timestamp_track-1, 4] == list_column_1[4]:
                self.label_panel_v5.config(text = "Key_5: Labeled by both")
                self.label_panel_v5.config(bg = "green")
                self.label_panel_v5.config(foreground="white")
            
            elif df_loaded_first.iloc[timestamp_track-1, 4] == list_column_1[4] and df_loaded_second.iloc[timestamp_track-1, 4] != list_column_1[4]:
                self.label_panel_v5.config(text = f"Key_5: Labeled by {player_first}")
                self.label_panel_v5.config(bg = "red")
                self.label_panel_v5.config(foreground="black")
                
            elif df_loaded_first.iloc[timestamp_track-1, 4] != list_column_1[4] and df_loaded_second.iloc[timestamp_track-1, 4] == list_column_1[4]:
                self.label_panel_v5.config(text = f"Key_5: Labeled by {player_second}")
                self.label_panel_v5.config(bg = "red")
                self.label_panel_v5.config(foreground="black")
            
            elif df_loaded_first.iloc[timestamp_track-1, 4] != list_column_1[4] and df_loaded_second.iloc[timestamp_track-1, 4] != list_column_1[4]:
                self.label_panel_v5.config(text = "Key_5: Unlabeled by both")
                self.label_panel_v5.config(bg = "blue")
                self.label_panel_v5.config(foreground="white")
            
            if "None" in list_column_1[5] and "None" in list_column_2[5]:
                self.label_panel_v6.config(text = "Unused")
                self.label_panel_v6.config(bg = "#8B8B83")
            
            elif df_loaded_first.iloc[timestamp_track-1, 5] == list_column_1[2] and df_loaded_second.iloc[timestamp_track-1, 5] == list_column_1[5]:
                self.label_panel_v6.config(text = "Key_6: Labeled by both")
                self.label_panel_v6.config(bg = "green")
                self.label_panel_v6.config(foreground="white")
            
            elif df_loaded_first.iloc[timestamp_track-1, 5] == list_column_1[5] and df_loaded_second.iloc[timestamp_track-1, 5] != list_column_1[5]:
                self.label_panel_v6.config(text = f"Key_6: Labeled by {player_first}")
                self.label_panel_v6.config(bg = "red")
                self.label_panel_v6.config(foreground="black")
                
            elif df_loaded_first.iloc[timestamp_track-1, 5] != list_column_1[5] and df_loaded_second.iloc[timestamp_track-1, 5] == list_column_1[5]:
                self.label_panel_v6.config(text = f"Key_6: Labeled by {player_second}")
                self.label_panel_v6.config(bg = "red")
                self.label_panel_v6.config(foreground="black")
            
            elif df_loaded_first.iloc[timestamp_track-1, 5] != list_column_1[5] and df_loaded_second.iloc[timestamp_track-1, 5] != list_column_1[5]:
                self.label_panel_v6.config(text = "Key_6: Unlabeled by both")
                self.label_panel_v6.config(bg = "blue")
                self.label_panel_v6.config(foreground="white")
                
            if "None" in list_column_1[6] and "None" in list_column_2[6]:
                self.label_panel_v7.config(text = "Unused")
                self.label_panel_v7.config(bg = "#8B8B83")
            
            elif df_loaded_first.iloc[timestamp_track-1, 6] == list_column_1[6] and df_loaded_second.iloc[timestamp_track-1, 6] == list_column_1[6]:
                self.label_panel_v7.config(text = "Key_7: Labeled by both")
                self.label_panel_v7.config(bg = "green")
                self.label_panel_v7.config(foreground="white")
            
            elif df_loaded_first.iloc[timestamp_track-1, 6] == list_column_1[6] and df_loaded_second.iloc[timestamp_track-1, 6] != list_column_1[6]:
                self.label_panel_v7.config(text = f"Key_7: Labeled by {player_first}")
                self.label_panel_v7.config(bg = "red")
                self.label_panel_v7.config(foreground="black")
                
            elif df_loaded_first.iloc[timestamp_track-1, 6] != list_column_1[6] and df_loaded_second.iloc[timestamp_track-1, 6] == list_column_1[6]:
                self.label_panel_v7.config(text = f"Key_7: Labeled by {player_second}")
                self.label_panel_v7.config(bg = "red")
                self.label_panel_v7.config(foreground="black")
            
            elif df_loaded_first.iloc[timestamp_track-1, 6] != list_column_1[6] and df_loaded_second.iloc[timestamp_track-1, 6] != list_column_1[6]:
                self.label_panel_v7.config(text = "Key_7: Unlabeled by both")
                self.label_panel_v7.config(bg = "blue")
                self.label_panel_v7.config(foreground="white")
            
            if "None" in list_column_1[7] and "None" in list_column_2[7]:
                self.label_panel_v8.config(text = "Unused")
                self.label_panel_v8.config(bg = "#8B8B83")
            
            elif df_loaded_first.iloc[timestamp_track-1, 7] == list_column_1[7] and df_loaded_second.iloc[timestamp_track-1, 7] == list_column_1[7]:
                self.label_panel_v8.config(text = "Key_8: Labeled by both")
                self.label_panel_v8.config(bg = "green")
                self.label_panel_v8.config(foreground="white")
            
            elif df_loaded_first.iloc[timestamp_track-1, 7] == list_column_1[7] and df_loaded_second.iloc[timestamp_track-1, 7] != list_column_1[7]:
                self.label_panel_v8.config(text = f"Key_8: Labeled by {player_first}")
                self.label_panel_v8.config(bg = "red")
                self.label_panel_v8.config(foreground="black")
                
            elif df_loaded_first.iloc[timestamp_track-1, 7] != list_column_1[7] and df_loaded_second.iloc[timestamp_track-1, 7] == list_column_1[7]:
                self.label_panel_v8.config(text = f"Key_8: Labeled by {player_second}")
                self.label_panel_v8.config(bg = "red")
                self.label_panel_v8.config(foreground="black")
            
            elif df_loaded_first.iloc[timestamp_track-1, 7] != list_column_1[7] and df_loaded_second.iloc[timestamp_track-1, 7] != list_column_1[7]:
                self.label_panel_v8.config(text = "Key_8: Unlabeled by both")
                self.label_panel_v8.config(bg = "blue")
                self.label_panel_v8.config(foreground="white")
            
            if "None" in list_column_1[8] and "None" in list_column_2[8]:
                self.label_panel_v9.config(text = "Unused")
                self.label_panel_v9.config(bg = "#8B8B83")
            
            elif df_loaded_first.iloc[timestamp_track-1, 8] == list_column_1[8] and df_loaded_second.iloc[timestamp_track-1, 8] == list_column_1[8]:
                self.label_panel_v9.config(text = "Key_9: Labeled by both")
                self.label_panel_v9.config(bg = "green")
                self.label_panel_v9.config(foreground="white")
            
            elif df_loaded_first.iloc[timestamp_track-1, 8] == list_column_1[8] and df_loaded_second.iloc[timestamp_track-1, 8] != list_column_1[8]:
                self.label_panel_v9.config(text = f"Key_9: Labeled by {player_first}")
                self.label_panel_v9.config(bg = "red")
                self.label_panel_v9.config(foreground="black")
                
            elif df_loaded_first.iloc[timestamp_track-1, 8] != list_column_1[8] and df_loaded_second.iloc[timestamp_track-1, 8] == list_column_1[8]:
                self.label_panel_v9.config(text = f"Key_9: Labeled by {player_second}")
                self.label_panel_v9.config(bg = "red")
                self.label_panel_v9.config(foreground="black")
            
            elif df_loaded_first.iloc[timestamp_track-1, 8] != list_column_1[8] and df_loaded_second.iloc[timestamp_track-1, 8] != list_column_1[8]:
                self.label_panel_v9.config(text = "Key_9: Unlabeled by both")
                self.label_panel_v9.config(bg = "blue")
                self.label_panel_v9.config(foreground="white")
            
            self.player_v3.set_time(int(df_loaded_first.iloc[timestamp_track-1,9]))
            if controler_slider:
                self.player_v3.play()
                self.player_v3.pause()
            controler_slider = True
video_object = Application()
video_object.root.mainloop()


"""
TODO

-- Button to choose a picture
__ Display picture path

-- Display colors in the picture
-- Button to choose the color

-- Button to display scatter plot of the color

-- Button to save pixel locations to a text file

-> Choose a picture
-> Display colors of the picture in a color frame widget
-> Choose a color from a color frame widget
-> Display scatter plot of the color

-- Fix the color frame widget -> don't know how to change its color from the inside
"""

import customtkinter as ctk
import matplotlib.pyplot as plt
from tkinter import filedialog
import tkinter as tk
from PIL import Image
import numpy as np

class App(ctk.CTk):
    def __init__(self, title: str, fg_color = None, **kwargs):
        super().__init__(fg_color, **kwargs)

        self.img = None
        self.img_path = None
        
        self.__set_appearance_and_theme(appearance_mode='dark')

        self.__set_rows_and_columns(2, 2)
        
        self.geometry('800x600')
        self.minsize(800, 600)
        
        self.title(title)
        
        # # Paddings
        __base_padding = {'padx': 2.5, 'pady': 2.5}
        __5_padding = {'padx': 5, 'pady': 5}
        
        # # Fonts
        __my_font_1=ctk.CTkFont(size=18, weight='bold')
        __my_font_2=ctk.CTkFont(weight='bold')
        
        # # Frames
        self.load_fr = ctk.CTkFrame(self)
        self.load_fr.grid(row=0, column=0, sticky='nsew', **__5_padding)    
        
        self.control_fr = ctk.CTkFrame(self)
        self.control_fr.grid(row=1, column=0, sticky='nsew', **__5_padding)
        
        self.color_fr = ctk.CTkFrame(self)
        self.color_fr.grid(row=0, column=1, rowspan=2, sticky='nsew', **__5_padding)
        
        
        # # Load Frame
        self.load_frame_tit = ctk.CTkLabel(self.load_fr, text="Load Image:", font=__my_font_1)
        self.load_frame_tit.pack(**__base_padding)
        
        self.load_path_lab = ctk.CTkLabel(self.load_fr, text="File path:", font=__my_font_2)
        self.load_path_lab.pack()
        
        self.load_path_name_lab = ctk.CTkLabel(self.load_fr, text="No file selected")
        self.load_path_name_lab.pack()
        
        self.load_butt = ctk.CTkButton(self.load_fr, text="Browse file", width=120, command=lambda: self.upload_img())
        self.load_butt.pack(**__5_padding)
        
        
        # # Control Frame
        # test_color = "#%02x%02x%02x" % (100,100,100)
        # self.test_text = ctk.CTkFrame(self.control_fr, fg_color=test_color)
        # self.test_text.pack()
        
        # # Color Frame
        self.test = ColorWidget(master=self.color_fr, color=(100,100,100,255))
        self.test.pack()
    
    def upload_img(self):
        
        file_types = [('PNG files', '*.png'), ('All files', '*')]
        file = filedialog.askopenfilename(title='Open a file', filetypes=file_types)
        
        self.image_path = file
        
        # Handle cancel
        if file == '':
            return
        
        # Change the 'load_path' label to the file path
        self.load_path_name_lab.configure(text=file)
        
        # Save image to the GUI
        self.img = Image.open(file)
    
    def __set_appearance_and_theme(self, appearance_mode='system', theme='blue'):
        '''
        Sets appearance mode and theme of the GUI. 
        appearance_mode: 'system', 'light', 'dark'
        theme: 'blue', 'dark-blue', 'green'
        
        Default appearance mode is 'system'.
        Default theme is 'blue'.
        '''
        
        ctk.set_appearance_mode(appearance_mode)
        ctk.set_default_color_theme(theme)
        
    def __set_rows_and_columns(self, rows: int, columns: int):
        '''
        Sets the number of rows and columns in the grid.
        '''
        
        for i in range(rows):
            self.rowconfigure(i, weight=1)
            
        for i in range(columns):
            self.columnconfigure(i, weight=1)
            

class ColorWidget(ctk.CTkFrame):
    def __init__(self, master: any, 
                 color,
                 width: int = 200, height: int = 200, corner_radius: int | str | None = None, border_width: int | str | None = None, bg_color: str | tuple[str, str] = "transparent", fg_color: str | tuple[str, str] | None = None, border_color: str | tuple[str, str] | None = None, background_corner_colors: tuple[str | tuple[str, str]] | None = None, overwrite_preferred_drawing_method: str | None = None, **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
        
        self.color: np.array[int, int, int, int] = color
        self.hex_color: str = "#%02x%02x%02x" % (color[0], color[1], color[2])
        
        self._bg_color = self.hex_color
        self._fg_color = self.hex_color
        
        self.label = ctk.CTkLabel(self, text="R: %d\nG: %d\nB: %d" % (color[0], color[1], color[2]))
        self.pack()
        
        self.radio_button = ctk.CTkRadioButton(self, variable=None, value=None)
        self.pack()
        
        
        
    def get_color(self):
        return self.color
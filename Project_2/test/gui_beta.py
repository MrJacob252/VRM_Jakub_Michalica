"""
TODO

-- Button to choose a picture
__ Display picture path

-- Display colors in the picture
-- Button to choose the color - DONE
-- Generate color pickers

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

class Storage:
    def __init__(self) -> None:
        self.img = None
        self.img_arr = None
        self.img_path = None
        self.img_colors = None

class App(ctk.CTk):
    def __init__(self, title: str, fg_color = None, **kwargs):
        super().__init__(fg_color, **kwargs)

        self.storage = Storage()
        
        # self.colors = np.array([[255, 255, 0, 255], 
        #                         [255, 0, 255, 255], 
        #                         [0, 255, 255, 255]])
        
        self.color_widgets = {}
        self.color_var = ctk.IntVar()        
        
        self.__set_appearance_and_theme(appearance_mode='dark')

        self.__set_rows_and_columns(2, 2)
        
        self.__width_min = 1000
        self.__height_min = 600
        
        self.geometry(f'{self.__width_min}x{self.__height_min}')
        self.minsize(self.__width_min, self.__height_min)
        
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
        self.__set_rows_and_columns(rows=12, columns=3, frame=self.color_fr)
        
        
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
        self.extract_butt = ctk.CTkButton(self.control_fr, text='Extract colors', width=120, command=lambda: self.create_color_widgets())
        self.extract_butt.pack(**__5_padding)
        
        self.show_area_butt = ctk.CTkButton(self.control_fr, text='Show color area', width=120, command=lambda: self.plot_color_area())
        self.show_area_butt.pack(**__5_padding)
        
        self.save_to_txt_but = ctk.CTkButton(self.control_fr, text='Save to txt', width=120, command=lambda: self.save_cords_to_txt())
        self.save_to_txt_but.pack(**__5_padding)
        
        
        # # Color Frame
    
    def upload_img(self):
        
        file_types = [('PNG files', '*.png'), ('All files', '*')]
        file = filedialog.askopenfilename(title='Open a file', filetypes=file_types)
        
        self.storage.img_path = file
        
        # Handle cancel
        if file == '':
            return
        
        # Change the 'load_path' label to the file path
        self.load_path_name_lab.configure(text=file)
        
        # Save image to the GUI
        self.storage.img = Image.open(file)
        
    def extract_colors(self):
        '''
        Extracts colors from the image.
        '''
        
        # Check if image exists
        if self.storage.img == None:
            return
        
        # Get the image as a numpy array
        self.storage.img_arr = np.asarray(self.storage.img)
        
        # Get the unique colors
        self.storage.img_colors = np.unique(self.storage.img_arr.copy().reshape(-1, self.storage.img_arr.shape[2]), axis=0)
        
        # print(self.storage.img_colors)
    
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
        
    def __set_rows_and_columns(self, rows: int, columns: int, frame=None):
        '''
        Sets the number of rows and columns in the self or given frame.
        '''
        
        if frame == None:
            for i in range(rows):
                self.rowconfigure(i, weight=1)
                
            for i in range(columns):
                self.columnconfigure(i, weight=1)
                
        else:
            for i in range(rows):
                frame.rowconfigure(i, weight=1)
                
            for i in range(columns):
                frame.columnconfigure(i, weight=1)
    
    def reset_color_widgets(self):
        '''
        Destroys all color widgets.
        '''
        for i in self.color_widgets:
            self.color_widgets[i].destroy()
        
        self.color_widgets = {}
               
    def create_color_widgets(self):
        """
        Creates color widgets from colors stored in self.storage.colors.
        """
        row = 0
        column = 0
        
        self.reset_color_widgets()
        
        self.extract_colors()
        
        if type(self.storage.img_colors) != np.ndarray:
            return
        # if self.storage.img_colors.any() == None:
        #     return
        
        for i, color in enumerate(self.storage.img_colors):
            # self.color_widgets.append(ColorWidget(master=self.color_fr, color=color))
            self.color_widgets[str(color)] = ColorWidget(master=self.color_fr, color=color, variable=self.color_var, value=i)
            self.color_widgets[str(color)].grid(row=row, column=column)
            
            column += 1
            if column == 3:
                row += 1
                column = 0

    def plot_color_area(self):
        """
        Plots the area of the chosen color.
        """
        
        if len(self.color_widgets) == 0:
            return
        
        # Get the color
        color = self.color_var.get()
        color_arr = self.storage.img_colors[color]
        
        active_cords = self.__generate_color_cord(color_arr)
                 
        fig, ax = plt.subplots()
        
        ax.set_xlim(0, len(self.storage.img_arr))
        ax.set_ylim(0, len(self.storage.img_arr[0]))
        ax.set_aspect('equal')
        
        plot = ax.scatter([i[0] for i in active_cords], 
                          [i[1] for i in active_cords])
        plt.show()

    def __generate_color_cord(self, color_array):
        
        coordinates = []
        
        for i in range(len(self.storage.img_arr)):
            for j in range(len(self.storage.img_arr[i])):
                if np.array_equal(self.storage.img_arr[i][j], color_array):
                    # Coordinates transformed for origin in the bottom left corner
                    # X axis goes from left to right
                    # Y axis goes from bottom to top
                    y = 127 - i
                    coordinates.append([j, y])
                    
        return coordinates
    
    def save_cords_to_txt(self):
        
        if len(self.color_widgets) == 0:
            return
        
        color = self.color_var.get()
        color_arr = self.storage.img_colors[color]
        
        active_cords = self.__generate_color_cord(color_arr)
        
        with open('cords.txt', 'w') as f:
            for cord in active_cords:
                
                if cord == active_cords[-1]:
                    f.write(f'{cord[0]} {cord[1]}')
                
                else:
                    f.write(f'{cord[0]} {cord[1]}\n')  


class ColorWidget(ctk.CTkFrame):
    def __init__(self, master: any, 
                 color, variable, value,
                 width: int = 200, height: int = 200, corner_radius: int | str | None = None, border_width: int | str | None = None, bg_color: str | tuple[str, str] = "transparent", fg_color: str | tuple[str, str] | None = None, border_color: str | tuple[str, str] | None = None, background_corner_colors: tuple[str | tuple[str, str]] | None = None, overwrite_preferred_drawing_method: str | None = None, **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
        
        
        self.color: np.array[int, int, int, int] = color
        self.hex_color: str = "#%02x%02x%02x" % (color[0], color[1], color[2])
        
        self._text_color: np.array[int, int, int, int] = 255 - self.color
        self._text_hex_color: str = "#%02x%02x%02x" % (self._text_color[0], self._text_color[1], self._text_color[2])
        
        self.configure(fg_color=self.hex_color)
        
        # # Widgets
        self.radio_button = ctk.CTkRadioButton(self, text="R: %d\nG: %d\nB: %d" % (color[0], color[1], color[2]), text_color=self._text_hex_color, variable=variable, value=value)
        self.radio_button.pack()
        
    def get_color(self):
        return self.color
    
    def get_var_val(self):
        return self.radio_button.getint()
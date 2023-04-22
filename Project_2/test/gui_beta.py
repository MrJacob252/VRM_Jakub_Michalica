"""
TODO
-- Button to choose a picture - DONE
-- Display picture path - DONE

-- Display colors in the picture - DONE
-- Button to choose the color - DONE
-- Generate color pickers - DONE

-- Button to display scatter plot of the color - DONE

-- Button to save pixel locations to a text file - DONE

-> Choose a picture                                         - DONE
-> Display colors of the picture in a color frame widget    - DONE
-> Choose a color from a color frame widget                 - DONE
-> Display scatter plot of the color                        - DONE

-- Creating outline is slow as hell
"""
import customtkinter as ctk
import matplotlib.pyplot as plt
from tkinter import filedialog
from PIL import Image
import numpy as np


class Storage:
    """
    Data storage class
    """
    def __init__(self) -> None:
        self.img = None
        self.img_arr = None
        self.img_path = None
        self.img_size = None
        self.img_mode = None
        self.img_colors = None
        self.outline = None


class App(ctk.CTk):
    """
    Main GUI class
    """
    def __init__(self, title: str, fg_color = None, **kwargs):
        super().__init__(fg_color, **kwargs)

        # Data storage
        self.storage = Storage()
        
        # Color widgets
        self.color_widgets = {}
        
        # Radio button variable
        self.color_var = ctk.IntVar()        
        
        # Appearance setup
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
        
        self.color_fr_columns = 4
        self.color_fr_rows = 20
        self.color_fr = ctk.CTkFrame(self)
        self.color_fr.grid(row=0, column=1, rowspan=2, sticky='nsew', **__5_padding)
        self.__set_rows_and_columns(rows=self.color_fr_rows, columns=self.color_fr_columns, frame=self.color_fr)
        
        
        # # Load Frame
        self.load_frame_tit = ctk.CTkLabel(self.load_fr, text="Load Image:", font=__my_font_1)
        self.load_frame_tit.pack(**__base_padding)
        
        self.load_path_lab = ctk.CTkLabel(self.load_fr, text="File path:", font=__my_font_2)
        self.load_path_lab.pack()
        
        self.load_path_name_lab = ctk.CTkLabel(self.load_fr, text="No file selected")
        self.load_path_name_lab.pack()
        
        self.load_butt = ctk.CTkButton(self.load_fr, text="Browse file", width=120, command=lambda: self.upload_img())
        self.load_butt.pack(**__5_padding)
        
        self.img_properties_tit = ctk.CTkLabel(self.load_fr, text="Image Properties:", font=__my_font_1)
        self.img_properties_tit.pack(**__base_padding)
        
        self.img_size_tit = ctk.CTkLabel(self.load_fr, text="Image size:", font=__my_font_2)
        self.img_size_tit.pack()
        
        self.img_size_lab = ctk.CTkLabel(self.load_fr, text="None x None")
        self.img_size_lab.pack()
        
        self.img_mode_tit = ctk.CTkLabel(self.load_fr, text="Image mode:", font=__my_font_2)
        self.img_mode_tit.pack()
        
        self.img_mode_lab = ctk.CTkLabel(self.load_fr, text="None")
        self.img_mode_lab.pack()
        
        # # Control Frame
        self.extract_butt = ctk.CTkButton(self.control_fr, text='Extract colors', width=120, command=lambda: self.create_color_widgets())
        self.extract_butt.pack(**__5_padding)
        
        self.show_area_butt = ctk.CTkButton(self.control_fr, text='Show color area', width=120, command=lambda: self.plot_color_area())
        self.show_area_butt.pack(**__5_padding)
        
        self.save_to_txt_butt = ctk.CTkButton(self.control_fr, text='Save to txt', width=120, command=lambda: self.save_cords_to_txt())
        self.save_to_txt_butt.pack(**__5_padding)
        
        self.create_outline_butt = ctk.CTkButton(self.control_fr, text='Create outline', width=120, command=lambda: self.create_outline())
        self.create_outline_butt.pack(**__5_padding)
        
        
        # # Color Frame
    
    def upload_img(self):
        """
        Lets the user choose an image file.
        Saves the image to the storage.
        Saves the image path to the storage.
        """
        
        file_types = [('PNG files', '*.png'), ('All files', '*')]
        file = filedialog.askopenfilename(title='Open a file', filetypes=file_types)
        
        self.storage.img_path = file
        
        # Handle cancel
        if file == '':
            return
        
        # Change the 'load_path' label to the file path
        self.load_path_name_lab.configure(text=file)
        
        # Save image and its properties to the storage
        self.storage.img = Image.open(file)
        self.storage.img_mode = self.storage.img.mode
        self.storage.img_size = self.storage.img.size
        
        # Change the 'img_size' label to the image size
        self.img_size_lab.configure(text=f'{self.storage.img_size[0]} x {self.storage.img_size[1]}')
        
        # Change the 'img_mode' label to the image mode
        self.img_mode_lab.configure(text=self.storage.img_mode)
        
    def extract_colors(self):
        '''
        Creates a numpy array of the image.
        Extracts colors from the image array.
        '''
        
        # Check if image exists
        if self.storage.img == None:
            return
        
        # Get the image as a numpy array
        self.storage.img_arr = np.asarray(self.storage.img)
        
        # Get the unique colors
        self.storage.img_colors = np.unique(self.storage.img_arr.reshape(-1, self.storage.img_arr.shape[2]), axis=0)
        # self.storage.img_colors = np.unique(self.storage.img_arr, axis=0)
        # print(self.storage.img_colors)
    
    def create_outline(self):
        
        # Handle if no colors are present
        if len(self.color_widgets) == 0:
            return
        
        # Get the color from radio button
        color = self.color_var.get()
        color_arr = self.storage.img_colors[color]
        
        # Generate coordinates of the color
        active_cords = self.__generate_color_cord(color_arr)
        # print(active_cords)
        
        delete_cords = []
        
        for i in active_cords:
            current_cord_x_p = [i[0] + 1, i[1]]
            current_cord_x_m = [i[0] - 1, i[1]]
            current_cord_y_p = [i[0], i[1] + 1]
            current_cord_y_m = [i[0], i[1] - 1]
            
            # if current_cord_x_p in active_cords and current_cord_x_m in active_cords and current_cord_y_p in active_cords and current_cord_y_m in active_cords:
            #     delete_cords.append(i)
            if current_cord_x_p in active_cords and current_cord_x_m in active_cords and current_cord_y_p in active_cords and current_cord_y_m in active_cords:
                delete_cords.append(i)
        
        outline_cords = []
          
        for j in active_cords:
            if j not in delete_cords:
                outline_cords.append(j)
        
        # Creates subplot
        fig, ax = plt.subplots()
        
        # Configure subplot axes
        ax.set_xlim(0, len(self.storage.img_arr) - 1)
        ax.set_ylim(0, len(self.storage.img_arr[0]) - 1)
        ax.set_aspect('equal')
        
        # Plot the coordinates of the color as a scatter plot
        plot = ax.scatter([i[0] for i in outline_cords], 
                          [i[1] for i in outline_cords])
        
        plt.show()
        
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
        # Self
        if frame == None:
            for i in range(rows):
                self.rowconfigure(i, weight=1)
                
            for i in range(columns):
                self.columnconfigure(i, weight=1)
        
        # Given frame  
        else:
            for i in range(rows):
                frame.rowconfigure(i, weight=1)
                
            for i in range(columns):
                frame.columnconfigure(i, weight=1)
    
    def reset_color_widgets(self):
        '''
        Destroys all color widgets and resets the dict.
        '''
        for i in self.color_widgets:
            self.color_widgets[i].destroy()
        
        self.color_widgets = {}
               
    def create_color_widgets(self):
        """
        Creates color widgets from colors stored in self.storage.colors.
        """
        # Initialose rows and columns
        row = 0
        column = 0
        
        # Reset color widgets
        self.reset_color_widgets()
        
        # Extract colors
        self.extract_colors()
        
        # Handls if no colors are present
        if type(self.storage.img_colors) != np.ndarray:
            return
        
        # Create color widget for each color
        for i, color in enumerate(self.storage.img_colors):
            # self.color_widgets.append(ColorWidget(master=self.color_fr, color=color))
            self.color_widgets[str(color)] = ColorWidget(master=self.color_fr, color=color, variable=self.color_var, value=i)
            self.color_widgets[str(color)].grid(row=row, column=column)
            
            # Increment rows and columns
            column += 1
            if column == self.color_fr_columns:
                row += 1
                column = 0

    def plot_color_area(self):
        """
        Plots the area of the chosen color.
        """
        
        # Handle if no colors are present
        if len(self.color_widgets) == 0:
            return
        
        # Get the color from radio button
        color = self.color_var.get()
        color_arr = self.storage.img_colors[color]
        
        # Generate coordinates of the color
        active_cords = self.__generate_color_cord(color_arr)
        
        # Creates subplot
        fig, ax = plt.subplots()
        
        # Configure subplot axes
        ax.set_xlim(0, len(self.storage.img_arr) - 1)
        ax.set_ylim(0, len(self.storage.img_arr[0]) - 1)
        ax.set_aspect('equal')
        
        # Plot the coordinates of the color as a scatter plot
        plot = ax.scatter([i[0] for i in active_cords], 
                          [i[1] for i in active_cords])
        
        plt.show()

    def __generate_color_cord(self, color_array):
        """
        Returns a list of coordinates of the given color.
        """
        coordinates = []
        
        for i in range(len(self.storage.img_arr)):
            for j in range(len(self.storage.img_arr[i])):
                if np.array_equal(self.storage.img_arr[i][j], color_array):
                    # Coordinates transformed for origin in the bottom left corner
                    # X axis goes from left to right
                    # Y axis goes from bottom to top
                    # y = 127 - i
                    # height of the image - y position
                    y = (len(self.storage.img_arr) - 1) - i
                    coordinates.append([j, y])
                    
        return coordinates
    
    def save_cords_to_txt(self):
        '''
        Saves list of coordinates of the chosen color to a txt file.
        '''
        
        # Handle if no colors are present
        if len(self.color_widgets) == 0:
            return
        
        # Get the color from radio button
        color = self.color_var.get()
        color_arr = self.storage.img_colors[color]
        
        # Generate coordinates of the color
        active_cords = self.__generate_color_cord(color_arr)
        
        # Write the coordinates to a txt file
        with open('cords.txt', 'w') as f:
            for cord in active_cords:
                
                if cord != active_cords[-1]:
                    f.write(f'{cord[0]} {cord[1]}\n')
                # Last coordinate line does not have a new line character
                else:
                    f.write(f'{cord[0]} {cord[1]}')  


class ColorWidget(ctk.CTkFrame):
    '''
    Color widget class.
    '''
    def __init__(self, master: any, 
                 color, variable, value,
                 width: int = 200, height: int = 200, corner_radius: int | str | None = None, border_width: int | str | None = None, bg_color: str | tuple[str, str] = "transparent", fg_color: str | tuple[str, str] | None = None, border_color: str | tuple[str, str] | None = None, background_corner_colors: tuple[str | tuple[str, str]] | None = None, overwrite_preferred_drawing_method: str | None = None, **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
        
        # Color format from the picture array
        self.color: np.array[int, int, int, int] = color
        # Convert given color to hex string format
        self.hex_color: str = "#%02x%02x%02x" % (color[0], color[1], color[2])
        
        # Calculate text color as an inverse of the given color
        self._text_color: np.array[int, int, int, int] = 255 - self.color
        self._text_hex_color: str = "#%02x%02x%02x" % (self._text_color[0], self._text_color[1], self._text_color[2])
        
        # Set the background color of the widget
        self.configure(fg_color=self.hex_color)
        
        # Radio button
        self.radio_button = ctk.CTkRadioButton(self, text="R: %d\nG: %d\nB: %d" % (color[0], color[1], color[2]), text_color=self._text_hex_color, variable=variable, value=value)
        self.radio_button.pack()
    
    # # Getters
    def get_color(self):
        '''
        Returns the color of the widget as np array.
        '''
        return self.color
    
    def get_var_val(self):
        '''
        Returns the value of the radio button variable.
        '''
        return self.radio_button.getint()
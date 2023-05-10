"""
TODO
Refactor gui
Add conversion to rapid code
add scaling of the picture
"""
from typing import Optional, Tuple, Union
import customtkinter as ctk
import matplotlib.pyplot as plt
from tkinter import filedialog
import numpy as np
import cv2

class Storage:
    """
    Data storage class
    """
    def __init__(self) -> None:
        self.img = None
        self.img_path = None
        self.img_shape = [None, None, None] # [height, width, channels]
        self.img_grey = None
        self.img_only_black = None
        self.img_only_grey = None
        self.img_only_white = None
        
        self.outline_black = None
        self.outline_grey = None
        
        self.encoded_black = None
        self.encoded_grey = None
        
        self.BLACK = [0, 63]
        self.GREY = [self.BLACK[0], 152]
        self.WHITE = [self.GREY[1] + 1, 255]
        
        self.paper_scale_img = None

class App(ctk.CTk):
    """
    Main GUI class
    """
    def __init__(self, title: str, fg_color = None, **kwargs):
        super().__init__(fg_color, **kwargs)

        # Data storage
        self.storage = Storage()
        
        # Paper size
        self.paper_size = (380, 260) # Width x Height [mm]
        self.mm_per_px = 1 # mm = 1 px
        self.max_px_size = (self.paper_size[0] / self.mm_per_px, self.paper_size[1] / self.mm_per_px) # Width x Height [px]
                
        # Color entries
        self.color_entry = {}       
        
        # Appearance setup
        self.__set_appearance_and_theme(appearance_mode='dark')

        self.__set_rows_and_columns(2, 2)
        
        self.__width_min = 1000
        self.__height_min = 1000
        
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
        
        self.img_size_tit = ctk.CTkLabel(self.load_fr, text="Image width, height:", font=__my_font_2)
        self.img_size_tit.pack()
        
        self.img_size_lab = ctk.CTkLabel(self.load_fr, text="None x None")
        self.img_size_lab.pack()
        
        self.img_chan_tit = ctk.CTkLabel(self.load_fr, text="Image channels:", font=__my_font_2)
        self.img_chan_tit.pack()
        
        self.img_mode_lab = ctk.CTkLabel(self.load_fr, text="None")
        self.img_mode_lab.pack()
        
        # # Control Frame
        self.extract_butt = ctk.CTkButton(self.control_fr, text='Grayscale', width=120, command=lambda: self.turn_grayscale())
        self.extract_butt.pack(**__5_padding)
        
        self.show_area_butt = ctk.CTkButton(self.control_fr, text='Resize', width=120, command=lambda: self.resize_image(width=480))
        self.show_area_butt.pack(**__5_padding)
        
        self.black_limits = ColorLimitEntry(self.control_fr, name='Black', default_values=self.storage.BLACK)
        self.black_limits.pack(**__base_padding)
        self.color_entry['black'] = self.black_limits
        
        self.gen_black_area_butt = ctk.CTkButton(self.control_fr, text='Generate black', width=120, command=lambda: self.show_color(self.storage.BLACK))
        self.gen_black_area_butt.pack(**__5_padding)
        
        self.black_limits = ColorLimitEntry(self.control_fr, name='Grey', default_values=self.storage.GREY)
        self.black_limits.pack(**__base_padding)
        self.color_entry['grey'] = self.black_limits
        
        self.gen_gray_area_butt = ctk.CTkButton(self.control_fr, text='Generate grey', width=120, command=lambda: self.show_color(self.storage.GREY))
        self.gen_gray_area_butt.pack(**__5_padding)
        
        self.black_limits = ColorLimitEntry(self.control_fr, name='White', default_values=self.storage.WHITE)
        self.black_limits.pack(**__base_padding)
        self.color_entry['white'] = self.black_limits
        
        self.gen_white_area_butt = ctk.CTkButton(self.control_fr, text='Generate white', width=120, command=lambda: self.show_color(self.storage.WHITE))
        self.gen_white_area_butt.pack(**__5_padding)
        
        self.display_blk_outline_butt = ctk.CTkButton(self.control_fr, text='Show black outline', width=120, command=lambda: self.show_black_outline())
        self.display_blk_outline_butt.pack(**__5_padding)
        
        self.display_grey_outline_butt = ctk.CTkButton(self.control_fr, text='Show grey outline', width=120, command=lambda: self.show_grey_outline())
        self.display_grey_outline_butt.pack(**__5_padding)
        
        self.paper_scale_butt = ctk.CTkButton(self.control_fr, text='Scale to paper', width=120, command=lambda: self.scale_to_paper(self.storage.img_grey, self.paper_size, self.mm_per_px))
        self.paper_scale_butt.pack(**__5_padding)
        
        self.generate_cords_butt = ctk.CTkButton(self.control_fr, text='Generate cords', width=120, command=lambda: self.generate_cords())
        self.generate_cords_butt.pack(**__5_padding)
        
        # # Color Frame
        self.how_to_tit = ctk.CTkLabel(self.color_fr, text='How to:', font=__my_font_1)
        self.how_to_tit.pack(**__base_padding)
        
        import how_to_text
        self.how_to_lab = ctk.CTkLabel(self.color_fr, text=how_to_text.text)
        self.how_to_lab.pack(**__base_padding)
    
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
    
    def __image_resize(self, image: np.ndarray, width = None, height = None, inter = cv2.INTER_AREA):
        # initialize the dimensions of the image to be resized and
        # grab the image size
        dim = None
        (h, w) = image.shape[:2]

        # if both the width and height are None, then return the
        # original image
        if width is None and height is None:
            return image

        # check to see if the width is None
        if width is None:
            # calculate the ratio of the height and construct the
            # dimensions
            r = height / float(h)
            dim = (int(w * r), height)

        # otherwise, the height is None
        else:
            # calculate the ratio of the width and construct the
            # dimensions
            r = width / float(w)
            dim = (width, int(h * r))

        # resize the image
        resized = cv2.resize(image, dim, interpolation = inter)

        # return the resized image
        return resized
        
    def upload_img(self):
        """
        Lets the user choose an image file.
        Saves the image to the storage.
        Saves the image path to the storage.
        """
        
        file_types = [('PNG files', '*.png'), ('JPG files', '*.jpg'), ('All files', '*')]
        file = filedialog.askopenfilename(title='Open a file', filetypes=file_types)
        
        self.storage.img_path = file
        
        # Handle cancel
        if file == '':
            return
        
        # Change the 'load_path' label to the file path
        self.load_path_name_lab.configure(text=file)
        
        # Save image and its properties to the storage
        self.storage.img = cv2.imread(file)
        # self.storage.img_mode = self.storage.img.mode
        self.storage.img_shape[:3] = self.storage.img.shape
        
        
        
        # Change the 'img_size' label to the image size
        self.img_size_lab.configure(text=f'{self.storage.img_shape[0]} x {self.storage.img_shape[1]}')
        
        # Change the 'img_channel' label to the image mode
        self.img_mode_lab.configure(text=self.storage.img_shape[2])

    def turn_grayscale(self):
        '''
        Turn the original image grayscale.
        '''
        
        if self.storage.img_path == None:
            return
        
        self.storage.img_grey = cv2.cvtColor(self.storage.img, cv2.COLOR_BGR2GRAY)
        
        cv2.imshow('Grayscale', self.storage.img_grey)
        # cv2.waitKey(0)
        
    def resize_image(self, width=None, height=None):
        
        if self.storage.img_path == None:
            return
        
        self.storage.img_grey = self.__image_resize(self.storage.img_grey, width=width, height=height)
          
    
    def __get_color_limits(self, COLOR):
        '''
        Retrieves color limits from entries
        '''
        
        match COLOR:
            case self.storage.BLACK:
                tmp_min = self.color_entry['black'].min_entry.get()
                self.storage.BLACK[0] = int(tmp_min)
                
                tmp_max = self.color_entry['black'].max_entry.get()
                self.storage.BLACK[1] = int(tmp_max)
            
            case self.storage.GREY:
                tmp_min = self.color_entry['grey'].min_entry.get()
                self.storage.GREY[0] = int(tmp_min)
                
                tmp_max = self.color_entry['grey'].max_entry.get()
                self.storage.GREY[1] = int(tmp_max)
            
            case self.storage.WHITE:
                tmp_min = self.color_entry['white'].min_entry.get()
                self.storage.WHITE[0] = int(tmp_min)
                
                tmp_max = self.color_entry['white'].max_entry.get()
                self.storage.WHITE[1] = int(tmp_max)

            case _:
                return
        pass
    
    def show_color(self, COLOR: tuple[int, int]):
        '''
        Shows only the pixels of a given shade
        '''
        self.__get_color_limits(COLOR)
        
        temp_img = self.storage.img_grey.copy()
        
        for i in range(len(temp_img)):
            for j in range(len(temp_img[i])):
                
                if temp_img[i][j] >= COLOR[0] and temp_img[i][j] <= COLOR[1]:
                    temp_img[i][j] = 0
                
                else:
                    temp_img[i][j] = 255
        
        match COLOR:
            case self.storage.BLACK:
                self.storage.img_only_black = temp_img
            
                cv2.imshow('Black only', temp_img)
                
                # print(temp_img)
            
            case self.storage.GREY:
                self.storage.img_only_grey = temp_img
            
                cv2.imshow('Grey only', temp_img)

                # print(temp_img)
                
            case self.storage.WHITE:
                self.storage.img_only_white = temp_img

                cv2.imshow('White only', temp_img)

                # print(temp_img)
                       
            case _:
                return
            
    def show_black_outline(self):
        '''
        Shows outline of black pixels
        '''
        img = self.storage.img_only_black
        
        # Find contours
        y_len = len(img)
        x_len = len(img[0])
        
        new_img = img.copy()
        
        for i in range(y_len):
            for j in range(x_len):
                
                if img[i][j] == 0:
                    
                    if j == 0 or j == x_len - 1:
                        new_img[i][j] = 0
    
                    elif img[i][j-1] == 0 and img[i][j+1] == 0:
                        new_img[i][j] = 255
                                  
    
            self.storage.outline_black = new_img
            
            cv2.imshow('Outline black', new_img)
                    
    def show_grey_outline(self):
        '''
        Shows outline of grey pixels
        '''
        img = self.storage.img_only_grey
        
        # Find contours
        y_len = len(img)
        x_len = len(img[0])
        
        new_img = img.copy()
        
        for i in range(y_len):
            for j in range(x_len):
                
                if img[i][j] == 0:
                    
                    if i == 0 or i == y_len - 1:
                        new_img[i][j] = 0
    
                    elif img[i-1][j] == 0 and img[i+1][j] == 0:
                        new_img[i][j] = 255
                                  
    
            self.storage.outline_grey = new_img
            
            cv2.imshow('Outline grey', new_img)                
    
    def scale_to_paper(self, image: np.ndarray[np.uint8], paper_size: tuple[int, int], mm_per_px: int):
        '''
        Scales the image to the paper size
        '''
        max_px_size = (int(np.floor(paper_size[0] / mm_per_px)), int(np.floor(paper_size[1] / mm_per_px))) # Width x Height [px]
        
        # Find the longest side
        w, h = image.shape[:2]
        print(w, h)
        
        if w >= h:
            image = self.__image_resize(image, height=max_px_size[1])
        else:
            image = self.__image_resize(image, width=max_px_size[0])
        
        print(image.shape) 
        cv2.imshow('Scaled to paper', image)
        
        self.storage.img_grey = image
        
        # self.generate_black_coords()
        # self.generate_grey_cords()
        
        
    def generate_black_coords(self, outline: np.ndarray[np.uint8]):
        '''
        Generates coordinates of black pixels
        '''
        
        h, w = outline.shape[:2]
        
        if h >= w:
            cords = np.zeros((h, h), dtype=np.uint32)
        else:
            cords = np.zeros((w, w), dtype=np.uint32)
        
        cords_location = [0, 0]
        
        for i in range(h):
            
            for j in range(w):
                # print('-------------------')
                # print(h, w)
                # print(i, j)
                # print(cords_location)
                if outline[i][j] == 0:
                    cords[cords_location[0]][cords_location[1]] = j
                    
                    cords_location[1] += 1

            cords_location[0] += 1
            cords_location[1] = 0
        
        cords = cords.T
        cords = cords[~np.all(cords == 0, axis=1)]
        cords = cords.T
        
        self.storage.encoded_black = cords
        
        print(cords)
        
    def generate_grey_cords(self, outline: np.ndarray[np.uint8]):
        '''
        Generates coordinates of grey pixels
        '''
        
        outline = outline.T
        
        h, w = outline.shape[:2]
        
        if h >= w:
            cords = np.zeros((h, h), dtype=np.uint32)
        else:
            cords = np.zeros((w, w), dtype=np.uint32)
        
        cords_location = [0, 0]
        
        for i in range(h):
            
            for j in range(w):
                
                if outline[i][j] == 0:
                    cords[cords_location[0]][cords_location[1]] = j
                    
                    cords_location[1] += 1
                    
            cords_location[0] += 1
            cords_location[1] = 0
        
        cords = cords.T
        cords = cords[~np.all(cords == 0, axis=1)]
        cords = cords.T
        
        self.storage.encoded_black = cords
        
        print(cords)
        
    def generate_cords(self):
        self.generate_black_coords(self.storage.outline_black)
        self.generate_grey_cords(self.storage.outline_grey) 
              
            
            

class ColorLimitEntry(ctk.CTkFrame):
    def __init__(self, master: any, 
                 name, default_values: list[int, int],
                 width: int = 200, height: int = 200, corner_radius: int | str | None = None, border_width: int | str | None = None, bg_color: str | Tuple[str, str] = "transparent", fg_color: str | Tuple[str, str] | None = None, border_color: str | Tuple[str, str] | None = None, background_corner_colors: Tuple[str | Tuple[str, str]] | None = None, overwrite_preferred_drawing_method: str | None = None, **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
        
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        
        # self.min_var = ctk.IntVar()
        # self.max_var = ctk.IntVar()

        self.min_var = ctk.StringVar()
        self.max_var = ctk.StringVar()

        self.min_entry = ctk.CTkEntry(self, textvariable=self.min_var)
        self.min_entry.grid(row=0, column=0)
        self.min_entry.insert(0, str(default_values[0]))
        
        self.max_entry = ctk.CTkEntry(self, textvariable=self.max_var)
        self.max_entry.grid(row=0, column=1)
        self.max_entry.insert(0, str(default_values[1]))
        
        
    
if __name__ == "__main__":
    test = App('Test GUI')
    test.mainloop()
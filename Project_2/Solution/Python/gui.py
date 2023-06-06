"""
TODO:
    - The whole thing
    
    - Image file input frame
    
    - Image conversion properties frame
    
    - Rapid code properties
    
    - 3 Columns
        - 1st: Split into two rows
        
        
    - Matplitlib preview
    - Save filedialog
"""
# Libraries
from typing import Optional, Tuple, Union
import customtkinter as ctk
from tkinter import filedialog
import numpy as np
import cv2
# Custom libraries
import func
import rapid_export


class App(ctk.CTk):
    def __init__(self, 
                 title: str, 
                 fg_color = None, **kwargs) -> None:
        super().__init__(fg_color, **kwargs)

        # # # Setup
        # # Data storage
        self.storage = func.Storage()
        
        # # Window properties
        self.__min_size = (1200, 650) # (width, height)
        self.__max_size = (1920, 1080) # (width, height)
        self.__rows_columns = (2, 3) # (rows, columns)
        
        # # Window setup
        self.title(title)
        self.__set_appearance_and_theme('dark', 'blue')
        
        self.geometry(f'{self.__min_size[0]}x{self.__min_size[1]}')
        self.minsize(self.__min_size[0], self.__min_size[1])
        self.maxsize(self.__max_size[0], self.__max_size[1])
        
        self.__set_rows_and_columns(self.__rows_columns[0], self.__rows_columns[1])
        
        # # Paddings
        self.__base_padding = {'padx': 2.5, 'pady': 2.5}
        self.__5_padding = {'padx': 5, 'pady': 5}
        
        # # Fonts        
        self.__my_font_1=ctk.CTkFont(size=18, weight='bold')
        self.__my_font_2=ctk.CTkFont(weight='bold')
        
        # # Parameter widgets
        self.__entry_widgets = []
        
        # # Image processed
        self.image_processed = False
        self.image_loaded = False
        
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # Base frames - [Row, Column] - indexed from 0
        # # 0 0 
        # self.rowconfigure(0, weight=1)
        self.__frame_0_0 = ctk.CTkFrame(self)
        self.__frame_0_0.grid(row=0, column=0, 
                              sticky='nsew', 
                              **self.__5_padding)

        # # 1 0
        # self.rowconfigure(1, weight=3)
        self.__frame_1_0 = ctk.CTkFrame(self)
        self.__frame_1_0.grid(row=1, column=0, 
                              sticky='nsew', 
                              **self.__5_padding)
        
        # # 0 1
        self.__frame_0_1 = ctk.CTkFrame(self)
        self.__frame_0_1.grid(row=0, column=1, 
                              rowspan=2, 
                              sticky='nsew', 
                              **self.__5_padding)
        
        # # 0 2
        self.__frame_0_2 = ctk.CTkFrame(self)
        self.__frame_0_2.grid(row=0, column=2,
                              rowspan=2, 
                              sticky='nsew', 
                              **self.__5_padding)
        
        # # # 1 2
        # self.__frame_1_2 = ctk.CTkFrame(self)
        # self.__frame_1_2.grid(row=1, column=2,
        #                       sticky='nsew',
        #                       **self.__5_padding)
        
        # # # GUI design
        # # Frame 0 0 - Image file input
        current_frame = self.__frame_0_0
        
        self.load_frame_tit = ctk.CTkLabel(current_frame, 
                                           text="Load Image:", 
                                           font=self.__my_font_1)
        self.load_frame_tit.pack(**self.__base_padding)
        
        self.load_path_lab = ctk.CTkLabel(current_frame, 
                                          text="File path:", 
                                          font=self.__my_font_2)
        self.load_path_lab.pack()
        
        self.load_path_name_lab = ctk.CTkLabel(current_frame, 
                                               text="No file selected")
        self.load_path_name_lab.pack()
        
        self.load_butt = ctk.CTkButton(current_frame, 
                                       text="Browse file", 
                                       width=120,
                                       command=lambda: self.upload_img())
        self.load_butt.pack(**self.__5_padding)
        
        self.img_properties_tit = ctk.CTkLabel(current_frame, 
                                               text="Image Properties:", 
                                               font=self.__my_font_1)
        self.img_properties_tit.pack(**self.__base_padding)
        
        self.img_size_tit = ctk.CTkLabel(current_frame, 
                                         text="Image width, height:", 
                                         font=self.__my_font_2)
        self.img_size_tit.pack()
        
        self.img_size_lab = ctk.CTkLabel(current_frame, 
                                         text="None x None")
        self.img_size_lab.pack()
        
        self.img_chan_tit = ctk.CTkLabel(current_frame, 
                                         text="Image channels:", 
                                         font=self.__my_font_2)
        self.img_chan_tit.pack()
        
        self.img_mode_lab = ctk.CTkLabel(current_frame, 
                                         text="None")
        self.img_mode_lab.pack()
        
        # # Frame 1 0 - Image transformation properties
        current_frame = self.__frame_1_0
        
        self.frame_1_0_tit = ctk.CTkLabel(current_frame, 
                                          text="Image export setup", 
                                          font=self.__my_font_1)
        self.frame_1_0_tit.pack(fill='x', **self.__base_padding)
        
        self.black_values_entry = EntryWidget(current_frame, 
                                              title="Range of black:",
                                              default_values=self.storage.BLACK, 
                                              button=False)
        self.black_values_entry.pack(fill='x')
        self.__entry_widgets.append(self.black_values_entry)
        
        self.grey_values_entry = EntryWidget(current_frame, 
                                             title="Range of grey:",
                                             default_values=self.storage.GREY, 
                                             button=False)
        self.grey_values_entry.pack(fill='x')
        self.__entry_widgets.append(self.grey_values_entry)
        
        self.pixel_spacing_entry = EntryWidget(current_frame, 
                                               title="Spacing between lines [mm]:",
                                               default_values=(self.storage.mm_per_px,), 
                                               button=False)
        self.pixel_spacing_entry.pack(fill='x')
        self.__entry_widgets.append(self.pixel_spacing_entry)
        
        self.paper_size_entry = EntryWidget(current_frame, 
                                            title="Paper size [mm]:",
                                            default_values=self.storage.paper_size, 
                                            button=False)
        self.paper_size_entry.pack(fill='x')
        self.__entry_widgets.append(self.paper_size_entry)
        
        # # Frame 0 1 - Rapid code names and properties
        current_frame = self.__frame_0_1
        
        self.frame_0_1_tit = ctk.CTkLabel(current_frame, 
                                          text="RAPID code setup", 
                                          font=self.__my_font_1)
        self.frame_0_1_tit.pack(fill='x', 
                                **self.__base_padding)
        
        # # Remove or modify this
        self.robot_name_entry = EntryWidget(current_frame, 
                                            title="Robot name:",
                                            default_values=(self.storage.robot_name,), 
                                            button=False)
        self.robot_name_entry.pack(fill='x')
        self.__entry_widgets.append(self.robot_name_entry)
        
        self.module_name_entry = EntryWidget(current_frame, 
                                             title="Module name:",
                                             default_values=(self.storage.module_name,),
                                             button=False)
        self.module_name_entry.pack(fill='x')
        self.__entry_widgets.append(self.module_name_entry)
        
        self.proc_name_entry = EntryWidget(current_frame, 
                                           title="Procedure name:", 
                                           default_values=(self.storage.proc_name,), 
                                           button=False)
        self.proc_name_entry.pack(fill='x')
        self.__entry_widgets.append(self.proc_name_entry)
        
        self.origin_name_entry = EntryWidget(current_frame, 
                                             title="Origin point name:",
                                             default_values=(self.storage.origin_name,), 
                                             button=False)
        self.origin_name_entry.pack(fill='x')
        self.__entry_widgets.append(self.origin_name_entry)
        
        self.origin_pos_entry = EntryWidget(current_frame, 
                                            title="Origin position [X, Y, Z]:", 
                                            default_values=self.storage.origin_pos, 
                                            button=False)
        self.origin_pos_entry.pack(fill='x')
        self.__entry_widgets.append(self.origin_pos_entry)
        
        self.tool_entry = EntryWidget(current_frame, 
                                      title="Tool name:",
                                      default_values=(self.storage.tool,), 
                                      button=False)
        self.tool_entry.pack(fill='x')
        self.__entry_widgets.append(self.tool_entry)
        
        self.speed_entry = EntryWidget(current_frame, 
                                       title="Speed [drawing, rapid]:", 
                                       default_values=self.storage.speed, 
                                       button=False)
        self.speed_entry.pack(fill='x')
        self.__entry_widgets.append(self.speed_entry)
        
        
        # # Frame 0 2 - Magic buttons frame
        current_frame = self.__frame_0_2
        
        self.frame_0_2_tit = ctk.CTkLabel(current_frame, 
                                          text="Magic Buttons", 
                                          font=self.__my_font_1)
        self.frame_0_2_tit.pack(fill='x', 
                                **self.__base_padding)
        
        # Image loaded label
        self.ready_loaded_lab = ctk.CTkLabel(current_frame,
                                             text="Image not loaded!",
                                             text_color='red',
                                             font=self.__my_font_2)
        self.ready_loaded_lab.pack(**self.__base_padding)
        
        # Process greyscale img to black and grey
        self.process_img_butt = ctk.CTkButton(current_frame,
                                              text='Process Image',
                                              width=150,
                                              command=lambda: self.process_img())
        self.process_img_butt.pack(**self.__base_padding)
        
        # Label if image is ready for rapid processing
        self.ready_process_lab = ctk.CTkLabel(current_frame,
                                              text="Image not ready!",
                                              text_color='red',
                                              font=self.__my_font_2)
        self.ready_process_lab.pack(**self.__base_padding)
        
        # preview greyscale image
        self.prev_greyscale_butt = ctk.CTkButton(current_frame,
                                                 text='Preview Greyscale',
                                                 width=150,
                                                 command=lambda: self.display_img(self.storage.img_greyscale,
                                                                                  "Greyscale"))
        self.prev_greyscale_butt.pack(**self.__base_padding)
        
        # Preview black and grey buttons
        prev_buttons = {"Preview Black": lambda: self.display_img(self.storage.img_only_black, 
                                                                  "Black"), 
                        "Preview Grey": lambda: self.display_img(self.storage.img_only_grey, 
                                                                 "Grey")}
        self.preview_clrs = ButtonsWidget(current_frame, buttons=prev_buttons)
        self.preview_clrs.pack(**self.__base_padding, fill='x')
        
        # Preview black and grey outlines buttons
        outline_buttons = {"Show Black Outline": lambda: self.display_img(self.storage.outline_black, 
                                                                          "Black Outline"), 
                           "Show Grey Outline": lambda: self.display_img(self.storage.outline_grey, 
                                                                         "Grey Outline")}
        self.preview_outlines = ButtonsWidget(current_frame, buttons=outline_buttons)
        self.preview_outlines.pack(**self.__base_padding, fill='x')
        
        # Save RAPID code
        self.save_butt = ctk.CTkButton(current_frame, 
                                         text='Save RAPID',
                                         width=150,
                                         command=lambda: self.generate_rapid(),)
        self.save_butt.pack(**self.__base_padding)
        
    
    # Private methods
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
        
        # Given frame  
        else:
            for i in range(rows):
                frame.rowconfigure(i, weight=1)
                
            for i in range(columns):
                frame.columnconfigure(i, weight=1)
    
    def __update_values(self):
        """
        Updates values from entry widgets
        """
        self.storage.BLACK = [eval(i) for i in self.black_values_entry.return_parameters()]
        self.storage.GREY = [eval(i) for i in self.grey_values_entry.return_parameters()]
        self.storage.mm_per_px = int(self.pixel_spacing_entry.return_parameters())
        self.storage.paper_size = [eval(i) for i in self.paper_size_entry.return_parameters()]
        
        self.storage.robot_name = self.robot_name_entry.return_parameters()
        self.storage.module_name = self.module_name_entry.return_parameters()
        self.storage.proc_name = self.proc_name_entry.return_parameters()
        self.storage.origin_name = self.origin_name_entry.return_parameters()
        self.storage.origin_pos = [eval(i) for i in self.origin_pos_entry.return_parameters()]
        self.storage.tool = self.tool_entry.return_parameters()
        self.storage.speed = [eval(i) for i in self.speed_entry.return_parameters()]
         
    def upload_img(self):
        """
        Uploads image
        Updates labels in GUI
        """
        
        # open dialog window
        file_types = [('PNG files', '*.png'), ('JPG files', '*.jpg, *jpeg'), ('All files', '*')]
        file_path = filedialog.askopenfilename(title='Open a file', filetypes=file_types)
    
        # handle cancel button
        if file_path == '':
            return
        
        # Get greyscaled img and its properties
        self.storage.img_greyscale, self.storage.img_path, self.storage.img_shape[:3] = func.upload_and_greyscale(file_path)
        
        # Change the 'img_path' label to the image size
        self.load_path_name_lab.configure(text=self.storage.img_path)
        
        # Change the 'img_size' label to the image size
        self.img_size_lab.configure(text=f'{self.storage.img_shape[0]} x {self.storage.img_shape[1]}')
        
        # Change the 'img_channel' label to the image mode
        self.img_mode_lab.configure(text=self.storage.img_shape[2])
        
        # update loaded image label
        self.ready_loaded_lab.configure(text="Image loaded!",
                                        text_color='green')
        self.image_loaded = True
        
        # update process ready label
        self.ready_process_lab.configure(text="Image not ready!",
                                         text_color='red')
        self.image_processed = False
        
    def process_img(self):
        """
        Processes image
        Generates black and grey masks and outlines of those masks
        """
        if not self.image_loaded:
            print("Image is not loaded!")
            return
        
        # Update values from entries
        self.__update_values()
        
        # Scale img to fir paper size
        self.storage.img_greyscale = func.scale_to_paper(self.storage.img_greyscale,
                                                         self.storage.paper_size,
                                                         self.storage.mm_per_px)
        
        # Generate black and grey masks
        self.storage.img_only_black = func.isolate_color(self.storage.img_greyscale,
                                                         self.storage.BLACK)
        
        self.storage.img_only_grey = func.isolate_color(self.storage.img_greyscale,
                                                        self.storage.GREY)
        
        # Generate black and grey outlines
        self.storage.outline_black = func.get_outline(self.storage.img_only_black, "black")
        self.storage.outline_grey = func.get_outline(self.storage.img_only_grey, "grey")
        
        # update process ready label
        self.ready_process_lab.configure(text="Image ready!",
                                         text_color='green')
        self.image_processed = True
    
    def generate_rapid(self):
        '''
        Encode outlines and then call RapidWriter class and generates the rapid code
        '''
        if not self.image_processed:
            print("Image is not ready!")
            return
        
        # update user values
        self.__update_values()
        
        # Encode outlines
        self.storage.encoded_black = func.encode_outline(self.storage.outline_black,
                                                         self.storage.mm_per_px)
        self.storage.encoded_grey = func.encode_outline(self.storage.outline_grey,
                                                        self.storage.mm_per_px,
                                                        grey=True)
        # Create RapidWriter object
        rapid = rapid_export.RapidWriter(robot_name=self.storage.robot_name,
                                         module_name=self.storage.module_name,
                                         proc_name=self.storage.proc_name,
                                         origin_name=self.storage.origin_name,
                                         origin_pos=self.storage.origin_pos,
                                         tool=self.storage.tool,
                                         speed=self.storage.speed,
                                         encoded_black=self.storage.encoded_black,
                                         encoded_grey=self.storage.encoded_grey,
                                         mm_per_px=self.storage.mm_per_px)
        # Create file dialog and write the code
        rapid.write_rapid()
                                            
    def display_img(self, image: np.ndarray, title: str):
        """
        Displays given image 
        """
        if not self.image_processed:
            print("Image is not ready!")
            return
        
        func.display_image(image, title, 500)
               

class EntryWidget(ctk.CTkFrame):
    '''
    Frame with two rows
    1st row: title
    2nd row: number of entries depending on the size of the default value tuple/list, 
             button to get/apply those entries
    '''
    def __init__(self, master: any, 
                 title: str,
                 default_values: tuple[int] | tuple[float] | tuple[str] | list[int] | list[float] | list[str],
                 button: bool = True, 
                 button_txt = 'Apply', 
                 command: any = None,
                 width: int = 200, 
                 height: int = 200, 
                 corner_radius: int | str | None = None, 
                 border_width: int | str | None = None, 
                 bg_color: str | Tuple[str, str] = "transparent", 
                 fg_color: str | Tuple[str, str] | None = None, 
                 border_color: str | Tuple[str, str] | None = None, 
                 background_corner_colors: Tuple[str | Tuple[str, str]] | None = None, 
                 overwrite_preferred_drawing_method: str | None = None, **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, 
                         bg_color, fg_color, border_color, background_corner_colors, 
                         overwrite_preferred_drawing_method, **kwargs)
        
        self.__padding = {'padx': 5, 'pady': 5}
        self.__title_font = ctk.CTkFont(weight='bold')
        
        # # Rows and columns
        self.num_entries = len(default_values)
        self.__rows_columns = (2, self.num_entries + button) # (rows, columns)
        self.__set_rows_and_columns(self.__rows_columns[0], self.__rows_columns[1])
        
        # # Title
        self.title = ctk.CTkLabel(self, 
                                  text=title, 
                                  font=self.__title_font)
        self.title.grid(row=0, column=0, 
                        columnspan=self.num_entries+1, 
                        sticky='nsew', 
                        **self.__padding)
        
        # # Variables
        self.variables: list = self.__set_variables(default_values)
        
        # # Widgets
        self.entries: list = self.__set_entries()
        
        # # Button
        if button:
            self.button = ctk.CTkButton(self, 
                                        text=button_txt, 
                                        width=80, 
                                        command=lambda: command())
            self.button.grid(row=1, column=(self.num_entries + 1), 
                             columnspan=self.num_entries, 
                             sticky='nsew', 
                             **self.__padding)
        
          
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
                
    def __set_variables(self, default_values: tuple[int, int] | tuple[float, float]):
        '''
        Sets the variables for the entries.
        '''
        tmp_variables = []
        
        for i in range(self.num_entries):
            tmp_variables.append(ctk.StringVar())
            tmp_variables[i].set(str(default_values[i]))
            
        return tmp_variables
    
    def __set_entries(self):
        '''
        Sets the entries.
        '''
        
        tmp_entries = []
        
        for i in range(self.num_entries):
            tmp_entries.append(ctk.CTkEntry(self, textvariable=self.variables[i]))
            tmp_entries[i].grid(row=1, column=i, sticky='nsew', **self.__padding)
            
        return tmp_entries
            
    def return_parameters(self):
        '''
        Returns list of values from all entries
        '''
        if self.num_entries == 1:
            return self.variables[0].get()
        
        else:
            tmp = []
            for i in range(self.num_entries):
                tmp.append(self.variables[i].get())

            return tmp


class ButtonsWidget(ctk.CTkFrame):
    '''
    Frame with one row
    1st row: number of buttons depending on the size of the {name: command} dictionary
    '''
    def __init__(self, 
                 master: any,
                 buttons: dict[str, any],
                 width: int = 200, 
                 height: int = 200, 
                 corner_radius: int | str | None = None, 
                 border_width: int | str | None = None, 
                 bg_color: str | Tuple[str, str] = "transparent", 
                 fg_color: str | Tuple[str, str] | None = None, 
                 border_color: str | Tuple[str, str] | None = None, 
                 background_corner_colors: Tuple[str | Tuple[str, str]] | None = None, 
                 overwrite_preferred_drawing_method: str | None = None, **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, 
                         bg_color, fg_color, border_color, background_corner_colors, 
                         overwrite_preferred_drawing_method, **kwargs)
        
        self.__padding = {'padx': 5, 'pady': 5}
        self.__title_font = ctk.CTkFont(weight='bold')
        
        # # Rows and columns
        self.num_buttons = len(buttons)
        self.__rows_columns = (1, self.num_buttons) # (rows, columns)
        self.__set_rows_and_columns(self.__rows_columns[0], self.__rows_columns[1])
        
        # # Buttons
        self.buttons: list = self.__set_buttons(buttons)
        
          
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
    
    def __set_buttons(self, buttons: dict[str, any]):
        '''
        Create buttons and places them in the frame.
        '''
        tmp_buttons = []
        
        for i in buttons:
            tmp = ctk.CTkButton(self,
                                width=150, 
                                text=i, 
                                command=buttons[i])            
            tmp_buttons.append(tmp)
            
        for i in tmp_buttons:
            i.grid(row=0, 
                   column=tmp_buttons.index(i),
                   **self.__padding)
            
        return tmp_buttons    
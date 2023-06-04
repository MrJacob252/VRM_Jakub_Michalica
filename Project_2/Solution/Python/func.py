import numpy as np
from tkinter import filedialog
import cv2

class Storage:
    '''
    Data storage class
    '''
    def __init__(self) -> None:
        self.img: np.ndarray = None
        self.img_path: str = None
        self.img_shape: list = [None, None, None]       # [height, width, channels]
        
        self.img_greyscale: np.ndarray = None            # grayscale image
        self.img_only_black: np.ndarray = None          # only black pixels
        self.img_only_grey: np.ndarray = None           # only grey pixels
        
        self.outline_black: np.ndarray = None           # outline of black pixels
        self.outline_grey: np.ndarray = None            # outline of grey pixels
        
        self.paper_size: list = [None, None]            # [height, width] [mm]
        self.max_size: list = [None, None]              # [height, width] [px]
        self.mm_per_px: int = 1 # mm = 1 px             # scale of image in mm per px
        # self.paper_scale_img: np.ndarray = None         # image scaled to paper size

        self.encoded_black: np.ndarray = None           # encoded outline of black pixels
        self.encoded_grey: np.ndarray = None            # encoded outline of grey pixels
        
        self.BLACK = [0, 63]                            # black color range
        self.GREY = [self.BLACK[0], 152]                # grey color range
        
        # # Parameters for rapid writer
        self.robot_name: str = None                     # name of robot
        self.module_name: str = None                    # name of module
        self.proc_name: str = None                      # name of procedure
        self.origin_name: str = None                    # name of origin
        self.origin_pos: list[int, int, int] = None     # position of origin
        self.tool: str = None                           # name of tool
        self.speed: list[int, int] = None               # speed of robot [speed, rapid_speed]
        
def upload_img(file_path):
    '''
    Opens dialog window to upload image
    Converts image to grayscale
    Updates storage
    '''
    # read image
    img = cv2.imread(file_path)
    
    # convert to grayscale
    img_greyscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # save image path
    img_path = file_path
    # save image shape
    img_shape = img.shape
    
    return (img_greyscale, img_path, img_shape)
    

def image_resize(image: np.ndarray, width = None, height = None, inter = cv2.INTER_AREA):
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

def scale_to_paper(image: np.ndarray[np.uint8], paper_size: list[int, int], mm_per_px: int):
    '''
    Scales the image to the paper size
    '''
    # print(paper_size)
    # cv2.imshow('Original', image)
    max_px_size = (int(np.floor(paper_size[0] / mm_per_px)), int(np.floor(paper_size[1] / mm_per_px))) # Width x Height [px]
    
    # Find the longest side
    w, h = image.shape[:2]
    # print(w, h)
    
    if w >= h:
        image = image_resize(image, height=max_px_size[1])
    else:
        image = image_resize(image, width=max_px_size[0])
    
    # print(image.shape)
    # cv2.imshow('Scaled to paper', image)
    
    return image
    
def isolate_color(greyscale_img: np.ndarray, color: list[int, int]):
    
    tmp_img = greyscale_img.copy()
    
    for i in range(len(tmp_img)):
            for j in range(len(tmp_img[i])):
                
                if tmp_img[i][j] >= color[0] and tmp_img[i][j] <= color[1]:
                    tmp_img[i][j] = 0
                
                else:
                    tmp_img[i][j] = 255
    
    return tmp_img

def get_outline(img: np.ndarray, color_mode: str):
    '''
    Creates outline of image
    color_mode [str]: 'black' or 'grey'
    '''
        
    # Find contours
    y_len = len(img)
    x_len = len(img[0])
    
    new_img = img.copy()
    
    match color_mode:
        case 'black':
            for i in range(y_len):
                for j in range(x_len):
                    
                    if img[i][j] == 0:
                        
                        if j == 0 or j == x_len - 1:
                            new_img[i][j] = 0

                        elif img[i][j-1] == 0 and img[i][j+1] == 0:
                            new_img[i][j] = 255
    
        case 'grey':
            for i in range(y_len):
                    for j in range(x_len):
                        
                        if img[i][j] == 0:
                            
                            if i == 0 or i == y_len - 1:
                                new_img[i][j] = 0
            
                            elif img[i-1][j] == 0 and img[i+1][j] == 0:
                                new_img[i][j] = 255
        case _:
            raise ValueError('Invalid mode')
                             
    return new_img

def encode_outline(outline: np.ndarray[np.uint8],
                         mm_per_px: int,
                         grey: bool = False):
    '''
    Generates coordinates of black pixels
    '''
    
    if grey:
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
                cords[cords_location[0]][cords_location[1]] = (j * mm_per_px) + 1
                
                cords_location[1] += 1

        cords_location[0] += 1
        cords_location[1] = 0
    
    cords = cords.T
    cords = cords[~np.all(cords == 0, axis=1)]
    cords = cords.T
    
    print(cords)
    return cords

def process_image(storage):
    pass

def display_image(image, title):
    # cv2.imshow(title, image)
    cv2.imshow(title+' resized', image_resize(image, width=500))
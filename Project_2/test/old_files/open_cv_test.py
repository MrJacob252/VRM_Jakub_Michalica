import cv2
from PIL import Image
import numpy as np

def main():
    # Read the original image
    # img = cv2.imread('vut_red.jpg')
    img = cv2.imread('color_test_png.png')  
    # Display original image
    cv2.imshow('Original', img)
    # cv2.waitKey(0)
    print(img)
    # Convert to graycsale
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Blur the image for better edge detection
    img_blur = cv2.GaussianBlur(img_gray, (3,3), 0) 
        
    # # Canny Edge Detection
    # edges = cv2.Canny(image=img_blur, threshold1=100, threshold2=200) # Canny Edge Detection
    # # Display Canny Edge Detection Image
    # cv2.imshow('Canny Edge Detection', edges)
    # cv2.imwrite('opencv_test.png', edges)
    # cv2.waitKey(0)
   
    # test = cv2.resize(img, (256, 256))
    # test = image_resize(img, width=256)
    # cv2.imshow('resize', test)
    # cv2.waitKey(0)
   
    cv2.imshow('gray', img_gray)
    cv2.waitKey(0)
   
   
   
   
   
    
    cv2.destroyAllWindows()
    
def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
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

def color_test():
    
    black = (np.uint8(255), np.uint8(200))
    grey = (np.uint8(black[1] - 1), np.uint8(90))
    white = (np.uint8(grey[1] - 1), np.uint8(0))
    
    # clr_arr = np.array([black, grey, white])
    clr_arr = np.array([[[black[0]], [black[1]]],
                        [[grey[0]], [grey[1]]],
                        [[white[0]], [white[1]]],])
    
    clr_arr = cv2.resize(clr_arr, (640, 960))
    
    print(clr_arr)
    
    cv2.imshow('clr_test', clr_arr)
    cv2.waitKey(0)
    
    cv2.destroyAllWindows()
    
    obr = cv2.imread('vut_red.jpg')
    print(type(obr))
    print(type(clr_arr))

def test_color():
    img = cv2.imread('color_test_png.png')

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = image_resize(img, width=512)
    
    cv2.imshow('test_color', img)
    
    GRAY = [0, 63]
    
    img_gray = img.copy()
    
    for i in range(len(img_gray)):
        for j in range(len(img_gray[i])):
            if img_gray[i][j] >= GRAY[0] and img_gray[i][j] <= GRAY[1]:
                img_gray[i][j] = 0
            else:
                img_gray[i][j] = 255
    
    cv2.imshow('test_gray', img_gray)
    cv2.waitKey(0)
    
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # main()
    # color_test()
    test_color()
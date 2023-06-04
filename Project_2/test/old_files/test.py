import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

"""
TODO

The picture is rotated 90 degrees for some reason, figure out why


"""

class Lines:
    def __init__(self) -> None:
        self.TAB = '    '
        self.ENTER = '\n'
    
        self.lines = {'start': 'Write to txt test'+self.ENTER,}

def test():
    img = Image.open("four_squares_png.png")
    
    data = np.asarray(img)
    print(data.shape)
    print(data)
    
    black = np.array([0, 0, 0, 255])
    print(black)
    
    pixels = 0
    
    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j].all() == black.all():
                pixels += 1
                
def test_write():
    # img = Image.open("four_squares_png.png")
    img = Image.open("test_pic_png.png")
    data = np.asarray(img)
    black = np.array([0, 0, 0, 255])
    
    lines = Lines()
    
    locations = []
    
    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j].all() == black.all():
                locations.append([i, j])
                
    with open('test_write.txt', 'w') as f:
        f.write(lines.lines['start'])
        f.write(lines.ENTER)
        f.write('The locations of the black pixels are:')
        
        for i in range(len(locations)):
            f.write(lines.TAB + str(locations[i]) + lines.ENTER)
            
        f.write(lines.ENTER + 'The number of black pixels is: ' + str(len(locations)))
        f.write(lines.ENTER)
        f.write("END OF FILE")
        
    fig, ax = plt.subplots()
    
    # ax.set_xlim(0, 32)
    # ax.set_ylim(0, 32)
    ax.set_xlim(-32, 0)
    ax.set_ylim(-32, 0)
    ax.set_aspect('equal')
    
    
    plot = ax.scatter([-i[0] for i in locations], [-i[1] for i in locations])
    plt.show()
                
if __name__ == "__main__":
    # test()
    test_write()
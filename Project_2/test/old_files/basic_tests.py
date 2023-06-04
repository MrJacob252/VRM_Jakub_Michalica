import numpy as np

def is_even(x):
    return x % 2 == 0

def black(array):
    
    h, w = array.shape

    if h >= w:
        cords = np.zeros((h,h), dtype=int)
    else:
        cords = np.zeros((w,w), dtype=int)
        

    cords_location = [0, 0]


    for i in range(h):
        for j in range(w):
            
            if is_even(array[i][j]):
                cords[cords_location[0]][cords_location[1]] = j + 1
                
                cords_location[1] += 1
                
        cords_location[0] += 1
        cords_location[1] = 0

    
    print(cords)
    
    return cords

def grey(array):
    
    array = array.T
    
    h, w = array.shape

    if h >= w:
        cords = np.zeros((h,h), dtype=int)
    else:
        cords = np.zeros((w,w), dtype=int)
        

    cords_location = [0, 0]


    for i in range(h):
        for j in range(w):
            
            if is_even(array[i][j]):
                cords[cords_location[0]][cords_location[1]] = j + 1
                
                cords_location[1] += 1
                
        cords_location[0] += 1
        cords_location[1] = 0

    
    print(cords)
    
    return cords

###############################################
     
array = np.array([[1, 2, 3],
                  [4, 5, 6], 
                  [7, 8, 9],
                  [10, 11, 12],
                  [13, 14, 15],])

print("Original array: ")
print(array)

print("Encoded array: ")
blarray = black(array)
grarray = grey(array)

blarray = blarray.T
blarray = blarray[~np.all(blarray == 0, axis=1)]
blarray = blarray.T

grarray = grarray.T
grarray = grarray[~np.all(grarray == 0, axis=1)]
grarray = grarray.T

print('Removed zero columns')
print(blarray)
print(grarray)

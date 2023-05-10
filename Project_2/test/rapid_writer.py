import numpy as np

class ScaraWriter():
    def __init__(self, module_name, proc_name,
                 speed: tuple[int, int],
                 tool,
                 paper_size:tuple[int, int],
                 origin_name: str = 'Target_drawing_origin',
                 origin_pos: tuple[int, int, int] = (290, 10, -2),
                 encoded_black = None, 
                 encoded_grey = None) -> None:
        
        '''
        speed [Tuple[int, int]]: (speed, rapid_speed)
        '''
        
        self.module_name = module_name
        self.proc_name = proc_name
        self.origin_name = origin_name
        self.origin_pos = origin_pos
        self.speed = speed
        self.tool = tool
        self.paper_size = paper_size
        self.encoded_black = encoded_black
        self.encoded_grey = encoded_grey
        
        self.TAB = '    '
        self.ENT = '\n'
        
        self.ORIGIN = f'CONST robtarget {origin_name}:=[[{origin_pos[0]},{origin_pos[1]},{origin_pos[2]}],[1,0,0,0],[0,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];'
    
    def movej(self, offs: tuple[int, int, int], speed: int) -> str:
        '''
        Creates movej command
        offs [Tuple[int, int, int]]: (x, y, z)
        '''
            
        movej = f'MoveJ Offs({self.origin_name},{offs[0]},{offs[1]},{offs[2]}),v{speed},fine,{self.tool};'
        
        return movej
        
    def movel(self, offs: tuple[int, int, int], speed: int) -> str:
        '''
        Creates movel command
        offs [Tuple[int, int, int]]: (x, y, z)
        '''
        
        movel = f'MoveL Offs({self.origin_name},{offs[0]},{offs[1]},{offs[2]}),v{speed},fine,{self.tool};'
        
        return movel
        
    
    def draw_black_proc(self, encoded_black: np.ndarray) -> str:
        '''
        Creates procedure for drawing black
        encoded [np.ndarray]: Encoded array of black outline
        '''
        
        draw_black = [
            self.movej((0, 0, 0), self.speed[1]),  # home
        ]
        
        h, w = encoded_black.shape
        
        for i in range(h):
            
            for j in range(w):
                
                if encoded_black[i][j] == 0:
                    break
                
                draw_black.append(self.movel((-(encoded_black[i][j] - 1), i, 0), self.speed[0]))
                
        draw_black = self.ENT.join(draw_black)
        
        return draw_black
        
    def draw_grey_proc(self, encoded_grey: np.ndarray) -> str:
        '''
        Creates procedure for drawing grey
        encoded [np.ndarray]: Encoded array of grey outline
        '''
        
        draw_black = [
            self.movej((0, 0, 0), self.speed[1]),  # home
        ]
        
        h, w = encoded_grey.shape
        
        for i in range(h):
            
            for j in range(w):
                
                if encoded_grey[i][j] == 0:
                    break
                
                draw_black.append(self.movel((-i, (encoded_grey[i][j] - 1), 0), self.speed[0]))
                
        draw_black = self.ENT.join(draw_black)   
        
        return draw_black
    
     
    def main_proc(self, draw_grey: str, draw_black: str) -> str:
        '''
        Creates main procedure
        draw_grey [str]: Joined string of movel commands for grey
        draw_black [str]: Joined string of movel commands for black
        '''
        
        main = [
            'PROC main()',
            self.ENT,
            '! Draw grey',
            draw_grey,
            self.ENT,
            '! Draw black',
            draw_black,
            self.ENT,
            'ENDPROC',
        ] 
        
        main = self.ENT.join(main)
        
        return main
    
    def module(self, main_proc: str) -> str:
        '''
        Creates module
        main_proc [str]: Joined string of main procedure
        '''
        
        module = [
            'MODULE '+self.module_name,
            self.TAB+self.ORIGIN,
            self.ENT,
            '! Main procedure',
            main_proc,
            self.ENT,
            'ENDMODULE',
        ]
        
        module = self.ENT.join(module)
        
        return module
    
    def write_code(self):
        '''
        Writes code to file
        '''
        
        draw_black = self.draw_black_proc(self.encoded_black)
        draw_grey = self.draw_grey_proc(self.encoded_grey)
        main_proc = self.main_proc(draw_grey, draw_black)
        module = self.module(main_proc)
        
        with open('rapid_out.txt', 'w', encoding='utf-8') as f:
            f.write(module)
    
    
def main():
    # Picture size [8x6]
    
    # values in matrices are increased by 1 to avoid 0 values if the line starts from 0
    
    # Horizontal
    encoded_black = np.array([
        [1, 11, 41, 61],
        [0, 0, 0, 0],
        [11, 41, 0, 0],
        [0, 0, 0, 0],
        [11, 41, 0, 0],
        [0, 0, 0, 0],
        [31, 51, 0, 0],
        [0, 0, 0, 0],
    ])
    
    # Vertical
    encoded_grey = np.array([
        [1, 21, 31, 41],
        [11, 51, 0, 0],
        [0, 0, 0, 0],
        [31, 41, 0, 0],
        [11, 21, 0, 0],
        [0, 11, 41, 61],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ])
    
    test = ScaraWriter('Module2', 'Calib_square2', (100, 100), 'PencilHolder\WObj:=PAPER', (380, 260), encoded_black=encoded_black, encoded_grey=encoded_grey)
    test.write_code()

if __name__ == "__main__":
    main()
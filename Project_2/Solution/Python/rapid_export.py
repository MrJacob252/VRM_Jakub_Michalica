import numpy as np
from tkinter import filedialog

class RapidWriter:
    def __init__(self, robot_name:str, module_name:str, proc_name:str,
                 origin_name:str, origin_pos:list[int, int, int], tool:str,
                 speed:list[int, int], encoded_black:np.ndarray, encoded_grey:np.ndarray, 
                 mm_per_px:int
                 ) -> None:
        
        self.robot_name = robot_name
        self.module_name = module_name
        self.proc_name = proc_name
        self.origin_name = origin_name
        self.origin_pos = origin_pos
        self.tool = tool
        self.speed = speed
        self.encoded_black = encoded_black
        self.encoded_grey = encoded_grey
        self.mm_per_px = mm_per_px
        
        self.pen_rise = -5 # mm
        
        self.TAB = '    '
        self.ENT = '\n'
        
        self.ORIGIN = f'CONST robtarget {origin_name}:=[[{origin_pos[0]},{origin_pos[1]},{origin_pos[2]}],[1,0,0,0],[0,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];'
        
    def movej(self, offs: list[int, int, int], speed: int) -> str:
        '''
        Creates movej command
        offs [list[int, int, int]]: (x, y, z)
        '''
            
        movej = f'MoveJ Offs({self.origin_name},{offs[0]},{offs[1]},{offs[2]}),v{speed},fine,{self.tool};'
        
        return movej
    
    def movel(self, offs: list[int, int, int], speed: int) -> str:
        '''
        Creates movel command
        offs [list[int, int, int]]: (x, y, z)
        '''
        
        movel = f'MoveL Offs({self.origin_name},{offs[0]},{offs[1]},{offs[2]}),v{speed},fine,{self.tool};'
        
        return movel
        
    
    def draw_black_proc(self, encoded_black: np.ndarray) -> str:
        '''
        Creates procedure for drawing black
        encoded [np.ndarray]: Encoded array of black outline
        '''
        
        draw_black = [
            self.movej((0, 0, self.pen_rise), self.speed[1]),  # home
        ]
        
        h, w = encoded_black.shape
        
        # controlls if the pen should rise or descent
        pen_up = 1
        # controlls if the TCP trace should draw or not
        should_draw = 0
        
        for i in range(h):
            
            for j in range(w):
                
                if encoded_black[i][j] == 0:
                    break
                
                
                draw_black.append(self.movel((-(encoded_black[i][j] - 1), i * self.mm_per_px, self.pen_rise * pen_up), self.speed[0]))
                draw_black.append(self.in_pos())
                
                # drawing off
                if should_draw == 1:
                    draw_black.append(self.draw_on(0))
                    draw_black.append(self.draw_off(1))
                
                # update pen_up
                pen_up = (pen_up + 1)%2
                draw_black.append(self.movel((-(encoded_black[i][j] - 1), i * self.mm_per_px, self.pen_rise * pen_up), self.speed[0]))
                draw_black.append(self.in_pos())
                
                # drawing on
                if should_draw == 0:
                    draw_black.append(self.draw_on(1))
                    draw_black.append(self.draw_off(0))
                
                # update should_draw
                should_draw = (should_draw + 1)%2
                
        # draw_black.append(self.draw_off(1))       
        # join the whole procedure to one string
        draw_black = self.ENT.join(draw_black) 
        
        return draw_black
        
    def draw_grey_proc(self, encoded_grey: np.ndarray) -> str:
        '''
        Creates procedure for drawing grey
        encoded [np.ndarray]: Encoded array of grey outline
        '''
        
        draw_grey = [
            self.movej((0, 0, self.pen_rise), self.speed[1]),  # home
        ]
        
        h, w = encoded_grey.shape
        
        # controlls if the pen should rise or descent
        pen_up = 1
        # controlls if the TCP trace should draw or not
        should_draw = 0
        
        for i in range(h):
            
            for j in range(w):
                
                if encoded_grey[i][j] == 0:
                    break
                
                draw_grey.append(self.movel((-i * self.mm_per_px, (encoded_grey[i][j] - 1), self.pen_rise * pen_up), self.speed[0]))
                draw_grey.append(self.in_pos())
                
                # drawing off
                if should_draw == 1:
                    draw_grey.append(self.draw_on(0))
                    draw_grey.append(self.draw_off(1))
                
                # update pen_up
                pen_up = (pen_up + 1)%2
                
                draw_grey.append(self.movel((-i * self.mm_per_px, (encoded_grey[i][j] - 1), self.pen_rise * pen_up), self.speed[0]))
                draw_grey.append(self.in_pos())
                
                # drawing on
                if should_draw == 0:
                    draw_grey.append(self.draw_on(1))
                    draw_grey.append(self.draw_off(0))
                
                # update should_draw
                should_draw = (should_draw + 1)%2
                
        draw_grey.append(self.draw_off(1))       
        draw_grey = self.ENT.join(draw_grey)   
        
        return draw_grey
    
     
    def main_proc(self, draw_grey: str, draw_black: str) -> str:
        '''
        Creates main procedure
        draw_grey [str]: Joined string of movel commands for grey
        draw_black [str]: Joined string of movel commands for black
        '''
        
        main = [
            'PROC main()',
            self.ENT,
            '! Clean',              # Cleans the TCP Trace lines
            self.clean(1),
            self.clean(0),
            self.draw_off(1),
            self.draw_on(0),
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
    
    def clean(self, do: int) -> str:
        '''
        Returns the Do_Clean DO
        '''
        return f'SetDO Do_Clean, {do};'
    
    def draw_off(self, do: int) -> str:
        '''
        Returns the Do_Kreslit_OFF DO
        '''
        return f'SetDO Do_Kreslit_OFF, {do};'
    
    def draw_on(self, do: int) -> str:
        '''
        Returns the Do_Kreslit_ON DO
        '''
        return f'SetDO Do_Kreslit_ON, {do};'
    
    def in_pos(self):
        '''
        Returns wait until in position command
        '''
        return "WaitRob \InPos;"
    
    def write_rapid(self):
        '''
        Create filedialog for user to choose save location
        Write the rapid code string into a .txt file
        '''
        
        draw_black = self.draw_black_proc(self.encoded_black)
        draw_grey = self.draw_grey_proc(self.encoded_grey)
        main_proc = self.main_proc(draw_grey, draw_black)
        module = self.module(main_proc)
        
        filetypes = [('Text files', '*.txt'), ('All files', '*')]
        file_path = filedialog.asksaveasfilename(title='Save file', filetypes=filetypes)
        
        if file_path == '':
            return
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(module)
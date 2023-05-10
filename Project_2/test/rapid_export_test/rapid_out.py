


def main():
    TAB = "    "
    ENTER = "\n"
    
    ORIGIN = 'CONST robtarget Target_drawing_origin:=[[290,10,-2],[1,0,0,0],[0,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];'

    MODULE_NAME = 'Module2'
    PROC_NAME = 'Calib_square2'
    
    MAIN_PROC = 'PROC main()'+ENTER+TAB+PROC_NAME+';'+ENTER+'ENDPROC'+ENTER
    
    TOOL = "PencilHolder\WObj:=PAPER"
    
    speed = 100
    width = 380
    height = 260
    
    procedure = [
        'PROC '+PROC_NAME+'()'+ENTER,
        TAB+f'MoveJ Offs(Target_drawing_origin,0,0,0),v{speed},fine,{TOOL};'+ENTER,
        TAB+f'MoveL Offs(Target_drawing_origin,0,{width},0),v{speed},fine,{TOOL};'+ENTER,
        TAB+f'MoveL Offs(Target_drawing_origin,-{height},{width},0),v{speed},fine,{TOOL};'+ENTER,
        TAB+f'MoveL Offs(Target_drawing_origin,-{height},0,0),v{speed},fine,{TOOL};'+ENTER,
        TAB+f'MoveL Offs(Target_drawing_origin,0,0,0),v{speed},fine,{TOOL};'+ENTER,
        'ENDPROC'+ENTER
    ]

    with open('rapid_out.txt', 'w', encoding='utf-8') as f:
        f.write('MODULE '+MODULE_NAME+';'+ENTER)
        f.write(ORIGIN+ENTER)
        f.write(MAIN_PROC+ENTER)
        for line in procedure:
            f.write(line)
        f.write('ENDMODULE'+ENTER)
    

if __name__ == "__main__":
    main()
MODULE Module2;
CONST robtarget Target_drawing_origin:=[[290,10,-2],[1,0,0,0],[0,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
PROC main()
    Calib_square;
ENDPROC

PROC Calib_square()    MoveJ Offs(Target_drawing_origin,0,0,0),v100,fine,tool0;
    MoveL Offs(Target_drawing_origin,0,380,0),v100,fine,tool0;
    MoveL Offs(Target_drawing_origin,-260,380,0),v100,fine,tool0;
    MoveL Offs(Target_drawing_origin,-260,0,0),v100,fine,tool0;
    MoveL Offs(Target_drawing_origin,0,0,0),v100,fine,tool0;
ENDPROC
ENDMODULE

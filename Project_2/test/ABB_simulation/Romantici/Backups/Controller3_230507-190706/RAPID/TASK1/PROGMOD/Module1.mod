MODULE Module1
    CONST robtarget Target_10:=[[30,100,0],[1,0,0,0],[0,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_20:=[[300,100,0],[1,0,0,0],[0,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_30:=[[300,200,0],[1,0,0,0],[0,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_40:=[[200,200,0],[1,0,0,0],[0,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_50:=[[200,100,0],[1,0,0,0],[0,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_60:=[[30,200,0],[1,0,0,0],[0,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_drawing_origin:=[[290,10,-2],[1,0,0,0],[0,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
!***********************************************************
    !
    ! Module:  Module1
    !
    ! Description:
    !   <Insert description here>
    !
    ! Author: jurdo
    !
    ! Version: 1.0
    !
    !***********************************************************
    
    
    !***********************************************************
    !
    ! Procedure main
    !
    !   This is the entry point of your program
    !
    !***********************************************************
    PROC main()
        
        Calib_square;
        
    ENDPROC
    PROC Path_10()
        MoveL Target_10,v1000,z0,PencilHolder\WObj:=PAPER;
        MoveL Target_20,v1000,z0,PencilHolder\WObj:=PAPER;
        MoveL Target_30,v1000,z0,PencilHolder\WObj:=PAPER;
        MoveL Target_40,v1000,z0,PencilHolder\WObj:=PAPER;
        MoveL Target_50,v1000,z0,PencilHolder\WObj:=PAPER;
        MoveL Target_60,v1000,z0,PencilHolder\WObj:=PAPER;
    ENDPROC
    
    PROC Calib_square()
        VAR num width := 380;
        VAR num height := 260;
        
        MoveJ Offs(Target_drawing_origin,0,0,0),v100,fine,PencilHolder\WObj:=PAPER;
        
        MoveL Offs(Target_drawing_origin,0,width,0),v100,fine,PencilHolder\WObj:=PAPER;
        
        MoveL Offs(Target_drawing_origin,-height,width,0),v100,fine,PencilHolder\WObj:=PAPER;
        
        MoveL Offs(Target_drawing_origin,-height,0,0),v100,fine,PencilHolder\WObj:=PAPER;
        
        MoveL Offs(Target_drawing_origin,0,0,0),v100,fine,PencilHolder\WObj:=PAPER;
    
    ENDPROC
ENDMODULE
MODULE Module1
    CONST robtarget Target_10:=[[30,100,-5],[1,0,0,0],[0,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_20:=[[300,100,-5],[1,0,0,0],[0,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_30:=[[300,200,-5],[1,0,0,0],[0,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_40:=[[200,200,-5],[1,0,0,0],[0,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_50:=[[200,100,-5],[1,0,0,0],[0,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_60:=[[30,200,-5],[1,0,0,0],[0,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
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
        !Add your code here
    ENDPROC
    PROC Path_10()
        MoveL Target_10,v100,z0,PencilHolder\WObj:=PAPER;
        MoveL Target_20,v100,z0,PencilHolder\WObj:=PAPER;
        MoveL Target_30,v100,z0,PencilHolder\WObj:=PAPER;
        MoveL Target_40,v100,z0,PencilHolder\WObj:=PAPER;
        MoveL Target_50,v100,z0,PencilHolder\WObj:=PAPER;
        MoveL Target_60,v100,z0,PencilHolder\WObj:=PAPER;
    ENDPROC
ENDMODULE
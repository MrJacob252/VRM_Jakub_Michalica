MODULE Module1
    CONST robtarget Target_10:=[[30,100,-3],[1,0,0,0],[0,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_20:=[[300,100,-3],[1,0,0,0],[0,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_30:=[[300,200,-3],[1,0,0,0],[0,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_40:=[[200,200,-3],[1,0,0,0],[0,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_50:=[[200,100,-3],[1,0,0,0],[0,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_60:=[[30,200,-3],[1,0,0,0],[0,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget T_Home:=[[110.671383078,70.744658199,-55.557174295],[0.859242955,0,0,-0.511567732],[-1,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
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
        SetDO Do_Clean,0;
        SetDO Do_Kreslit_OFF,1;
        SetDO Do_Kreslit_ON,0;
        
        MoveL T_Home,v100,z0,PencilHolder\WObj:=PAPER;
        SetDO Do_Kreslit_OFF,0;
        MoveL offs(Target_10,0,0,-15),v100,z0,PencilHolder\WObj:=PAPER;
        MoveL Target_10,v100,fine,PencilHolder\WObj:=PAPER;
        WaitRob \InPos;
        SetDO Do_Kreslit_ON,1;
        MoveL Target_20,v100,z0,PencilHolder\WObj:=PAPER;
        MoveL Target_30,v100,z0,PencilHolder\WObj:=PAPER;
        MoveL Target_40,v100,z0,PencilHolder\WObj:=PAPER;
        MoveL Target_50,v100,z0,PencilHolder\WObj:=PAPER;
        MoveL Target_60,v100,z0,PencilHolder\WObj:=PAPER;
        WaitTime 0.5;
        SetDO Do_Kreslit_ON,0;
        SetDO Do_Kreslit_OFF,1;
        MoveL T_Home,v100,z0,PencilHolder\WObj:=PAPER;
        
        Waittime 1;
        SetDO Do_Clean,1;
      
    ENDPROC
    PROC Path_10()
        MoveL offs(Target_10,0,0,-15),v100,z0,PencilHolder\WObj:=PAPER;
        MoveL Target_10,v100,z0,PencilHolder\WObj:=PAPER;
        MoveL Target_20,v100,z0,PencilHolder\WObj:=PAPER;
        MoveL Target_30,v100,z0,PencilHolder\WObj:=PAPER;
        MoveL Target_40,v100,z0,PencilHolder\WObj:=PAPER;
        MoveL Target_50,v100,z0,PencilHolder\WObj:=PAPER;
        MoveL Target_60,v100,z0,PencilHolder\WObj:=PAPER;
        MoveL offs(Target_60,0,0,-50),v100,z0,PencilHolder\WObj:=PAPER;
        
    ENDPROC
    PROC NO_SCAN()
        MoveJ Target_10,v1000,z100,PencilHolder\WObj:=PAPER;
        MoveJ Target_20,v1000,z100,PencilHolder\WObj:=PAPER;
        MoveJ Target_30,v1000,z100,PencilHolder\WObj:=PAPER;
        MoveJ Target_40,v1000,z100,PencilHolder\WObj:=PAPER;
        MoveJ Target_50,v1000,z100,PencilHolder\WObj:=PAPER;
        MoveJ Target_60,v1000,z100,PencilHolder\WObj:=PAPER;
        MoveJ T_Home,v1000,z100,PencilHolder\WObj:=PAPER;
    ENDPROC
ENDMODULE
MODULE Module1
        CONST robtarget Target_home:=[[302.008,0,443.82],[0,1,0,0],[0,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_start:=[[-45.133,348.327,80.118],[0,1,0,0],[0,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_convStart:=[[236.852,345.386,135.118],[0,1,0,0],[0,0,-2,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_convEnd:=[[236.852,-254.614,135.118],[0,1,0,0],[-1,0,-3,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
!***********************************************************
!***********************************************************
    PROC main()
        ! Reset enviroment
        reset_env;
        
        ! Move to starting point
        MoveJ Offs(Target_start, 0, 0, 100),v200,z100,Servo;
        MoveL Target_start, v100, fine, Servo;
        PulseDO DO_CLOSE_GRIP;
        PulseDO DO_ATTACH_OBJ;
        WaitTime 1;
        MoveL Offs(Target_start, 0, 0, 100),v100,z100,Servo;
        
        ! Place on conveyer
        MoveL Offs(Target_convStart, 0, 0, 100),v200,z100,Servo;
        MoveL Target_convStart, v100, fine, Servo;
        PulseDO DO_OPEN_GRIP;
        PulseDO DO_DETACH_OBJ;
        waitTime 1;
        MoveL Offs(Target_convStart, 0, 0, 100),v100,z100,Servo;
        
        ! Move to the conveyor end and start conveyor
        SetDO DO_CONV_MOVE, 1;
        MoveJ Offs(Target_convEnd, 0, 0, 100), v200, fine, Servo;
        ! I've chosen a fine zone here because if I'd use any zone, I'd get "50024 - Corner Path failiure" warning
        ! According to RobotStudio forums that happens because I had zone right before wait function
        ! Wait for sensor
        WaitDI DI_CONV_SENS, 1;
        SetDO DO_CONV_MOVE, 0;
        
        ! Pick at the conveyor end
        MoveL Target_convEnd, v100, fine, Servo;
        PulseDO DO_CLOSE_GRIP;
        PulseDO DO_ATTACH_OBJ;
        WaitTime 1;
        MoveL Offs(Target_convEnd, 0, 0, 100), v100, z100, Servo;
        
        ! Move to the start
        MoveJ Offs(Target_start, 0, 0, 100), v200, z100, Servo;
        MoveL Target_start, v100, fine, Servo;
        PulseDO DO_OPEN_GRIP;
        PulseDO DO_DETACH_OBJ;
        WaitTime 1;
        MoveL Offs(Target_start, 0, 0, 100), v100, z100, Servo;
        
        ! Move back home
        MoveJ Target_home, v200, fine, Servo;
    ENDPROC
    
    
    PROC reset_env()
        PulseDO DO_DETACH_OBJ;
        PulseDO DO_OPEN_GRIP;
        PulseDO DO_RESET_ENV;
        SetDO DO_CONV_MOVE, 0;
        MoveJ Target_home,v200,fine,Servo;
    ENDPROC
    
    PROC Path()
        MoveJ Target_home,v100,fine,Servo\WObj:=wobj0;
        MoveJ Target_start,v100,fine,Servo\WObj:=wobj0;
        MoveL Target_convStart,v100,fine,Servo\WObj:=wobj0;
        MoveJ Target_home,v100,fine,Servo\WObj:=wobj0;
        MoveJ Target_convEnd,v100,fine,Servo\WObj:=wobj0;
        MoveJ Target_home,v100,fine,Servo\WObj:=wobj0;
        MoveJ Target_start,v100,fine,Servo\WObj:=wobj0;
    ENDPROC
ENDMODULE
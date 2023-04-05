MODULE Module1
    ! Structure for storeing parameters
    RECORD robot_struct
        num state;
        speeddata speed;
        zonedata zone;
        num offset;
        num wait_time;
    ENDRECORD
    
    
    CONST robtarget target_50_plate_conv_end:=[[362.326,-2630.49,182.325],[0,0.707106781,0.707106781,0],[0,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget target_01_home_robot_2:=[[451,-3204.758,692.9],[0,0,1,0],[-1,0,-1,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget target_60_plate_box:=[[662.326,-3241.69,73.485],[0,0.707106781,0.707106781,0],[-1,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget target_70_lid_open:=[[491.903,-3701.034,12.306],[0,0,1,0],[-1,-3,2,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget target_80_lid_closed:=[[660.78,-3241.145,92.981],[0,0,1,0],[-1,-3,2,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];

    
    VAR robot_struct r_params;
    
    
    PROC main()
            TEST r_params.state
                CASE 0:
                    !  ######### INITIALIZATION
                    ! Init parameters
                    INIT_PARAMS;
                    ! Reset enviroment
                    RESET_ENV;
                    ! Robot is ready 
                    SetDO DO_ROBOT_2_RDY, 1;
                    ! Wait for the first robot
                    WaitDO DO_ROBOT_1_RDY, 1;
                    ! Change state -> wait for the conveyor
                    r_params.state := 10;
                CASE 10:
                    ! ######### WAIT FOR THE CONVEYOR         
                    ! Wait for the sensor input
                    WaitDI DI_CONV_SENSE, 1;
                    ! Stop conveyor
                    SetDO DO_CONV_MOVE, 0;
                    ! Change state -> move plate to the box
                    r_params.state := 20;
                CASE 20:
                    ! ######### MOVE PLATE TO THE BOX
                    ! Pick the plate
                    MoveL Offs(target_50_plate_conv_end, 0, 0, r_params.offset),r_params.speed,r_params.zone,Servo;
                    MoveL target_50_plate_conv_end, r_params.speed, fine, Servo;
                    PulseDO DO_CLOSE_GRIP_2;
                    PulseDO DO_ATTACH_PLATE_END;
                    WaitTime r_params.wait_time;
                    MoveL Offs(target_50_plate_conv_end, 0, 0, r_params.offset),r_params.speed,r_params.zone,Servo;
                    ! Place the plate
                    MoveL Offs(target_60_plate_box, 0, 0, 200),r_params.speed,r_params.zone,Servo;
                    MoveL target_60_plate_box, r_params.speed, fine, Servo;
                    PulseDO DO_OPEN_GRIP_2;
                    PulseDO DO_DETACH_PLATE;
                    WaitTime r_params.wait_time;
                    MoveL Offs(target_60_plate_box, 0, 0, r_params.offset),r_params.speed,r_params.zone,Servo;
                    ! Change state -> close box
                    r_params.state := 30;
                CASE 30:
                    ! ######### CLOSE BOX
                    ! Pick the lid
                    MoveL Offs(target_70_lid_open, 0, 0, r_params.offset),r_params.speed,r_params.zone,VaccumOne;
                    MoveL target_70_lid_open, r_params.speed, fine, VaccumOne;
                    PulseDO DO_ATTACH_LID;
                    WaitTime r_params.wait_time;
                    MoveL Offs(target_70_lid_open, 0, 0, r_params.offset),r_params.speed,r_params.zone,VaccumOne;
                    ! Close the box
                    MoveL Offs(target_80_lid_closed, 0, 0, r_params.offset),r_params.speed,r_params.zone,VaccumOne;
                    MoveL target_80_lid_closed, r_params.speed, fine, VaccumOne;
                    PulseDO DO_DETACH_LID;
                    WaitTime r_params.wait_time;
                    MoveL Offs(target_80_lid_closed, 0, 0, r_params.offset),r_params.speed,r_params.zone,VaccumOne;
                    ! Change state -> move home
                    r_params.state := 40;
                CASE 40:
                    ! ######### MOVE HOME
                    MoveJ target_01_home_robot_2, r_params.speed, fine, Servo;
                    ! Change state -> end state
                    r_params.state := 100;
                CASE 100:
                    ! ######### END
                    Stop;
            ENDTEST
    ENDPROC
    
    PROC RESET_ENV()
        ! ########## Reset enviroment
        ! Robot ready -> false
        SetDO DO_ROBOT_2_RDY, 0;
        ! Detach everything
        PulseDO DO_DETACH_ALL;
        ! Turn off conveyor
        SetDO DO_CONV_MOVE, 0;
        ! Position everything on their starting positions
        PulseDO DO_RESET_ENV;
        ! Open gripper
        PulseDO DO_OPEN_GRIP_1;
        ! Call robot home
        MoveJ target_01_home_robot_2,v300,fine,Servo\WObj:=wobj0;
    ENDPROC

    PROC INIT_PARAMS()
        ! Set default parameters for the robot
        ! Speed
        r_params.speed := [200, 200, 200, 200];
        ! Zone
        r_params.zone := z50;
        ! Offset
        r_params.offset := 100;
        ! Wait
        r_params.wait_time := 1;
    ENDPROC
    
    PROC Path_10()
        MoveL target_50_plate_conv_end,v100,fine,Servo\WObj:=wobj0;
        MoveL target_01_home_robot_2,v100,fine,Servo\WObj:=wobj0;
        MoveL target_60_plate_box,v100,fine,Servo\WObj:=wobj0;
        MoveL target_70_lid_open,v100,fine,VaccumOne\WObj:=wobj0;
        MoveL target_80_lid_closed,v100,fine,VaccumOne\WObj:=wobj0;
    ENDPROC
ENDMODULE
MODULE Module1
    ! Structure for storeing parameters
    RECORD robot_struct
        num state;
        speeddata speed;
        zonedata zone;
        num offset;
        num wait_time;
    ENDRECORD
    
    
    CONST robtarget target_10_plate_home:=[[202.326001965,523.309968177,43.980971259],[0.000000008,0.707106791,0.707106772,-0.00000007],[0,-1,1,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget target_20_red_R:=[[657.114,272.272,27.981],[0,0.707106781,0.707106781,0],[0,-1,1,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget target_21_blue_R:=[[569.614,272.272,27.981],[0,0.707106781,0.707106781,0],[0,-1,1,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget target_22_orange_R:=[[482.114,272.272,27.981],[0,0.707106781,0.707106781,0],[0,-1,1,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget target_30_red_L:=[[657.114,-27.728,27.981],[0,0.707106781,0.707106781,0],[0,-1,1,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget target_31_blue_L:=[[569.614,-27.728,27.981],[0,0.707106781,0.707106781,0],[0,-1,1,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget target_32_orange_L:=[[482.114,-27.728,27.981],[0,0.707106781,0.707106781,0],[0,-1,1,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget target_40_plate_conv_start:=[[362.326,-621.69,182.325],[0,0.707106781,0.707106781,0],[-1,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget target_41_block_conv_start_R:=[[274.824,-621.688,166.821],[0,0.707106781,0.707106781,0],[-1,-2,1,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget target_42_block_conv_start_L:=[[449.824,-621.688,166.821],[0,0.707106781,0.707106781,0],[-1,-2,1,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget target_00_home_robot_1:=[[451.000000019,-0.000000001,692.89999999],[0,0,1,0],[-1,0,-1,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    
    
    VAR robot_struct r_params;
    
    ! #################### USER CHOICE ####################
    ! Users choice for which color to pick
    ! 0 = Orange
    ! 1 = Blue
    ! 2 = Red
    VAR num user_choice := 2;
    ! #####################################################
    
    PROC main()
            TEST r_params.state
                CASE 0:
                    ! ######### INITIALIZATION
                    ! Init parameters
                    INIT_PARAMS;
                    ! Reset enviroment
                    RESET_ENV;
                    ! Robot is ready
                    SetDO DO_ROBOT_1_RDY, 1;
                    ! Wait for second robot
                    WaitDO DO_ROBOT_2_RDY, 1;
                    ! Change state -> Move holder plate
                    r_params.state := 10;
                CASE 10:
                    ! ######### MOVE HOLDER PLATE
                    ! Pick the plate
                    MoveL Offs(target_10_plate_home, 0, 0, r_params.offset),r_params.speed,r_params.zone,Servo;
                    MoveL target_10_plate_home, r_params.speed, fine, Servo;
                    PulseDO DO_CLOSE_GRIP_1;
                    PulseDO DO_ATTACH_PLATE;
                    WaitTime r_params.wait_time;
                    MoveL Offs(target_10_plate_home, 0, 0, r_params.offset),r_params.speed,r_params.zone,Servo;
                    ! Place the plate on the conveyor
                    MoveL Offs(target_40_plate_conv_start, 0, 0, r_params.offset),r_params.speed,r_params.zone,Servo;
                    MoveL target_40_plate_conv_start, r_params.speed, fine, Servo;
                    PulseDO DO_OPEN_GRIP_1;
                    PulseDO DO_DETACH_PLATE;
                    WaitTime r_params.wait_time;
                    MoveL Offs(target_40_plate_conv_start, 0, 0, 200),r_params.speed,r_params.zone,Servo;
                    ! Change state -> move blocks to the plate
                    r_params.state := 20;
                CASE 20:
                    ! ######### MOVE CLR BLOCKS TO THE PLATE
                    TEST user_choice
                        CASE 0:
                            MOVE_ORANGE;
                        CASE 1:
                            MOVE_BLUE;
                        CASE 2:
                            MOVE_RED;
                    ENDTEST
                    ! Change state -> start conveyor
                    r_params.state := 30;
                CASE 30:
                    ! ######### START CONVEYOR
                    ! Start the conveyor
                    SetDO DO_CONV_MOVE, 1;
                    ! Change state -> move home
                    r_params.state := 40;
                CASE 40:
                    ! ######### MOVE HOME
                    MoveJ target_00_home_robot_1, r_params.speed, fine, Servo;
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
        SetDO DO_ROBOT_1_RDY, 0;
        ! Detach everything
        PulseDO DO_DETACH_ALL;
        ! Turn off conveyor
        SetDO DO_CONV_MOVE, 0;
        ! Position everything on their starting positions
        PulseDO DO_RESET_ENV;
        ! Open gripper
        PulseDO DO_OPEN_GRIP_1;
        ! Call robot home
        MoveJ target_00_home_robot_1,v300,fine,Servo\WObj:=wobj0;
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
    
    PROC MOVE_ORANGE()
        ! Pick right
        MoveL Offs(target_22_orange_R, 0, 0, r_params.offset),r_params.speed,r_params.zone,VaccumOne;
        MoveL target_22_orange_R, r_params.speed, fine, VaccumOne;
        PulseDO DO_ATTACH_ORANGE_R;
        WaitTime r_params.wait_time;
        MoveL Offs(target_22_orange_R, 0, 0, r_params.offset),r_params.speed,r_params.zone,VaccumOne;
        ! Place right
        MoveL Offs(target_41_block_conv_start_R, 0, 0, r_params.offset),r_params.speed,r_params.zone,VaccumOne;
        MoveL target_41_block_conv_start_R, r_params.speed, fine, VaccumOne;
        PulseDO DO_DETACH_ORANGE_R;
        WaitTime r_params.wait_time;
        MoveL Offs(target_41_block_conv_start_R, 0, 0, r_params.offset),r_params.speed,r_params.zone,VaccumOne;
        ! Pick left
        MoveL Offs(target_32_orange_L, 0, 0, r_params.offset),r_params.speed,r_params.zone,VaccumOne;
        MoveL target_32_orange_L, r_params.speed, fine, VaccumOne;
        PulseDO DO_ATTACH_ORANGE_L;
        WaitTime r_params.wait_time;
        MoveL Offs(target_32_orange_L, 0, 0, r_params.offset),r_params.speed,r_params.zone,VaccumOne;
        ! Place left
        MoveL Offs(target_42_block_conv_start_L, 0, 0, r_params.offset),r_params.speed,r_params.zone,VaccumOne;
        MoveL target_42_block_conv_start_L, r_params.speed, fine, VaccumOne;
        PulseDO DO_DETACH_ORANGE_L;
        WaitTime r_params.wait_time;
        PulseDO DO_ATTACH_ORANGE_TO_PLATE;
        MoveL Offs(target_42_block_conv_start_L, 0, 0, r_params.offset),r_params.speed,r_params.zone,VaccumOne;
    ENDPROC
    
    PROC MOVE_BLUE()
        ! Pick right
        MoveL Offs(target_21_blue_R, 0, 0, r_params.offset),r_params.speed,r_params.zone,VaccumOne;
        MoveL target_21_blue_R, r_params.speed, fine, VaccumOne;
        PulseDO DO_ATTACH_BLUE_R;
        WaitTime r_params.wait_time;
        MoveL Offs(target_21_blue_R, 0, 0, r_params.offset),r_params.speed,r_params.zone,VaccumOne;
        ! Place right
        MoveL Offs(target_41_block_conv_start_R, 0, 0, r_params.offset),r_params.speed,r_params.zone,VaccumOne;
        MoveL target_41_block_conv_start_R, r_params.speed, fine, VaccumOne;
        PulseDO DO_DETACH_BLUE_R;
        WaitTime r_params.wait_time;
        MoveL Offs(target_41_block_conv_start_R, 0, 0, r_params.offset),r_params.speed,r_params.zone,VaccumOne;
        ! Pick left
        MoveL Offs(target_31_blue_L, 0, 0, r_params.offset),r_params.speed,r_params.zone,VaccumOne;
        MoveL target_31_blue_L, r_params.speed, fine, VaccumOne;
        PulseDO DO_ATTACH_BLUE_L;
        WaitTime r_params.wait_time;
        MoveL Offs(target_31_blue_L, 0, 0, r_params.offset),r_params.speed,r_params.zone,VaccumOne;
        ! Place left
        MoveL Offs(target_42_block_conv_start_L, 0, 0, r_params.offset),r_params.speed,r_params.zone,VaccumOne;
        MoveL target_42_block_conv_start_L, r_params.speed, fine, VaccumOne;
        PulseDO DO_DETACH_BLUE_L;
        WaitTime r_params.wait_time;
        PulseDO DO_ATTACH_BLUE_TO_PLATE;
        MoveL Offs(target_42_block_conv_start_L, 0, 0, r_params.offset),r_params.speed,r_params.zone,VaccumOne;

    ENDPROC
    
    PROC MOVE_RED()
        ! Pick right
        MoveL Offs(target_20_red_R, 0, 0, r_params.offset),r_params.speed,r_params.zone,VaccumOne;
        MoveL target_20_red_R, r_params.speed, fine, VaccumOne;
        PulseDO DO_ATTACH_RED_R;
        WaitTime r_params.wait_time;
        MoveL Offs(target_20_red_R, 0, 0, r_params.offset),r_params.speed,r_params.zone,VaccumOne;
        ! Place right
        MoveL Offs(target_41_block_conv_start_R, 0, 0, r_params.offset),r_params.speed,r_params.zone,VaccumOne;
        MoveL target_41_block_conv_start_R, r_params.speed, fine, VaccumOne;
        PulseDO DO_DETACH_RED_R;
        WaitTime r_params.wait_time;
        MoveL Offs(target_41_block_conv_start_R, 0, 0, r_params.offset),r_params.speed,r_params.zone,VaccumOne;
        ! Pick left
        MoveL Offs(target_30_red_L, 0, 0, r_params.offset),r_params.speed,r_params.zone,VaccumOne;
        MoveL target_30_red_L, r_params.speed, fine, VaccumOne;
        PulseDO DO_ATTACH_RED_L;
        WaitTime r_params.wait_time;
        MoveL Offs(target_30_red_L, 0, 0, r_params.offset),r_params.speed,r_params.zone,VaccumOne;
        ! Place left
        MoveL Offs(target_42_block_conv_start_L, 0, 0, r_params.offset),r_params.speed,r_params.zone,VaccumOne;
        MoveL target_42_block_conv_start_L, r_params.speed, fine, VaccumOne;
        PulseDO DO_DETACH_RED_L;
        WaitTime r_params.wait_time;
        PulseDO DO_ATTACH_RED_TO_PLATE;
        MoveL Offs(target_42_block_conv_start_L, 0, 0, r_params.offset),r_params.speed,r_params.zone,VaccumOne;
    ENDPROC
    
    PROC Path_10()
        MoveL target_10_plate_home,v100,fine,Servo\WObj:=wobj0;
        MoveL target_20_red_R,v100,fine,VaccumOne\WObj:=wobj0;
        MoveL target_21_blue_R,v100,fine,VaccumOne\WObj:=wobj0;
        MoveL target_22_orange_R,v100,fine,VaccumOne\WObj:=wobj0;
        MoveL target_30_red_L,v100,fine,VaccumOne\WObj:=wobj0;
        MoveL target_31_blue_L,v100,fine,VaccumOne\WObj:=wobj0;
        MoveL target_32_orange_L,v100,fine,VaccumOne\WObj:=wobj0;
        MoveL target_40_plate_conv_start,v100,fine,Servo\WObj:=wobj0;
        MoveL target_41_block_conv_start_R,v100,fine,VaccumOne\WObj:=wobj0;
        MoveL target_42_block_conv_start_L,v100,fine,VaccumOne\WObj:=wobj0;
        MoveL target_00_home_robot_1,v100,fine,Servo\WObj:=wobj0;
    ENDPROC
ENDMODULE
#!/usr/bin/env python

# --- Import libraries

import os
import rospy

import numpy as np
import time

from std_msgs.msg import Int16MultiArray, Bool

from jonas.srv import sequence, sequenceResponse

from dynamixel_sdk import *

import copy


# ----- Serial setup

if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


# ----------- Classes

class Robot(object):

    # ------------------- Joint Variables

    qDes = np.array([2048, 2048, 2048, 2048, 2048, 2048]) # --- Desired Position [2048, 2048, 2048, 2048, 2048, 2048] [0, 0, 0, 0, 0, 0, 0]
    qAct = np.array([2048, 2048, 2048, 2048, 2048, 2048]) # --- Actual Position

    # ------------------- General Variables
    
    DXL_ID = np.array([1,2,3,4,5,6])

    DXL_status = np.array([0,0,0,0,0,0]) # --- Are they moving? Boolean

    DXL_speed = 175

    # ------------------- Server Variables

    sequence_active = False
    motors_moving = False

    order_sent = False

    sequence_start_time = 0
    sequence_time = 0

    msg_motor = Bool()

    # ------------------- Addresses

    ADDR_TORQUE_EN = 24
    ADDR_LED_EN = 25

    ADDR_GOAL_POSITION = 30
    ADDR_MOV_SPEED = 32

    ADDR_MOV_STATUS = 46

    #b_max = 1023 #10-bit Max Value

    # ------------------- General Settings

    PROT_VR = 1.0
    BRATE = 1000000
    DEVICE = '/dev/ttyUSB0'


    portHandler = PortHandler(DEVICE)
    packetHandler = PacketHandler(PROT_VR)


    def __init__(self):


        # ------------------------------------- Open port

        try:
            self.portHandler.openPort()
            print("\nSucceeded to open the port.\n")

        except:
            print("Failed to open the port.\n")
            getch()
            quit()

        # ------------------------------------- Set Baudrate

        try:
            self.portHandler.setBaudRate(self.BRATE)
            print("Baudrate changed to " + str(self.BRATE) + "\n")
        except:
            print("Failed to change the baudrate.\n")
            getch()
            quit()


        # ------------------------------------- Create subscriber

        self.jointSubscriber = rospy.Subscriber("joint_value",Int16MultiArray, self.UpdateGoal)
        
        rospy.sleep(0.005)

        # ------------------------------------- Create publisher

        self.motorPublisher = rospy.Publisher("motors_status",Bool, queue_size=10)
        
        rospy.sleep(0.005)

        # ------------------------------------- Create Server 

        self.server = rospy.Service("sequence_service", sequence, self.StartSequence)

        rospy.sleep(0.005)


        # ------------------------------------- Set up Servomotors 

        for ID in self.DXL_ID:

            # ------------------------------------- Identify

            dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, ID, self.ADDR_LED_EN, True)

            # ------------------------------------- Turn on

            dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, ID, self.ADDR_TORQUE_EN, True)

            # ------------------------------------- Speed

            dxl_comm_result, dxl_error = self.packetHandler.write2ByteTxRx(self.portHandler, ID, self.ADDR_MOV_SPEED, self.DXL_speed)
            

            # ------------------------------------- Verify errors

            if dxl_comm_result != COMM_SUCCESS:

                print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
                print("Failed setup for Motor ID: " + str(ID) + "\n")
                self.Shutdown()

            elif dxl_error != 0:

                print("%s" % self.packetHandler.getRxPacketError(dxl_error))
                print("Failed setup for Motor ID: " + str(ID) + "\n")
                self.Shutdown()

            else:

                print("Motor ID: " + str(ID) + " ready to use!\n")


    def StartSequence(self, request):

        # -------------------------- Recieves a status from client.

        if self.sequence_active == False:

            self.sequence_active = request.sequence_active
            self.sequence_start_time = rospy.get_time()
            self.order_sent = True

            return sequenceResponse(self.order_sent)

        else:

            self.order_sent = False
            return sequenceResponse(self.order_sent)


    def UpdateGoal(self,msg):

        # -------------------------- Recieved angles from subscriber

        data_array = msg.data

        if len(data_array) == len(self.DXL_ID):

            self.qDes = np.array(data_array)

        else:

            print("Invalid joint array, try again.\n")


    def SetPosition(self):

        # -------------------------- Set positions to servomotors

        for ID in self.DXL_ID:

            dxl_comm_result, dxl_error = self.packetHandler.write2ByteTxRx(self.portHandler, ID, self.ADDR_GOAL_POSITION, self.qDes[ID-1])
            #print("Goal position set to Motor ID: " + str(ID) + " to " + str(self.qDes[ID-1] * 0.088) + " degrees." + "\n")

            if dxl_comm_result != COMM_SUCCESS or dxl_error != 0:

                print("Timeout for Motor ID: " + str(ID) + "\n")
                self.Shutdown()


        #print("Joints moving, please wait." + "\n")

        rospy.sleep(0.1)


    def UpdateStatus(self):

        # -------------------------- Verifies the status for every ID

        mask = 0

        for ID in self.DXL_ID:

            status, dxl_comm_result, dxl_error = self.packetHandler.read1ByteTxRx(self.portHandler, ID, self.ADDR_MOV_STATUS)

            self.DXL_status[ID-1] = status

            mask += status

            if dxl_comm_result != COMM_SUCCESS or dxl_error != 0:
                print("Timeout for Motor ID: " + str(ID) + "\n")
                self.Shutdown()

        # -------------------------- Changes sequence status based on movement

        if mask == 0:

            self.sequence_active = False
            self.motors_moving = False

            self.sequence_time = rospy.get_time() - self.sequence_start_time

            #print("Joints awaiting a new sequence \n. Total time elapsed (s): " + str(round(self.sequence_time,2)) + "\n")

        else:

            self.motors_moving = True


        self.msg_motor.data = self.motors_moving
        self.motorPublisher.publish(self.msg_motor)


    def Shutdown(self):

        for ID in self.DXL_ID:

            # -------------------------- Turn off

            dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, ID, self.ADDR_LED_EN, False)
            dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, ID, self.ADDR_TORQUE_EN, False)

            print("Shutting down Motor ID: " + str(ID) + "\n")
        
        getch()
        quit()


def main():

    rospy.init_node("joint_node")
    freq = 10
    rate = rospy.Rate(freq)

    robot = Robot()

    while not rospy.is_shutdown():

        if robot.sequence_active == True:

            if robot.motors_moving == False:
                
                robot.SetPosition()

            robot.UpdateStatus()

        rate.sleep()

    rospy.on_shutdown(robot.Shutdown())


if __name__ == '__main__':
    main()

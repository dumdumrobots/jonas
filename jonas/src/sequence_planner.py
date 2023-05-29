#!/usr/bin/env python

# --- Import libraries

import rospy

import numpy as np
import time
import actionlib

from std_msgs.msg import Int16MultiArray, Bool, String

from jonas.srv import sequence, sequenceResponse


# ----------- Classes

class Planner(object):

    # ------------------- General Variables

    sequence_active = True

    motors_moving = False

    action_string = "Rest"

    action_active = False

    msg = Int16MultiArray()


    def __init__(self):

        # ------------------------------------- Create publisher

        self.jointPublisher = rospy.Publisher("joint_value",Int16MultiArray, queue_size=10)
        
        rospy.sleep(0.005)

        # ------------------------------------- Create subscribers

        self.motorSubscriber = rospy.Subscriber("motors_status",Bool, self.UpdateStatus)

        self.guiSubscriber = rospy.Subscriber("servos_coms_topic",String, self.SendAction)
        
        rospy.sleep(0.005)

    def SendAction(self,msg):

        # -------------------------- Recieves action string from GUI.

        self.action_string = msg.data
        self.action_active = True


    def UpdateStatus(self,msg):

        # -------------------------- Recieves a motor status from topic.

        self.motors_moving =  msg.data


    def SequenceClient(self,joint_values):

        # ------------------------------------- Publish joint values

        self.msg.data = joint_values.tolist()
        self.jointPublisher.publish(self.msg)

        rospy.wait_for_service("sequence_service")

        self.client = rospy.ServiceProxy("sequence_service", sequence)
        self.service = self.client(self.sequence_active)


def main():

    rospy.init_node("planner_node")

    print("Jonas sequence planner active.\n")

    freq = 10
    rate = rospy.Rate(freq)

    planner = Planner()

    request = "Rest"

    # -------------------------- Diferent positions for robot.

    poses = {
        "Rest"       : np.array([180, 100, 170, 180, 100, 170]),

        "Serve"      : np.array([90, 90, 180, 270, 90, 180]),

        "Show"      : np.array([0, 90, 180, 360, 90, 180]),

        "Salute 1"   : np.array([45, 100, 155, 180, 100, 170]),
        "Salute 2"   : np.array([45, 90, 155, 180, 100, 170]),

        "Walking 1"  : np.array([135, 100, 170, 135, 100, 170]),
        "Walking 2"  : np.array([225, 100, 170, 225, 100, 170]),

        "Dance 1"    : np.array([0, 105, 255, 180, 105, 255]),
        "Dance 2"    : np.array([0, 125, 235, 180, 125, 235]),

        "Hug 1"      : np.array([90, 135, 180, 270, 135, 180]),
        "Hug 2"      : np.array([90, 90, 135, 270, 90, 135]),

        "Curl 1"      : np.array([180, 125, 160, 180, 125, 160]),
        "Curl 2"      : np.array([0, 160, 90, 360, 160, 90]),

    }

    sequences = {
        "Salute"  : np.array(["Rest", "Salute 1", "Salute 2",
            "Salute 1", "Salute 2",
            "Salute 1", "Salute 2", "Rest"]),

        "Walking" : np.array(["Rest","Walking 1", "Walking 2", 
            "Walking 1", "Walking 2", 
            "Walking 1", "Walking 2", "Rest"]),

        "Dance"   : np.array(["Rest","Dance 1", "Dance 2", 
            "Dance 1", "Dance 2",
            "Dance 1", "Dance 2", 
            "Dance 1", "Dance 2", "Rest"]),

        "Hug"     : np.array(["Rest","Hug 1", "Hug 2", 
            "Hug 1", "Hug 2", 
            "Hug 1", "Hug 2", "Rest"]),

        "Curl"    : np.array(["Rest","Curl 1", "Curl 2",
            "Curl 1", "Curl 2",
            "Curl 1", "Rest"])
    }



    while not rospy.is_shutdown():

        if planner.motors_moving == False and planner.action_active == True:

            request = planner.action_string

            try: 
                order = sequences[request]
                #print("Sent activation for " + request + " sequence.\n")

                for i in order:

                    while planner.motors_moving == True:
                        pass

                    planner.SequenceClient(poses[i]/0.088)
                    
                    rospy.sleep(0.5)

            except KeyError:

                try:
                    planner.SequenceClient(poses[request]/0.088)
                    #print("Sent activation for " + request + " pose.\n")
                    rospy.sleep(0.5)

                except KeyError:
                    pass
                    #print("Neither pose nor sequence exists with name " + request + ", try again.\n")

            
            planner.action_active = False


                
                


        rate.sleep()

if __name__ == '__main__':
    main()
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import rospy
from os.path import expanduser


from std_msgs.msg import Int8
from std_msgs.msg import String
from PyQt5 import QtCore, QtGui, QtWidgets

home = expanduser("~")

main_path = home + '/jonas_ws/src/jonas_hybridrobot/interface_rpi/src/faces/'


blink_count = 5
heart_count = 25
fire_count = 23 
music_count = 33
smile_count = 7

def callback_face(data,self):
    print(data.data)
    self.image_label = data.data


class App(QtWidgets.QWidget):
    def __init__(self):
        super(App,self).__init__()
        # Initialize variables
        self.title = 'My Screen'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.image_label = 'blink'
        self.image_paths = []
        self.current_image = 1


        self.images_counts = 0
        self.flag_loop = False

        # ROS Variables 
        rospy.init_node('node_interface')
        self.pub_face = rospy.Subscriber('face_coms_topic',String,callback_face,(self))


        # Construct GUI
        self.initUI()
        
        

    def initUI(self):
        # print(path_of_image)
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.label = QtWidgets.QLabel(self)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_image)
        timer.start(100)
        # self.showFullScreen()
        self.update_image()
        

    def update_image(self):

        if self.flag_loop:
            final_path = self.image_paths + '_' + str(self.current_image) + '.png'



        else: 
            # Create map of string with direction
            if self.image_label == 'blink':
                self.images_counts = blink_count
            elif self.image_label == 'fire':
                self.images_counts = fire_count
            elif self.image_label == 'heart':
                self.images_counts = heart_count
            elif self.image_label == 'music':
                self.images_counts = music_count
            elif self.image_label == 'smile':
                self.images_counts = smile_count

            flag_loop = True

            self.image_paths = main_path + self.image_label + '/' + self.image_label 


            final_path = self.image_paths + '_' + str(self.current_image) + '.png'
            print(final_path)

        
        if self.current_image > self.images_counts:
            if self.image_label != 'blink':
                self.image_label = 'blink'
                self.images_counts = blink_count
            
            self.current_image = 1
        
        pixmap = QtGui.QPixmap(final_path)
        if not pixmap.isNull():
            self.label.setPixmap(pixmap)
            self.label.adjustSize()
            self.resize(pixmap.size())
            self.current_image += 1


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
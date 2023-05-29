#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import numpy as np
import serial
import time

#Dimensiones del robot
l = 0.18 #Distancia del centro a cada rueda
r = 0.1524 #Radio de las ruedas

#Velocidad máxima de las ruedas (rad/s)
vw_max = 8.5

#Iniciar comunicación serial con los arduinos
# arduino1 = serial.Serial('/dev/ttyUSB0',9600)
# arduino2 = serial.Serial('/dev/ttyUSB1',9600)
# arduino3 = serial.Serial('/dev/ttyUSB2',9600) 
# time.sleep(2)

#Limitar velocidad de las ruedas	
def lim_wheels_speed(wheels_des_speed):

	w_lim = np.array([-vw_max, vw_max])

	for i in range(3):
		
		if wheels_des_speed[i] < w_lim[0]:
		    wheels_des_speed[i] = w_lim[0]

		elif wheels_des_speed[i] > w_lim[1]: 
		    wheels_des_speed[i] = w_lim[1]

		else:
		    wheels_des_speed[i] = wheels_des_speed[i]

	return wheels_des_speed

#Cinematica directa
def fkine(vel_wheels):
	
	vx = (math.sqrt(3)*r*(-vel_wheels[0]+vel_wheels[1]))/3
	vy = (r*(-vel_wheels[0]-vel_wheels[1]+2*vel_wheels[2]))/3
	w = -(r*(vel_wheels[0]+vel_wheels[1]+vel_wheels[2]))/(3*l)
	
	vel_robot = np.array([vx,vy,w])
	
	return vel_robot
	
#Cinematica inversa
def ikine(vel_robot):
	
	vw1 = -(math.sqrt(3)*vel_robot[0]+vel_robot[1]+2*vel_robot[2]*l)/(2*r)
	vw2 = (math.sqrt(3)*vel_robot[0]-vel_robot[1]-2*vel_robot[2]*l)/(2*r)
	vw3 = (vel_robot[1]-vel_robot[2]*l)/r
	
	vel_wheels = np.array([vw1,vw2,vw3])
	
	return vel_wheels
	
#Enviar velocidades angulares al arduino
def send_vel_robot(vx,vy,w):

	vel_robot = np.array([vx,vy,w])
	vel_wheels = ikine(vel_robot)
	vel_wheels = lim_wheels_speed(vel_wheels)
	vel_wheels = np.round(vel_wheels,4)
	#print(vel_wheels)
	
	# arduino1.write(str(vel_wheels[0]).encode())
	# arduino2.write(str(vel_wheels[1]).encode())
	# arduino3.write(str(vel_wheels[2]).encode())
	
#Velocidades maximas del robot
vx_max = fkine(np.array([-vw_max,vw_max,0]))[0] #m/s            [-w   w     0]
vy_max = fkine(np.array([-vw_max/2,-vw_max/2,vw_max]))[1] #m/s  [-w/2 -w/2  w]
w_max = fkine(np.array([-vw_max,-vw_max,-vw_max]))[2]  #rad/s   [-w   -w   -w]
vxy_max = (vw_max*2*r)/(1+math.sqrt(3))

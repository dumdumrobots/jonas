# Jonas the Robot 🤖
Jonas is a hybrid robot developed by the Mechatronics and Robotics Laboratory at UTEC for research and display purposes. Inside this repo, we are sharing the files necessary to enable the main features of Jonas, which include: 

- It can move freely in a 2D terrain due to its three-wheel omnidirectional configuration. 
- It can follow arm movement sequences to salute, give hugs, and dance, among other actions.
- It can be controlled remotely from a PC, as currently, it's not autonomous.  

## Environment and Dependencies

Jonas has a Raspberry Pi 3 B+ with Ubuntu MATE 18.04 as a main computer, with ROS Melodic installed. It depends on the [Dynamixel SDK](https://github.com/ROBOTIS-GIT/DynamixelSDK) and PyQt5. However, both dependencies can also be used in a newer version of ROS. Also, to control Jonas remotely, it's important to have a computer with Ubuntu 18.04 with ROS Melodic installed. 

## Setting Up Jonas

### Power

Jonas has two power supplies:
- A 5V USB power bank connected to the RPI. 
- A 11.1V LiPO battery connected to the actuators.

Both batteries need to be correctly charged before using Jonas. 

### Bring Up
Jonas needs to be booted up using the following command lines:

On remote PC \
`roslaunch jonas remote_pc.launch`

On Jonas \
`roslaunch jonas jonas.launch`

⚠️ *SSH cannot be used due to the graphic interface library. We are currently finding a way to bring up all files of Jonas by powering it on.*

### Remote Control

*Working on this README!*

Our friendly robot could not be possible without the work and support of the following:
- Raúl Escandon (elmer.escandon@utec.edu.pe)
- Ricardo Terreros (ricardo.terreros@utec.edu.pe)
- Sergio Morales (sergio.morales@utec.edu.pe)
- Diego Palma (diego.palma@utec.edu.pe)
- Del Piero Flores (delpiero.flores@utec.edu.pe)
- Claudia Castañeda (claudia.castaneda@utec.edu.pe)
- Joaquín Cornejo (joaquin.cornejo@utec.edu.pe)

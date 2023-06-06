# Jonas the Robot 🤖
Jonas is a hybrid robot developed by the Mechatronics and Robotics Laboratory at UTEC for research and display purposes. Inside this repo, we are sharing the files necessary to enable the main features of Jonas, which include: 

- It can move freely in a 2D terrain due to its three-wheel omnidirectional configuration. 
- It can follow arm movement sequences to salute, give hugs, and dance, among other actions.
- It can be controlled remotely from a PC, as currently, it's not autonomous.  


## Environment and Dependencies

Jonas has a Raspberry Pi 3 B+ with Ubuntu MATE 18.04 as a main computer, with ROS Melodic installed. It depends on the [Dynamixel SDK](https://github.com/ROBOTIS-GIT/DynamixelSDK) and PyQt5. However, both dependencies can also be used in a newer version of ROS. Also, to control Jonas remotely, it's important to have a computer with Ubuntu 18.04 or 20.04 with [ROS Melodic](http://wiki.ros.org/melodic/Installation/Ubuntu) or [ROS Noetic](http://wiki.ros.org/melodic/Installation/Ubuntu) installed. 


## Setting Up Jonas

Before working with Jonas, it's important to set it up following the next sections related to power, network settings and bring up launch files. 

### Power

Jonas has two power supplies:
- A 5V USB power bank connected to the RPI. 
- A 11.1V LiPO battery connected to the actuators.

Both batteries need to be fully charged and connected before using Jonas. Also, it has two switches on the base for controlling the supply of both arms (left switch) and mobile base motors (right switch). We recommend to turn the switches moments before running the launch files to save energy. 


### Network

The ROS TCP/IP communication settings are easy to set up; however, they should be done with attention to detail as any misplaced number could throw undesired errors. Here are the necessary steps: 

1. Retrieve the IPs corresponding to Jonas and the remote PC by using the `ifconfig` command line. For convenience purposes, from now on we are using the substitutes `<JONAS_IP>` and `<REMOTE_PC_IP>`. 
> ⚠️ NAT addresses or similar cannot be used in ROS, as it requires the network to have bi-directional connectivity and a name that every machine can resolve. In other words, Jonas can only be used if it is connected to mobile hotspots, local routers, or similar.  

3. Open the `.bashrc` script with the text editor of your preference in the default terminal directory and add the following text lines on the bottom:

Add this line to `.bashrc` inside Remote PC. \
`export ROS_MASTER_URI=http:/<REMOTE_PC_IP>:11311
export ROS_HOSTNAME=<REMOTE_PC_IP>`

Add this line to `bashrc` inside Jonas.\
`export ROS_MASTER_URI=http:/<REMOTE_PC>:11311
export ROS_HOSTNAME=<JONASC_IP>`


### Bring Up
Jonas needs to be booted up using the following command lines:

Run this command in Remote PC.\
`roslaunch jonas remote_pc.launch`

Run this command in Jonas.\
`roslaunch jonas jonas.launch`

> ⚠️ *SSH cannot be used due to the graphic interface library. We are currently finding a way to bring up all files of Jonas by powering it on.*

### Remote Control

To control the movement of Jonas, the team developed a UI with all the basic functionalities of Jonas. Here is a screenshot of it.

<img src="https://github.com/dumdumrobots/jonas/assets/77807539/c73df4a1-feee-4b7c-9d32-911ad46a58f6" width="500" height="350"> <br />

The arms sequences are controlled by the buttons on the right side. There are a total of five sequences: 

1. Salute 👋
2. Curl 💪
3. Hug 💞
4. Dance 🎶
5. Serve 🆘
 
On the other hand, the mobile base is controlled by the remaining buttons. By pressing them, Jonas will follow that direction. The velocity of Jonas is controlled by the top-left slider, and its numeric value is displayed next to the `START` button. 

> We recommend keeping Jonas inside the 10-20u velocity range, as greater velocities can cause him to tumble on braking. 

> The control interface is a work in progress!

*Working on this README!*

Our friendly robot could not be possible without the work and support of the following:
- Raúl Escandon (elmer.escandon@utec.edu.pe)
- Ricardo Terreros (ricardo.terreros@utec.edu.pe)
- Sergio Morales (sergio.morales@utec.edu.pe)
- Diego Palma (diego.palma@utec.edu.pe)
- Del Piero Flores (delpiero.flores@utec.edu.pe)
- Claudia Castañeda (claudia.castaneda@utec.edu.pe)
- Joaquín Cornejo (joaquin.cornejo@utec.edu.pe)

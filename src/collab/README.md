# MSc-S2-Autonomous-Systems-Perception-ROS - collab

Package with launch files to start multiple robots at once and establish communication between them via TCP.

## Clone:
This shell script copies the files of this package to your PC and removes the repository later.
Be in Working Dir: ``~/catkin_ws/src``
```shell
mkdir collab
mkdir MSc-S2-Autonomous-Systems-Perception-ROS
git clone https://github.com/jan222ik/MSc-S2-Autonomous-Systems-Perception-ROS --no-checkout MSc-S2-Autonomous-Systems-Perception-ROS --depth 1
cd MSc-S2-Autonomous-Systems-Perception-ROS
git sparse-checkout init --cone
git sparse-checkout set src/collab
cp -R src/collab/* ../collab
cd ..
rm -rf MSc-S2-Autonomous-Systems-Perception-ROS
```

## Launch Files

### 1. Environment - emptyWorld.launch
Loads an empty world inside Gazebo.

### 2. Robot - single.launch
Launch file for a single robot. 
It spawns the robot and creates a TCP-ClientServer node for communication.
It takes arguments for the robot:
  - robot_name: Name of the robot
  - init_pose: Initial Pose in shape ``"-x -1 -y 1 -z 0"``
  - model: Name of turtlebot
  - tcpFlag: Determines if the robot is a tcp server or a tcp client.
The launch file also expects the param robot_description to be set.

### 3. Two Robots combined - multi.launch
Starts two robots in different namespaces, defines args and params required by single.launch and stats
a terminal with a teleop node for each of the turtles.

**⚠ WARNING - Teleop Terminal**: The used terminal is started with ``gnome-terminal -e``; thus the executing
system must have this terminal available.

```shell
roslaunch collab multi.launch

```

## TCP Node - tcpCommunication.py

Handles TCP communication the node can instantiate either a server, or a client based on the provided
flag. 
Due to the asynchronous nature of the environment a connection on the first try is unlikely or at least not expected.
Hence, the client will retry the connection after a short delay. The client will retry up to 10 times before
forfeiting.

The robots will print each other linear x and angular z velocities in the console after they are successfully connected.




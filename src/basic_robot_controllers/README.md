# MSc-S2-Autonomous-Systems-Perception-ROS - basic_robot_controllers

Package with first controllers utilizing sensors and motors.

## Clone:
This shell script copies the files of this package to your PC and removes the repository later.
Be in Working Dir: ``~/catkin_ws/src``
```shell
mkdir basic_robot_controllers
mkdir MSc-S2-Autonomous-Systems-Perception-ROS
git clone https://github.com/jan222ik/MSc-S2-Autonomous-Systems-Perception-ROS --no-checkout MSc-S2-Autonomous-Systems-Perception-ROS --depth 1
cd MSc-S2-Autonomous-Systems-Perception-ROS
git sparse-checkout init --cone
git sparse-checkout set src/basic_robot_controllers
cp -R src/basic_robot_controllers/* ../basic_robot_controllers
cd ..
rm -rf MSc-S2-Autonomous-Systems-Perception-ROS
```

## Task 2: WallFollow.py
Simple WallFollower node. The controller will follow a wall alongside its right side.

Start:
1. World:
```shell
export TURTLEBOT3_MODEL=burger
export SVGA_VGPU10=0
roslaunch turtlebot3_gazebo turtlebot3_stage_1.launch
```
2. WallFollow.py node
```shell
export TURTLEBOT3_MODEL=burger
export SVGA_VGPU10=0
rosrun basic_robot_controllers WallFollow.py
```

## Task 3: DriveToNearestObstacle.py
Simple DriveToNearestObstacle node. The controller will turn until it faces the closest obstacle, then drive towards it.
To determine the direction to go the LaserScan sensor is used, the index of the largest value of the array can 
be used directly as the angle towards the nearest obstacle.

The launch file ``driveTowards.launch`` can be used to start the world ``world_with_obstacle.world`` which contains
an obstacle and a roboter.

Start:
1. World:
```shell
export TURTLEBOT3_MODEL=burger
export SVGA_VGPU10=0
roslaunch basic_robot_controllers driveTowards.launch
```
2. DriveToNearestObstacle.py node
```shell
export TURTLEBOT3_MODEL=burger
export SVGA_VGPU10=0
rosrun basic_robot_controllers DriveToNearestObstacle.py
```


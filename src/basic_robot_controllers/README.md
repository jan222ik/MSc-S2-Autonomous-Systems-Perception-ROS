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
## Exercise Image: CamVisualisation.py

Node visualises the provided raw image (Topic: "/camera/rgb/image_raw") in a window after converting
it with OpenCV via a bridge.
Two different examples are displayed. 
Firstly, the original image and secondly, a greyscale version of the image.
The node exports the images again as a message on different topics ("image_cv" and "image_cv_grey").

Start:
```shell
export SVGA_VGPU10=0
roslaunch roslaunch basic_robot_controllers imageVis.launch
```
This launch file will initiate the given example world and spawn a waffle robot.
Afterwards the camera node is started.
Finally, a controller that rotates the roboter is started. 
With the rotation enabled it is easier to assure the image is updated and all colors can be seen.

## Task 2: WallFollow\<Version>.py
Simple WallFollower node. The controller will follow a wall alongside its right side.

Both versions are limited in their capability to follow a wall like the outside of the character T.

### Version 1:
Uses different states to determine the applied twist to the robot.

### Version 2:
Uses the angle of the nearest obstacle, it will be aligned to the right of the robot.
Is more reliable than Version 1.


Start:
1. World:
```shell
export TURTLEBOT3_MODEL=burger
export SVGA_VGPU10=0
roslaunch turtlebot3_gazebo turtlebot3_stage_1.launch
```
2. WallFollow\<Version>.py node
```shell
export TURTLEBOT3_MODEL=burger
export SVGA_VGPU10=0
# Choose one of:
rosrun basic_robot_controllers WallFollowV2.py

rosrun basic_robot_controllers WallFollowV1.py
```

## Task 3: DriveToNearestObstacle.py
Simple DriveToNearestObstacle node. The controller will turn until it faces the closest obstacle, then drive towards it.
To determine the direction to go the LaserScan sensor is used, the index of the largest value of the array can 
be used directly as the angle towards the nearest obstacle.

The launch file ``driveTowards.launch`` can be used to start the world ``world_with_obstacle.world`` which contains
an obstacle and a robot.

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


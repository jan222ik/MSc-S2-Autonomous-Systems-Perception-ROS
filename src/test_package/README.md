# MSc-S2-Autonomous-Systems-Perception-ROS - test_package

Learning about ROS.

## Clone:
This shell script copies the files of this package to your PC and removes the repository later.
Be in Working Dir: ``~/catkin_ws/src``
```shell
mkdir test_package
mkdir MSc-S2-Autonomous-Systems-Perception-ROS
git clone https://github.com/jan222ik/MSc-S2-Autonomous-Systems-Perception-ROS --no-checkout MSc-S2-Autonomous-Systems-Perception-ROS --depth 1
cd MSc-S2-Autonomous-Systems-Perception-ROS
git sparse-checkout init --cone
git sparse-checkout set src/test_package
cp -R src/test_package/* ../test_package
cd ..
rm -rf MSc-S2-Autonomous-Systems-Perception-ROS
```

## Nodes:
### CollectAndAggregate.py
Subscribes to the desired topics of the turtlesim_node.
When all topics have a new value or one topic updated for the second time; the state is aggregated in a custom message and published.
(See below Messages > CustAggregatedMsg.msg)

### LoggerNode.py
Subscribes to the aggregated message topic. This node converts the message into json and prints it to the console.
This string could be appended to a sting or saved into a database.

The rate the note does this can be controlled by a Service ``LogRateService.py`` the default is 10hz.

### turtleMoverPublisher.py
Controller for the turtle from the turtlesim. The movement of the turtle is achieved by modifying the twist of the turtle via the sim's ``cmd_vel`` topic

This control can be stopped and started via a Service ``StartStopService.py``. The default for the node is started.

The turtle is controlled by the values present on the parameter server.
To change the parameters use:
```shell
rosparam set twist_turtle_angular_z 10.75
```
Higher values makes turtle spin faster.
Or for the turtles speed use:
```shell
rosparam set twist_turtle_linear_x 5
```

## Messages:
### CustAggregatedMsg.msg:
Encapsulates the messages provided by the turtlesim node.
These messages are color, pose and twist.
```text
turtlesim/Color color
turtlesim/Pose pose
geometry_msgs/Twist twist
```

## How to start:
### Build:
```shell
catkin_make
```

### Launch file - all.launch:
Sets:
- param file twistTurtle.yaml

Starts:
- node ``turtlesim turtlesim_node``
- node ``test_package turtleMoverPublisher.py``
- node ``test_package CollectAndAggregate.py``
- node ``test_package LoggerNode.py``
```shell
roslaunch test_package all.launch
```

### Services:
- Start and Stop controller:
  - arg0:Int
  - Start
    ```shell
    rosrun test_package StartStopService.py 1
    ```
  - Stop
    ```shell
    rosrun test_package StartStopService.py 0
    ```

- Log rate 
  - arg0:float
  ```shell
  rosrun test_package LogRateService.py 1.0
  ```

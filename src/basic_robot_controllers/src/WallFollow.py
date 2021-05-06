#! /usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf import transformations

import math

class WallFollower:

    def __init__(self):
        rospy.init_node('WallFollower')
        self.rate = rospy.Rate(20)
        self.state = 0
        self.botVelPub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        self.laserSub = rospy.Subscriber('/scan', LaserScan, self.updateLaserData)
        self.laserData = {
            'r': 0,
            'fr': 0,
            'f': 0,
            'l': 0,
            'fl': 0
        }

    def updateLaserData(self, msg):
        self.laserData = {
            'fr': min(min(msg.ranges[30:60]), 10),
            'r': min(min(msg.ranges[61:120]), 10),
            'f': min(min(msg.ranges[330:359]), min(msg.ranges[0:30]), 10),
            'l': min(min(msg.ranges[260:299]), 10),
            'fl': min(min(msg.ranges[300:329]), 10)
        }
        print(self.laserData)

    def step(self):
        self.sensePlan()
        print("State %d" % self.state)
        twist = Twist()
        if self.state == 0:
            twist = self.findWall()
        elif self.state == 1:
            twist = self.turnLeft()
        elif self.state == 2:
            twist = self.followWall()
        elif self.state == 3:
            twist = self.turnRight()
            pass
        else:
            rospy.logerr('Unknown state!')

        self.botVelPub.publish(twist)

        self.rate.sleep()

    def sensePlan(self):
        r = self.laserData['r']
        fr = self.laserData['fr']
        f = self.laserData['f']
        l = self.laserData['l']
        fl = self.laserData['fl']

        d = 0.35
        state_description = ""

        if f < d:
            if f > r < d:
                self.state = 2
            else:
                self.state = 1
        elif fr == 10 or fr < d:
            if r < d:
                self.state = 1
            else:
                self.state  = 2
        elif r < 5 * d:
            self.state = 3
        elif f > d and fr > d and r > d:
            self.state = 0
        else:
            state_description = 'unknown case'

        print(state_description)

    def findWall(self):
        twist = Twist()
        twist.linear.x = 0.2
        return twist

    def turnLeft(self):
        twist = Twist()
        twist.angular.z = 0.2
        return twist

    def turnRight(self):
        twist = Twist()
        twist.angular.z = -0.2
        twist.linear.x = 0.2
        return twist

    def followWall(self):
        twist = Twist()
        twist.linear.x = 0.2
        twist.angular.z = -0.2
        return twist


def main():
    wall = WallFollower()
    try:
        while not rospy.is_shutdown():
            wall.step()
    except rospy.ROSInterruptException:
        pass


if __name__ == '__main__':
    main()

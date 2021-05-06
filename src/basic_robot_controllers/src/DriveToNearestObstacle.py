#! /usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist


class DriveToNearestObstacle:
    def __init__(self):
        rospy.init_node('WallFollower')
        self.rate = rospy.Rate(20)
        self.state = 0
        self.botVelPub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        self.laserSub = rospy.Subscriber('/scan', LaserScan, self.updateLaserData)
        self.laserData = 0
        self.hasReached = False

    def updateLaserData(self, msg):
        self.laserData = msg.ranges.index(min(msg.ranges))
        if msg.ranges[self.laserData] < 0.15:
            self.hasReached = True
        print(self.laserData)

    def step(self):
        twist = Twist()
        if self.hasReached:
            twist.linear.x = 0
            twist.angular.z = 0
        else:
            if self.laserData < 10 or self.laserData > 350:
                twist.linear.x = 0.3
            else:
                if self.laserData > 180:
                    twist.angular.z = -0.3
                else:
                    twist.angular.z = 0.3

        self.botVelPub.publish(twist)


def main():
    controller = DriveToNearestObstacle()
    try:
        while not rospy.is_shutdown():
            controller.step()
    except rospy.ROSInterruptException:
        pass


if __name__ == '__main__':
    main()

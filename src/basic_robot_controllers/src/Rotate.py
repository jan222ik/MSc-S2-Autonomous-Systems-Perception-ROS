#! /usr/bin/env python

import rospy
from geometry_msgs.msg import Twist


class Rotate:
    def __init__(self):
        rospy.init_node('rotate')
        self.rate = rospy.Rate(20)
        self.botVelPub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

    def step(self):
        twist = Twist()
        twist.angular.z = 0.3
        self.botVelPub.publish(twist)


def main():
    controller = Rotate()
    try:
        while not rospy.is_shutdown():
            controller.step()
    except rospy.ROSInterruptException:
        pass


if __name__ == '__main__':
    main()

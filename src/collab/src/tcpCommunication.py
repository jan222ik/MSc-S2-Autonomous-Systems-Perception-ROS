#!/usr/bin/env python

import rospy
import sys
import socket
from geometry_msgs.msg import Twist
import time


class ClientServer:
    def __init__(self, isServer, turtle):
        self.isServer = isServer
        poseTopic = rospy.get_namespace() + "cmd_vel"
        self.sub = rospy.Subscriber(poseTopic, Twist, self.nextTwist)
        rospy.logdebug("Subscribe for Pose on topic: %s" % poseTopic)
        self.sock = None
        self.latestPose = None
        self.hasConnection = False
        self.awaitRes = False

    def connect(self, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if self.isServer:
            self.sock.bind(("127.0.0.1", port))
            self.server()
        else:
            tries = 10
            while tries > 0 and not self.hasConnection:
                tries -= 1
                try:
                    self.sock.connect(("127.0.0.1", port))
                    rospy.logdebug("Client connected")
                    self.hasConnection = True
                except (OSError, ConnectionRefusedError) as e:
                    rospy.logdebug("Client connection failed: %d tries remaining." % tries)
                    # Close old socket and create new socket
                    self.sock.close()
                    time.sleep(10)
                    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def nextTwist(self, msg):
        self.latestPose = msg

    def send(self):
        if self.latestPose is None:
            return
        try:
            self.awaitRes = True
            self.sock.sendall(bytes("x: " + str(self.latestPose.linear.x) + " ang.z: " + str(self.latestPose.angular.z), "utf-8"))
            while self.awaitRes:
                res: str = str(self.sock.recv(1024), "utf-8")
                if res:
                    rospy.loginfo("From Server - Incoming: %s" % res)
                    self.awaitRes = False
        except BrokenPipeError as e:
            rospy.logerr("Broken Pipe at Client 2")
            self.awaitRes = False
            pass
        time.sleep(1)

    def server(self):
        self.sock.listen(1)
        con, _ = self.sock.accept()
        self.hasConnection = True
        while self.hasConnection:
            try:
                res: str = str(con.recv(1024), "utf-8")
                if res:
                    rospy.loginfo("From Client - Incoming: %s" % str(res))
                    con.sendall(bytes("x: " + str(self.latestPose.linear.x) + " ang.z: " + str(self.latestPose.angular.z), "utf-8"))
            except BrokenPipeError as e:
                print("Broken Pipe at Server")
                pass
        con.close()

    def close(self):
        self.sock.close()


if __name__ == '__main__':
    port = 8080
    if len(sys.argv) < 1:
        rospy.logerr("Insufficient arguments - please provide: -s if server or -c for client and turtle name")
    else:
        rospy.loginfo("Args" + str(sys.argv))
        it = None
        try:
            isServer = sys.argv[1] == '-s'
            if isServer:
                rospy.init_node("tcp_server", log_level=rospy.DEBUG, anonymous=True)
                it = ClientServer(
                    isServer=isServer,
                    turtle=sys.argv[2]
                )
            else:
                rospy.init_node("tcp_client", log_level=rospy.DEBUG, anonymous=True)
                it = ClientServer(
                    isServer=isServer,
                    turtle=sys.argv[2]
                )
            it.connect(port)
            if isServer:
                rospy.spin()
            else:
                while not rospy.is_shutdown():
                    it.send()
        except rospy.ROSInterruptException:
            it.close()
            pass

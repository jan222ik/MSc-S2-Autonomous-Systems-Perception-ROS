#!/usr/bin/env python

import rospy
import sys
import socket
from turtlesim.msg import Pose
import time


class ClientServer:
    def __init__(self, port, isServer, turtle):
        self.isServer = isServer
        self.sub = rospy.Subscriber(turtle + "/pose", Pose, self.nextPose)
        self.sock = None
        self.latestPose = None
        self.connect(port)

    def connect(self, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if self.isServer:
            self.sock.bind(("127.0.0.1", port))
            self.server()
        else:
            self.sock.connect(("127.0.0.1", port))

    def nextPose(self, msg):
        rospy.loginfo("Next Pose")
        self.latestPose = msg
        if not self.isServer:
            self.sock.send(msg.encode())
            res: str = self.sock.recv(1024)
            if res:
                rospy.loginfo("From Server - Incoming: ", res)

    def server(self):
        self.sock.listen(1)
        while True:
            con, _ = self.sock.accept()
            try:
                res: str = con.recv(1024).decode()
                if res:
                    rospy.loginfo("From Client - Incoming: ", res)
                    con.send(self.latestPose.encode())
            finally:
                con.close()
                return

    def close(self):
        self.sock.close()


if __name__ == '__main__':
    port = 8080
    if len(sys.argv) < 1:
        rospy.logerr("Insufficient arguments - please provide: -s if server or -c for client and turtle name")
    else:
        rospy.loginfo("Args" + str(sys.argv))
        tries = 10
        it = None
        try:
            while tries > 0:
                tries -= 1
                try:
                    if sys.argv[1] == '-s':
                        rospy.init_node("tcp_server", log_level=rospy.DEBUG, anonymous=True)
                        it = ClientServer(
                            port=port,
                            isServer=True,
                            turtle=sys.argv[2]
                        )
                    else:
                        rospy.init_node("tcp_client", log_level=rospy.DEBUG, anonymous=True)
                        it = ClientServer(
                            port=port,
                            isServer=False,
                            turtle=sys.argv[2]
                        )
                    rospy.spin()
                except ConnectionRefusedError:
                    pass
                finally:
                    it.close()
                time.sleep(10000)
        except rospy.ROSInterruptException:
            it.close()
            pass

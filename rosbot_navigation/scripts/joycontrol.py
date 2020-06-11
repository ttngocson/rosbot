#!/usr/bin/python2
import rospy
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist
"""
axex:
    0   left/right Axis stick left
    1   up/down Axis stick left
    2   left/right Axis stick right
    3   up/down Axis stick right
    4   cross key left/right
    5   cross key up/down
buttons:
    0   X
    1   A
    2   B
    3   Y
    4   LB
    5   RB
    6   LT
    7   RT
    8   BACK
    9   START
    10  stick click LEFT
    11  stick click right
"""

STEER_LIMIT = 60.0
MAX_SPEED = 0.5
MIN_SPEED = 0.0
STEER = 5.0

class JC:
    def __init__(self):
        self.speed = 0.0
        self.steer = 0.0
        self.mode = 1
        self.recording = 0
        self.count = 0
        print("Joy Control OK")
        self.subscriber = rospy.Subscriber("/joy", Joy, self.callBack, queue_size = 10)
        self.pub = rospy.Publisher('cmd_vel', Twist, queue_size = 1)

    def callBack(self, ros_data):
        self.steer = round((ros_data.axes[2])*STEER, 3)
        #record
        # button LT
        if(ros_data.buttons[4] == 1):
            self.recording = 0
        # button RT
        if(ros_data.buttons[5] == 1):
            self.recording = 1
        #mode switch
        # button START
        if(ros_data.buttons[9] == 1):
            self.mode +=1
            if(self.mode == 2):
                self.mode = 0
        #mode 0
        if (self.mode == 0):
            if(ros_data.axes[5] == -1):
                self.speed = self.speed - speed_amount
                if(self.speed < 10.0 and self.speed > 0):
                    self.speed = 0.0
                if(self.speed < MIN_SPEED):
                    self.speed = MIN_SPEED
            if(ros_data.axes[5] == 1):
                self.speed = self.speed + speed_amount
                # self.speed = 20.0
                if(self.speed < 10.0):
                    self.speed = 10.0
                if(self.speed > MAX_SPEED):
                    self.speed = MAX_SPEED
            if (ros_data.buttons[0] == 1):
                self.speed = 0.0
                self.recording = 0
        #mode 1
        if (self.mode == 1):   
            #if(ros_data.axes[1] > 0):
            self.speed = MAX_SPEED * ros_data.axes[1]
            # if(ros_data.axes[1] < 0):
            #     self.speed = 15.0 * ros_data.axes[1]
            # if(ros_data.axes[1] == 0):
            #     self.speed = 0.0

        # if (ros_data.buttons[3] == 1):
        #     self.speed = -100.0 
            
        # if(self.speed < 5):
        #     self.speed = 0.0
        self.speed = round(self.speed, 3)
        self.pub.publish(self.toTwist())
        

    def toTwist(self):
        twist = Twist()
        twist.linear.x = self.speed
        twist.angular.z = self.steer
        return twist

if __name__ == '__main__':
    rospy.init_node("SubJoy", anonymous=True)
    joy = JC()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        exit()
        


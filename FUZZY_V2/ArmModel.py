# -*- coding: utf-8 -*-

class ArmModel: 
    'Physical model of a balancing arm with two rotors  '
    
    def __init__(self, inertial_moment, arm_length):
        self.inertial_moment = inertial_moment 
        self.arm_length = arm_length
        self.angle = 0.0
        self.angular_speed = 0.0        # positive - cv, negative - ccv
        self.left_rotor_thrust = 0.0    # directed up
        self.right_rotor_thrust = 0.0   # directed up 
        
    def setInitialConditions(self, angle, angular_speed):
        self.angle = angle
        self.angular_speed = angular_speed
        
    def updateState(self, interval, new_left_thrust, new_right_thrust):
        self.left_rotor_thrust = new_left_thrust
        self.right_rotor_thrust = new_right_thrust        

        moment = self.arm_length * (self.left_rotor_thrust - \
            self.right_rotor_thrust)    # this preserves sign - cv/ccv info
        
        angular_acceleration = moment / self.inertial_moment

        angle_change = self.angular_speed * interval + angular_acceleration * \
            interval * interval / 2.0
            
        # update state 
        self.angular_speed += angular_acceleration * interval
        self.angle += angle_change
        
    def getAngle(self):
        return self.angle
        
    def getAngularSpeed(self):
        return self.angular_speed
        
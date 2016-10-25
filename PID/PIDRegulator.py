# -*- coding: utf-8 -*-

class PIDRegulator:
    
    def __init__(self, proportional, integral, derivative, min_thrust, 
                 max_thrust):
        self.p = proportional
        self.d = derivative
        self.i = integral
        self.max_thrust = max_thrust
        self.min_thrust = min_thrust
        self.errSum = 0.0
        self.lastErr = 0.0
        self.recommended_left = 0.0
        self.recommended_right = 0.0
        
    def calcNewThrusts(self, angle, desired_angle, interval):
        err = desired_angle - angle; 
        Derr = (err - self.lastErr) / interval
        self.lastErr = err
        self.errSum += err * interval 
        
        r_recommendation = self.p * err + self.d * Derr + self.i * self.errSum
        r_recommendation = -r_recommendation 
        
        if r_recommendation < self.min_thrust:
            r_recommendation = self.min_thrust
        elif r_recommendation > self.max_thrust:
            r_recommendation = self.max_thrust
            
        self.recommended_right = r_recommendation
        
        l_recommendation = self.p * err + self.d * Derr + self.i * self.errSum
        
        if l_recommendation < self.min_thrust:
            l_recommendation = self.min_thrust
        elif l_recommendation > self.max_thrust:
            l_recommendation = self.max_thrust
            
        self.recommended_left = l_recommendation
        
        
    def getRightThrust(self):
        return self.recommended_right 
        
    def getLeftThrust(self):
        return self.recommended_left 
        
    def getLastErr(self):
        return self.lastErr
        
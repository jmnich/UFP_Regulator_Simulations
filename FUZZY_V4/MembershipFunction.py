# -*- coding: utf-8 -*-

class MembershipFunction:
    """
    this class represents a simple membership function which is spit into four 
    zones: left_saturation zone, left_active_zone, right_active_zone and 
    right_saturation_zone
    """
    
    def __init__(self, left_saturation, right_saturation, slope_factor, 
                 central_point):
        self.slope_factor = slope_factor
        self.central_boundary = central_point
        self.left_boundary = self.central_boundary - 1.0 / self.slope_factor
        self.right_boundary = self.central_boundary + 1.0 / self.slope_factor
        self.left_saturation = left_saturation
        self.right_saturation = right_saturation
                             
    def getMembershipFactor(self, value):
        if value == self.central_boundary:  # peak 
            return 1.0
        elif value < self.central_boundary and value > self.left_boundary and\
            not self.left_saturation:       # left zone - no saturation 
            return self.slope_factor * (value - self.left_boundary)
        elif value < self.central_boundary and value > self.left_boundary and\
            self.left_saturation:           # left zone - saturation
            return 1.0
        elif value > self.central_boundary and value < self.right_boundary and\
            not self.right_saturation:      # right zone - no saturation
            return -self.slope_factor * (value - self.right_boundary)
        elif value > self.central_boundary and value < self.right_boundary and\
            self.right_saturation:          # right zone - saturation
            return 1.0
        elif value <= self.left_boundary and self.left_saturation:
            return 1.0
        elif value <= self.left_boundary and not self.left_saturation:
            return 0.0
        elif value >= self.right_boundary and self.right_saturation:
            return 1.0
        elif value >= self.right_boundary and not self.right_saturation:
            return 0.0
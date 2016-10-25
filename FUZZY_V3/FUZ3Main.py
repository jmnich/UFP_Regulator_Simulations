# -*- coding: utf-8 -*-

"""
This algorithm is designed to optimize fuzzy algorithm behaviour through simulation of an arm with two rotors.
"""

import math
import ArmModel
import FuzzyRegulator
import ReactionsGenerator
import matplotlib.pyplot as plt

structure_mass = 1.0
arm_length = 0.25
arm_radius = 0.01
interval = 0.01

'''
reactions = [8, 8, 8, 7, 8, 4, 4, 5, 6,
             8, 7, 7, 5, 6, 3, 3, 4, 2,
             8, 7, 5, 3, 4, 2, 2, 3, 0,
             7, 6, 4, 2, 2, 1, -1, -2, -3,
             7, 5, 3, 2, 0, -2, -3, -5, -7,
             3, 2, 1, -1, -2, -2, -4, -6, -7,
             0, -3, -2, -2, -4, -3, -5, -7, -8,
             -2, -4, -3, -3, -6, -5, -7, -7, -8,
             -6, -5, -4, -4, -8, -7, -8, -8, -8]


record = []
fit_factor = 0.0
'''


arm_inertial_moment = (1.0 / 12.0) * structure_mass * \
    (math.pow(arm_radius, 2) * 3 + math.pow(arm_length * 2, 2))

arm = ArmModel.ArmModel(arm_inertial_moment, arm_length)

arm.setInitialConditions(45.0, 0.0)


reaction_generator = ReactionsGenerator.ReactionsGenerator()


for i in range(1, 1000):
    '''
    regulator.calcNewThrusts(arm.angle, arm.angular_speed, 0.0)
    arm.updateState(interval, 
                    regulator.getLeftThrust(), regulator.getRightThrust())
    record.append(arm.angle)
    fit_factor += abs(regulator.getLastErr() * interval)
    #print(arm.angle)
    '''
    
#plt.plot(record)
#plt.show()
#print(fit_factor)
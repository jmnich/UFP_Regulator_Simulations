# -*- coding: utf-8 -*-

"""
FUZZY REGULATOR 
1. Create an instance of the balanced arm
2. Set initial conditions
3. Prepare a fuzzy regulator
4. Begin iterating:
    a)
    
5. Visualize results

note: all values are scaled in standard metric units
note: input params: angle, angular_velocity
note: output params: left thrust, right thrust
""" 

import math
import ArmModel
import FuzzyRegulator
import matplotlib.pyplot as plt

structure_mass = 1.0
arm_length = 0.25
arm_radius = 0.01
interval = 0.01

reactions = [8, 8, 8, 7, 8, 8, 7, 6, 5,
             8, 7, 7, 5, 6, 6, 6, 5, 4,
             8, 7, 5, 3, 4, 5, 4, 3, 2,
             8, 6, 4, 2, 2, 3, -1, -5, -7,
             8, 6, 4, 2, 0, -2, -4, -6, -8,
             7, 5, 1, -3, -2, -2, -4, -6, -8,
             -2, -3, -4, -5, -4, -3, -5, -7, -8,
             -4, -5, -6, -6, -6, -5, -7, -7, -8,
             -5, -6, -7, -8, -8, -7, -8, -8, -8]

record = []
fit_factor = 0.0

arm_inertial_moment = (1.0 / 12.0) * structure_mass * \
    (math.pow(arm_radius, 2) * 3 + math.pow(arm_length * 2, 2))

arm = ArmModel.ArmModel(arm_inertial_moment, arm_length)

arm.setInitialConditions(5.0, 0.0)

regulator = FuzzyRegulator.FuzzyRegulator(0.0, 10.0, reactions)

for i in range(1, 1000):
    regulator.calcNewThrusts(arm.angle, arm.angular_speed, 0.0)
    arm.updateState(interval, 
                    regulator.getLeftThrust(), regulator.getRightThrust())
    record.append(arm.angle)
    fit_factor += abs(regulator.getLastErr() * interval)
    #print(arm.angle)
    
plt.plot(record)
plt.show()
print(fit_factor)
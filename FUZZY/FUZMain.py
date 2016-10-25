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

record = []
fit_factor = 0.0

arm_inertial_moment = (1.0 / 12.0) * structure_mass * \
    (math.pow(arm_radius, 2) * 3 + math.pow(arm_length * 2, 2))

arm = ArmModel.ArmModel(arm_inertial_moment, arm_length)

arm.setInitialConditions(45.0, 0.0)

regulator = FuzzyRegulator.FuzzyRegulator(0.0, 10.0)

for i in range(0, 1000):
    regulator.calcNewThrusts(arm.angle, arm.angular_speed, 0.0)
    arm.updateState(interval, 
                    regulator.getLeftThrust(), regulator.getRightThrust())
    record.append(arm.angle)
    fit_factor += abs(regulator.getLastErr() * interval)
    
plt.plot(record)
plt.show()
print(fit_factor)
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

structure_mass = 2
arm_length = 0.25
arm_radius = 0.01
interval = 0.01
desired_angle = 0.0

reactions = [8, 8, 8, 8,        8,      8, 7, 6, 5,
             8, 8, 8, 7,        8,      6, 6, 5, 4,
             8, 8, 7, 6,        6,      5, 4, 3, 2,
             8, 8, 6, 5,        5,      5, 3, -6, -8,

             8, 8, 6, 5,        0,      -5, -6, -8, -8,

             8, 6, -3, -5,      -5,     -5, -6, -8, -8,
             -2, -3, -4, -5,    -6,     -6, -7, -8, -8,
             -4, -5, -6, -6,    -8,     -7, -8, -8, -8,
             -5, -6, -7, -8,    -8,     -8, -8, -8, -8]

record = []
fit_factor = 0.0

arm_inertial_moment = (1.0 / 12.0) * structure_mass * \
    (math.pow(arm_radius, 2) * 3 + math.pow(arm_length * 2, 2))

arm = ArmModel.ArmModel(arm_inertial_moment, arm_length)

arm.setInitialConditions(5.0, 0.0)

regulator = FuzzyRegulator.FuzzyRegulator(0.0, 10.0, reactions)



for i in range(1, 1000):
    regulator.calcNewThrusts(arm.angle, arm.angular_speed, desired_angle)
    arm.updateState(interval, 
                    regulator.getLeftThrust(), regulator.getRightThrust())
    record.append(arm.angle)
    fit_factor += abs(regulator.getLastErr() * interval)

    # if i == 300:
    #     desired_angle = 10
    #
    # if i == 600:
    #     desired_angle = -15

plt.plot(record)
plt.show()
print(fit_factor)
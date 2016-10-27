# -*- coding: utf-8 -*-

"""
PID REGULATOR 
1. Create an instance of the balanced arm
2. Set initial conditions of the arm 
3. Begin iterating: 
    a) load current state of the arm from the model to the regulator 
    b) calculate new parameters for the rotors 
    c) load new parameters and time interval to the model 
    d) ...repeat for the simulations' duration... 
4. Visualize results

note: all values are scaled in standard metric units
"""

import math
import ArmModel
import PIDRegulator
import matplotlib.pyplot as plt

structure_mass = 1.0
arm_length = 0.25
arm_radius = 0.01
interval = 0.01
desired_angle = 0
p = 0.5
i = 0.01
d = 0.3

record = []

arm_inertial_moment = (1.0 / 12.0) * structure_mass * \
    (math.pow(arm_radius, 2) * 3 + math.pow(arm_length * 2, 2))

arm = ArmModel.ArmModel(arm_inertial_moment, arm_length)

regulator = PIDRegulator.PIDRegulator(p, i, d, 0.0, 10.0)

arm.setInitialConditions(45.0, 0.0)

fit_factor = 0.0

for i in range(0, 1000):
    regulator.calcNewThrusts(arm.angle, desired_angle, interval)
    arm.updateState(interval, 
                    regulator.getLeftThrust(), regulator.getRightThrust())
    record.append(arm.angle)
    fit_factor += abs(regulator.getLastErr()) * interval
    # if i == 300:
    #     desired_angle = 10
    #
    # if i == 600:
    #     desired_angle = -15
        

        
plt.plot(record)
plt.show()
print(fit_factor)
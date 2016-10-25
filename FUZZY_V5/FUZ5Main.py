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
import copy
import numpy as np

fig, ax = plt.subplots()

structure_mass = 1.0
arm_length = 0.25
arm_radius = 0.01
interval = 0.01
arm_initial_angle = 45.0
arm_initial_velocity = 0.0

reactions = [8, 8, 8, 7, 8, 4, 4, 5, 6,
             8, 7, 7, 5, 6, 3, 3, 4, 2,
             8, 7, 5, 3, 4, 2, 2, 3, 0,
             7, 6, 4, 2, 2, 1, -1, -2, -3,
             7, 5, 3, 2, 0, -2, -3, -5, -7,
             3, 2, 1, -1, -2, -2, -4, -6, -7,
             0, -3, -2, -2, -4, -3, -5, -7, -8,
             -2, -4, -3, -3, -6, -5, -7, -7, -8,
             -6, -5, -4, -4, -8, -7, -8, -8, -8]

rules_usage_2d = []

record = []
rules_raw_record = []
rules_processed_record = {}
fit_factor = 0.0

arm_inertial_moment = (1.0 / 12.0) * structure_mass * \
    (math.pow(arm_radius, 2) * 3 + math.pow(arm_length * 2, 2))

arm = ArmModel.ArmModel(arm_inertial_moment, arm_length)

arm.setInitialConditions(arm_initial_angle, arm_initial_velocity)

regulator = FuzzyRegulator.FuzzyRegulator(0.0, 10.0, reactions)

for arm_initial_angle_iter in range(-45, 46, 1):
    arm.setInitialConditions(arm_initial_angle_iter, 0.0)

    for i in range(1, 1000):
        regulator.calcNewThrusts(arm.angle, arm.angular_speed, 0.0)
        arm.updateState(interval,
                        regulator.getLeftThrust(), regulator.getRightThrust())
        record.append(arm.angle)
        fit_factor += abs(regulator.getLastErr() * interval)
        for rule_usage in regulator.recently_used_rules:
            rules_raw_record.append(copy.deepcopy(rule_usage))

    print(str(arm_initial_angle_iter + 46) + "  iterations done")

# process rules usage data
for i in range(81):
    rules_processed_record[i] = 0.0

for record in rules_raw_record:
    rules_processed_record[record[0]] += record[1]

# rules_processed_record[40] = 0.0

for i in range(81):

    if rules_processed_record[i] < 0:
        rules_processed_record[i] = -math.log(abs(rules_processed_record[i]))
    elif rules_processed_record[i] > 0:
        rules_processed_record[i] = math.log(rules_processed_record[i])
    else:
        rules_processed_record[i] = 0

for verse in range(9):
    dummy_verse = []
    for column in range(9):
        dummy_verse.append(rules_processed_record[column + 9 * verse])
    rules_usage_2d.append(copy.deepcopy(dummy_verse))
    dummy_verse.clear()

data = np.asarray(rules_usage_2d)

heatmap = ax.pcolor(data)

ax.invert_yaxis()
ax.xaxis.tick_top()

ax.set_xticklabels(['-4', '-3', '-2', '-1', '0', '1', '2', '3', '4'], minor=False)
ax.set_yticklabels(['-4', '-3', '-2', '-1', '0', '1', '2', '3', '4'], minor=False)

ax.set_xticks(np.arange(data.shape[0] + 0.5))
ax.set_yticks(np.arange(data.shape[1] + 0.5))

plt.colorbar(heatmap)
plt.show()
print(fit_factor)

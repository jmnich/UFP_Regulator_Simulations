# -*- coding: utf-8 -*-

"""
This algorithm is designed to optimize fuzzy algorithm behaviour through simulation of an arm with two rotors.
"""

import math
import ArmModel
import Field
import FuzzyRegulator
import ReactionZone
import ReactionsGenerator
import matplotlib.pyplot as plt
import time

structure_mass = 1.0
arm_length = 0.25
arm_radius = 0.01
interval = 0.01
arm_init_ang = -10.0
arm_init_vel = 0.0

reactions = [8, 8, 8, 7, 8, 4, 4, 5, 6,
             8, 7, 7, 5, 6, 3, 3, 4, 2,
             8, 7, 5, 3, 4, 2, 2, 3, 0,
             7, 6, 4, 2, 2, 1, -1, -2, -3,
             7, 5, 3, 2, 0, -2, -3, -5, -7,
             3, 2, 1, -1, -2, -2, -4, -6, -7,
             0, -3, -2, -2, -4, -3, -5, -7, -8,
             -2, -4, -3, -3, -6, -5, -7, -7, -8,
             -6, -5, -4, -4, -8, -7, -8, -8, -8]

initial_reactions_as_fields = []

for i in range(81):
    initial_reactions_as_fields.append(Field.Field(i, reactions[i], 8, -8))

# record = []
# fit_factor = 0.0

# group reactions into zones
zones = []

zone_0_indexes = [0, 1, 2,
                  9, 10, 11,
                  18, 19, 20]

zone_1_indexes = [3, 4, 5,
                  12, 13, 14,
                  21, 22, 23]

zone_2_indexes = [6, 7, 8,
                  15, 16, 17,
                  24, 25, 26]

zone_3_indexes = [27, 28, 29,
                  36, 37, 38,
                  45, 46, 47]

zone_4_indexes = [30, 31, 32,
                  39, 40, 41,
                  48, 49, 50]

zone_5_indexes = [33, 34, 35,
                  42, 43, 44,
                  51, 52, 53]

zone_6_indexes = [54, 55, 56,
                  63, 64, 65,
                  72, 73, 74]

zone_7_indexes = [57, 58, 59,
                  66, 67, 68,
                  75, 76, 77]

zone_8_indexes = [60, 61, 62,
                  69, 70, 71,
                  78, 79, 80]

zones.append(ReactionZone.ReactionZone(zone_0_indexes, initial_reactions_as_fields))
zones.append(ReactionZone.ReactionZone(zone_1_indexes, initial_reactions_as_fields))
zones.append(ReactionZone.ReactionZone(zone_2_indexes, initial_reactions_as_fields))
zones.append(ReactionZone.ReactionZone(zone_3_indexes, initial_reactions_as_fields))
zones.append(ReactionZone.ReactionZone(zone_4_indexes, initial_reactions_as_fields))
zones.append(ReactionZone.ReactionZone(zone_5_indexes, initial_reactions_as_fields))
zones.append(ReactionZone.ReactionZone(zone_6_indexes, initial_reactions_as_fields))
zones.append(ReactionZone.ReactionZone(zone_7_indexes, initial_reactions_as_fields))
zones.append(ReactionZone.ReactionZone(zone_8_indexes, initial_reactions_as_fields))

arm_inertial_moment = (1.0 / 12.0) * structure_mass * \
    (math.pow(arm_radius, 2) * 3 + math.pow(arm_length * 2, 2))

arm = ArmModel.ArmModel(arm_inertial_moment, arm_length)

arm.setInitialConditions(arm_init_ang, arm_init_vel)


reaction_generator = ReactionsGenerator.ReactionsGenerator(initial_reactions_as_fields, zones)

current_best_reactions = reactions
current_best_fit_factor = 1000000000.0
best_record = []
last_set_of_reactions = reactions

while reaction_generator.zones_processed < 9:
    start = time.time()
    new_reactions = reaction_generator.nextSetOfReactions(last_set_of_reactions, current_best_reactions)

    # compare new and last reactions
    identical = True
    dif_sum = 0
    for i in range(81):
        dif = new_reactions[i] - last_set_of_reactions[i]
        if dif != 0:
            identical = False
            dif_sum += dif
    if identical:
        print("New reactions are identical to last")
    else:
        print("Difference between reactions:  " + str(dif_sum))

    last_set_of_reactions = new_reactions

    regulator = FuzzyRegulator.FuzzyRegulator(0.0, 10.0, new_reactions)
    fit_factor = 0.0
    record = []

    arm.setInitialConditions(arm_init_ang, arm_init_vel)     # reset the arm model

    for i in range(1000):
        regulator.calcNewThrusts(arm.angle, arm.angular_speed, 0.0)
        arm.updateState(interval, regulator.getLeftThrust(), regulator.getRightThrust())
        fit_factor += abs(regulator.getLastErr() * interval)
        record.append(arm.angle)

    if fit_factor < current_best_fit_factor:
        current_best_fit_factor = fit_factor
        current_best_reactions = reactions
        best_record = record

    end = time.time()

    print("Iteration " + str(reaction_generator.iterations_done) + " done.\t Best fit factor:   " +
          str(current_best_fit_factor) + "   Current fit:   " + str(fit_factor) + "  time taken: " +
          str(round((end - start) * 1000, 1)) + " ms")

    # filter the list of applied rules
    no_duplicates_list = list(set(regulator.rules_used))
    print(str(sorted(no_duplicates_list)))

print("\n\nAlgorithm DONE")
print("Best fit factor:   " + str(current_best_fit_factor))

plt.plot(best_record)
plt.show()

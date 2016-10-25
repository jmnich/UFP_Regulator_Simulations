# -*- coding: utf-8 -*-
import MembershipFunction


class FuzzyRegulator:
    def __init__(self, min_thrust, max_thrust, reactions):
        self.min_thrust = min_thrust
        self.max_thrust = max_thrust
        self.recommended_left = 0.0
        self.recommended_right = 0.0
        self.lastErr = 0.0
        self.recently_used_rules = []

        # prepare membership functions for input parameters
        self.angle_err = {}
        self.angle_err[4] = MembershipFunction.MembershipFunction(False, True, 1.0 / 15.0, 60.0)
        self.angle_err[3] = MembershipFunction.MembershipFunction(False, False, 1.0 / 15.0, 45.0)
        self.angle_err[2] = MembershipFunction.MembershipFunction(False, False, 1.0 / 15.0, 25.0)
        self.angle_err[1] = MembershipFunction.MembershipFunction(False, False, 1.0 / 10.0, 10.0)
        self.angle_err[0] = MembershipFunction.MembershipFunction(False, False, 1.0 / 10.0, 0.0)
        self.angle_err[-1] = MembershipFunction.MembershipFunction(False, False, 1.0 / 10.0, -10.0)
        self.angle_err[-2] = MembershipFunction.MembershipFunction(False, False, 1.0 / 15.0, -25.0)
        self.angle_err[-3] = MembershipFunction.MembershipFunction(False, False, 1.0 / 15.0, -45.0)
        self.angle_err[-4] = MembershipFunction.MembershipFunction(True, False, 1.0 / 15.0, -60.0)

        self.ang_vel = {}
        self.ang_vel[4] = MembershipFunction.MembershipFunction(False, True, 1.0 / 7.5, 30.0)
        self.ang_vel[3] = MembershipFunction.MembershipFunction(False, False, 1.0 / 7.5, 22.5)
        self.ang_vel[2] = MembershipFunction.MembershipFunction(False, False, 1.0 / 7.5, 12.5)
        self.ang_vel[1] = MembershipFunction.MembershipFunction(False, False, 1.0 / 5.0, 5.0)
        self.ang_vel[0] = MembershipFunction.MembershipFunction(False, False, 1.0 / 5.0, 0.0)
        self.ang_vel[-1] = MembershipFunction.MembershipFunction(False, False, 1.0 / 5.0, -5.0)
        self.ang_vel[-2] = MembershipFunction.MembershipFunction(False, False, 1.0 / 7.5, -12.5)
        self.ang_vel[-3] = MembershipFunction.MembershipFunction(False, False, 1.0 / 7.5, -22.5)
        self.ang_vel[-4] = MembershipFunction.MembershipFunction(True, False, 1.0 / 7.5, -30.0)

        # prepare membership functions for output thrust recommendations
        span = max_thrust - min_thrust
        factor = span / 8.0
        self.thr_reco = {}
        self.thr_reco[8] = MembershipFunction.MembershipFunction(False, False, factor, max_thrust)
        self.thr_reco[7] = MembershipFunction.MembershipFunction(False, False, factor, min_thrust + span / 8.0 * 7)
        self.thr_reco[6] = MembershipFunction.MembershipFunction(False, False, factor, min_thrust + span / 8.0 * 6)
        self.thr_reco[5] = MembershipFunction.MembershipFunction(False, False, factor, min_thrust + span / 8.0 * 5)
        self.thr_reco[4] = MembershipFunction.MembershipFunction(False, False, factor, min_thrust + span / 8.0 * 4)
        self.thr_reco[3] = MembershipFunction.MembershipFunction(False, False, factor, min_thrust + span / 8.0 * 3)
        self.thr_reco[2] = MembershipFunction.MembershipFunction(False, False, factor, min_thrust + span / 8.0 * 2)
        self.thr_reco[1] = MembershipFunction.MembershipFunction(False, False, factor, min_thrust + span / 8.0 * 1)
        self.thr_reco[0] = MembershipFunction.MembershipFunction(False, False, factor, min_thrust)

        # prepare rulebase
        self.rules = []

        z = 0

        for verse in range(9):
            for column in range(9):
                self.rules.append(Rule(verse - 4, column - 4, reactions[z]))
                z += 1
        print(str(z) + " rules loaded")

    def calcNewThrusts(self, angle, ang_vel, desired_angle):
        self.lastErr = desired_angle - angle

        self.recently_used_rules.clear()

        # fuzzyfication of the input
        fuzzy_angle = []

        for fuzzy_state in self.angle_err:
            pertinence = self.angle_err[fuzzy_state].getMembershipFactor(angle)
            if pertinence > 0.0:  # is a member
                fuzzy_angle.append(FuzzyInput(fuzzy_state, pertinence))

        fuzzy_vel = []

        for fuzzy_state in self.ang_vel:
            pertinence = self.ang_vel[fuzzy_state].getMembershipFactor(ang_vel)
            if pertinence > 0.0:  # is a member
                fuzzy_vel.append(FuzzyInput(fuzzy_state, pertinence))

        # gather recommendations from rules and save used rules
        recommendations = []

        for r in range(len(self.rules)):
            for ang in fuzzy_angle:
                for vel in fuzzy_vel:
                    if self.rules[r].angle == ang.input_value and \
                                    self.rules[r].angular_velocity == vel.input_value:
                        # rule is on
                        recommendations.append(Recommendation(self.rules[r].recommended_thrust,
                                                              min(ang.pertinence, vel.pertinence)))
                        self.recently_used_rules.append([r, min(ang.pertinence, vel.pertinence)])

        # defuzzyfication
        total_val = 0.0
        total_pertinence = 0.0

        for reco in recommendations:
            abs_rec = abs(reco.recommended_thrust)
            center = self.thr_reco[abs_rec].central_boundary

            if reco.recommended_thrust >= 0:  # left thruster
                total_val += center * reco.pertinence
            else:  # right thruster
                total_val -= center * reco.pertinence
            total_pertinence += reco.pertinence

        # center-average calculation
        final_recommendation = total_val / total_pertinence

        # safety check
        if final_recommendation > self.max_thrust:
            final_recommendation = self.max_thrust
            # elif final_recommendation < self.min_thrust:
            # final_recommendation = self.min_thrust      # !!! bug

        # save results to proper fields
        if final_recommendation == 0.0:  # thrusters disabled
            self.recommended_left = self.min_thrust
            self.recommended_right = self.min_thrust
        elif final_recommendation > 0:  # left thruster active
            self.recommended_left = final_recommendation
            self.recommended_right = self.min_thrust
        elif final_recommendation < 0:  # right thruster active
            self.recommended_right = -final_recommendation
            self.recommended_left = self.min_thrust

    def getRightThrust(self):
        return self.recommended_right

    def getLeftThrust(self):
        return self.recommended_left

    def getLastErr(self):
        return self.lastErr


class Recommendation:
    def __init__(self, thrust_level, pertinence):
        self.recommended_thrust = thrust_level
        self.pertinence = pertinence


class FuzzyInput:
    def __init__(self, input_value, pertinence):
        self.input_value = input_value
        self.pertinence = pertinence


class Rule:
    def __init__(self, angle, angular_velocity, recommended_thrust):
        self.angle = angle
        self.angular_velocity = angular_velocity
        self.recommended_thrust = recommended_thrust

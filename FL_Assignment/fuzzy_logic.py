import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


class FuzzyLogicSystem:
    def __init__(self):
        # Define fuzzy variables
        self.genHlth = ctrl.Antecedent(np.arange(1, 11, 1), 'genHlth')
        self.systolicBp = ctrl.Antecedent(np.arange(70, 221, 1), 'systolicBp')
        self.cholesterol = ctrl.Antecedent(np.arange(70, 301, 1), 'cholesterol')
        self.age = ctrl.Antecedent(np.arange(0, 101, 1), 'age')
        self.stroke = ctrl.Antecedent(np.arange(0, 2, 1), 'stroke')
        self.diabetes = ctrl.Antecedent(np.arange(0, 2, 1), 'diabetes')
        self.physHlth = ctrl.Antecedent(np.arange(0, 31, 1), 'physHlth')
        self.diffWalk = ctrl.Antecedent(np.arange(0, 2, 1), 'diffWalk')

        self.cvd_risk = ctrl.Consequent(np.arange(0, 11, 1), 'cvd_risk')

        # Define membership functions for inputs
        self.genHlth['bad'] = fuzz.trimf(self.genHlth.universe, [1, 1, 3])    # poor
        self.genHlth['fair'] = fuzz.trimf(self.genHlth.universe, [2, 3, 5])    # fair
        self.genHlth['good'] = fuzz.trimf(self.genHlth.universe, [4, 5, 7])    # good
        self.genHlth['very_good'] = fuzz.trimf(self.genHlth.universe, [6, 8, 9])    # very good
        self.genHlth['excellent'] = fuzz.trimf(self.genHlth.universe, [8, 10, 10])    # excellent

        self.systolicBp['normal'] = fuzz.trapmf(self.systolicBp.universe, [70, 70, 100, 120])
        self.systolicBp['elevated'] = fuzz.trimf(self.systolicBp.universe, [110, 120, 140])
        self.systolicBp['hypertension-stage1'] = fuzz.trimf(self.systolicBp.universe, [130, 140, 160])
        self.systolicBp['hypertension-stage2'] = fuzz.trapmf(self.systolicBp.universe, [140, 180, 220, 220])

        self.cholesterol['normal'] = fuzz.trapmf(self.cholesterol.universe, [70, 70, 180, 200])
        self.cholesterol['at-risk'] = fuzz.trapmf(self.cholesterol.universe, [180, 200, 230, 250])
        self.cholesterol['dangerous'] = fuzz.trapmf(self.cholesterol.universe, [230, 240, 300, 300])

        self.age['child'] = fuzz.trapmf(self.age.universe, [0, 5, 9, 12])
        self.age['teen'] = fuzz.trapmf(self.age.universe, [11, 15, 17, 19])
        self.age['adult'] = fuzz.trapmf(self.age.universe, [18, 26, 32, 39])
        self.age['middle_age'] = fuzz.trapmf(self.age.universe, [38, 46, 52, 59])
        self.age['senior_adult'] = fuzz.trapmf(self.age.universe, [58, 90, 100, 100])

        self.stroke['no'] = fuzz.trimf(self.stroke.universe, [0, 0, 0])  # no
        self.stroke['yes'] = fuzz.trimf(self.stroke.universe, [1, 1, 1])  # yes

        self.diabetes['no'] = fuzz.trimf(self.diabetes.universe, [0, 0, 0])  # no
        self.diabetes['yes'] = fuzz.trimf(self.diabetes.universe, [1, 1, 1])  # yes

        self.physHlth['few'] = fuzz.trimf(self.physHlth.universe, [0, 0, 10])
        self.physHlth['some'] = fuzz.trimf(self.physHlth.universe, [5, 10, 15])
        self.physHlth['many'] = fuzz.trimf(self.physHlth.universe, [10, 20, 25])
        self.physHlth['most'] = fuzz.trimf(self.physHlth.universe, [20, 30, 30])

        self.diffWalk['no'] = fuzz.trimf(self.diffWalk.universe, [0, 0, 0])  # no
        self.diffWalk['yes'] = fuzz.trimf(self.diffWalk.universe, [1, 1, 1])  # yes

        # Define membership functions for output
        self.cvd_risk['healthy'] = fuzz.trimf(self.cvd_risk.universe, [0, 2, 4])
        self.cvd_risk['low_risk'] = fuzz.trimf(self.cvd_risk.universe, [2, 4, 6])
        self.cvd_risk['medium_risk'] = fuzz.trimf(self.cvd_risk.universe, [4, 6, 8])
        self.cvd_risk['high_risk'] = fuzz.trimf(self.cvd_risk.universe, [6, 8, 10])

        # Visualization of membership functions
        # self.genHlth.view()
        # self.systolicBp.view()
        # self.cholesterol.view()
        # self.age.view()
        # self.stroke.view()
        # self.diabetes.view()
        # self.diffWalk.view()
        # self.physHlth.view()
        # self.cvd_risk.view()

        # Define fuzzy rules
        rules = [
            # HEALTHY
            ctrl.Rule((self.genHlth['excellent'] | self.genHlth['very_good'] | self.genHlth['good'] | self.genHlth['fair']) &
                      self.systolicBp['normal'] &
                      self.cholesterol['normal'] &
                      (self.age['child'] | self.age['teen'] | self.age['adult'] | self.age['middle_age'] | self.age['senior_adult']) &
                      self.stroke['no'] &
                      self.diabetes['no'] &
                      (self.physHlth['most'] | self.physHlth['many'] | self.physHlth['some'] | self.physHlth['few']) &
                      (self.diffWalk['no'] | self.diffWalk['yes']),
                      self.cvd_risk['healthy']),

            # LOW RISK
            ctrl.Rule((self.genHlth['excellent'] | self.genHlth['very_good'] | self.genHlth['good'] | self.genHlth['fair']) &
                      self.systolicBp['elevated'] &
                      self.cholesterol['normal'] &
                      (self.age['child'] | self.age['teen'] | self.age['adult'] | self.age['middle_age']) &
                      self.stroke['no'] &
                      (self.diabetes['no'] | self.diabetes['yes']) &
                      (self.physHlth['most'] | self.physHlth['many'] | self.physHlth['some'] | self.physHlth['few']) &
                      (self.diffWalk['no'] | self.diffWalk['yes']),
                      self.cvd_risk['low_risk']),

            # MEDIUM RISK
            ctrl.Rule((self.genHlth['excellent'] | self.genHlth['very_good'] | self.genHlth['good'] | self.genHlth['fair']) &
                      self.systolicBp['elevated'] &
                      self.cholesterol['normal'] &
                      self.age['senior_adult'] &
                      self.stroke['no'] &
                      (self.diabetes['no'] | self.diabetes['yes']) &
                      (self.physHlth['most'] | self.physHlth['many'] | self.physHlth['some'] | self.physHlth['few']) &
                      (self.diffWalk['no'] | self.diffWalk['yes']),
                      self.cvd_risk['medium_risk']),

            ctrl.Rule((self.genHlth['good'] | self.genHlth['fair'] | self.genHlth['bad']) &
                      (self.systolicBp['elevated'] | self.systolicBp['hypertension-stage1']) &
                      self.cholesterol['at-risk'] &
                      (self.age['child'] | self.age['teen'] | self.age['adult'] | self.age['middle_age']) &
                      (self.stroke['no'] | self.stroke['yes']) &
                      (self.diabetes['no'] | self.diabetes['yes']) &
                      (self.physHlth['many'] | self.physHlth['some'] | self.physHlth['few']) &
                      (self.diffWalk['no'] | self.diffWalk['yes']),
                      self.cvd_risk['medium_risk']),

            # HIGH RISK
            ctrl.Rule((self.genHlth['good'] | self.genHlth['fair'] | self.genHlth['bad']) &
                      (self.systolicBp['elevated'] | self.systolicBp['hypertension-stage1']) &
                      self.cholesterol['at-risk'] &
                      self.age['senior_adult'] &
                      (self.stroke['no'] | self.stroke['yes']) &
                      (self.diabetes['no'] | self.diabetes['yes']) &
                      (self.physHlth['many'] | self.physHlth['some'] | self.physHlth['few']) &
                      (self.diffWalk['no'] | self.diffWalk['yes']),
                      self.cvd_risk['high_risk']),

            ctrl.Rule((self.genHlth['fair'] | self.genHlth['bad']) &
                      (self.systolicBp['hypertension-stage1'] | self.systolicBp['hypertension-stage2']) &
                      (self.cholesterol['at-risk'] | self.cholesterol['dangerous']) &
                      (self.age['adult'] | self.age['middle_age'] | self.age['senior_adult']) &
                      (self.stroke['no'] | self.stroke['yes']) &
                      (self.diabetes['no'] | self.diabetes['yes']) &
                      (self.physHlth['many'] | self.physHlth['some'] | self.physHlth['few']) &
                      (self.diffWalk['no'] | self.diffWalk['yes']),
                      self.cvd_risk['high_risk'])
        ]

        # Add control system and simulation
        self.control_system = ctrl.ControlSystem(rules)
        self.simulation = ctrl.ControlSystemSimulation(self.control_system)

    def compute_cvd_risk(self, genHlth, systolicBp, cholesterol, age, stroke, diabetes, physHlth, diffWalk):
        # Fuzzify inputs
        self.simulation.input['genHlth'] = genHlth
        self.simulation.input['systolicBp'] = systolicBp
        self.simulation.input['cholesterol'] = cholesterol
        self.simulation.input['age'] = age
        self.simulation.input['stroke'] = stroke
        self.simulation.input['diabetes'] = diabetes
        self.simulation.input['physHlth'] = physHlth
        self.simulation.input['diffWalk'] = diffWalk

        # Compute the result
        self.simulation.compute()

        # Return the defuzzified result
        return self.simulation.output['cvd_risk']
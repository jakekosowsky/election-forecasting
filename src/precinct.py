"""Precinct state and live-result adjustment logic."""

import numpy as np

class Precinct:
    def __init__(self, id, estimated_dem, estimated_rep, estimated_turnout, similar_precincts):
        """
        Initializes a precinct.
        :param id: Precinct ID
        :param estimated_dem: Estimated Democratic vote share
        :param estimated_rep: Estimated Republican vote share
        :param estimated_turnout: Estimated turnout
        :param similar_precincts: List of tuples with similar precincts (id, distance)
        """
        self.id = id
        self.estimated_dem = estimated_dem
        self.estimated_rep = estimated_rep
        self.estimated_turnout = estimated_turnout
        self.similar_precincts = similar_precincts
        self.reported = False
        self.actual_dem = None
        self.actual_rep = None
        self.actual_turnout = None
        self.adjusted_dem = estimated_dem
        self.adjusted_rep = estimated_rep
        self.adjusted_turnout = estimated_turnout

def sigmoid(x):
    """ Sigmoid function for scaling adjustments based on the reporting rate """
    return 1 / (1 + np.exp(-x))

def update_precinct_results(precinct, actual_dem, actual_rep, actual_turnout):
    """ Update precinct with actual results """
    precinct.reported = True
    precinct.actual_dem = actual_dem
    precinct.actual_rep = actual_rep
    precinct.actual_turnout = actual_turnout

def calculate_adjustments(precincts, hyper_parameter = 1):
    """ Adjust the baseline predictions based on reported results from similar precincts """
    for precinct in precincts:
        if not precinct.reported:
            total_weight = 0
            dem_deviation_sum = 0
            rep_deviation_sum = 0
            turnout_deviation_sum = 0

            for similar_id, distance in precinct.similar_precincts:
                similar_precinct = next((p for p in precincts if p.id == similar_id), None)
                if similar_precinct and similar_precinct.reported and distance > 0:  # Ensure valid distance
                    weight = 1 / distance  # Weight inversely proportional to the distance
                    dem_deviation = similar_precinct.actual_dem - similar_precinct.estimated_dem
                    rep_deviation = similar_precinct.actual_rep - similar_precinct.estimated_rep
                    turnout_deviation = similar_precinct.actual_turnout - similar_precinct.estimated_turnout
                    dem_deviation_sum += dem_deviation * weight
                    rep_deviation_sum += rep_deviation * weight
                    turnout_deviation_sum += turnout_deviation * weight
                    total_weight += weight

            if total_weight > 0:
                reporting_factor = hyper_parameter # Apply sigmoid to scale the impact
                precinct.adjusted_dem += (dem_deviation_sum / total_weight) * reporting_factor
                precinct.adjusted_rep += (rep_deviation_sum / total_weight) * reporting_factor
                precinct.adjusted_turnout += (turnout_deviation_sum / total_weight) * reporting_factor

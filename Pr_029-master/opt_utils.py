"""
A collection of functions for computing the cost function and optimizing it
"""
from sklearn.metrics.pairwise import pairwise_distances
import numpy as np

# SCALE_FACTOR = 500

def LinCostClosest(crime_locs, car_locs):
    """
    Calculates the distance from each crime point to the nearest police car and returns the sum
    """
    dist = pairwise_distances(crime_locs,car_locs)
    min_dist = np.amin(dist, axis=1)
    cost = np.sum(min_dist)
    return cost

def LinCostAll(crime_locs, car_locs):
    """
    Calculates the distance from each crime point to the nearest police car and returns the sum
    """
    dist = pairwise_distances(crime_locs,car_locs)
    min_dist = np.mean(dist, axis=1)
    cost = np.sum(min_dist)
    return cost

def LinCostWeight(crime_locs, car_locs, weight):
    return LinCostClosest(crime_locs, car_locs)*weight + LinCostClosest(crime_locs, car_locs)* (1-weight)

def PerturbCars(car_locs, SCALE_FACTOR):
    deltas = np.random.rand(car_locs.shape[0], car_locs.shape[1])*SCALE_FACTOR
    return car_locs + deltas


def SimpleOptimizeStep(crime_locs, car_locs):
    current_cost = LinCost(crime_locs, car_locs)
    candidate_state = PerturbCars(car_locs)
    candidate_cost = LinCost(crime_locs, candidate_state)
    if candidate_cost < current_cost:
        return candidate_state
    else:
        return car_locs

    
##### KDE FUNCTIONS #####
def KDECostClosest(crime_locs, crime_weights, car_locs):
    """
    Calculates the distance from each crime point to the nearest police car and returns the sum
    """
    dist = pairwise_distances(crime_locs,car_locs)
    min_dist = np.amin(dist, axis=1)
    cost = np.sum(min_dist*crime_weights)
    return cost


def KDECostClosestAll(crime_locs, crime_weights, car_locs):
    """
    Calculates the distance from each crime point to the nearest police car and returns the sum
    """
    n_closest = 3
    dist = pairwise_distances(crime_locs,car_locs)
    dist.sort(axis=1)
    dist = dist[:,:n_closest]
    mean_dist = np.mean(dist, axis=1)
    cost = np.sum(mean_dist*crime_weights)
    return cost

def KDECostWeighted(crime_locs, crime_weights, car_locs):
    return 0.6*KDECostClosest(crime_locs, crime_weights, car_locs) + 0.4*KDECostClosestAll(crime_locs, crime_weights, car_locs)




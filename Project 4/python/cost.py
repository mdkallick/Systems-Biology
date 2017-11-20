import math
import warnings
import numpy as np
from odes import goldbeter_fly
from ode_utils import ode15s
from utils import get_period, get_amps

def simple_island_cost_function( params ):
    if(params[0] < 20 or params[0] > 40):
        cost = math.inf
    elif(params[1] < 10 or params[1] > 50):
        cost = math.inf
    else:
        cost = abs(100 - (params[0]*params[1]*0.1))
    return cost

def goldbeter_fly_cost_function( params ):
    # initial conditions
    M = 1
    P0 = 1
    P1 = 1
    P2 = 1
    PN = 1

    yinit = [M, P0, P1, P2, PN]


    t0 = 0
    tf = 800
    dt = .1
    with warnings.catch_warnings():
        warnings.filterwarnings('error')
        try:
            t, sol = ode15s(goldbeter_fly, yinit, t0, dt, tf, params)
        except (ValueError, UserWarning) as e:
            cost = math.inf
            return cost
    mid = int(len(t)/2)

    desired_per = 23.6
    desired_amp = .1
    with warnings.catch_warnings():
        warnings.filterwarnings('error')
        try:
            per = get_period(sol[mid:, 1], t[mid:])
            amps = get_amps(sol[mid:], t[mid:])
        except RuntimeWarning as e:
            # something went wrong, most likely no oscillation was created
            cost = math.inf
            return cost

    rate = math.log(.001)/.1
    amperrvals = np.exp(np.multiply(amps, rate))
    amperrval = np.sum(amperrvals)

    perrval = math.pow(((per-desired_per)/desired_per),2)

    return (perrval + amperrval)

import math
import warnings
import numpy as np
from odes import goldbeter_fly
from ode_utils import ode15s
from utils import get_period, get_amp

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
    M = .5
    P0 = 1
    P1 = .4
    P2 = .4
    PN = .4

    yinit = [M, P0, P1, P2, PN]


    t0 = 0
    tf = 144
    dt = (tf / 360)
    with warnings.catch_warnings():
        warnings.filterwarnings('error')
        try:
            t, sol = ode15s(goldbeter_fly, yinit, t0, dt, tf, params)
        except (ValueError, UserWarning) as e:
            cost = math.inf
            return cost


    j = 2

    desired_per = 23.6
    lowest_amp = .75
    startup_time = 48
    with warnings.catch_warnings():
        warnings.filterwarnings('error')
        try:
            per = get_period(np.sum(sol[startup_time:-j, 1:4], axis=1),
                                                        t[startup_time:-j])
            amp = get_amp(np.sum(sol[startup_time:-j, 1:4], axis=1),
                                                        t[startup_time:-j])
        except RuntimeWarning as e:
            # something went wrong, most likely no oscillation was created
            cost = math.inf
            return cost

    if(amp < lowest_amp):
        cost = math.inf
    cost = abs(per - desired_per) + (abs(amp - (lowest_amp*2))*.1)

    return cost

import math
import warnings
import numpy as np
from odes import goldbeter_fly
from odes import gonze_goodwin
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
    RelTol = 1e-8
    with warnings.catch_warnings():
        warnings.filterwarnings('error')
        try:
            t, sol = ode15s(goldbeter_fly, yinit, t0, dt, tf, params, rtol=RelTol)
        except (ValueError, UserWarning) as e:
            cost = math.inf
            return cost
    mid = int(len(t)/2)

    desired_per = 23.6
    desired_amp = .1
    with warnings.catch_warnings():
        warnings.filterwarnings('error')
        try:
            per = get_period(t[mid:], sol[mid:, 1])
            amps = get_amps(sol[mid:])
        except RuntimeWarning as e:
            # something went wrong, most likely no oscillation was created
            cost = math.inf
            return cost

    rate = math.log(.001)/.1
    amperrvals = np.exp(np.multiply(amps, rate))
    amperrval = np.sum(amperrvals)

    perrval = math.pow(((per-desired_per)/desired_per),2)

    return (perrval + amperrval)

# function to run the modified Goodwin oscillator as presented in
# Gonze et al, Biophysical Journal, 89:120-129, 2005.
# Abritrary initial conditions
# Modified from Stephanie Taylor's MatLab code for python by Mathias D Kallick
def gonzeGoodwinFullCircadianError2( params ):
    M0 = 1
    P0 = 1
    I0 = 1

    yinit = [M0,P0,I0]

    t0 = 0
    tf = 800
    dt = .1

    # Simulate the model
    RelTol = 1e-8
    with warnings.catch_warnings():
        warnings.filterwarnings('error')
        try:
            t, sol = ode15s(gonze_goodwin, yinit, t0, dt, tf, params, rtol=RelTol);
        except (ValueError, UserWarning) as e:
            cost = math.inf
            return cost
    mid = int(len(t)/2)

    with warnings.catch_warnings():
        warnings.filterwarnings('error')
        try:
            per = get_period(t[mid:], sol[mid:, 1])
            amps = get_amps(sol[mid:])
        except RuntimeWarning as e:
            # something went wrong, most likely no oscillation was created
            cost = math.inf
            return cost

    perrval = math.pow((per-24)/24,2)

    # an amplitude larger than 0.1 is going to have low cost
    rate = math.log(0.001)/0.1;
    amp_errvals = np.exp(np.multiply(rate,amps));

    errval = perrval + np.sum(amp_errvals);

    return errval

def vdpCircadianError( params ):
    # Initial condition and time bounds
    t0 = 0;
    y0 = [2, 0];
    tend = 480;
    dt = .1

    # Get the "true solution"
    tm,ym = ode15s(vdp, y0, t0, dt, tend, params);
    mid = round(len(tm)/2);

    per = get_period(ym[mid:, 1], tm[mid:]);
    perrval = math.pow(((per-24)/24),2)

    return perrval

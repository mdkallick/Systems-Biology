import copy
import numpy as np
from utils import get_period
from utils import get_amps
from ode_utils import ode15s

# where j is the index of the param to perturb and percent is the percent to perturb it by
def relative_sensitivity( cost_func, params, j, percent ):
    params_star = copy.copy(params)
    params_star[j] = (1+percent)*params[j]
    c_p = cost_func( params )
    c_p_star = cost_func( params_star )
    return (c_p_star-c_p)/percent

# Currently only for Gonze-Goodwin period
# TODO: need to think about injecting y_init, and also ti, dt, tend
# TODO: also need to find out how I'm going to calculate period from the output of ode15s
def period_sensitivity( ode_func, params, j, percent,
                        y_init, t0, dt, tf, mid=True):
    params_star = copy.copy(params)
    params_star[j] = (1+percent)*params[j]
    t, sol = ode15s(ode_func, y_init, t0, dt, tf, params)
    t_star, sol_star = ode15s(ode_func, y_init, t0, dt, tf, params_star)
    #ignore the first half of the simulation if mid is True (let the system settle)
    if(mid==True):
        mid = int(len(t)/2)
        per = get_period(t[mid:], sol[mid:, 1])
        per_star = get_period(t_star[mid:], sol_star[mid:, 1])
    else:
        per = get_period( t, y[0] )
        per_star = get_period( t_star, y_star[0] )
    return (per_star-per)/percent

# TODO: need to think about injecting y_init, and also ti, dt, tend
# TODO: also need to find out how I'm going to calculate amplitude from the output of ode15s
def amp_sensitivity( ode_func, params, j, percent,
                        y_init, t0, dt, tf, mid=True):
    params_star = copy.copy(params)
    params_star[j] = (1+percent)*params[j]
    t, sol = ode15s(ode_func, y_init, t0, dt, tf, params)
    t_star, sol_star = ode15s(ode_func, y_init, t0, dt, tf, params_star)
    if(mid==True):
        mid = int(len(t)/2)
        amp = get_amps( sol[mid:] )
        amp_star = get_amps( sol_star[mid:] )
    else:
        amp = get_amps( y )
        amp_star = get_amps( y_star )
    return (np.sum(amp_star)-np.sum(amp))/percent

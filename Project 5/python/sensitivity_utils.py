import copy
from utils import get_period
from utils import get_amps

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
def period_sensitivity( ode_func, params, j, percent ):
    params_star = copy.copy(params)
    params_star[j] = (1+percent)*params[j]
    t, y = ode15s(ode_func, y_init, 0, .1, 1000, params)
    per = get_period( t, y[0] )
    t_star, y_star = ode15s(ode_func, y_init, 0, .1, 1000, params_star)
    per_star = get_period( t_star, y_star[0] )
    return (per_star-per)/percent

# TODO: need to think about injecting y_init, and also ti, dt, tend
# TODO: also need to find out how I'm going to calculate amplitude from the output of ode15s
def amp_sensitivity( ode_func, params, j, percent ):
    params_star = copy.copy(params)
    params_star[j] = (1+percent)*params[j]
    t, y = ode15s(ode_func, y_init, 0, .1, 1000, params)
    amp = get_amps( y[0] )
    t_star, y_star = ode15s(ode_func, y_init, 0, .1, 1000, params_star)
    amp_star = get_amps(  )
    return (amp_star-amp)/percent

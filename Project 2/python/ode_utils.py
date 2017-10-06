import numpy as np
from scipy.integrate import odeint
from scipy.integrate import ode
import math

"""
Where the input is an array big enough for every timestep, which also can change at
every timestep.

TODO: add error checking to make sure that inputs is the right size (given t0, dt, and tf)
"""


def ode15s(function, yinit, t0, dt, tf, params, inputs=None):
    if (inputs is not None):
        inputs = np.array([inputs])
        params = np.array([params])
        params = np.repeat(params, inputs.shape[1], axis=0).T
        params = np.concatenate([params, inputs], axis=0)
        r = set_ode15s(function, yinit, t0, params[:, 0])

    if (inputs is None):
        r = set_ode15s(function, yinit, t0, params)

    t = np.arange(t0, tf + (dt * 2), dt)

    sol = np.zeros((t.shape[0], len(yinit)))
    sol[0] = yinit

    i = 0
    if (inputs is None):
        while r.successful() and r.t < tf:
            i += 1
            sol[i] = r.integrate(r.t + dt)

    elif (inputs is not None):
        while r.successful() and r.t < tf:
            i += 1
            sol[i] = r.integrate(r.t + dt)
            r = set_ode15s(function, r.y, r.t, params[:, i])

    return t, sol


def set_ode15s(function, yinit, t0, params):
    return ode(function).set_f_params(params).set_initial_value(yinit, t0).set_integrator('vode', method='bdf', order=5)


def hill(X, K, n):
    return (math.pow(K, n) / (math.pow(K, n) + math.pow(X, n)))


# returns index of nearest value in the array
def find_nearest(array, value):
    return (np.abs(array - value)).argmin()

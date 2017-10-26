import numpy as np
from scipy.integrate import odeint
from scipy.integrate import ode
import math

"""
Where the input is an array big enough for every timestep, which also can change at
every timestep.
"""


def ode15s(function, yinit, t0, dt, tf, params, inputs=None):
    t = np.arange(t0, tf + (dt * 2), dt)    
    
    if (inputs is not None):
        inputs = np.array([inputs])
        if(inputs.shape[0] != t.shape[0]):
            raise Exception("Size of input matrix does not match the number of time steps")
        params = np.array([params])
        params = np.repeat(params, inputs.shape[1], axis=0).T
        params = np.concatenate([params, inputs], axis=0)
        r = set_ode15s(function, yinit, t0, params[:, 0])

    if (inputs is None):
        r = set_ode15s(function, yinit, t0, params)



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

def ode_func(function, yinit, t0, dt, tf, params, method, inputs=None):
    if (inputs is not None):
        inputs = np.array([inputs])
        params = np.array([params])
        params = np.repeat(params, inputs.shape[1], axis=0).T
        params = np.concatenate([params, inputs], axis=0)
        
    if (method == 'forward_euler'):
        stepfunc = forward_euler
    elif (method == 'explicit_trapezoid'):
        stepfunc = explicit_trapezoid

    t = np.arange(t0, tf + (dt), dt)

    sol = np.zeros((t.shape[0], len(yinit)))
    sol[0] = yinit

    i = 0
    for i in range(t.shape[0] - 1):
        if (inputs is None):
            p = params
        elif (inputs is not None):
            p = params[i+1]

        sol[i+1] = stepfunc(function, t, dt, sol[i], p)
        
    return t, sol

def forward_euler(function, t, dt, prev, params):
    return prev + (dt * function(t, prev, params))

def explicit_trapezoid(function, t, dt, prev, params):
    pred_step = function(t, forward_euler(function, t, dt, prev, params), params)
    return prev + (.5 * dt * (function(t, prev, params) + pred_step))

def pred_ode_func(function, yinit, t0, tf, EST, params,
					dt_init=float(tf-t0)/100., dt_out=None, inputs=None):
	if (inputs is not None):
        inputs = np.array([inputs])
        params = np.array([params])
        params = np.repeat(params, inputs.shape[1], axis=0).T
        params = np.concatenate([params, inputs], axis=0)

	t_cur = t0
	t = [t_cur]
	h = dt_init

	if (dt_out != None):
		t_out = np.arange(t0, tf + (dt_out), dt_out)
		tmp_t = t_cur

    sol = np.zeros((t.shape[0], len(yinit)))
    sol[0] = yinit
    sol_out = sol

    i = 0
    if (dt_out != None):
	    j = 0
    while (t_cur < tf):
        if (inputs is None):
            p = params
        elif (inputs is not None):
            p = params[i+1]

		tmp_sol = forward_euler(function, t_cur, h, sol[i], p)
		tmp_pred_sol = explicit_trapezoid(function, t_cur, h, sol[i], p)

		err = np.linalg.norm(tmp_pred_sol - tmp_sol)

		h_new = h * math.pow((.9 * EST/err), .5)
		if (h_new > 2 * h):
			h_new = 2 * h

		if (err <= EST):
	        sol[i+1] = tmp_sol
	    	t_cur = t_cur + h
	    	if(t_cur + h > tf):
	    		h_new = tf - t_cur
	    	t.append(t_cur)

			if (dt_out != None):
				while (tmp_t < t_cur):
					slope = float(sol[i+1] - sol[i])/h
					sol_out[j+1] = sol_out[j] + (dt_out * slope)
					j = j + 1
					tmp_t = tmp_t + dt_out


		h = h_new

    if (dt_out != None):
		return t_out, sol_out
	else:
	    return t, sol

def hill(X, K, n):
    return (math.pow(K, n) / (math.pow(K, n) + math.pow(X, n)))


# returns index of nearest value in the array
def find_nearest(array, value):
    return (np.abs(array - value)).argmin()

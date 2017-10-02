import numpy as np
from scipy.integrate import odeint
from scipy.integrate import ode
"""
Where the input is an array big enough for every timestep, which also can change at
every timestep.

TODO: add error checking to make sure that inputs is the right size (given t0, dt, and tf)
"""
def ode15s(function, yinit, t0, dt, tf, params, inputs=None):

	if(inputs != None):
		params = np.repeat(params, inputs.shape()[0], axis=0)
		params = np.concatenate(params, inputs)
		print(params)

	  r = ode(function).set_f_params(params[0]).set_integrator('vode', method='bdf', order=5)
	
	elif(inputs == None):
		r = ode(function).set_f_params(params).set_integrator('vode', method='bdf', order=5)

  t = np.arange(t0, tf+(dt*2), dt)

  r.set_initial_value(yinit, t0)

  sol = np.zeros((t.shape[0], 3))
  sol[0] = yinit

  i = 0;
  if(inputs == None):
	while r.successful() and r.t < tf:
		i+=1
		sol[i] = r.integrate(r.t+dt)

	elif(inputs != None):
		while r.successful() and r.t < tf:
		i+=1
		sol[i] = r.integrate(r.t+dt)
		r.set_f_params(params[i])

  return t, sol

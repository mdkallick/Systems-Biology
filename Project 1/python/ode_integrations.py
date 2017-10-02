import numpy as np
from scipy.integrate import odeint
from scipy.integrate import ode

def ode15s(function, yinit, t0, dt, tf, params):
  r = ode(function).set_f_params(params).set_integrator('vode', method='bdf', order=5)

  t = np.arange(t0, tf+(dt*2), dt)

  r.set_initial_value(yinit, t0)

  sol = np.zeros((t.shape[0], 3))
  sol[0] = yinit

  i = 0;
  while r.successful() and r.t < tf:
      i+=1
      sol[i] = r.integrate(r.t+dt)

  return t, sol

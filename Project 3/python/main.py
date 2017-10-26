import numpy as np
import matplotlib.pyplot as plt
from odes import n_degrade, lotka_volterra
from ode_utils import ode15s, find_nearest, ode_func

"""
Degradation
"""

# parameters
alpha = .1
beta = .2

params = [alpha, beta]

# initial conditions
X0 = 1
Y0 = 1

yinit = [X0, Y0]

t0 = 0
dts = np.arange(0.01, 0.09, 0.01)    
tf = 10
for dt in dts:
  t_fe, sol_fe = ode_func(n_degrade, yinit, t0, dt, tf, params, 'forward_euler')
  t_et, sol_et = ode_func(n_degrade, yinit, t0, dt, tf, params, 'explicit_trapezoid')

  # considered "correct", so very small dt
  t, sol = ode15s(n_degrade, yinit, t0, .001, tf, params)

  d = np.abs(sol-sol_fe)
  avg_err = mean(d)

f, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(12, 4), sharey=True)
ax1.plot(t_fe, sol_fe[:, 0], 'g', label='X')
ax1.plot(t_fe, sol_fe[:, 1], 'm', label='Y')
ax1.legend(loc='best')
ax1.set_xlabel('time (s)')
ax1.set_ylabel('concentrations (nM)')
ax1.set_title('Degradation (forward_euler)')
ax1.grid()
ax2.plot(t_et, sol_et[:, 0], 'g', label='X')
ax2.plot(t_et, sol_et[:, 1], 'm', label='Y')
ax2.legend(loc='best')
ax2.set_xlabel('time (s)')
ax2.set_ylabel('concentrations (nM)')
ax2.set_title('Degradation (explicit_trapezoid)')
ax2.grid()
ax3.plot(t, sol[:, 0], 'g', label='X')
ax3.plot(t, sol[:, 1], 'm', label='Y')
ax3.legend(loc='best')
ax3.set_xlabel('time (s)')
ax3.set_ylabel('concentrations (nM)')
ax3.set_title('Degradation (ode15s)')
ax3.grid()
plt.show()

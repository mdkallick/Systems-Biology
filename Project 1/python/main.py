import numpy as np
import matplotlib.pyplot as plt
from odes import dimer_v1
from odes import dimer_w_degr_v1
from ode_integrations import ode15s

"""
Dimerization
"""

# initial conditions
yinit = [2, 3, 1];

k1 = 1; # dimerization rate (in units of nM^-1s^-1)
k2 = 2; # de-dimerization rate (in units of s^-1)
params = [k1,k2]

t, sol = ode15s(dimer_v1, yinit, 0, .001, 10, params)

plt.plot(t, sol[:, 0], 'b', label='P1')
plt.plot(t, sol[:, 1], 'g', label='P2')
plt.plot(t, sol[:, 2], 'm', label='P1P2')
plt.legend(loc='best')
plt.xlabel('time (s)')
plt.ylabel('concentrations (nM)')
plt.title('Dimerization of P1 and P2 into P1P2')
plt.grid()
plt.show()

"""
Dimerization with Degradation
"""

# initial conditions
yinit = [2, 3, 1]

# parameters
k1 = 1 # dimerization rate (in units of nM^-1s^-1)
k2 = .1 # de-dimerization rate (in units of s^-1)
d1 = .1 # degradation rate of P1 (in units of s^-1)
d2 = .1 # degradation rate of P2 (in units of s^-1)
d3 = .1 # degradation rate of P1P2 (in units of s^-1)
params = [k1,k2,d1,d2,d3]

t, sol = ode15s(dimer_w_degr_v1, yinit, 0, .001, 10, params)

plt.plot(t, sol[:, 0], 'b', label='P1')
plt.plot(t, sol[:, 1], 'g', label='P2')
plt.plot(t, sol[:, 2], 'm', label='P1P2')
plt.legend(loc='best')
plt.xlabel('time (s)')
plt.ylabel('concentrations (nM)')
plt.title('Dimerization of P1 and P2 into P1P2 with Degradation')
plt.grid()
plt.show()

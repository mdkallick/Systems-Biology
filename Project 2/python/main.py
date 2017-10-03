import numpy as np
import matplotlib.pyplot as plt
from odes import activator_cascade
from odes import feed_forward
from ode_integrations import ode15s

"""
Activator Cascade
"""

# parameters
vy_max = 1 # (in units of nM^-1s^-1)
ky =  .5 # (in units of nM)
ny = 2
dy = .1
vz_max = 1 # (in units of nM^-1s^-1)
kz = .5 # (in units of nM)
nz = 2
dz = .1

params = [vy_max, ky, ny, dy, vz_max, kz, nz, dz]

#initial conditions
Y0 = 0
Z0 = 0

yinit = [Y0, Z0]

t0 = 0
dt = .1
tf = 150

# Input variable
for i in range(1,2):
    X_star = np.array([0]*500 + [i] * 1002).T

    t, sol = ode15s(activator_cascade, yinit, t0, dt, tf, params, inputs=X_star)

    plt.plot(t, X_star, 'b', label='X*')
    plt.plot(t, sol[:, 0], 'g', label='Y')
    plt.plot(t, sol[:, 1], 'm', label='Z')
    plt.legend(loc='best')
    plt.xlabel('time (s)')
    plt.ylabel('concentrations (nM)')
    plt.title('Activator Cascade')
    plt.grid()
    plt.show()


"""
Feed-Forward Loop
"""

# parameters
vy_max = 1 # (in units of nM^-1s^-1)
ky =  .5 # (in units of nM)
ny = 2
dy = .1
vz_max = 1 # (in units of nM^-1s^-1)
kzx = .5 # (in units of nM)
nzx = 2
kzy = .5 # (in units of nM)
nzy = 2
dz = .1

params = [vy_max, ky, ny, dy, vz_max, kzx, nzx, kzy, nzy, dz]

#initial conditions
Y0 = 0
Z0 = 0

yinit = [Y0, Z0]

t0 = 0
dt = .1
tf = 150

# Input variable
for i in range(1,2):
    X_star = np.array([0]*500 + [i] * 1002).T

    t, sol = ode15s(feed_forward, yinit, t0, dt, tf, params, inputs=X_star)

    plt.plot(t, X_star, 'b', label='X*')
    plt.plot(t, sol[:, 0], 'g', label='Y')
    plt.plot(t, sol[:, 1], 'm', label='Z')
    plt.legend(loc='best')
    plt.xlabel('time (s)')
    plt.ylabel('concentrations (nM)')
    plt.title('Feed-Forward Loop')
    plt.grid()
    plt.show()

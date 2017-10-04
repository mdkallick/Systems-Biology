import numpy as np
import matplotlib.pyplot as plt
from odes import activator_cascade
from odes import feed_forward
from odes import neg_feedback
from ode_utils import ode15s

# """
# Activator Cascade
# """
#
# # parameters
# vy_max = 1 # (in units of nM^-1s^-1)
# ky =  .5 # (in units of nM)
# ny = 2
# dy = .1
# vz_max = 1 # (in units of nM^-1s^-1)
# kz = .5 # (in units of nM)
# nz = 2
# dz = .1
#
# params = [vy_max, ky, ny, dy, vz_max, kz, nz, dz]
#
# #initial conditions
# Y0 = 0
# Z0 = 0
#
# yinit = [Y0, Z0]
#
# t0 = 0
# dt = .1
# tf = 150
#
# # Input variable
# for i in range(1,2):
#     X_star = np.array([0]*500 + [i] * 1002).T
#
#     t, sol = ode15s(activator_cascade, yinit, t0, dt, tf, params, inputs=X_star)
#
#     plt.plot(t, X_star, 'b', label='X*')
#     plt.plot(t, sol[:, 0], 'g', label='Y')
#     plt.plot(t, sol[:, 1], 'm', label='Z')
#     plt.legend(loc='best')
#     plt.xlabel('time (s)')
#     plt.ylabel('concentrations (nM)')
#     plt.title('Activator Cascade')
#     plt.grid()
#     plt.show()
#
#
# """
# Feed-Forward Loop
# """
#
# # parameters
# vy_max = 1 # (in units of nM^-1s^-1)
# ky =  .5 # (in units of nM)
# ny = 2
# dy = .1
# vz_max = 1 # (in units of nM^-1s^-1)
# kzx = .5 # (in units of nM)
# nzx = 2
# kzy = .5 # (in units of nM)
# nzy = 2
# dz = .1
#
# params = [vy_max, ky, ny, dy, vz_max, kzx, nzx, kzy, nzy, dz]
#
# #initial conditions
# Y0 = 0
# Z0 = 0
#
# yinit = [Y0, Z0]
#
# t0 = 0
# dt = .1
# tf = 150
#
# # Input variable
# for i in range(1,2):
#     X_star = np.array([0]*500 + [i] * 1002).T
#
#     t, sol = ode15s(feed_forward, yinit, t0, dt, tf, params, inputs=X_star)
#
#     plt.plot(t, X_star, 'b', label='X*')
#     plt.plot(t, sol[:, 0], 'g', label='Y')
#     plt.plot(t, sol[:, 1], 'm', label='Z')
#     plt.legend(loc='best')
#     plt.xlabel('time (s)')
#     plt.ylabel('concentrations (nM)')
#     plt.title('Feed-Forward Loop')
#     plt.grid()
#     plt.show()

"""
Negative Feedback Loop
From: "A model for circadian oscillations in the Drosophila period protein"
Goldbeter, A. : 1995
"""

# parameters
n = 4
k1 = 2
k2 = 2
k3 = 2
k4 = 2
km = .5
ks = .38
kd = .2
ki = 1
v1 = 3.2
v2 = 1.58
v3 = 5
v4 = 2.5
vm = .65
vd = .95
vs = .76
small_k1 = 1.9
small_k2 = 1.3
params = [n, k1, k2, k3, k4, km, ks, kd, ki, v1, v2, v3, v4, vm, vd, vs,
            small_k1, small_k2]

#initial conditions
M = .5
P0 = .5
P1 = .5
P2 = .5
PN = 1

yinit = [M, P0, P1, P2, PN]

t0 = 0
dt = (72/3600)
tf = 500

t, sol = ode15s(neg_feedback, yinit, t0, dt, tf, params)

plt.plot(t, sol[:, 0], 'b', label='M')
plt.plot(t, sol[:, 1], 'g', label='P0')
plt.plot(t, sol[:, 2], 'm', label='P1')
plt.plot(t, sol[:, 3], 'r', label='P2')
plt.plot(t, sol[:, 4], 'k', label='PN')
plt.legend(loc='best')
plt.xlabel('time / h')
plt.ylabel('PER forms or M')
plt.title('Oscillations in PER over Time')
plt.grid()
plt.show()

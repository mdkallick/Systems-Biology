import numpy as np
import matplotlib.pyplot as plt
from gen_al_utils import ES
from cost import simple_island_cost_function
from cost import goldbeter_fly_cost_function
from ode_utils import ode15s
from odes import goldbeter_fly
from utils import get_period
from utils import get_amps

lb = [0] * 18
ub = [10] * 18
num_parents = 40
num_children = 40
num_generations = 5
mutation = .05

selection_type = 'tournament_select'

P, Pcost = ES(goldbeter_fly_cost_function, selection_type, lb, ub,
                        num_parents, num_children, num_generations, mutation,
                        num_elites=1,
                        tourney_size=4,
                        truncation_thres=.5,
                        eta_minus=.1)

params = P[np.argmin(Pcost)]

# P, Pcost = ES(simple_island_cost_function, selection_type, lb, ub,
#                         num_parents, num_children, num_generations, mutation,
#                         num_elites=0,
#                         tourney_size=4,
#                         truncation_thres=.5,
#                         eta_minus=.1)

# print("P: ", P)
# print("Pcost: ", Pcost)

#
# tourney_size = 4
#
# G, Gcost = tournament_select(P, Pcost, tourney_size, num_parents)
#
# print("G: ", G)
# print("Gcost: ", Gcost)
#
# G, Gcost = truncation_select(P, Pcost, .5)
#
# print("G: ", G)
# print("Gcost: ", Gcost)

# """
# Negative Feedback Loop
# From: "A model for circadian oscillations in the Drosophila period protein"
# Goldbeter, A. : 1995
# """
#
# # parameters
# n = 4
# k1 = 2
# k2 = 2
# k3 = 2
# k4 = 2
# km = .5
# ks = .38
# kd = .2
# ki = 1
# v1 = 3.2
# v2 = 1.58
# v3 = 5
# v4 = 2.5
# vm = .65
# vd = .95
# vs = .76
# small_k1 = 1.9
# small_k2 = 1.3
#
# params = [n, k1, k2, k3, k4, km, kd, ki, v1, v2, v3, v4, vm, vd, vs,
#           small_k1, small_k2, ks]
#
# initial conditions
M = .5
P0 = 1
P1 = .4
P2 = .4
PN = .4

yinit = [M, P0, P1, P2, PN]

t0 = 0
tf = 800
dt = .1

t, sol = ode15s(goldbeter_fly, yinit, t0, dt, tf, params)

j = 2

print(get_period(np.sum(sol[:-j, 1:4], axis=1),t[:-j]))
print(get_amps(sol[:-j],t[:-j]))

plt.plot(t[:-j], sol[:-j, 0], 'b', label='M')
plt.plot(t[:-j], sol[:-j, 1], 'g', label='P0')
plt.plot(t[:-j], sol[:-j, 2], 'm', label='P1')
plt.plot(t[:-j], sol[:-j, 3], 'r', label='P2')
plt.plot(t[:-j], sol[:-j, 4], 'k', label='PN')
plt.plot(t[:-j], np.sum(sol[:-j, 1:4], axis=1), 'c', label='PT')
plt.legend(loc='best')
plt.xlabel('time / h')
plt.ylabel('PER forms or M')
plt.ylim(ymin=0, ymax=5.5)
plt.title('Oscillations in PER over Time')
plt.grid()
plt.show()

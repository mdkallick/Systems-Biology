import os
import numpy as np
import matplotlib.pyplot as plt
from gen_al_utils import ES, GA
from cost import simple_island_cost_function
from cost import goldbeter_fly_cost_function
from ode_utils import ode15s
from odes import goldbeter_fly
from utils import get_period
from utils import get_amps

lb = [0] * 18
ub = [50] * 18
num_parents = 8
num_children = 40
num_generations = 8
mutation = .05

run_type = 'calc'
selection_type = 'evolutionary_strategy'

# run_name = input("enter the run name: ")
#
# if not os.path.exists(run_name):
#     os.makedirs(run_name)
#
# if(run_type == 'calc'):
#     if(selection_type == 'evolutionary_strategy'):
#         P, Pcost = ES(goldbeter_fly_cost_function, lb, ub, num_parents,
#                                     num_children, num_generations, mutation,
#                                     run_name=run_name)
#     else:
#         P, Pcost = GA(goldbeter_fly_cost_function, selection_type, lb, ub,
#                             num_parents, num_children, num_generations, mutation,
#                             num_elites=1,
#                             tourney_size=4,
#                             truncation_thres=.5,
#                             eta_minus=.1,
#                             run_name=run_name)
#
#     params = P[np.argmin(Pcost)]
#     np.savetxt(run_name + '/params.csv', params)
#
# elif(run_type == 'test'):
#     if(selection_type == 'evolutionary_strategy'):
#         P, Pcost = ES(goldbeter_fly_cost_function, lb, ub, num_parents,
#                                     num_children, num_generations, mutation)
#     else:
#         P, Pcost = GA(simple_island_cost_function, selection_type, lb, ub,
#                             num_parents, num_children, num_generations, mutation,
#                             num_elites=0,
#                             tourney_size=4,
#                             truncation_thres=.5,
#                             eta_minus=.1)
#
#     print("P: ", P)
#     print("Pcost: ", Pcost)


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
# parameters
sols = []
init_v_d = 7.373693905413831295e+00
vds = [init_v_d-3,init_v_d-2,init_v_d-1,init_v_d,init_v_d+1,init_v_d+2]
for v_d in vds:
    n = 7.789240172216601366e+00
    K_1 = 4.723385574345797089e+00
    K_2 = 4.416341055766348056e+00
    K_3 = 3.226165081850925542e+00
    K_4 = 7.676774524383656484e+00
    K_m = 9.705226661182379644e+00
    K_d = 3.144345189131494411e+00
    K_I = 5.932895096333227869e+00
    V_1 = 9.240761193183432809e+00
    V_2 = 3.675398184416379443e+00
    V_3 = 4.419510804611295640e+00
    V_4 = 4.777594516344628062e+00
    v_m = 7.595838010803721119e+00
    # v_d = 7.373693905413831295e+00
    v_s = 9.732090670887192374e+00
    k_1 = 9.933699686612648350e+00
    k_2 = 1.610484328327749681e+00
    k_s = 5.417930141693463320e+00

    params = [n,K_1,K_2,K_3,K_4,K_m,K_d,K_I,V_1,V_2,V_3,V_4,v_m,v_d,v_s,k_1,k_2,k_s]
    #
    # initial conditions
    if(run_type == 'calc'):
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

        sols.append(sol)

        j = 2

        print(get_period(np.sum(sol[:-j, 1:4], axis=1),t[:-j]))
        print(get_amps(sol[:-j],t[:-j]))

        # plt.plot(t[:-j], sol[:-j, 0], 'b', label='M')
        # plt.plot(t[:-j], sol[:-j, 1], 'g', label='P0')
        # plt.plot(t[:-j], sol[:-j, 2], 'm', label='P1')
        # plt.plot(t[:-j], sol[:-j, 3], 'r', label='P2')
        # plt.plot(t[:-j], sol[:-j, 4], 'k', label='PN')
        # plt.plot(t[:-j], np.sum(sol[:-j, 1:4], axis=1), 'c', label='PT')
        # plt.legend(loc='best')
        # plt.xlabel('time / h')
        # plt.ylabel('PER forms or M')
        # plt.ylim(ymin=0, ymax=5.5)
        # plt.title('Oscillations in PER over Time')
        # plt.grid()
        # plt.show()

f, axs = plt.subplots(2, 3, figsize=(9, 9), sharey=True)
i, j, k = [0, 0, 0]
for sol in sols:
    f.suptitle('Oscillations in PER over Time')
    cur = j + i
    axs[k][i].plot(t[:-2], sol[:-2, 0], 'b', label='M')
    axs[k][i].plot(t[:-2], sol[:-2, 1], 'g', label='P0')
    axs[k][i].plot(t[:-2], sol[:-2, 2], 'm', label='P1')
    axs[k][i].plot(t[:-2], sol[:-2, 3], 'r', label='P2')
    axs[k][i].plot(t[:-2], sol[:-2, 4], 'k', label='PN')
    axs[k][i].plot(t[:-2], np.sum(sol[:-2, 1:4], axis=1), 'c', label='PT')
    # axs[k][i].plot(ts[cur], np.abs(np.subtract(sol[:,0], tss[cur][:,0])),
    #                                                     'r-', label='x error')
    # axs[k][i].plot(ts[cur], np.abs(np.subtract(sol[:,1], tss[cur][:,1])),
    #                                                     'b-', label='y error')
    axs[k][i].legend(loc='best')
    axs[k][i].set_xlabel('time (s)')
    axs[k][i].set_ylabel('concentrations (nM)')
    axs[k][i].set_title('v_d = ' + str(round(vds[cur],2)))
    axs[k][i].set_ylim([0,30])
    axs[k][i].grid()
    if(i == 2):
        j = j + 3
        i = 0
        k = k + 1
    else:
        i = i + 1

plt.show()

import os
import numpy as np
import matplotlib.pyplot as plt
from gen_al_utils import ES, GA
from cost import simple_island_cost_function
from cost import gonzeGoodwinFullCircadianError2
from ode_utils import ode15s
from odes import gonze_goodwin
from utils import get_period
from utils import get_amps

def get_params(run_type, selection_type,
                lb, ub, num_parents, num_children,
                num_generations, mutation):
    if(run_type == 'calc'):
        if(selection_type == 'evolutionary_strategy'):
            P, Pcost = ES(gonzeGoodwinFullCircadianError2, lb, ub, num_parents,
                                        num_children, num_generations, mutation)
        else:
            P, Pcost = GA(gonzeGoodwinFullCircadianError2, selection_type, lb, ub,
                                num_parents, num_children, num_generations, mutation,
                                num_elites=1,
                                tourney_size=4,
                                truncation_thres=.5,
                                eta_minus=.1)

        params = P[np.argmin(Pcost)]

    elif(run_type == 'test'):
        if(selection_type == 'evolutionary_strategy'):
            P, Pcost = ES(simple_island_cost_function, lb, ub, num_parents,
                                        num_children, num_generations, mutation)
        else:
            P, Pcost = GA(simple_island_cost_function, selection_type, lb, ub,
                                num_parents, num_children, num_generations, mutation,
                                num_elites=0,
                                tourney_size=4,
                                truncation_thres=.5,
                                eta_minus=.1)

        print("P: ", P)
        print("Pcost: ", Pcost)
        return None

    return params

lb = [0] * 11
# lower upper bound for n (overflow errors happen otherwise)
ub = [10] + [100] * 10
num_parents = 100
num_children = 100
num_generations = 10
mutation = .05

num_params = 10
param_mat = np.zeros([num_params,len(lb)])

for i in range(num_params):
    param_mat[i,:] = get_params('calc', 'tournament_select',
                              lb, ub, num_parents, num_children,
                              num_generations, mutation)

np.savetxt('gen_params.csv', param_mat.T, delimiter=',')

#
# M0 = 1
# P0 = 1
# I0 = 1
#
# yinit = [M0,P0,I0]
#
# t, sol = ode15s(gonze_goodwin, yinit, 0, .01, 800, params)
#
# mid = int(len(t)/2)
#
# plt.plot(t[mid:], sol[mid:, 0], 'b', label='X')
# plt.plot(t[mid:], sol[mid:, 1], 'g', label='Y')
# plt.plot(t[mid:], sol[mid:, 2], 'm', label='Z')
# plt.legend(loc='best')
# plt.xlabel('time (s)')
# plt.ylabel('concentrations (nM)')
# plt.title('Gonze Goodwin Model')
# plt.grid()
# plt.show()

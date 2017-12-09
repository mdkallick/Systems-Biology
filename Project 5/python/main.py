import os
import numpy as np
import matplotlib.pyplot as plt
from ode_utils import ode15s
from odes import gonze_goodwin
from odes import goldbeter_fly
from cost import simple_island_cost_function
from cost import gonzeGoodwinFullCircadianError2
from cost import goldbeter_fly_cost_function
from utils import get_period
from utils import get_amps
from utils import update_progress
from gen_al_utils import get_params
from sensitivity_utils import amp_sensitivity
from sensitivity_utils import period_sensitivity

"""
Generate and save 10 excellent parameter sets
(takes a long time - only needs to happen once, not every run)
"""

# lb = [0] * 18
# # lower upper bound for n (overflow errors happen otherwise)
# ub = [10] + [50] * 17
# num_parents = 40
# num_children = 40
# num_generations = 8
# mutation = .05
#
# num_params = 1
# param_mat = np.zeros([num_params,len(lb)])
#
# for i in range(num_params):
#     param_mat[i,:] = get_params('tournament_select', goldbeter_fly_cost_function,
#                               lb, ub, num_parents, num_children,
#                               num_generations, mutation)
#
# np.savetxt('gen_params_goldbeter.csv', param_mat.T, delimiter=',')

"""
Analyze sensitivities of the parameter sets
"""

param_mat = np.loadtxt('gen_params_goldbeter.csv', delimiter=',')

percent_perturb = .01

period_sensitivities = []
amp_sensitivities = []
for i in range(param_mat.shape[1]):
    params = param_mat[:,i]
    M = 1
    P0 = 1
    P1 = 1
    P2 = 1
    PN = 1

    y_init = [M, P0, P1, P2, PN]


    t0 = 0
    dt = .1
    tf = 800

    param_per_sensitivities = []
    param_amp_sensitivities = []
    for j in range(param_mat.shape[0]):
        update_progress((j+(i*param_mat.shape[0]))/(param_mat.shape[0]*param_mat.shape[1]))
        per_sens = period_sensitivity(goldbeter_fly, params, j, percent_perturb,
                                            y_init, t0, dt, tf, mid=True)
        param_per_sensitivities.append(per_sens)
        amp_sens = amp_sensitivity(goldbeter_fly, params, j, percent_perturb,
                                            y_init, t0, dt, tf, mid=True)
        param_amp_sensitivities.append(amp_sens)

    period_sensitivities.append(param_per_sensitivities)
    amp_sensitivities.append(param_amp_sensitivities)

update_progress(1)

param_names = ['n','K_1','K_2','K_3','K_4','K_m','K_d','K_I','V_1','V_2',
                'V_3','V_4','v_m','v_d','v_s','k_1','k_2','k_s']

percent_perturb = percent_perturb*100

i=1
x = range(param_mat.shape[0])
for param_set_per_sens in period_sensitivities:
    plt.plot(x, param_set_per_sens, '.', label='Parameter Set ' + str(i))
    i+=1
plt.xticks(x, param_names)
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.axhline(0, alpha=.3, color='black')
plt.xlabel('Parameter Name')
plt.ylabel('Sensitivity to ' + str(percent_perturb) + '% Perturbation')
plt.title('Parameter Sensitivity in the Goldbeter Fly Model (Measuring Change in Period)')
plt.savefig('../plots/gf_period_sens_' + str(percent_perturb) + '.png', bbox_inches='tight')

plt.clf()

i=1
x = range(param_mat.shape[0])
for param_set_amp_sens in amp_sensitivities:
    plt.plot(x, param_set_amp_sens, '.', label='Parameter Set ' + str(i))
    i+=1
plt.xticks(x, param_names)
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.axhline(0, alpha=.3, color='black')
plt.xlabel('Parameter Name')
plt.ylabel('Sensitivity to ' + str(percent_perturb) + '% Perturbation')
plt.title('Parameter Sensitivity in the Goldbeter Fly Model (Measuring Change in Amplitude)')
plt.savefig('../plots/gf_amp_sens_' + str(percent_perturb) + '.png', bbox_inches='tight')

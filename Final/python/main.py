import os
import numpy as np
import matplotlib.pyplot as plt
from ode_utils import ode15s
from odes import becker_weimann
from utils import update_progress
from sensitivity_utils import period_sensitivity_becker
import time

"""
becker_weimann
"""
# found by running the system for 1000 steps - doesn't require startup time, makes
# sensitivity analysis quicker
yinit = [ 0.73596498,1.17439347,1.86399739,1.70414403,0.69847778,0.79337722,0.86097782]

#parameters
v1b = 9
k1b = 1
k1i = .56
c = .01
p = 8
k1d = .12
k2b = .3
q = 2
k2d = .05
k2t = .24
k3t = .02
k3d = .12
v4b = 3.6
k4b = 2.16
r = 3
k4d = .75
k5b = .24
k5d = .06
k5t = .45
k6t = .06
k6d = .12
k6a = .09
k7a = .003
k7d = .09

params = [v1b, k1b, k1i, c, p, k1d, k2b, q, k2d, k2t, k3t, k3d, v4b, k4b,
            r, k4d, k5b, k5d, k5t, k6t, k6d, k6a, k7a, k7d]

RelTol = 1e-6
AbsTol = 1e-8

"""
Sensitivity Analysis
"""

percent_perturb = .01
t0 = 0
dt = .1
tf = 200

param_per_sensitivities = []
for j in range(len(params)):
    update_progress(j/len(params))
    per_sens = period_sensitivity_becker(becker_weimann, params, j, percent_perturb,
                                            yinit, t0, dt, tf)
    param_per_sensitivities.append(per_sens)

period_sensitivities = [param_per_sensitivities]

x = range(len(params))
i=1
for param_set_per_sens in period_sensitivities:
    plt.plot(x, param_set_per_sens, '.', label='Parameter Set ' + str(i))
    i+=1
plt.axhline(0, alpha=.3, color='black')
plt.xlabel('Parameter Name')
plt.ylabel('Sensitivity to ' + str(percent_perturb) + '% Perturbation')
plt.title('Parameter Sensitivity in the Goldbeter Fly Model (Measuring Change in Period)')
plt.savefig('../plots/gf_period_sens_' + str(percent_perturb) + '.png', bbox_inches='tight')


"""
Generate Fig. 3A
"""

# start = time.time()
# t, sol = ode15s(becker_weimann, yinit, 0, .01, 1000, params, rtol=RelTol, atol=AbsTol)
# end = time.time()
# runtime = end-start
# print("runtime, ode15s (s): ", runtime)
#
#
# print("sol[-1,:]:", sol[-1,:])
# t, sol = ode15s(becker_weimann, sol[-1,:], 0, .01, 50, params, rtol=RelTol, atol=AbsTol)
#
# plt.plot( t, sol[:,0], 'r--' )
# plt.plot( t, sol[:,2], 'r' )
# plt.plot( t, sol[:,3], 'g--' )
# plt.plot( t, sol[:,6], 'g' )
# plt.plot( t, np.add(np.add(sol[:,4],sol[:,5]),sol[:,6]), 'b' )
# plt.legend( ['Per2/CRY mRNA','Per2/CRY complex in nucleus','Bmal1 mRNA',
#             'transcriptionally active BMAL1*', 'total BMAL1 protein'] )
# plt.title('Becker-Weimann Feedback Loop')
# plt.xlabel('time (s)')
# plt.ylabel('concentration (nM)')
# plt.show()

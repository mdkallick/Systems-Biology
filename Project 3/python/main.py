import time
import numpy as np
import matplotlib.pyplot as plt
from odes import n_degrade, lotka_volterra
from ode_utils import ode15s, find_nearest, ode_func, pred_ode_func

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
dt = .001
tf = 100

starttime = time.clock()
t_rk4_deg, sol_rk4_deg = ode_func(n_degrade, yinit, t0, dt, tf, params, 'RK4')
endtime = time.clock()
print("rk4 runtime: {}".format(endtime-starttime))


# parameters
alpha = .25
beta = .01
gamma = 1
delta = .01

params = [alpha, beta, gamma, delta]

# initial conditions
X0 = 1
Y0 = 1

yinit = [X0, Y0]

t0 = 0
dt = .01

tf = 100

t_rk4_lv, sol_rk4_lv = ode_func(lotka_volterra, yinit, t0, dt, tf, params, 'RK4')



f, axs = plt.subplots(1, 2, figsize=(8, 4), sharey=False)
f.suptitle('Runge-Kutta 4')
axs[0].plot(t_rk4_deg, sol_rk4_deg[:,0], 'b', label='X')
axs[0].plot(t_rk4_deg, sol_rk4_deg[:,1], 'm', label='Y')
axs[0].legend(loc='best')
axs[0].set_title('Degradation')
axs[0].set_xlabel('time (s)')
axs[0].set_ylabel('concentrations (nM)')
axs[1].plot(t_rk4_lv, sol_rk4_lv[:,0], 'b', label='X')
axs[1].plot(t_rk4_lv, sol_rk4_lv[:,1], 'm', label='Y')
axs[1].legend(loc='best')
axs[1].set_title('Lotka-Volterra')
axs[1].set_xlabel('time (s)')
axs[1].set_ylabel('concentrations (nM)')
plt.grid()
plt.show()

# considered "correct", so very small dt
t, sol = ode15s(n_degrade, yinit, t0, .001, tf, params)

ts = []
sols = []

for dt in dts:
    starttime = time.clock()
    t_fe, sol_fe = ode_func(n_degrade, yinit, t0, dt, tf, params, 'explicit_trapezoid')
    endtime = time.clock()
    ts.append(t_fe)
    sols.append(sol_fe)
    print("forward euler runtime: {}".format(endtime-starttime))
    # starttime = time.clock()
    # t_et, sol_et = ode_func(lotka_volterra, yinit, t0, dt, tf, params, 'explicit_trapezoid')
    # endtime = time.clock()
    # print("explicit trapezoid runtime: {}".format(endtime-starttime))
    # starttime = time.clock()
    # t_rk4, sol_rk4 = ode_func(lotka_volterra, yinit, t0, dt, tf, params, 'RK4')
    # endtime = time.clock()
    # print("RK4 runtime: {}".format(endtime-starttime))

f, axs = plt.subplots(2, 3, figsize=(9, 9), sharey=True)
i, j, k = [0, 0, 0]
for sol in sols:
    f.suptitle('Explicit Trapezoid with Varying dt')
    cur = j + i
    axs[k][i].plot(ts[cur], sol[:,0], 'g', label='X')
    axs[k][i].plot(ts[cur], sol[:,1], 'm', label='Y')
    # axs[k][i].plot(ts[cur], np.abs(np.subtract(sol[:,0], tss[cur][:,0])),
    #                                                     'r-', label='x error')
    # axs[k][i].plot(ts[cur], np.abs(np.subtract(sol[:,1], tss[cur][:,1])),
    #                                                     'b-', label='y error')
    axs[k][i].legend(loc='best')
    axs[k][i].set_xlabel('time (s)')
    axs[k][i].set_ylabel('concentrations (nM)')
    axs[k][i].set_title('dt = ' + str(dts[cur]))
    axs[k][i].grid()
    if(i == 2):
        j = j + 3
        i = 0
        k = k + 1
    else:
        i = i + 1

plt.show()

"""
Lotka Volterra
"""
"""
# parameters
alpha = .25
beta = .01
gamma = 1
delta = .01

params = [alpha, beta, gamma, delta]

# initial conditions
X0 = 1
Y0 = 1

yinit = [X0, Y0]

t0 = 0
dts = np.arange(0.01, .13, 0.02)
tf = 100

# considered "correct", so very small dt
t, sol = ode15s(lotka_volterra, yinit, t0, .001, tf, params)

ts = []
sols = []
tts = []
tss = []

for dt in dts:
    starttime = time.clock()
    t_fe, sol_fe = ode_func(lotka_volterra, yinit, t0, dt, tf, params, 'explicit_trapezoid')
    true_t, true_s = ode15s(lotka_volterra, yinit, t0, dt, tf, params)
    endtime = time.clock()
    ts.append(t_fe)
    sols.append(sol_fe)
    tts.append(true_t[:-1])
    tss.append(true_s[:-1])
    print("forward euler runtime: {}".format(endtime-starttime))
    # starttime = time.clock()
    # t_et, sol_et = ode_func(lotka_volterra, yinit, t0, dt, tf, params, 'explicit_trapezoid')
    # endtime = time.clock()
    # print("explicit trapezoid runtime: {}".format(endtime-starttime))
    # starttime = time.clock()
    # t_rk4, sol_rk4 = ode_func(lotka_volterra, yinit, t0, dt, tf, params, 'RK4')
    # endtime = time.clock()
    # print("RK4 runtime: {}".format(endtime-starttime))



	# d = np.abs(sol-sol_fe)
	#   avg_err = mean(d)

f, axs = plt.subplots(2, 3, figsize=(9, 9), sharey=True)
i, j, k = [0, 0, 0]
for sol in sols:
    f.suptitle('Explicit Trapezoid with Varying dt')
    cur = j + i
    axs[k][i].plot(ts[cur], sol[:,0], 'g', label='X')
    axs[k][i].plot(ts[cur], sol[:,1], 'm', label='Y')
    # axs[k][i].plot(ts[cur], np.abs(np.subtract(sol[:,0], tss[cur][:,0])),
    #                                                     'r-', label='x error')
    # axs[k][i].plot(ts[cur], np.abs(np.subtract(sol[:,1], tss[cur][:,1])),
    #                                                     'b-', label='y error')
    axs[k][i].legend(loc='best')
    axs[k][i].set_xlabel('time (s)')
    axs[k][i].set_ylabel('concentrations (nM)')
    axs[k][i].set_title('dt = ' + str(dts[cur]))
    axs[k][i].grid()
    if(i == 2):
        j = j + 3
        i = 0
        k = k + 1
    else:
        i = i + 1

plt.show()
"""

"""
Testing function for predictive time steps
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
tf = 10

ests = [5e-1, 5e-2, 5e-3, 5e-4, 5e-5, 5e-6]

t_pres = []
s_pres = []
for est in ests:
    t_pre, sol_pre = pred_ode_func(n_degrade, yinit, t0, tf, est, params)#,
                                #dt_out=.1)
    t_pres.append(t_pre)
    s_pres.append(sol_pre)

f, axs = plt.subplots(2, 3, figsize=(12, 8), sharey=True)
i, j, k = [0, 0, 0]
f.suptitle('Size of Predictive Time-Steps with Varying Error Tolerance')
for t_pre in t_pres:
    cur = j + i
    axs[k][i].plot(t_pre[:-1], np.diff(t_pre), 'g', label='X')
    axs[k][i].legend(loc='best')
    axs[k][i].set_xlabel('time (s)')
    axs[k][i].set_ylabel('time step size (s)')
    axs[k][i].set_title('EST = ' + str(ests[cur]))
    axs[k][i].grid()
    if(i == 2):
        j = j + 3
        i = 0
        k = k + 1
    else:
        i = i + 1
f.show()

# plt.plot(t_pre[:-1], dt_pre, 'b', label='time step size')
# plt.legend(loc='best')
# plt.xlabel('time (s)')
# plt.ylabel('time step size (s)')
# plt.title('Size of time steps')
# plt.grid()
# plt.show()

# considered "correct", so very small dt
t, sol = ode15s(n_degrade, yinit, t0, .001, tf, params)

f, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4), sharey=True)
ax1.plot(t_pre, sol_pre[:, 0], 'g', label='X')
ax1.plot(t_pre, sol_pre[:, 1], 'm', label='Y')
ax1.legend(loc='best')
ax1.set_xlabel('time (s)')
ax1.set_ylabel('concentrations (nM)')
ax1.set_title('Degradation (predictive time steps)')
ax1.grid()
ax2.plot(t, sol[:, 0], 'g', label='X')
ax2.plot(t, sol[:, 1], 'm', label='Y')
ax2.legend(loc='best')
ax2.set_xlabel('time (s)')
ax2.set_ylabel('concentrations (nM)')
ax2.set_title('Degradation (ode15s)')
ax2.grid()
plt.show()

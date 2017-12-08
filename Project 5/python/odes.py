import math
import numpy as np
from ode_utils import hill

def goldbeter_fly(t, y, params):
    n = params[0]
    K_1 = params[1]
    K_2 = params[2]
    K_3 = params[3]
    K_4 = params[4]
    K_m = params[5]
    K_d = params[6]
    K_I = params[7]
    V_1 = params[8]
    V_2 = params[9]
    V_3 = params[10]
    V_4 = params[11]
    v_m = params[12]
    v_d = params[13]
    v_s = params[14]
    k_1 = params[15]
    k_2 = params[16]
    k_s = params[17]

    M = y[0]
    P0 = y[1]
    P1 = y[2]
    P2 = y[3]
    PN = y[4]

    dydt = np.zeros(len(y))

    # dydt = [M, P0, P1, P2, PN]

    dydt[0] = v_s*(hill(PN, K_I, n)) - v_m*(M/(K_m + M))
    dydt[1] = k_s*M - V_1*(P0/(K_1 + P0)) + V_2*(P1/(K_2 + P1))
    dydt[2] =( V_1*(P0/(K_1 + P0))
             - V_2*(P1/(K_2 + P1))
             - V_3*(P1/(K_3 + P1))
             + V_4*(P2/(K_4 + P2)) )
    dydt[3] =( V_3*(P1/(K_3 + P1)) \
             - V_4*(P2/(K_4 + P2)) \
             - k_1*P2 + k_2*PN \
             - v_d*(P2/(K_d + P2)) )
    dydt[4] = k_1*P2 - k_2*PN

    return dydt

def gonze_goodwin(t, y, params):
    n = params[0]
    K_1 = params[1]
    K_2 = params[2]
    K_4 = params[3]
    K_6 = params[4]
    v_1 = params[5]
    v_2 = params[6]
    v_4 = params[7]
    v_6 = params[8]
    k_3 = params[9]
    k_5 = params[10]

    X = y[0]
    Y = y[1]
    Z = y[2]

    dydt = np.zeros(len(y))

    # dydt = [X, Y, Z]

    dydt[0] = v_1*hill(K_1, Z, n) - v_2*hill(X, K_2, 1)
    dydt[1] = k_3*X - v_4*hill(Y, K_4, 1)
    dydt[2] = k_5*Y - v_6*hill(Z, K_6, 1)

    return dydt

def vdp(t,y,mu):
    dydt = [y[1], mu[0]*(1-math.pow(y[0],2))*y[1]-y[0]]

    return dydt

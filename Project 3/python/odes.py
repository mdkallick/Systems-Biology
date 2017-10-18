import math
import numpy as np

def n_degrade(t, y, params):

    # dydt = [y1, y1,...,yn]
    dydt = np.multiply(np.negative(params), y)

    return dydt

def lotka_volterra(t, y, params):
    alpha = params[0]
    beta = params[1]
    gamma = params[2]
    delta = params[3]

    X = y[0]
    Y = y[1]

    dydt = [None] * len(y)

    # dydt = [Y, Z]
    dydt[0] = (alpha * X) - (beta * X * Y)
    dydt[1] = (-gamma * Y) + (delta * X * Y)

    return dydt

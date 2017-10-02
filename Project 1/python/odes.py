def dimer_v1( t, y, params ):
    k1 = params[0]
    k2 = params[1]

    P1 = y[0]
    P2 = y[1]
    P1P2 = y[2]

    dydt = [None]*3

    dydt[0] = k2*P1P2 - k1*P1*P2
    dydt[1] = k2*P1P2 - k1*P1*P2
    dydt[2] = k1*P1*P2 - k2*P1P2

    return dydt

def dimer_w_degr_v1( t, y, params ):
    k1 = params[0]
    k2 = params[1]
    d1 = params[2]
    d2 = params[3]
    d3 = params[4]

    P1 = y[0]
    P2 = y[1]
    P1P2 = y[2]

    dydt = [None]*3

    dydt[0] = k2*P1P2 - k1*P1*P2 - d1*P1
    dydt[1] = k2*P1P2 - k1*P1*P2 - d2*P2
    dydt[2] = k1*P1*P2 - k2*P1P2 - d3*P1P2

    return dydt

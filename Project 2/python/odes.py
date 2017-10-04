import math

def activator_cascade( t, y, params ):
    vy_max = params[0]
    ky = params[1]
    ny = params[2]
    dy = params[3]
    vz_max = params[4]
    kz = params[5]
    nz = params[6]
    dz = params[7]

    # This needs to be the last parameter
    X_star = params[8]

    Y = y[0]
    Z = y[1]

    dydt = [None]*len(y)

    dydt[0] = (vy_max*(math.pow(X_star,ny)))/((math.pow(ky,ny)) +
                                        (math.pow(X_star,ny))) - dy*Y
    dydt[1] = (vz_max*(math.pow(Y,nz)))/((math.pow(kz,nz)) +
                                        (math.pow(Y,nz))) - dz*Z

    return dydt

def feed_forward( t, y, params ):
    vy_max = params[0]
    ky = params[1]
    ny = params[2]
    dy = params[3]
    vz_max = params[4]
    kzx = params[5]
    nzx = params[6]
    kzy = params[7]
    nzy = params[8]
    dz = params[9]

    # This needs to be the last parameter
    X_star = params[10]

    Y = y[0]
    Z = y[1]

    dydt = [None]*len(y)

    dydt[0] = (vy_max*(math.pow(X_star,ny)))/((math.pow(ky,ny)) +
                                        (math.pow(X_star,ny))) - dy*Y
    dydt[1] = (vz_max
            *(((math.pow(X_star,nzx)))/((math.pow(kzx,nzx))
            + (math.pow(X_star,nzx))))
            *(((math.pow(Y,nzy)))/((math.pow(kzy,nzy))
            + (math.pow(Y,nzy))))
            ) - dz*Z

    return dydt

def neg_feedback( t, y, params ):
    n = params[0]
    k1 = params[1]
    k2 = params[2]
    k3 = params[3]
    k4 = params[4]
    km = params[5]
    ks = params[6]
    kd = params[7]
    ki = params[8]
    v1 = params[9]
    v2 = params[10]
    v3 = params[11]
    v4 = params[12]
    vm = params[13]
    vd = params[14]
    vs = params[15]
    small_k1 = params[16]
    small_k2 = params[17]

    M = y[0]
    P0 = y[1]
    P1 = y[2]
    P2 = y[3]
    PN = y[4]

    dydt = [None] * len(y)

    # dydt = M, P0, P1, P2, PN
    dydt[0] = (vs*(math.pow(ki,n)/(math.pow(ki,n) + math.pow(PN,n)))
                - vm*(M/(km + M)))
    dydt[1] = ks*M - v1*(P0/(k1 + P0)) + v2*(P1/(k2 + P1))
    dydt[2] = (v1*(P0/(k1 + P0)) - v2*(P1/(k2 + P1))
                    - v3*(P1/(k3 + P1)) + v4*(P2/(k4 + P2)))
    dydt[3] = (v3*(P1/(k3 + P1)) - v4*(P2/(k4 + P2)) - k1*P2
                    + k2*PN - vd*(P2/(kd + P2)))
    dydt[4] = small_k1*P2 - small_k2*PN

    return dydt

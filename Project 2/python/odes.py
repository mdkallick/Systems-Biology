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

    dydt = [None]*2

    # TODO: replace with math.pow
    dydt[0] = (vy_max*(math.pow(X_star,ny)))/((math.pow(ky,ny)) +
                                        (math.pow(X_star,ny))) - dy*Y
    dydt[1] = (vz_max*(math.pow(Y,nz)))/((math.pow(kz,nz)) +
                                        (math.pow(Y,nz))) - dz*Z

    return dydt

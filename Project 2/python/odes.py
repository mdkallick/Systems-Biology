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
    
    dydt = [None]*3

	# TODO: replace with math.pow
    dydt[0] = (vy_max*(X_star^ny))/((ky^ny) + (X_star^ny)) - dy*Y
    dydt[1] = (vz_max*(Y^nz))/((kz^nz) + (Y^nz)) - dz*Z
    
    return dydt

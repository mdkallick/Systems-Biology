import math

def simple_island_cost_function( params ):
    if(params[0] < 20 or params[0] > 40):
        cost = math.inf
    elif(params[1] < 10 or params[1] > 50):
        cost = math.inf
    else:
        cost = abs(100 - (params[0]*params[1]*0.1))
    return cost

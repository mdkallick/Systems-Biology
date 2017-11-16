import numpy as np
import math
import random
random.seed()

# lb: lower bound, ub: upper bound
def ES(cost_func, lb, ub, num_parents, num_children, num_generations, mutation):
    mu = num_parents
    lam = num_children
    all_params = np.zeros([num_generations + 1, num_children, len(lb)])
    all_costs = np.full([num_generations+1,num_children], math.inf)

    P = np.zeros([mu, len(lb)])
    Pcost = np.zeros([mu, 1])
    for i in range(mu):
        P[i,:], Pcost[i] = generate_parent(cost_func, lb, ub)

    all_params[0,0:num_parents,:] = P
    all_costs[0,0:num_parents] = Pcost[:,0]

    for g in range(num_generations):
        print("Creating generation " + str(g))
        G = np.zeros([lam, len(lb)])
        Gcost= np.zeros([1, lam])
        print("Starting generation " + str(g))
        # generate the children for generation g
        for i in range(lam):
            G[i,:], Gcost[:,i] = generate_child(cost_func, P, lb, ub, mutation)

        # assign parents for next generation
        # to do this, I must first sort the children of this generation
        idx = np.argsort(Gcost)
        Gcost = Gcost[:,idx]
        G = G[idx]
        all_params[g+1,:,:] = G
        all_costs[g+1, :] = Gcost
        Pcost = Gcost[0,:,0:mu].T
        P = G[0,0:mu,:]
        print("Best of generation " + str(g) + " has cost " + str(Pcost[0]))

    return P, Pcost

def generate_parent(cost_func, lb, ub):
    params = np.zeros(len(lb))
    cost = math.inf
    for i in range(1000):
        params = np.add(lb, np.multiply(np.random.rand(len(lb)),
                                                np.subtract(ub,lb)))
        cost = cost_func(params)
        if(math.isfinite(cost)):
            return params, cost
    return params, cost

# P : parent pool
def generate_child(cost_func, P, lb, ub, mutation):
    params = np.zeros(len(lb))
    cost = math.inf
    num_parents = len(P[0])
    for i in range(1000):
        P1 = random.choice(P)
        P2 = random.choice(P)

        for j in range(len(lb)):
            # uniform cross-over
            if(random.random() < .5):
                params[j] = P1[j]
            else:
                params[j] = P2[j]

        # mutation
        params = np.add(
                    np.multiply(
                        np.add(1,np.random.randn(len(params)))
                                , mutation)
                                    , params)
        params = np.maximum(params,lb)
        params = np.minimum (params,ub)
        cost = cost_func(params)
        if(math.isfinite(cost)):
            return params, cost
    return params, cost

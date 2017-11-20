import numpy as np
import math
import random
from utils import update_progress
random.seed()

# lb: lower bound, ub: upper bound
def ES(cost_func, selection_func, lb, ub, num_parents,
                num_children, num_generations, mutation, num_elites=0,
                tourney_size=None, truncation_thres=None, eta_minus=None):
    if(selection_func=='tournament_select' and tourney_size==None):
        raise Exception("Tournament size must be specified to use the ",
                        "tournament selection algorithm")
    if(selection_func=='truncation_select' and truncation_thres==None):
        raise Exception("Truncation threshold must be specified to use the ",
                        "truncation selection algorithm")
    if(selection_func=='linear_rank_select' and eta_minus==None):
        raise Exception("Eta minus must be specified to use the ",
                        "linear rank selection algorithm")
    mu = num_parents
    lam = num_children
    all_params = np.zeros([num_generations + 1, num_children, len(lb)])
    all_costs = np.full([num_generations+1,num_children], math.inf)

    P = np.zeros([mu, len(lb)])
    Pcost = np.zeros([mu, 1])
    print("Generating Parents")
    for i in range(mu):
        update_progress(i/(mu-1))
        P[i,:], Pcost[i] = generate_parent(cost_func, lb, ub)

    all_params[0,0:num_parents,:] = P
    all_costs[0,0:num_parents] = Pcost[:,0]

    for g in range(num_generations):
        if(num_elites > 0):
            elite_idx = np.argpartition(Pcost, num_elites, axis=0)
            elites = P[elite_idx][0:num_elites,0]
            elitescost = Pcost[elite_idx][0:num_elites,0]
        print("Creating generation " + str(g))
        G = np.zeros([lam, len(lb)])
        Gcost = np.zeros([lam, 1])
        print("Starting generation " + str(g))
        # generate the children for generation g
        for i in range(lam):
            G[i,:], Gcost[i] = generate_child(cost_func, P, lb, ub, mutation)

        # assign parents for next generation
        if(selection_func == 'tournament_select'):
            P, Pcost = tournament_select(G, Gcost, tourney_size,
                                                num_parents - num_elites)
        elif(selection_func == 'truncation_select'):
            P, Pcost = truncation_select(G, Gcost, truncation_thres,
                                                num_parents - num_elites)
        elif(selection_func == 'linear_rank_select'):
            P, Pcost = linear_rank_select(G, Gcost, eta_minus,
                                                num_parents - num_elites)
        elif(selection_func == 'evolutionary_strategy'):
            # assign parents for next generation
            # to do this, I must first sort the children of this generation
            idx = np.argsort(Gcost[:,0])
            Gcost = Gcost[idx]
            G = G[idx]
            all_params[g+1,:,:] = G
            all_costs[g+1] = Gcost[0]
            Pcost = Gcost[:,0:mu]
            P = G[:,0:mu]
            # print("Pcost: ", Pcost)
        if(num_elites > 0):
            P = np.concatenate([P, elites], axis=0)
            Pcost = np.concatenate([Pcost, elitescost],axis=0)
        print("Best of generation " + str(g) + " has cost " + str(Pcost[np.argmin(Pcost)]))

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

# N is the number of parameter sets returned
# t is the number of parameter sets in each tournament
def tournament_select(P, Pcost, t, N):
    G = np.zeros([N,P.shape[1]])
    Gcost = np.zeros([N,1])
    for i in range(N):
        idx = np.random.choice(P.shape[0],t) # randomly select some indices
        tourney_P = P[idx,:]
        tourney_cost = Pcost[idx,:]
        tourney_winner = np.argmin(tourney_cost)
        G[i] = tourney_P[tourney_winner]
        Gcost[i] = tourney_cost[tourney_winner]
    return G, Gcost

# N is the number of parameter sets returned
# T is the truncation threshold (T in [0,1])
def truncation_select(P, Pcost, T, N):
    T = int(T*P.shape[0])
    idx = np.argsort(Pcost[:,0])
    G = P[idx][0:T]
    Gcost = Pcost[idx][0:T]
    idx = np.random.choice(G.shape[0], N) # randomly select some indices
    G = G[idx]
    Gcost = Gcost[idx]
    return G, Gcost

# N is the number of parameter sets returned
# eta_minus is the reproduction rate of the worst individual
def linear_rank_select(P, Pcost, eta_minus, N):
    s = linear_eq(eta_minus, N)
    # sort P and Pcost by Pcost
    J = np.zeros([N,P.shape[1]])
    Jcost = np.zeros([N,1])
    idx = np.argsort(Pcost[:,0])
    G = P[idx]
    Gcost = Pcost[idx]
    for i in range(N):
        s_idx = np.argwhere(s>random.uniform(0,1))[0,0]
        J[i] = G[s_idx]
        Jcost[i] = Gcost[s_idx]
    return J, Jcost

# N is the number of individuals available to choose
def linear_eq(eta_minus, N):
    eta_term = 2 - 2*eta_minus
    # this lambda function is slightly different from the paper to deal with
    # python indexing - we get i/N-1, not i-1/N-1
    p = np.fromfunction(lambda i, j: (1/N)*(eta_minus + (eta_term*(i/(N-1)))),(N,1))
    s = np.zeros([N,1])
    s[0,0] = p[0,0]
    for i in range(1,N):
        s[i,0] = s[i-1,0] + p[i,0]
    return s

from utils import ES
from cost import simple_island_cost_function

lb = [0,0]
ub = [100,100]
num_parents = 10
num_children = 50
num_generations = 6
mutation = .05

P, Pcost = ES(simple_island_cost_function, lb, ub, num_parents,
                        num_children, num_generations, mutation)

# print(P)
# print(Pcost)

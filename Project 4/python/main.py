from utils import ES
from utils import tournament_select, truncation_select
from cost import simple_island_cost_function

lb = [0,0]
ub = [100,100]
num_parents = 10
num_children = 50
num_generations = 1
mutation = .05

P, Pcost = ES(simple_island_cost_function, lb, ub, num_parents,
                        num_children, num_generations, mutation)

print("P: ", P)
print("Pcost: ", Pcost)

tourney_size = 4

G, Gcost = tournament_select(P, Pcost, tourney_size, num_parents)

print("G: ", G)
print("Gcost: ", Gcost)

G, Gcost = truncation_select(P, Pcost, .5)

print("G: ", G)
print("Gcost: ", Gcost)

from gurobipy import *
import pickle
import networkx as nx

# define the constants
V_NUM = 21
K_NUM = 2
ORIGIN_IDX = 5
MAX = 1e5

# load and generate basic data
f = open("../data/distance", mode="rb")
distance = pickle.load(f)
f.close()
node_time = [9.03,1.8,7.32,7.36,4.2,7.2,15.35,7.52,7.56,15.42815,5.73,7.68,4.2,25.4,25.5,12,12.2008,25.8,15,24.948,5.67]

# failure occurrence
# V_left = [1, 2, 5, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
V_left = [1, 2, 5, 9, 10, 15, 16]
M_IDX = V_left.index(16) + 1
N_IDX = V_left.index(15) + 1
ORIGIN_IDX = V_left.index(ORIGIN_IDX) + 1
SERVICE_TIME = 600

V_left = [e-1 for e in V_left]
V_NUM = len(V_left)
V_l_0 = list(range(V_NUM))
V_l_0.remove(ORIGIN_IDX - 1)
V_l_0_m_n = list(range(V_NUM))
V_l_0_m_n.remove(M_IDX - 1)
V_l_0_m_n.remove(N_IDX - 1)
V_l_0_m_n.remove(ORIGIN_IDX - 1)
V_l_m_n = list(range(V_NUM))
V_l_m_n.remove(M_IDX - 1)
V_l_m_n.remove(N_IDX - 1)

dist = {(i, j, k): distance[V_left[i]][V_left[j]] for i in range(V_NUM) for j in range(V_NUM) for k in range(K_NUM)}
dict_linear = {(i, j, k): i*V_NUM*K_NUM + j*K_NUM + k for i in range(V_NUM) for j in range(V_NUM) for k in range(K_NUM)}

# create a model
MODEL = Model()
# MODEL.setParam('OutputFlag', 0)

# add variables
x = MODEL.addVars(dist.keys(), obj=dist, vtype=GRB.BINARY, name='x')
d = MODEL.addVar(name="d")
MODEL.update()

# set the objective
MODEL.setObjective(d, GRB.MINIMIZE)

# add constraints
MODEL.addConstrs(quicksum(x[i, j, k] for j in range(V_NUM) for k in range(K_NUM)) == 1 for i in V_l_0)
MODEL.addConstrs(quicksum(x[i, j, k] for j in range(V_NUM)) - quicksum(x[j, i, k] for j in range(V_NUM)) == 0 for i in V_l_0_m_n for k in range(K_NUM))
MODEL.addConstr(quicksum(x[i, j, k] for i in range(V_NUM) for j in [M_IDX - 1, N_IDX - 1] for k in range(K_NUM)) == 0)
MODEL.addConstrs(d - SERVICE_TIME * quicksum(x[M_IDX - 1, j, k] for j in range(V_NUM))
                 - quicksum(distance[V_left[i]][V_left[j]] / 1.5 * x[i, j, k]
                            + node_time[V_left[j]] * x[i, j, k] for i in range(V_NUM) for j in range(V_NUM)) >= 0 for k in range(K_NUM))
MODEL.addConstrs(x[i, i, k] == 0 for i in range(V_NUM) for k in range(K_NUM))
MODEL.addConstrs(x[i, j, k] + x[j, i, k] <= 1 for i in range(V_NUM) for j in range(V_NUM) for k in range(K_NUM))
# MODEL.addConstr(quicksum(x[i, ORIGIN_IDX - 1, k] for i in range(V_NUM) for k in range(K_NUM)) == 2)

# callback - use lazy constraints to eliminate sub-tours
def mycallback(model, where):
    if where == GRB.Callback.MIPSOL:
        vals = model.cbGetSolution(model._vars[:-1])
        edges = list((i, j, k) for i, j, k in dict_linear.keys() if vals[dict_linear[(i, j, k)]] > 0.5)
        shortest_cycle, k = cycle(edges)
        if shortest_cycle is not None:
            model.cbLazy(quicksum(x[i, j, k] for i in shortest_cycle for j in shortest_cycle) <= len(shortest_cycle) - 1)


# find the loops
def cycle(edges):
    node_vehicle = {}
    G = nx.DiGraph()
    for e in edges:
        G.add_edge(e[0], e[1])
        node_vehicle[e[0]] = e[2]
        node_vehicle[e[1]] = e[2]
    shortest_subtour = None
    min = V_NUM
    cycle: list
    for cycle in nx.simple_cycles(G):
        if cycle.count(ORIGIN_IDX - 1) == 0:
            if len(cycle) < min:
                min = len(cycle)
                shortest_subtour = cycle
    if shortest_subtour is None:
        k = None
    else:
        k = node_vehicle[shortest_subtour[0]]
    return shortest_subtour, k


MODEL._vars = MODEL.getVars()
MODEL.Params.lazyConstraints = 1
MODEL.optimize(mycallback)

for v in MODEL.getVars():
    if round(v.x, 0) == 1:
        print(v)
print(MODEL.getVarByName('d'))

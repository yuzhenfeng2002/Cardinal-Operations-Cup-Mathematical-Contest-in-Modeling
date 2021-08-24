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
dist = {(i, j, k): distance[i][j] for i in range(V_NUM) for j in range(V_NUM) for k in range(K_NUM)}
dict_linear = {(i, j, k): i*V_NUM*K_NUM + j*K_NUM + k for i in range(V_NUM) for j in range(V_NUM) for k in range(K_NUM)}

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

dmin = 201.24197185085075
origin_list = [2,6,1,5,4,3,7,11,10,19,9,16,20,8,21,14,17,15,18,13,12]
for o in origin_list:
    ORIGIN_IDX = o
    node_list = list(range(ORIGIN_IDX - 1)) + list(range(ORIGIN_IDX, V_NUM))

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
    MODEL.addConstrs(quicksum(x[i, j, k] for j in range(V_NUM) for k in range(K_NUM)) == 1 for i in node_list)
    MODEL.addConstrs(
        quicksum(x[i, j, k] for j in range(V_NUM)) - quicksum(x[j, i, k] for j in range(V_NUM)) == 0 for i in
        range(V_NUM) for k in range(K_NUM))
    MODEL.addConstrs(quicksum(x[ORIGIN_IDX - 1, j, k] for j in range(V_NUM)) == 1 for k in range(K_NUM))
    MODEL.addConstrs(
        d - quicksum(distance[i][j] / 1.5 * x[i, j, k] for i in range(V_NUM) for j in range(V_NUM)) >= 0 for k in
        range(K_NUM))
    MODEL.addConstrs(x[i, i, k] == 0 for i in range(V_NUM) for k in range(K_NUM))
    MODEL.addConstrs(x[i, j, k] + x[j, i, k] <= 1 for i in range(V_NUM) for j in range(V_NUM) for k in range(K_NUM))
    MODEL.addConstr(d <= dmin)

    MODEL._vars = MODEL.getVars()
    MODEL.Params.lazyConstraints = 1
    MODEL.optimize(mycallback)

    try:
        d_val = MODEL.getVarByName('d').x
        if d_val < dmin:
            dmin = d_val
        print(ORIGIN_IDX, MODEL.getVarByName('d'))
    except AttributeError:
        pass

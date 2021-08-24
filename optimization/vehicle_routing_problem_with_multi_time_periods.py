from gurobipy import *
import pickle
import networkx as nx

# define the constants
V_NUM = 8
K_NUM = 3
L_NUM = 3
ORIGIN_IDX = 4
MAX = 1e5

# load and generate basic data
f = open("../data/distance", mode="rb")
distance = pickle.load(f)
f.close()
v = range(V_NUM)
ORIGIN_IDX = v.index(ORIGIN_IDX) + 1
node_list = list(range(ORIGIN_IDX - 1)) + list(range(ORIGIN_IDX, V_NUM))
dist = {(i, j, k, l): distance[v[i]][v[j]] for i in range(V_NUM) for j in range(V_NUM) for k in range(K_NUM) for l in range(L_NUM)}
dict_linear = {(i, j, k, l): i*V_NUM*K_NUM*L_NUM + j*K_NUM*L_NUM + k*L_NUM + l
               for i in range(V_NUM) for j in range(V_NUM) for k in range(K_NUM) for l in range(L_NUM)}

# create a model
MODEL = Model()
# MODEL.setParam('OutputFlag', 0)

# add variables
x = MODEL.addVars(dist.keys(), obj=dist, vtype=GRB.BINARY, name='x')
d = MODEL.addVars(L_NUM, name="d")
MODEL.update()

# set the objective
MODEL.setObjective(quicksum(d[l] for l in range(L_NUM)), GRB.MINIMIZE)

# add constraints
MODEL.addConstrs(quicksum(x[i, j, k, l] for j in range(V_NUM) for k in range(K_NUM) for l in range(L_NUM)) == L_NUM for i in node_list)
MODEL.addConstrs(quicksum(x[i, j, k, l] for j in range(V_NUM) for l in range(L_NUM)) <= 1 for i in node_list for k in range(K_NUM))
MODEL.addConstrs(quicksum(x[i, j, k, l] for j in range(V_NUM)) - quicksum(x[j, i, k, l] for j in range(V_NUM)) == 0
                 for i in range(V_NUM) for k in range(K_NUM) for l in range(L_NUM))
MODEL.addConstrs(quicksum(x[ORIGIN_IDX - 1, j, k, l] for j in range(V_NUM) for k in range(K_NUM)) == 2 for l in range(L_NUM))
MODEL.addConstrs(d[l] - quicksum(distance[v[i]][v[j]] / 1.5 * x[i, j, k, l] for i in range(V_NUM) for j in range(V_NUM)) >= 0
                 for k in range(K_NUM) for l in range(L_NUM))
MODEL.addConstrs(x[i, i, k, l] == 0 for i in range(V_NUM) for k in range(K_NUM) for l in range(L_NUM))
MODEL.addConstrs(x[i, j, k, l] + x[j, i, k, l] <= 1 for i in range(V_NUM) for j in range(V_NUM) for k in range(K_NUM) for l in range(L_NUM))

# callback - use lazy constraints to eliminate sub-tours
def mycallback(model, where):
    if where == GRB.Callback.MIPSOL:
        vals = model.cbGetSolution(model._vars)
        cycles = []
        for l in range(L_NUM):
            for k in range(K_NUM):
                edges = list((i, j, k, l) for i, j, _, _ in dict_linear.keys() if vals[dict_linear[(i, j, k, l)]] > 0.5)
                if cycles.count(edges) == 0:
                    cycles += cycle(edges)
        if len(cycles) != 0:
            for l in range(L_NUM):
                for k in range(K_NUM):
                    for c in cycles:
                        model.cbLazy(quicksum(x[i, j, k, l] for i in c for j in c) <= len(c) - 1)


# find the loops
def cycle(edges):
    G = nx.DiGraph()
    for e in edges:
        G.add_edge(e[0], e[1])
    cycles = []
    cycle: list
    for cycle in nx.simple_cycles(G):
        if cycle.count(ORIGIN_IDX - 1) == 0:
            cycles.append(cycle)
    return cycles


MODEL._vars = MODEL.getVars()
MODEL.Params.lazyConstraints = 1
MODEL.optimize(mycallback)

for v in MODEL.getVars():
    if round(v.x, 0) > 0.5:
        print(v)
# print(MODEL.getVarByName('d'))

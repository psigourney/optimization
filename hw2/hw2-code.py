#! /usr/bin/python

from gurobipy import *
import numpy
import random
from scipy.io import *

##########
# 3) Ex 3.12
#
# minimize:     -2x1 - x2
# st:           x1 - x2 <= 2
#               x1 + x2 <= 6
#               x1,x2 >= 0
##########

print("\nHW2 Problem 3 - Ex.3.12(a)\n****************************************************************")

a = Model("ex3.12")

x1 = a.addVar(vtype=GRB.INTEGER, name="x1")
x2 = a.addVar(vtype=GRB.INTEGER, name="x2")



a.setObjective( (-2 * x1) - (x2), GRB.MINIMIZE)

a.addConstr( x1 >= 0, "constr_positiveX1")
a.addConstr( x2 >= 0, "constr_positiveX2")
a.addConstr( x1 - x2 <= 2, "constr_1")
a.addConstr( x1 + x2 <= 6, "constr_2")

a.optimize()
a.printAttr("x")



##########
# 4) Ex 3.17
#
# minimize:     2x1 + 3x2 + 3x3 + x4 - 2x5
# st:           x1 + 3x2 + 4x4 + x5 = 2
#               x1 + 2x2 - 3x4 + x5 = 2
#               -x1 - 4x2 + 3x3 = 1
#               x1,x2,x3,x4,x5 >= 0
##########


print("\nHW2 Problem 4 - Ex.3.17\n****************************************************************")

b = Model("ex3.17")

x1 = b.addVar(vtype=GRB.INTEGER, name="x1")
x2 = b.addVar(vtype=GRB.INTEGER, name="x2")
x3 = b.addVar(vtype=GRB.INTEGER, name="x3")
x4 = b.addVar(vtype=GRB.INTEGER, name="x4")
x5 = b.addVar(vtype=GRB.INTEGER, name="x5")


b.setObjective( (2 * x1) + (3 * x2) + (3 * x3) + (x4) - (2 * x5), GRB.MINIMIZE)

b.addConstr( x1 >= 0, "constr_positiveX1")
b.addConstr( x2 >= 0, "constr_positiveX2")
b.addConstr( x3 >= 0, "constr_positiveX3")
b.addConstr( x4 >= 0, "constr_positiveX4")
b.addConstr( x5 >= 0, "constr_positiveX5")

b.addConstr( (x1) + (3 * x2) + (4 * x4) + (x5) == 2, "constr_1")
b.addConstr( (x1) + (2 * x2) - (3 * x4) + (x5) == 2, "constr_2")
b.addConstr( (-1 * x1) - (4 * x2) + (3 * x3) == 1, "constr_3")

b.optimize()
b.printAttr("x")




##########
# 5) Ex 3.21
#
##########

print("\nHW2 Problem 5 - Ex.3.21\n****************************************************************")

g = Model("ex3.21")

x1 = g.addVar(vtype=GRB.INTEGER, name="x1") #Process 1
x2 = g.addVar(vtype=GRB.INTEGER, name="x2") #Process 2
x3 = g.addVar(vtype=GRB.INTEGER, name="x3") #Process 3

g.setObjective( (200 * x1) + (60 * x2) + (173 * x3), GRB.MAXIMIZE) #Net profit for one run of each process

g.addConstr( x1 >= 0, "constr_positiveX1")
g.addConstr( x2 >= 0, "constr_positiveX2")
g.addConstr( x3 >= 0, "constr_positiveX3")
g.addConstr( (3 * x1) + (1 * x2) + (5 * x3) <= 8000000, "constr_barrelsCrudeA")
g.addConstr( (5 * x1) + (1 * x2) + (3 * x3) <= 5000000, "constr_barrelsCrudeB")

g.optimize()
g.printAttr("x")




##########
# 6) Ex 7.3
""" The Tournament Problem:  Each of n teams plays against every other team a total of k games.  Assume that every game ends in a win or loss (no ties)
and let x(i) be the number of wins of team i.  Let X be the set of all possible outcome vectors(x(1)....x(n)), Given an arbitrary vector (x(1)...x(n)), we would like 
to determine whether it belongs to X, that is whether it is a possible tournament outcome vector.  Provide a nework flow formulation of this problem.
"""
#
##########

print("\nHW2 Problem 6 - Ex.7.3\n****************************************************************")


print("TODO....\n\n")


##########
# 7) Facility Location problem
""" Company operates 5 plants that produce widgets.  It must meet the demand of 4 warehouses.
Each plant has fixed costs for remaining open.
There are shipping costs.
More plants open means higher fixed costs, but lower transportation costs.

Which plants should the company keep open?  
How much should each plant produce and ship to each warehouse?
Minimize total cost.

"""
#
##########

print("\nHW2 Problem 7\n****************************************************************")

c = Model("FacLoc7")

wh_demand = [15,18,14,20] #demand for the 4 warehouses
plnt_capacity = [20,22,17,19,18] #production capacity for the 5 plants
plnt_fxd_cost = [12000,15000,17000,13000,16000] #fixed costs for keeping each plant open
trans_cost = [[4000, 2000, 3000, 2500, 4500],
              [2500,2600,3400,3000,4000],
              [1200,1800,2600,4100,3000],
              [2200,2600,3100,3700,3200]]

var_matrix = []

# n cols variables (5 plants)
# m rows constraints (4 warehouses)

for m in range(4):
    var_row = []
    for n in range(5):
        name1 = "var_" + str(m) + "," + str(n)
        var_row.append(c.addVar(vtype=GRB.INTEGER, name=name1))
    var_matrix.append(var_row)
    

#                Check each plant( Check each warehouse )
c.setObjective(quicksum(quicksum((trans_cost[m][n] * var_matrix[m][n]) for m in range(4))  for n in range(5)), GRB.MINIMIZE) 
print "\nTODO: add in the fixed cost somehow....\n"
    

for m in range(4): #for each warehouse
    c.addConstr( quicksum(var_matrix[m][n] for n in range(5)) == wh_demand[m], "constr_wh_total_demand_" + str(m) ) #Sum of deliveries == warehouse demand

for n in range(5): #for each factory
    c.addConstr( quicksum(var_matrix[m][n] for m in range(4)) <= plnt_capacity[n], "constr_plnt_total_cap_" + str(n) ) #Sum of deliveries <= plant capacity

for m in range(4):
    for n in range(5):
        c.addConstr( var_matrix[m][n] >= 0 )

c.optimize()
c.printAttr("x")


##########
# 8) Large problem
""" 
Load data from PS2_problem_8.zip
4860 variables.

Minimize:  c'x
st: Ax=b
and lo < x < hi

"""
#
##########

print("\nHW2 Problem 8\n****************************************************************")

d = Model("Large8")


a_matrix = mmread("A.mtx")
b_matrix = mmread("b.mtx")
c_matrix = mmread("c.mtx")
hi_scalar = mmread("upper_bd.mtx")
lo_scalar = mmread("lower_bd.mtx")

expr = LinExpr()

x_list = []

for num in range(len(c_matrix)):
    name1 = "var_" + str(num)
    x_list.append(d.addVar(vtype=GRB.CONTINUOUS, name=name1))
"""
for item in range(len(lo_scalar)):
    name2 = "constr_lo_" + str(item)
    d.addConstr( lo_scalar.tolist()[item] <= x_list[item] , name2)

#d.setObjective( numpy.dot(c_matrix, x_list), GRB.MINIMIZE)

"""

print "a_matrix is ", type(a_matrix)
print "b_matrix is ", type(b_matrix)
print "c_matrix is ", type(c_matrix)
print "hi_scalar is ", type(hi_scalar)
print "lo_scalar is ", type(lo_scalar)
print "x_list is ", type(x_list)

obj = LinExpr()

#for coeff, vari in c_matrix, x_list:
#    obj.AddTerm(item, vari)
    




    
#! /usr/bin/python

from gurobipy import *
import numpy

##########
#Ex 1.14a
##########

print("\nHW1 Ex.1.14(a)\n****************************************************************")

a = Model("ex1.14a")

x = a.addVar(vtype=GRB.INTEGER, name="x")
y = a.addVar(vtype=GRB.INTEGER, name="y")

a.setObjective( (6 * x) + (5.4 * y), GRB.MAXIMIZE)

a.addConstr( x >= 0, "constr_positiveX")
a.addConstr( y >= 0, "constr_positiveY")
a.addConstr( (3 * x) + (4 * y) <= 20000, "constr_machHours")
a.addConstr( (0.3 * x) + (0.38 * y) <= 4000, "constr_cost")

a.optimize()
a.printAttr("x")

##########
#Ex 1.14c
##########

print("\nHW1 Ex.1.14(c)\n****************************************************************")

b = Model("ex1.14c")

x = b.addVar(vtype=GRB.INTEGER, name="x")
y = b.addVar(vtype=GRB.INTEGER, name="y")

b.setObjective( (6 * x) + (5.4 * y), GRB.MAXIMIZE)

b.addConstr( x >= 0, "constr_positiveX")
b.addConstr( y >= 0, "constr_positiveY")
b.addConstr( (3 * x) + (4 * y) <= 22000, "constr_machHours")
b.addConstr( (0.3 * x) + (0.38 * y) <= 3600, "constr_cost")

b.optimize()
b.printAttr("x")

##########
#Ex 1.15a
##########

print("\nHW1 Ex.1.15(a)\n****************************************************************")

c = Model("ex1.15a")

x = c.addVar(vtype=GRB.INTEGER, name="x")
y = c.addVar(vtype=GRB.INTEGER, name="y")

c.setObjective( (7.8 * x) + (7.1 * y), GRB.MAXIMIZE)

c.addConstr( x >= 0, "constr_positiveX")
c.addConstr( y >= 0, "constr_positiveY")
c.addConstr( (0.25 * x) + (0.33 * y) <= 90, "constr_assemblyHours")
c.addConstr( (0.125 * x) + (0.33 * y) <= 80, "constr_testingHours")

c.optimize()
c.printAttr("x")

##########
#Ex 1.15b(i)
##########

print("\nHW1 Ex.1.15(b.1)\n****************************************************************")

d = Model("ex1.15b.1")

x = d.addVar(vtype=GRB.INTEGER, name="x")
y = d.addVar(vtype=GRB.INTEGER, name="y")
z = d.addVar(vtype=GRB.INTEGER, name="z") #Overtime assembly

d.setObjective( (7.8 * x) + (7.1 * y) - (7 * z), GRB.MAXIMIZE)

d.addConstr( x >= 0, "constr_positiveX")
d.addConstr( y >= 0, "constr_positiveY")
d.addConstr( z >= 0, "constr_positiveZ")
d.addConstr( (0.25 * x) + (0.33 * y) - (z) <= 90, "constr_assemblyHours")
d.addConstr( (0.125 * x) + (0.33 * y) <= 80, "constr_testingHours")
d.addConstr( z <= 50, "constr_maxOTHours")

d.optimize()
d.printAttr("x")

##########
#Ex 1.15b(ii)
##########

print("\nHW1 Ex.1.15(b.2)\n****************************************************************")

e = Model("ex1.15b.2.1")

x = e.addVar(vtype=GRB.INTEGER, name="x")
y = e.addVar(vtype=GRB.INTEGER, name="y")

e.setObjective( (7.92 * x) + (7.19 * y), GRB.MAXIMIZE)

e.addConstr( x >= 0, "constr_positiveX")
e.addConstr( y >= 0, "constr_positiveY")
e.addConstr( (1.2 * x) + (0.9 * y) >= 300, "constr_10pctDiscount")
e.addConstr( (0.25 * x) + (0.33 * y) <= 90, "constr_assemblyHours")
e.addConstr( (0.125 * x) + (0.33 * y) <= 80, "constr_testingHours")

e.optimize()

print("\nWith 10% Discount:")
e.printAttr("x")
print("\n (no change from 1.15a without the discount) \n")



##########
#Ex 1.16
##########

print("\nHW1 Ex.1.16\n****************************************************************")

g = Model("ex1.16")

x = g.addVar(vtype=GRB.INTEGER, name="x") #Process 1
y = g.addVar(vtype=GRB.INTEGER, name="y") #Process 2
z = g.addVar(vtype=GRB.INTEGER, name="z") #Process 3

g.setObjective( (200 * x) + (60 * y) + (173 * z), GRB.MAXIMIZE) #Net profit for one run of each process

g.addConstr( x >= 0, "constr_positiveX")
g.addConstr( y >= 0, "constr_positiveY")
g.addConstr( z >= 0, "constr_positiveZ")
g.addConstr( (3 * x) + (1 * y) + (5 * z) <= 8000000, "constr_barrelsCrudeA")
g.addConstr( (5 * x) + (1 * y) + (3 * z) <= 5000000, "constr_barrelsCrudeB")

g.optimize()
g.printAttr("x")



##########
#Ex Part 2 Problem 1
##########

print("\nHW1 Part 2, Problem 1\n****************************************************************")

h = Model("p1")
costs = numpy.load("cost.npy")

N = range(len(costs[0]))

array2 = []

#Create NxN array of binary variables
for i in N:
	newArray = []
	for j in N:
		name1 = "constr_" + str(i) + "_" + str(j)
		newArray.append(h.addVar(vtype=GRB.BINARY, name=name1))
	array2.append(newArray)

h.setObjective(quicksum(quicksum(costs[i][j] * array2[i][j] for j in N) for i in N), GRB.MINIMIZE)

for j in N:
	h.addConstr(quicksum(array2[i][j] for i in N) == 1, "constr_i")
for i in N:
	h.addConstr(quicksum(array2[i][j] for j in N) == 1, "constr_j")

h.optimize()

for x in N:
	print array2[0][x]

for x in N:
        print array2[1][x]

#Appears to be working correctly... only one 1.0 value per row




##########
#Ex Part 2 Problem 3
##########

print("\nHW1 Part 2, Problem 3\n****************************************************************")

i = Model("p3")

data = [1,666,3,704,8,94,46,22356,4,78]
print "Array: ", data

#Find 5 largest values
R = 5
print "Find ", R, " largest values."


N = range(len(data))

indicator = []

#Create NxN array of binary variables
for j in N:
	name1 = "constr_" + str(j)
	indicator.append(i.addVar(vtype=GRB.BINARY, name=name1))

i.setObjective(quicksum(data[x] * indicator[x] for x in N), GRB.MAXIMIZE)

i.addConstr(quicksum(indicator[i] for i in N) == R, "constr_R")
    
for k in N:
	i.addConstr(indicator[k] <= 1)
	i.addConstr(indicator[k] >= 0)

i.optimize()

for x in N:
	print data[x]

for x in N:
	print indicator[x]

        

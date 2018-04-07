#! /usr/bin/python

from gurobipy import *
from numpy import array as npyarray
from numpy import transpose
import random
from scipy.io import *
import pandas as pd

"""
Problem 1)
In this problem you will explore using linear programming to balance the tradeoff between optimality and
fairness. In many applications, a limited resource is distributed to different users, each with a particular
valuation (often called utility) of each unit of resource allocated to them. You will first solve a maximum
sum utility problem by finding the feasible allocation that maximizes the aggregate welfare (sum utility).
Later in the problem you will explore ways to decrease the gap between the agent receiving the maximum
allocation, and the agent receiving the minimum allocation.

In files A1.csv, b1.csv, c1.csv you will find data describing a resource allocation problem with a
maximization objective. This represents the resource allocation problem:
"""
print "******************************************************************************\nProblem 1"
a = Model("prob1")

a_file = open('A1.csv')
a_data = []
for line in a_file:
    row_array = line.strip().split(',')
    num_array = []
    for ele in row_array:
        num_array.append(int(ele))
    a_data.append(npyarray(num_array))

b_file = open('b1.csv')
b_data = []
for ele in b_file:
    b_data.append(int(ele))

c_file = open('c1.csv')
c_data = []
for ele in c_file:
    c_data.append(int(ele))
c_data = npyarray(c_data)    

#Create x variables
num=1
x_vars = []
for ele in a_data[0]:
    name1 = "x" + str(num)
    x_vars.append(a.addVar(vtype=GRB.INTEGER, name=name1))
    num = num + 1

#Create constraints
for iter in range(len(a_data)):
    a.addConstr( a_data[iter].dot(x_vars) <= b_data[iter] )

a.addConstr( x_vars >= 0 )

#Set objective
a.setObjective( c_data.dot(x_vars), GRB.MAXIMIZE )

a.optimize()
# 23756 is the optimal solution


# 1b) Gap between highest and lowest is 12 (2..14)
a.printAttr("x")
"""
    Variable            x 
-------------------------
          x7            3 
         x12            6 
         x30           14 
         x33            4 
         x36            9 
         x42            2 
         x56            5 
         x61            2 
         x62            4 
         x72            2 
         x73            5 
         x80            3 
         x81           11 
         x87            8 
         x90            4 
         x99           12
"""        
print "******************************************************************************\nProblem 2"
# Problem 2
"""
Download files A2.csv, b2.csv, defining 500 inequalities:

Ax <= b

As you will discover, these do not have a feasible solution, i.e., there is no x that satisfies all 500 inequali-
ties simultaneously. It turns out that there is a set of 101 of these inequalities, for which there is no feasible
solution. Find 101 of the 500 inequalities for which the problem is infeasible. Hint: let duality and comple-
mentary slackness be your guide."""

b = Model("prob2")

a_file = open('A2.csv')
a_data = []
for line in a_file:
    row_array = line.strip().split(',')
    num_array = []
    for ele in row_array:
        num_array.append(int(ele))
    a_data.append(npyarray(num_array))

b_file = open('b2.csv')
b_data = []
for ele in b_file:
    b_data.append(float(ele))

#Create x variables
num=1
x_vars = []
for ele in a_data[0]:
    name1 = "x" + str(num)
    x_vars.append(b.addVar(vtype=GRB.INTEGER, name=name1))
    num = num + 1

print "Nothing here."

    
#Create constraints
#for iter in range(len(a_data)):
#    b.addConstr( a_data[iter].dot(x_vars) <= b_data[iter] )
#b.addConstr( x_vars >= 0 )

#Set objective
#b.setObjective( c_data.dot(x_vars), GRB.MAXIMIZE )

#b.optimize()


        
print "******************************************************************************\nProblem 3"
# Problem 3
"""
There are 30 objects, and 100 subsets of these objects of varying size. The matrix A3.csv describes
these subsets in its rows. So for example, the first row has a 1 in the 10th and 21st locations. This means
that the first subset contains the 10th and 21st of the 30 objects. The 17th row of A has a 1 in locations
{7, 23, 24, 26}, which means that the 17th subset contains objects {7, 23, 24, 26}.

(a) Find the smallest collection of sets whose union contains every element (an element can appear in
more than one subset).
(b) Find the largest collection of sets that are each disjoint."""


"""
Notes:

A row is a subset which contains 30 binary values.
Find the smallest collection of subsets which contain every value


ex:
0,0,0,0,1
1,0,1,0,1
0,1,0,1,0


"""

c = Model("prob3")

a_file = open('A3.csv')
a_data = []
for line in a_file:
    row_array = line.strip().split(',')
    num_array = []
    for ele in row_array:
        num_array.append(int(ele))
    a_data.append(npyarray(num_array))





print "******************************************************************************\nProblem 4"
# Problem 4

"""Solve the 30 dimensional optimization problem specified by the files A4.csv, b4.csv, and c4.csv, as
given by:
max : 
    c T x

s.t. :

    Ax <= b
    x1^2 + x2^2 == 0.5"""

d = Model("prob4")

a_file = open('A4.csv')
a_data = []
for line in a_file:
    row_array = line.strip().split(',')
    num_array = []
    for ele in row_array:
        num_array.append(float(ele))
    a_data.append(npyarray(num_array))

b_file = open('b4.csv')
b_data = []
for ele in b_file:
    b_data.append(float(ele))

c_file = open('c4.csv')
c_data = []
for ele in c_file:
    c_data.append(float(ele))
c_data = npyarray(c_data)    

#Create x variables
num=1
x_vars = []
for ele in a_data[0]:
    name1 = "x" + str(num)
    x_vars.append(d.addVar(vtype=GRB.CONTINUOUS, name=name1))
    num = num + 1

#Create constraints
for iter in range(len(a_data)):
    d.addConstr( a_data[iter].dot(x_vars) <= b_data[iter] )

#Quadratic constraint
#d.addConstr( (x_vars[0] * x_vars[0]) + (x_vars[1] * x_vars[1]) == 0.5 )

#Without quadratic constraint:
# x0     0.263175    squared = 0.069261081
# x1     0.188131    squared = 0.035393273
#                       = 0.104654354

#Infeasible
#d.addConstr( (x_vars[0] * x_vars[0]) == 0.25 )
#d.addConstr( (x_vars[1] * x_vars[1]) == 0.25 )

#Set objective
#d.setObjective( c_data.dot(x_vars), GRB.MAXIMIZE )

#d.optimize()
#d.printAttr("x")


print "******************************************************************************\nProblem 5"
# Problem 5


"""Consider the same problem as in the previous problem (i.e., with the same data), but without the non-convex
constraint:
max :
s.t. :
c T x
Ax <=  b.
Convert the problem to standard form, and find the vertex that has as many negative reduced costs as possible."""

e = Model("prob5")

a_file = open('A4.csv')
a_data = []
for line in a_file:
    row_array = line.strip().split(',')
    num_array = []
    for ele in row_array:
        num_array.append(float(ele))
    a_data.append(npyarray(num_array))
print "len(a_data) = ", len(a_data)
print "len(a_data[0]) = ", len(a_data[0])

b_file = open('b4.csv')
b_data = []
for ele in b_file:
    b_data.append(float(ele))
print "len(b_data) = ", len(b_data)

c_file = open('c4.csv')
c_data = []
for ele in c_file:
    c_data.append(float(ele))
c_data = npyarray(c_data)    
print "len(c_data) = ", len(c_data)

#Create x variables
num=1
x_vars = []
for ele in a_data[0]:
    name1 = "x" + str(num)
    x_vars.append(e.addVar(vtype=GRB.CONTINUOUS, name=name1))
    num = num + 1

#Create constraints
for iter in range(len(a_data)):
    e.addConstr( a_data[iter].dot(x_vars) <= b_data[iter] )


#Set objective
e.setObjective( c_data.dot(x_vars), GRB.MAXIMIZE )

e.optimize()
e.printAttr("x")



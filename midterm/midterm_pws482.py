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

a = Model("prob1")

a_file = open('A1.csv')
a_data = []
for line in a_file:
    row_array = line.strip().split(',')
    num_array = []
    for ele in row_array:
        num_array.append(int(ele))
    a_data.append(npyarray(num_array))
print "len(a_data) = ", len(a_data)
print "len(a_data[0]) = ", len(a_data[0])

b_file = open('b1.csv')
b_data = []
for ele in b_file:
    b_data.append(int(ele))
print "len(b_data) = ", len(b_data)

c_file = open('c1.csv')
c_data = []
for ele in c_file:
    c_data.append(int(ele))
c_data = npyarray(c_data)    
print "len(c_data) = ", len(c_data)

#Create x variables
num=0
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
          x6            3 
         x11            6 
         x29           14 
         x32            4 
         x35            9 
         x41            2 
         x55            5 
         x60            2 
         x61            4 
         x71            2 
         x72            5 
         x79            3 
         x80           11 
         x86            8 
         x89            4 
         x98           12
"""        

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
print "len(a_data) = ", len(a_data)
print "len(a_data[0]) = ", len(a_data[0])

b_file = open('b2.csv')
b_data = []
for ele in b_file:
    b_data.append(int(ele))
print "len(b_data) = ", len(b_data)


#Create x variables
num=0
x_vars = []
for ele in a_data[0]:
    name1 = "x" + str(num)
    x_vars.append(b.addVar(vtype=GRB.INTEGER, name=name1))
    num = num + 1

#Create constraints
#for iter in range(len(a_data)):
#    b.addConstr( a_data[iter].dot(x_vars) <= b_data[iter] )

#b.addConstr( x_vars >= 0 )

#Set objective
#b.setObjective( c_data.dot(x_vars), GRB.MAXIMIZE )

#b.optimize()



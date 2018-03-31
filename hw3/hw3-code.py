#! /usr/bin/python

from gurobipy import *
import numpy
import random
from scipy.io import *

##########
# 2) Ex 4.1
#
# minimize:     x1 - x2
# maximize:     -x1 + x2
#
# st:           2x1 + 3x2 - x3 + x4 <= 0
#               3x1 + x2 + 4x3 - 2x4 >= 3
#               -x1 - x2 + 2x3 + x4 = 6
#               x1 <= 0
#               x2,x3 >= 0
#   Create Dual
##########

print("\nHW3 Problem 2 - Ex.4.1\n****************************************************************")

a = Model("ex4.1_Primal")

x1 = a.addVar(vtype=GRB.INTEGER, name="x1")
x2 = a.addVar(vtype=GRB.INTEGER, name="x2")
x3 = a.addVar(vtype=GRB.INTEGER, name="x3")
x4 = a.addVar(vtype=GRB.INTEGER, name="x4")


a.setObjective( (-1 * x1) + (x2), GRB.MAXIMIZE)

a.addConstr( x1 <= 0, "constr_negativeX1")
a.addConstr( x2 >= 0, "constr_positiveX2")
a.addConstr( x3 >= 0, "constr_positiveX3")

a.addConstr( (2 * x1) + (3 * x2) - (x3) + (x4) <= 0, "constr_1")
a.addConstr( (3 * x1) + (x2) + (4 * x3) - (2 * x4) >= 3, "constr_2")
a.addConstr( (-1 * x1) - (x2) + (2 * x3) + (x4) >= 6, "constr_3")
a.addConstr( (-1 * x1) - (x2) + (2 * x3) + (x4) <= 6, "constr_4")

a.optimize()
print "Primal: "
a.printAttr("x")


b = Model("ex4.1_Dual")

y1 = b.addVar(vtype=GRB.INTEGER, name="y1")
y2 = b.addVar(vtype=GRB.INTEGER, name="y2")
y3 = b.addVar(vtype=GRB.INTEGER, name="y3")
y4 = b.addVar(vtype=GRB.INTEGER, name="y4")
y5 = b.addVar(vtype=GRB.INTEGER, name="y5")
y6 = b.addVar(vtype=GRB.INTEGER, name="y6")


b.setObjective( (3 * y2) + (6 * y3), GRB.MINIMIZE)

b.addConstr( y1 >= 0, "constr_positiveY1")
b.addConstr( y2 <= 0, "constr_negativeY2")
#y3 has no sign constraint
b.addConstr( y4 >= 0, "constr_positiveY4")
b.addConstr( y5 <= 0, "constr_negativeY5")
b.addConstr( y6 <= 0, "constr_negativeY6")

b.addConstr( (2 * y1) + (3 * y2) - (y3) + (y4) <= -1, "constr_1")
b.addConstr( (3 * y1) + (y2) - (y3) + (y5) >= 1, "constr_2")
b.addConstr( (-1 * y1) + (4 * y2) + (2 * y3) + (y6) >= 0, "constr_3")
b.addConstr( (y1) - (2 * y2) + (y3) >= 0, "constr_4.1") #Should be == 0

b.optimize()
print "Dual: "
b.printAttr("x")



##########
# 5 Ex 5.6
# Minimize lamp production costs from Jan - April
#
# minimize: quicksum(35Xt + 5Yt + 50Zt) for t in range(4)
# st:       Dt = Xt + Yt-1 + Zt     //Monthly Demand = Production + Last month's Storage + Lamps Purchased
#           Yt = Xt + Yt-1 - Dt     //Monthly Storage = This month's production + Last month's storage - This month's demand               
#           Xt <= 160               //Monthly production limit
#           Xt,Yt,Zt >= 0           //All positive
#           Dt = {150,160,225,180}  //Monthly demand
##########

print("\nHW3 Problem 5 - Ex.5.6a\n****************************************************************")

c = Model("ex5.6a")

x = []
y = []
z = []
for i in range(4):
    name1 = "x" + str(i)    #Monthly Production
    x.append(c.addVar(vtype=GRB.INTEGER, name=name1))

    name2 = "y" + str(i)    #Monthly Storage
    y.append(c.addVar(vtype=GRB.INTEGER, name=name2))

    name3 = "z" + str(i)    #Monthly Purchase
    z.append(c.addVar(vtype=GRB.INTEGER, name=name3))
    
d = [150, 160, 225, 180]    #Monthly Demand

c.setObjective( quicksum( (35 * x[i]) + (5 * y[i]) + (50 * z[i]) for i in range(4)), GRB.MINIMIZE )

for i in range(4):
    c.addConstr( x[i] <= 160 )
    c.addConstr( x[i] >= 0 )
    c.addConstr( y[i] >= 0 )
    c.addConstr( z[i] >= 0 )
    
    if i == 0:              #Previous month storage (y) doesn't exist.
        c.addConstr( d[i] == x[i] + z[i] )                  #Demand = Production + Purchase
        c.addConstr( y[i] == x[i] + z[i] - d[i] )           #Storage = Production + Purchase - Demand
    else:
        c.addConstr( d[i] == x[i] + y[i-1] + z[i] )         #Demand = Production + Prev Storage + Purchase
        c.addConstr( y[i] == x[i] + y[i-1] + z[i] - d[i] )  #Storage = Production + Prev Storage + Purchase - Demand
        
c.optimize()
c.printAttr("x")


















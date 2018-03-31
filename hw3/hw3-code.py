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
# st:       Dt = Xt + Yt-1 + Zt - Yt //Monthly Demand = Production + Previous Storage + Purchased - Current Storage
#           Xt <= 160               //Monthly production limit
#           Xt,Yt,Zt >= 0           //All positive
#           Dt = [150,160,225,180]  //Monthly demand
##########

print("\nHW3 Problem 5 - Ex.5.6b\n****************************************************************")

c = Model("ex5.6b")

x = []
y = []
z = []
for i in range(4):
    name1 = "x" + str(i)    #Monthly Production
    name1 = "Produce_" + str(i)    #Monthly Production
    x.append(c.addVar(vtype=GRB.INTEGER, name=name1))

    name2 = "Store_" + str(i)    #Monthly Storage
    y.append(c.addVar(vtype=GRB.INTEGER, name=name2))

    name3 = "Purchase_" + str(i)    #Monthly Purchase
    z.append(c.addVar(vtype=GRB.INTEGER, name=name3))
    
d = [150, 160, 225, 180]    #Monthly Demand

c.setObjective( quicksum( (35 * x[i]) + (5 * y[i]) + (50 * z[i]) for i in range(4)), GRB.MINIMIZE )

for i in range(4):
    c.addConstr( x[i] <= 160 )
    c.addConstr( x[i] >= 0 )
    c.addConstr( y[i] >= 0 )
    c.addConstr( z[i] >= 0 )
    
    if i == 0:              #Previous month storage (y) doesn't exist.
        c.addConstr( d[i] == x[i] + z[i] - y[i] )                  #Demand = Production + Purchase - Storage
    else:
        c.addConstr( d[i] == x[i] + y[i-1] + z[i] - y[i] )         #Demand = Production + Prev Storage + Purchase - Storage
            
c.optimize()
c.printAttr("x")



print("\nHW3 Problem 5 - Ex.5.6c\n****************************************************************")
print("Run maintenance during which month?\n")

e = Model("ex5.6c")

x = []
y = []
z = []
for i in range(4):
    name1 = "Produce_" + str(i)    #Monthly Production
    x.append(e.addVar(vtype=GRB.INTEGER, name=name1))

    name2 = "Store_" + str(i)    #Monthly Storage
    y.append(e.addVar(vtype=GRB.INTEGER, name=name2))

    name3 = "Purchase_" + str(i)    #Monthly Purchase
    z.append(e.addVar(vtype=GRB.INTEGER, name=name3))
    
d = [150, 160, 225, 180]    #Monthly Demand

e.setObjective( quicksum( (35 * x[i]) + (5 * y[i]) + (50 * z[i]) for i in range(4)), GRB.MINIMIZE )

for i in range(4):
    e.addConstr( x[i] >= 0 )
    e.addConstr( y[i] >= 0 )
    e.addConstr( z[i] >= 0 )
    if i == 2:
        e.addConstr( x[i] <= 155 )  #Maintenance in i month reduces max production
    else:
        e.addConstr( x[i] <= 160 )
    
    if i == 0:              #Previous month storage (y) doesn't exist.
        e.addConstr( d[i] == x[i] + z[i] - y[i] )                  #Demand = Production + Purchase - Storage
    else:
        e.addConstr( d[i] == x[i] + y[i-1] + z[i] - y[i] )         #Demand = Production + Prev Storage + Purchase - Storage
            
e.optimize()
e.printAttr("x")




print("\nHW3 Problem 5 - Ex.5.6d\n****************************************************************")
print("Company D can provide 50 lamps in Jan, Feb, or Mar for $45/each.\n")

f = Model("ex5.6d")

x = []
y = []
z = []
q = []

for i in range(4):
    name1 = "Produce_" + str(i)    #Monthly Production @ $35
    x.append(f.addVar(vtype=GRB.INTEGER, name=name1))

    name2 = "Store_" + str(i)    #Monthly Storage @ $5
    y.append(f.addVar(vtype=GRB.INTEGER, name=name2))

    name3 = "Purchase_" + str(i)    #Monthly Purchase @ $50
    z.append(f.addVar(vtype=GRB.INTEGER, name=name3))
    
    name4 = "SpecPurch_" + str(i)    #Special Purchase <=50 @ $45
    q.append(f.addVar(vtype=GRB.INTEGER, name=name4))

d = [150, 160, 225, 180]    #Monthly Demand

f.setObjective( quicksum( (35 * x[i]) + (5 * y[i]) + (50 * z[i]) + (45 * q[i]) for i in range(4)), GRB.MINIMIZE )

for i in range(4):
    f.addConstr( x[i] <= 160 )
    f.addConstr( x[i] >= 0 )
    f.addConstr( y[i] >= 0 )
    f.addConstr( z[i] >= 0 )
    f.addConstr( q[i] >= 0 )
    
    if i == 0:              #Previous month storage (y) doesn't exist.
        f.addConstr( d[i] == x[i] + z[i] - y[i] + q[i] )                  #Demand = Production + Purchase - Storage + SpecPurch
    else:
        f.addConstr( d[i] == x[i] + y[i-1] + z[i] - y[i] + q[i] )         #Demand = Production + Prev Storage + Purchase - Storage + SpecPurch
    if i == 3:
        f.addConstr( q[i] == 0 )    #Special purchase not available in April
    else:
        f.addConstr( q[i] <= 50 )   #Special purchase <= 50

f.addConstr( quicksum(q[i] for i in range(3)) <= 50 )  #Sum of Special purchase <= 50 lamps
            
f.optimize()
f.printAttr("x")




print("\nHW3 Problem 5 - Ex.5.6e\n****************************************************************")
print("Company C will lower purchase price in Feb... what is minimum decrease to make worthwhile?\n")

g = Model("ex5.6e")

x = []
y = []
z = []
for i in range(4):
    name1 = "x" + str(i)    #Monthly Production
    name1 = "Produce_" + str(i)    #Monthly Production
    x.append(g.addVar(vtype=GRB.INTEGER, name=name1))

    name2 = "Store_" + str(i)    #Monthly Storage
    y.append(g.addVar(vtype=GRB.INTEGER, name=name2))

    name3 = "Purchase_" + str(i)    #Monthly Purchase
    z.append(g.addVar(vtype=GRB.INTEGER, name=name3))
    
d = [150, 160, 225, 180]    #Monthly Demand

g.setObjective( quicksum( (35 * x[i]) + (5 * y[i]) for i in range(4)) + (50 * z[0]) + (45 * z[1]) + (50 * z[2]) + (50 * z[3]), GRB.MINIMIZE )

for i in range(4):
    g.addConstr( x[i] <= 160 )
    g.addConstr( x[i] >= 0 )
    g.addConstr( y[i] >= 0 )
    g.addConstr( z[i] >= 0 )
    
    if i == 0:              #Previous month storage (y) doesn't exist.
        g.addConstr( d[i] == x[i] + z[i] - y[i] )                  #Demand = Production + Purchase - Storage
    else:
        g.addConstr( d[i] == x[i] + y[i-1] + z[i] - y[i] )         #Demand = Production + Prev Storage + Purchase - Storage
            
g.optimize()
g.printAttr("x")


""" BASE 
    Variable            x 
-------------------------
   Produce_0          160 
     Store_0           10 
   Produce_1          160 
     Store_1           10 
   Produce_2          160 
  Purchase_2           55 
   Produce_3          160 
  Purchase_3           20
"""




print("\nHW3 Problem 5 - Ex.5.6f\n****************************************************************")
print("Cost of storage in Feb is $8/unit; how does this change things?\n")

h = Model("ex5.6f")

x = []
y = []
z = []
for i in range(4):
    name1 = "x" + str(i)    #Monthly Production
    name1 = "Produce_" + str(i)    #Monthly Production
    x.append(h.addVar(vtype=GRB.INTEGER, name=name1))

    name2 = "Store_" + str(i)    #Monthly Storage
    y.append(h.addVar(vtype=GRB.INTEGER, name=name2))

    name3 = "Purchase_" + str(i)    #Monthly Purchase
    z.append(h.addVar(vtype=GRB.INTEGER, name=name3))
    
d = [150, 160, 225, 180]    #Monthly Demand

h.setObjective( quicksum( (35 * x[i]) + (5 * y[i]) + (50 * z[i]) for i in range(4)) + (3 * y[1]), GRB.MINIMIZE )

for i in range(4):
    h.addConstr( x[i] <= 160 )
    h.addConstr( x[i] >= 0 )
    h.addConstr( y[i] >= 0 )
    h.addConstr( z[i] >= 0 )
    
    if i == 0:              #Previous month storage (y) doesn't exist.
        h.addConstr( d[i] == x[i] + z[i] - y[i] )                  #Demand = Production + Purchase - Storage
    else:
        h.addConstr( d[i] == x[i] + y[i-1] + z[i] - y[i] )         #Demand = Production + Prev Storage + Purchase - Storage
            
h.optimize()
h.printAttr("x")



print("\nHW3 Problem 5 - Ex.5.6g\n****************************************************************")
print("If Jan demand is 90 units, what are upper and lower bounds of impact on optimal cost?\n")

j = Model("ex5.6g")

x = []
y = []
z = []
for i in range(4):
    name1 = "x" + str(i)    #Monthly Production
    name1 = "Produce_" + str(i)    #Monthly Production
    x.append(j.addVar(vtype=GRB.INTEGER, name=name1))

    name2 = "Store_" + str(i)    #Monthly Storage
    y.append(j.addVar(vtype=GRB.INTEGER, name=name2))

    name3 = "Purchase_" + str(i)    #Monthly Purchase
    z.append(j.addVar(vtype=GRB.INTEGER, name=name3))
    
d = [90, 160, 225, 180]    #Monthly Demand

j.setObjective( quicksum( (35 * x[i]) + (5 * y[i]) + (50 * z[i]) for i in range(4)), GRB.MINIMIZE )

for i in range(4):
    j.addConstr( x[i] <= 160 )
    j.addConstr( x[i] >= 0 )
    j.addConstr( y[i] >= 0 )
    j.addConstr( z[i] >= 0 )
    
    if i == 0:              #Previous month storage (y) doesn't exist.
        j.addConstr( d[i] == x[i] + z[i] - y[i] )                  #Demand = Production + Purchase - Storage
    else:
        j.addConstr( d[i] == x[i] + y[i-1] + z[i] - y[i] )         #Demand = Production + Prev Storage + Purchase - Storage
            
j.optimize()
j.printAttr("x")















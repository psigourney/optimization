#! /usr/bin/python

""" 
    Final Project
    Intro to Optimization
    Spring 2018
    Patrick Sigourney - pws482

    Determine estimated rollup completion time based on job dependencies and historical average runtimes.
"""

from gurobipy import *

a = Model("RollupCompletion")

MinsToCompletion = a.addVar(vtype=GRB.CONTINUOUS, name="MinsToCompletion")

#Completion time of MIDs
MID15442 = a.addVar(vtype=GRB.CONTINUOUS, name="MID15442"
MID24708 = a.addVar(vtype=GRB.CONTINUOUS, name="MID24708"
MID24670 = a.addVar(vtype=GRB.CONTINUOUS, name="MID24670"
MID15430 = a.addVar(vtype=GRB.CONTINUOUS, name="MID15430"
MID24709 = a.addVar(vtype=GRB.CONTINUOUS, name="MID24709"
MID15462 = a.addVar(vtype=GRB.CONTINUOUS, name="MID15462"
MID25012 = a.addVar(vtype=GRB.CONTINUOUS, name="MID25012"
MID16047 = a.addVar(vtype=GRB.CONTINUOUS, name="MID16047"
MID24671 = a.addVar(vtype=GRB.CONTINUOUS, name="MID24671"
MID23185 = a.addVar(vtype=GRB.CONTINUOUS, name="MID23185"
MID23184 = a.addVar(vtype=GRB.CONTINUOUS, name="MID23184"
MID16050 = a.addVar(vtype=GRB.CONTINUOUS, name="MID16050"
MID24672 = a.addVar(vtype=GRB.CONTINUOUS, name="MID24672"
MID22108 = a.addVar(vtype=GRB.CONTINUOUS, name="MID22108"
MID22357 = a.addVar(vtype=GRB.CONTINUOUS, name="MID22357"
MID15644 = a.addVar(vtype=GRB.CONTINUOUS, name="MID15644"


# Dependency Constraints
MID15442 = 0 #Currently running
MID24708 = 0 #Currently running
MID24670 = 0 #Currently running
MID15430 >= MID15542 + 3.45
MID24709 >= MID24708 + 0.72
MID15462 >= MID15442 + 3.45
MID25012 >= MID24709 + 0.80
MID16047 >= MID15430 + 3.97
MID24671 >= MID15462 + 8.70
MID24671 >= MID24670 + 5.37
MID23185 >= MID15462 + 8.70
MID23184 >= MID15462 + 8.70
MID16050 >= MID16047 + 4.35
MID24672 >= MID24671 + 5.67
MID22108 >= MID16050 + 3.93
MID22357 >= MID16047 + 4.35
MID22357 >= MID16050 + 3.93
MID22357 >= MID22108 + 3.57
MID15644 >= MID22357 + 2.30
MID15644 >= MID23184 + 1.37
MID15644 >= MID23185 + 6.38
MID15644 >= MID24672 + 6.20
MinsToCompletion = MID15644 + 0.03

a.setObjective(MinsToCompletion, GRB.MINIMIZE)

a.optimize()





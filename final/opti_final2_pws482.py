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

a.setObjective(MinsToCompletion, GRB.MINIMIZE)

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
MID25012 >= MID24709 + 
MID16047
MID24671
MID23185
MID23184
MID16050
MID24672
MID22108
MID22357
MID15644
MinsToCompletion = MID15644 + 0.03

# 16 MIDs
# 19 dependency constraints

ActiveNew = []      # Number of Active New disks each period
ActiveUsed = []     # Number of Active Used disks each period

FailedNew = []      # Number of Failed New disks each period
FailedUsed = []     # Number of Failed Used disks each period

ReplacedNew = []     # Number of Replaced New disks each period
ReplacedUsed = []    # Number of Replaced Used disks each period


# Period Variables
for i in range(n):
    varName = "ActiveNew_" + str(i)
    ActiveNew.append(a.addVar(vtype=GRB.INTEGER, name=varName))
    varName = "ActiveUsed_" + str(i)
    ActiveUsed.append(a.addVar(vtype=GRB.INTEGER, name=varName))
    varName = "FailedNew_" + str(i)
    FailedNew.append(a.addVar(vtype=GRB.INTEGER, name=varName))
    varName = "FailedUsed_" + str(i)
    FailedUsed.append(a.addVar(vtype=GRB.INTEGER, name=varName))

#    ActiveNew.append(0)
#    ActiveUsed.append(0)
#    FailedNew.append(0)
#    FailedUsed.append(0)
    
    varName = "ReplacedNew_" + str(i)
    ReplacedNew.append(a.addVar(vtype=GRB.INTEGER, name=varName))
    varName = "ReplacedUsed_" + str(i)
    ReplacedUsed.append(a.addVar(vtype=GRB.INTEGER, name=varName))


    # Global Period Constraints
    a.addConstr( ActiveNew[i] >= 0 )
    a.addConstr( ActiveUsed[i] >= 0 )
    a.addConstr( FailedNew[i] >= 0 )
    a.addConstr( FailedUsed[i] >= 0 )
    a.addConstr( ReplacedNew[i] >= 0 )
    a.addConstr( ReplacedUsed[i] >= 0 )
    
    a.addConstr( ActiveNew[i] + ActiveUsed[i] == 1024 )                                 # Total active disks always equals 1024
    
    a.addConstr( ReplacedNew[i] + ReplacedUsed[i] == FailedNew[i] + FailedUsed[i] )     # Replacements == Failures

    
# Period 0 Starting Values
a.addConstr( ActiveNew[0] == 1024 )     # Start with all disks being New
a.addConstr( ActiveUsed[0] == 0 )       # Unnecessary constraints?
a.addConstr( FailedNew[0] == 0 )
a.addConstr( FailedUsed[0] == 0 )
a.addConstr( ReplacedNew[0] == 0 )
a.addConstr( ReplacedUsed[0] == 0 )
    
    
# Subsequent Period Constraints
for i in range(1,n):
    a.addConstr( FailedNew[i] == ActiveNew[i-1] * FailureRateNew )                      # Period failures of New disks
    a.addConstr( FailedUsed[i] == ActiveUsed[i-1] * FailureRateUsed )                   # Period failures of Used disks
    
    a.addConstr( ActiveNew[i] == ActiveNew[i-1] - FailedNew[i] + ReplacedNew[i] )       # Previous Active New Disks - Failed + Replaced = Current Active New Disks
    a.addConstr( ActiveUsed[i] == ActiveUsed[i-1] - FailedUsed[i] + ReplacedUsed[i] )   # Previous Active Used Disks - Failed + Replaced = Current Active Used Disks

    
a.setObjective(  , GRB.MINIMIZE)

a.optimize()





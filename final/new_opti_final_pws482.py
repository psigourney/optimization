#! /usr/bin/python

""" 
    Final Project
    Intro to Optimization
    Spring 2018
    Patrick Sigourney - pws482

    A server cluster contains 1024 physical disks.
    When the cluster was assembled in period 1, all the disks were new.
    Each period, a certain percentage of the disks fail and need to be replaced.
    The replacement disks can either be purchased new or salvaged used from decommisioned servers.
    New disks are more expensive, but fail less frequently.
    There is a flat rate charged to send someone to the data center to replace a disk (in addition to the disk cost).
    
    If the cluster has a planned lifecycle of 10 periods, as disks fail each period
    should they be replaced with new disks or used disks in order to minimize total cost?
"""

from gurobipy import *

a = Model("DiskReplacement")

n = 11     # Number of time periods + initial period

LaborCharge = 300   # Labor Charge to replace a disk

PriceNew = 250 + LaborCharge    # Price for disk replacement using New disk
PriceUsed = 50 + LaborCharge    # Price for disk replacement using Used disk

FailureRateNew = 0.02   # Failure Rate of New disks per period
FailureRateUsed = 0.15  # Failure Rate of Used disks per period

ActiveNew = []      # Number of Active New disks each period
ActiveUsed = []     # Number of Active Used disks each period

FailedNew = []      # Number of Failed New disks each period
FailedUsed = []     # Number of Failed Used disks each period

ReplacedNew = []     # Number of Replaced New disks each period
ReplacedUsed = []    # Number of Replaced Used disks each period

FailedNewReplacedNew = []   # Number of Failed New Disks Replaced with New Disks
FailedNewReplacedUsed = []  # Number of Failed New Disks Replaced with Used Disks
FailedUsedReplacedNew = []  # Number of Failed Used Disks Replaced with New Disks
FailedUsedReplacedUsed = [] # Number of Failed Used Disks Replaced with Used Disks

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
    varName = "ReplacedNew_" + str(i)
    ReplacedNew.append(a.addVar(vtype=GRB.INTEGER, name=varName))
    varName = "ReplacedUsed_" + str(i)
    ReplacedUsed.append(a.addVar(vtype=GRB.INTEGER, name=varName))
    varName = "FailedNewReplacedNew_" + str(i)
    FailedNewReplacedNew.append(a.addVar(vtype=GRB.INTEGER, name=varName))
    varName = "FailedNewReplacedUsed_" + str(i)
    FailedNewReplacedUsed.append(a.addVar(vtype=GRB.INTEGER, name=varName))
    varName = "FailedUsedReplacedNew_" + str(i)
    FailedUsedReplacedNew.append(a.addVar(vtype=GRB.INTEGER, name=varName))
    varName = "FailedUsedReplacedUsed_" + str(i)
    FailedUsedReplacedUsed.append(a.addVar(vtype=GRB.INTEGER, name=varName))
   
   

    # Global Period Constraints
    a.addConstr( ActiveNew[i] >= 0 )
    a.addConstr( ActiveUsed[i] >= 0 )
    a.addConstr( FailedNew[i] >= 0 )
    a.addConstr( FailedUsed[i] >= 0 )
    a.addConstr( ReplacedNew[i] >= 0 )
    a.addConstr( ReplacedUsed[i] >= 0 )

    a.addConstr( FailedNewReplacedNew[i] >= 0 )
    a.addConstr( FailedNewReplacedUsed[i] >= 0 )
    a.addConstr( FailedUsedReplacedNew[i] >= 0 )
    a.addConstr( FailedUsedReplacedUsed[i] >= 0 )
    
    a.addConstr( ActiveNew[i] + ActiveUsed[i] == 1024 )                                 # Total active disks always equals 1024
    a.addConstr( ActiveNew[i] <= 1024 ) 
    a.addConstr( ActiveUsed[i] <= 1024 ) 
    
    a.addConstr( ReplacedNew[i] + ReplacedUsed[i] == FailedNew[i] + FailedUsed[i] )     # Replacements == Failures

    
# Period 0 Starting Values
a.addConstr( ActiveNew[0] == 1024 )     # Start with all disks being New
a.addConstr( ActiveUsed[0] == 0 )       # Unnecessary constraints?
a.addConstr( FailedNew[0] == 0 )
a.addConstr( FailedUsed[0] == 0 )
a.addConstr( ReplacedNew[0] == 0 )
a.addConstr( ReplacedUsed[0] == 0 )

a.addConstr( FailedNewReplacedNew[0] == 0 )
a.addConstr( FailedNewReplacedUsed[0] == 0 )
a.addConstr( FailedUsedReplacedNew[0] == 0 )
a.addConstr( FailedUsedReplacedUsed[0] == 0 )
    
    
# Subsequent Period Constraints
for i in range(1,n):
    a.addConstr( FailedNew[i] == ActiveNew[i-1] * FailureRateNew )                      # Period failures of New disks
    a.addConstr( FailedUsed[i] == ActiveUsed[i-1] * FailureRateUsed )                   # Period failures of Used disks
    
    a.addConstr( ActiveNew[i] == ActiveNew[i-1] - FailedNew[i] + ReplacedNew[i] )       # Previous Active New Disks - Failed + Replaced = Current Active New Disks
    a.addConstr( ActiveUsed[i] == ActiveUsed[i-1] - FailedUsed[i] + ReplacedUsed[i] )   # Previous Active Used Disks - Failed + Replaced = Current Active Used Disks
    
    a.addConstr( ReplacedNew[i] == FailedNewReplacedNew[i] + FailedUsedReplacedNew[i] )
    a.addConstr( ReplacedUsed[i] == FailedNewReplacedUsed[i] + FailedUsedReplacedUsed[i] )

    
a.setObjective( quicksum( (PriceNew * ReplacedNew[i]) + (PriceUsed * ReplacedUsed[i]) for i in range(n)) , GRB.MINIMIZE)

a.optimize()





# -*- coding: utf-8 -*-
# Ez egy copy. Teljesen lemásoltam a másik kódot és megpróbáltam számomra érthetőre fordítani.

import matplotlib
matplotlib.use('TkAgg')
import random
import networkx
import math
import pylab

diGraph = networkx.DiGraph()
numberOfSensors = 5

scope = 10; # homogenous sensor nodes Scope
minScopeRange = 10.0
maxScopeRange = 40.0
widthRange = (5, 40)
heightRange = (5, 40)

isDraw = True
isSave = True

scopeRndSugar = (minScopeRange, maxScopeRange) #Scope intervall - random sugar
nodeTypes = False # True = homogen False = heterogen
if nodeTypes == True:
    print "******* Undirected Graph *******"
else:
    print "******* Directed Graph *******"
random.seed() # random seed: need to be set. Default: None = current computer time.
clauseSet = []
#clauseSetReal = [] #not in use
clause = []
createClause = []
#model1 = [] #not in use
#model1Set = [] #not in use
#model2 = [] #not in use
#model2Set = [] #not in use
#list_of_cliques = [] #not in use
arrScope = [[]]
#WMclause =[] #not in use
#WMclauseSet = [] #not in use
clauseCount = 0
comm = 0




# Figure properties
if (isDraw):
    pylab.rcParams['figure.figsize'] = 7, 7
    fig = pylab.gcf()
    ax = pylab.gca()
    ax.cla()
    ax.set_xlim((0, 140))
    ax.set_ylim((0, 140))
    pylab.figure(1, figsize=(14, 10))
    pylab.plot() #Plot WirelesSensorNetwork (WSN)


######################## Creating network ###################################

# *****************************************************************
#   Sensors placement and Graph
# ***************************************************************** 

def simple_Cycle_Generator():
    for i in range(1, numberOfSensors):
        diGraph.add_edge(i, i+1)
        diGraph.add_path([i, i+1])
    diGraph.add_edge(numberOfSensors, 1)
    diGraph.add_path([numberOfSensors, 1])

# new def



def wsn_graph_gen():
    clause = []
    createClause = []
    for i in range(1, numberOfSensors+1):
        x = float(random.randrange(*widthRange))
        y = float(random.randrange(*heightRange))
        rndRad = random.randrange(*scopeRndSugar)
        diGraph.add_node(i, pos=(x, y))
        if nodeTypes == False:
            arrScope.append([i, rndRad])
            scope = rndRad
        else:
            arrScope.append([i, scope])
        circle = pylab.Circle((x, y), scope, color="blue", fill=False)
        if(isDraw):
            fig.gca().add_artist(circle)
        pos=networkx.get_node_attributes(diGraph,'pos')
        diGraph.node.values()
    if(isDraw):
        networkx.draw(diGraph, pos, with_labels=True)
        pylab.title('Sensor nodes')

    clauseCount = 0
    #Generating graph and CNF file
    for i in range(1, numberOfSensors+1):
        clause.append(i)
        for j in range(1, numberOfSensors+1):
            x1, y1 = pos[i]
            x2, y2 = pos[j]
            if i<>j:
                if nodeTypes == False:
                    comm = arrScope[i][1]+arrScope[j][1]
                else:
                    comm = 50
                if (math.sqrt(math.pow((x2-x1),2)+math.pow((y2-y1),2))) <= arrScope[i][1]:
                    diGraph.add_edge(i, j)
                    diGraph.add_path([i, j])
                    clause.append(j)
                    clauseCount = clauseCount + 1
        createClause = clause #Original sequence?
        consistsOf = False
        for i in xrange(len(clauseSet)):
            if clause == clauseSet[i]:
                consistsOf = True
        if consistsOf == False:
            clauseSet.append(clause)
        clause = []
        createClause = []

# *****************************************************************
#   Details
# ***************************************************************** 

def strong_model_cnf():
    if(isDraw):
        pylab.figure()
        pylab.plot()
        pylab.title('Communication graph - optimalized')
        networkx.draw(diGraph, with_labels=True)
    f_sm = open(str(numberOfSensors)+"_"+str(diGraph.number_of_edges())+"_"+str("%.2f" % float(graph_dens))+"_SM.cnf", "w")
    f_sm.write('p cnf ')
    f_sm.write('%s ' % numberOfSensors)
    f_sm.write('\n')

    for i in range(1, networkx.number_of_nodes(diGraph)+1):
        for j in (networkx.neighbors(diGraph, i)):
           f_sm.write('%s ' % -i)
           f_sm.write('%s ' % j)
           f_sm.write('%s\n' % 0)

    for m in range(1, numberOfSensors+1):
        f_sm.write('%s ' % m)
    f_sm.write('%s\n' % 0)

    for n in range(1, numberOfSensors+1):
       f_sm.write('%s ' % -m)
    f_sm.write('%s\n' % 0)
    f_sm.close()


#some
#code
#commented
wsn_graph_gen()

print "Number of nodes: ", numberOfSensors
print "The maximum number of edges (if the graph is directed -default): ", numberOfSensors*(numberOfSensors-1)
print "Number of edges: ", diGraph.number_of_edges()
graph_dens = float(diGraph.number_of_edges()) / float((numberOfSensors*(numberOfSensors-1)))
print " Graph density : %.2f (Coleman and More 1983)."  % (graph_dens)     

#simple_cicle_gen()
#wsn_graph_gen()

#diGraph = networkx.erdos_renyi_graph(100,0.15)


pylab.figure()
pylab.plot()   
pylab.title('Communication graph - optimalized')
networkx.draw(diGraph,with_labels=True)
strong_model_cnf()




#isStrConn =  networkx.is_strongly_connected(diGraph)


if(isSave):
    pylab.savefig(str(numberOfSensors)+"_"+str(diGraph.number_of_edges())+"_"+str(float(graph_dens))+".png")

#*****************************************************************
#is_strongly_connected????
#***************************************************************** 




#*****************************************************************
#Weak Model-VALID
#***************************************************************** 

#WM

f_wm = open(str(numberOfSensors)+"_"+str(diGraph.number_of_edges())+"_"+str("%.2f" % float(graph_dens))+"_WM.cnf", "w")
f_wm.write('p cnf ')
f_wm.write('%s ' % numberOfSensors)
f_wm.write('\n')

#NodeRep.......
nodeRep=[]

for i in range(1, numberOfSensors+1):
    if len(list(networkx.neighbors(diGraph, i))) != 0:
        f_wm.write('%s ' % -i)
        nodeRep = list(networkx.neighbors(diGraph, i))
        nodeRep.sort()
        for j in xrange(len(nodeRep)):
            f_wm.write('%s ' % nodeRep[j])
        f_wm.write('%s ' % 0)
        f_wm.write('\n')

from itertools import combinations
#import matplotlib.pyplot as plt

#circleRep, ide jön a lényeg. Folyt.Köv.

subDiGraph = []
tempCycles = []
finalCycles = [[]]

for i in range(2, numberOfSensors):

    comb = list(combinations(list([j for j in range(1, numberOfSensors+1)]), i))

    for k in range(0, len(comb)):
        subDiGraph = diGraph.subgraph(list(comb[k]))

        if networkx.is_strongly_connected(subDiGraph):
            subGraph = list(subDiGraph.nodes())
            for cycnodes in range(0, len(subGraph)):
                tempCycles.append(-list(subDiGraph.nodes)[cycnodes])
            for node in range(0, len(subGraph)):
                succ = list(diGraph.successors(list(subDiGraph)[node]))
                for succNode in range(0, len(succ)):
                    if -(succ[succNode]) not in tempCycles:
                        tempCycles.append(succ[succNode])
                tempCycles = set(tempCycles)
                tempCycles = list(tempCycles)
            finalCycles.append(tempCycles)
        tempCycles = []

# place final cycles in clauses

for finalCycleClause in range(1, len(finalCycles)):
    for element in range(0, len(finalCycles[finalCycleClause])):
        f_wm.write('%s ' % finalCycles[finalCycleClause][element])
    f_wm.write('%s\n' % 0)


# constraints
for i in range(1, numberOfSensors+1):
    f_wm.write('%s ' % i)
f_wm.write('%s\n' % 0)

for i in range(1, numberOfSensors+1):
    f_wm.write('%s ' % -i)
f_wm.write('%s\n' % 0)
f_wm.close()

#print(list(combinations(list([u for u in range(1,100+1)]) , 5)))
isStronglyConnected = networkx.is_strongly_connected(diGraph)
print "GG is strongly connected? " + str(isStronglyConnected)
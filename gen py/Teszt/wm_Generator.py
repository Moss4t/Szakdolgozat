# -*- coding: utf-8 -*-


import matplotlib
matplotlib.use('TkAgg')
import random as RD
import networkx as NX
import math as MT
import pylab as PL

g = NX.DiGraph()
N=5 #Number of sensors

Scope = 10  #Homogenous sensor nodes Scope
MinScope = 10.0 #Minimum scope range
MaxScope = 40.0 #Maximum scope range
rangeX = (5, 40)
rangeY = (5, 40)

isDraw =True
isSave = True

scopeRad = (MinScope, MaxScope) #Scope interval - random sugar
NodeTypes = False #homogeneous or heterogeneous  True = homogenius False=heterogeneus
if NodeTypes == True:
    print "*****Undirected graph******"
else:
    print "*****Directed graph*******"
RD.seed() #Random seed
clauseSet=[]
clauseSetReal = []
clause=[]
creal=[]
model1=[]
model1Set=[]
model2=[]
model2Set=[]
list_of_cliques = []
arrScope =  [[]]
WMclause =[]
WMclauseSet = []
kloz = 0
Comm = 0





# Figure properties
if (isDraw):
    PL.rcParams['figure.figsize'] = 7, 7
    fig = PL.gcf()
    ax = PL.gca()
    ax.cla()
    ax.set_xlim((0,140))
    ax.set_ylim((0,140))
    PL.figure(1, figsize=(14, 10))
    PL.plot() #Plot WSN


######################## Creating network ###################################

#*****************************************************************
#Sensors placement and Graph
#***************************************************************** 

def simple_cicle_gen():
    for i in range(1,N):
        g.add_edge(i,i+1)
        g.add_path([i,i+1])
    g.add_edge(N,1)
    g.add_path([N,1])


def tajti_graphs():
    print()

def wsn_graph_gen():
    clause=[]
    creal = []
    for i in range(1,N+1):
        x = float(RD.randrange(*rangeX))
        y = float(RD.randrange(*rangeY))
        rndRad = RD.randrange(*scopeRad)
        g.add_node(i,pos=(x,y)) 
        if NodeTypes == False:
            arrScope.append([i,rndRad])
            Scope = rndRad
        else: 
            arrScope.append([i,Scope])
        circle = PL.Circle((x,y), Scope,  color="blue", fill=False)
        if (isDraw):
            fig.gca().add_artist(circle) 
        pos=NX.get_node_attributes(g,'pos')
        g.node.values()
    if (isDraw):
        NX.draw(g,pos, with_labels=True)
        PL.title('Sensor nodes')
    
    kloz = 0
    # Generating graph & cnf file 
    for i in range(1,N+1):
        clause.append(i)
        for j in range(1,N+1):
            x1,y1 = pos[i]      
            x2,y2 = pos[j]
            if i<>j:
                if NodeTypes == False:
                    Comm = arrScope[i][1]+arrScope[j][1]
                else:
                    Comm = 50
                if (MT.sqrt(MT.pow((x2-x1),2)+MT.pow((y2-y1),2)))<= arrScope[i][1]:
                    g.add_edge(i,j)
                    g.add_path([i,j])
                    clause.append(j)
                    kloz= kloz+1
        creal = clause #original  sequence
        consistof = False
        for i in xrange(len(clauseSet)):
           if clause == clauseSet[i]:
               consistof = True           
        if consistof == False:
            clauseSet.append(clause)     
        clause = []
        creal = []

#*****************************************************************
#Details
#***************************************************************** 

def strong_model_cnf(): 
    if (isDraw):
        PL.figure()
        PL.plot()   
        PL.title('Communication graph - optimalized')
        NX.draw(g,with_labels=True)
    f_sm = open(str(N)+"_"+str(g.number_of_edges())+"_"+str("%.2f" % float(graph_dens))+"_SM.cnf", "w")
    f_sm.write('p cnf ')
    f_sm.write('%s ' % N)
    f_sm.write('\n')
     
    for i in range(1,NX.number_of_nodes(g)+1):
       for j in (NX.neighbors(g,i)):
           f_sm.write('%s ' % -i)
           f_sm.write('%s ' % j)
           f_sm.write('%s\n' % 0)
           
    for m in range(1, N+1):
       f_sm.write('%s ' % m)
    f_sm.write('%s\n' % 0)
    
    for m in range(1, N+1):
       f_sm.write('%s ' % -m)
    f_sm.write('%s\n' % 0)
    f_sm.close()
    
 
#d=NX.barabasi_albert_graph(N,2)
#reindexed_graph = NX.relabel.convert_node_labels_to_integers(d, first_label=1, ordering='default')
#g=NX.DiGraph(reindexed_graph) 
wsn_graph_gen()    

print "Number of nodes: " , N
print "The maximum number of edges (if the graph is directed -default): ", N*(N-1)
print "Number of edges: " , g.number_of_edges()
graph_dens = float(g.number_of_edges()) / float((N*(N-1)))
print " Graph density : %.2f (Coleman and More 1983)."  % (graph_dens)     

#simple_cicle_gen()    
#wsn_graph_gen()

#g=NX.erdos_renyi_graph(100,0.15)


PL.figure()
PL.plot()   
PL.title('Communication graph - optimalized')
NX.draw(g,with_labels=True)
strong_model_cnf()




#isStrConn =  NX.is_strongly_connected(g)


if (isSave):
    PL.savefig(str(N)+"_"+str(g.number_of_edges())+"_"+str(float(graph_dens))+".png")

#*****************************************************************
#is_strongly_connected????
#***************************************************************** 




#*****************************************************************
#Weak Model-VALID
#***************************************************************** 

#WM

f_wm = open(str(N)+"_"+str(g.number_of_edges())+"_"+str("%.2f" % float(graph_dens))+"_WM.cnf", "w")
f_wm.write('p cnf ')
f_wm.write('%s ' % N)
f_wm.write('\n')

#NodeRep.......
nodeRep=[]

for i in range(1,N+1):
    if len(list(NX.neighbors(g,i)))!=0:
        f_wm.write('%s ' % -i)
        nodeRep=list(NX.neighbors(g,i))
        nodeRep.sort()
        for j in xrange(len(nodeRep)):
            f_wm.write('%s ' % nodeRep[j])
        f_wm.write('%s ' % 0)
        f_wm.write('\n')

fCycles = []
finalCycles = [[]]

from itertools import combinations
import matplotlib.pyplot as plt

#circleRep

sg = []
fCycles = []
for i in range(2,N):

    comb = list(combinations(list([j for j in range(1,N+1)]), i))

    for k in range(0,len(comb)):
        sg = g.subgraph(list(comb[k]))

        if NX.is_strongly_connected(sg): 
            subGraph = list(sg.nodes())
            #a kör elemeinek hozzáadás a klózhoz
            for cnodes in range(0,len(subGraph)):
                fCycles.append(-list(sg.nodes)[cnodes])
            for nd in range(0, len(subGraph)):
                succList = list(g.successors(list(sg.nodes)[nd]))
                for nb in range(0, len(succList)):
                    if -(succList[nb]) not in fCycles:
                        fCycles.append(succList[nb])
                fCycles = set(fCycles)
                fCycles = list(fCycles)  
            finalCycles.append(fCycles)
        fCycles = []  
 
# create to final cycles clauses

for fcCLause in range(1,len(finalCycles)):
    for fcCLause_element in range(0, len(finalCycles[fcCLause])):
        f_wm.write('%s ' % finalCycles[fcCLause][fcCLause_element])
    f_wm.write('%s\n' % 0)


#Constraints
for m in range(1, N+1):
   f_wm.write('%s ' % m)
f_wm.write('%s\n' % 0)
#f_sm.write('\n')
for m in range(1, N+1):
   f_wm.write('%s ' % -m)
f_wm.write('%s\n' % 0)
f_wm.close()






#print(list(combinations(list([u for u in range(1,100+1)]) , 5)))
isStrConn =  NX.is_strongly_connected(g)
print "GG is strongly connected?  "  +str(isStrConn)
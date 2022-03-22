#240+os sorok BB modell.

import networkx.algorithms.traversal.edgedfs as nate
from networkx.algorithms.traversal.edgedfs import edge_dfs, helper_funcs, help
#from networkx.algorithms.traversal.edgedfs import out
import matplotlib
matplotlib.use('TkAgg')
import random as RD
import networkx as NX
import math as MT
import pylab as PL

def find_cycle(G, source=None, orientation='original'):

    out_edge, key, tailhead = helper_funcs(G, orientation)

    explored = set()
    cycle = []
    final_node = None
    for start_node in G.nbunch_iter(source):
        if start_node in explored:
            # No loop is possible.
            continue
        edges = []
        seen = {start_node}
        active_nodes = {start_node}
        previous_head = None

        for edge in NX.edge_dfs(G, start_node, orientation):
            tail, head = tailhead(edge)
            if head in explored:
                continue
            if previous_head is not None and tail != previous_head:
                while True:
                    try:
                        popped_edge = edges.pop()
                    except IndexError:
                        edges = []
                        active_nodes = {tail}
                        break
                    else:
                        popped_head = tailhead(popped_edge)[1]
                        active_nodes.remove(popped_head)

                    if edges:
                        last_head = tailhead(edges[-1])[1]
                        if tail == last_head:
                            break
            edges.append(edge)

            if head in active_nodes:
                # We have a loop!
                cycle.extend(edges)
                final_node = head
                break
            else:
                seen.add(head)
                active_nodes.add(head)
                previous_head = head

        if cycle:
            break
        else:
            explored.update(seen)

    else:
        return 0
    for i, edge in enumerate(cycle):
        tail, head = tailhead(edge)
        if tail == final_node:
            break

    return cycle[i:]


N=90  #Number of sensors

Scope = 10  #Homogenous sensor nodes Scope
MinScope = 20.0 #Minimum scope range
MaxScope = 40.0 #Maximum scope range
rangeX = (5, 90)
rangeY = (5, 90)

isDraw =False
isSave = False

scopeRad = (MinScope, MaxScope) #Scope interval - random sugar
NodeTypes = False #homogeneous or heterogeneous  True = homogenius False=heterogeneus
if NodeTypes == True:
    print("*****Undirected graph******")
else:
    print("*****Directed graph*******")
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




#Directed graph
g = NX.DiGraph()

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


for i in range(1,N+1):
    x = float(RD.randrange(*rangeX))
    y = float(RD.randrange(*rangeY))
    positions = (x,y)
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
    
   
#*****************************************************************
#Strong Model-VALID
#***************************************************************** 

kloz = 0
# Generating graph & cnf file 
for i in range(1,N+1):
    clause.append(i)
    for j in range(1,N+1):
        x1,y1 = pos[i]      
        x2,y2 = pos[j]
        if i!=j:
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


if (isSave):
    PL.savefig(str(N)+"_"+str(g.number_of_edges())+"_"+str(float(graph_dens))+".png")

#*****************************************************************
#is_strongly_connected????
#***************************************************************** 


if not(isStrConn):
    is_cycle = False
    raise SystemExit
else:
    is_cycle = True 
    dfs_path = list(NX.dfs_preorder_nodes(g))
    the_biggest_cycle = original_cycle= dfs_path
    if (isDraw):
        PL.figure()
        PL.plot()   
        PL.title('Communication graph - optimalized')
        NX.draw(g,with_labels=True)
    if (isSave):
        PL.savefig(str(N)+"_"+str(g.number_of_edges())+"_"+str("%.2f" % float(graph_dens))+".png")   
    f_sm = open(str(N)+"_"+str(g.number_of_edges())+"_"+str("%.2f" % float(graph_dens))+"_SM.cnf", "w")
    f_sm.write('p cnf ')                #header
    f_sm.write('%s ' % N)
    f_sm.write('%s ' % str(kloz+2))
    f_sm.write('\n')                    #header vége
 
    for i in xrange(len(clauseSet)):
       for j in xrange(len(clauseSet[i])-1):
           model1.append(-clauseSet[i][0])
           model1.append(clauseSet[i][j+1])
           for k in model1:
               f_sm.write('%s ' % k)
           model1.append(0)
           f_sm.write('%s\n' % 0)
           model1Set.append(model1)
           model1 = []
           
    for m in range(1, N+1):
       f_sm.write('%s ' % m)
    f_sm.write('%s\n' % 0)
    #f_sm.write('\n')
    for m in range(1, N+1):
       f_sm.write('%s ' % -m)
    f_sm.write('%s\n' % 0)
    #f_sm.write('\n')
    f_sm.close()
    
   
#*****************************************************************
#BalatonBoglár Model-VALID
#*****************************************************************
  
    f_bb = open(str(N)+"_"+str(g.number_of_edges())+"_"+str("%.2f" % float(graph_dens))+"_BB.cnf", "w")
    f_bb.write('p cnf ')
    f_bb.write('%s ' % N)
    f_bb.write('\n')
    
    #NodeRep......
    nodeRepBB =[]
    nodeRepBB_n = []


    #-++ t állítja elő a fájlban
    for i in range(1,N+1):
        if int(len(list(g.successors(i))))==0: #legalább egy leszármazott
            print("")
        else:
            nodeRepBB_n.append(-i)
            if len(list(g.successors(i)))==1:
                succList = list(g.successors(i))
                nodeRepBB_n.append(succList[0])#Lehet ez ami a klózok számát jelöli
                nodeRepBB.append(nodeRepBB_n)
                nodeRepBB_n=[]
            else:#több is van
                succList = list(g.successors(i)) #gráfról lekérdező beépített metódus
                n1 = RD.randrange(0,len(succList))
                nodeRepBB_n.append(succList[n1])#Lehet ez ami a klózok számát jelöli
                n2 = n1
                while n2 == n1:
                    n2 = RD.randrange(0,len(succList))
                nodeRepBB_n.append(succList[n2])#Lehet ez ami a klózok számát jelöli
                nodeRepBB.append(nodeRepBB_n)
                nodeRepBB_n=[]
    #Eddig a részig
     
    for bbNodeRepClause in range(0,len(nodeRepBB)): #listába gyűjti, és a fájlba írja
        for bbNodeRepClause_element in range(0, len(nodeRepBB[bbNodeRepClause])):
            f_bb.write('%s ' % nodeRepBB[bbNodeRepClause][bbNodeRepClause_element])
        f_bb.write('%s\n' % 0)
    
    
    #2-hop successors
    two_hop_n=[]
    two_hop_n_n = []
    
    for i in range(1,N+1):
        succList_1_hop = list(g.successors(i))
        for j in range(0,len(succList_1_hop)):
            succList_2_hop = list(g.successors(succList_1_hop[j]))
            for k in range(0,len(succList_2_hop)):
                two_hop_n_n.append(-i)
                two_hop_n_n.append(-succList_1_hop[j])
                if succList_2_hop[k] != i:
                    two_hop_n_n.append(succList_2_hop[k])
                if len(two_hop_n_n) == 3:
                    two_hop_n.append(two_hop_n_n)      
                two_hop_n_n = []
                
    for bb2hopRepClause in range(0,len(two_hop_n)):
        for bb2hopRepClause_element in range(0, len(two_hop_n[bb2hopRepClause])):
            f_bb.write('%s ' % two_hop_n[bb2hopRepClause][bb2hopRepClause_element])
        f_bb.write('%s\n' % 0)
    

    #Constraints......
    for m in range(1, N+1):
       f_bb.write('%s ' % m)
    f_bb.write('%s\n' % 0)
    #f_sm.write('\n')
    for m in range(1, N+1):
       f_bb.write('%s ' % -m)
    f_bb.write('%s\n' % 0)
    
    f_bb.close()
    
#*****************************************************************
#Simplified BalatonBoglár Model és MSBB  -VALID only strongly connected graphs
#***************************************************************** 
    
   
    if (not(is_cycle)):
        print("No good")
        
    else: 
        f_sbb = open(str(N)+"_"+str(g.number_of_edges())+"_"+str("%.2f" % float(graph_dens))+"_SBB.cnf", "w")
        f_sbb.write('p cnf ')
        f_sbb.write('%s ' % N)
        f_sbb.write('\n')
        f_msbb = open(str(N)+"_"+str(g.number_of_edges())+"_"+str("%.2f" % float(graph_dens))+"_MSBB.cnf", "w")
        f_msbb.write('p cnf ')
        f_msbb.write('%s ' % N)
        f_msbb.write('\n')
#SBB node rep.....
        nodeRepBB =[]
        nodeRepBB_n = []
        
        for i in range(1,N+1):
            if int(len(list(g.successors(i))))==0:
                print("")
            else:
                nodeRepBB_n.append(-i)
                if len(list(g.successors(i)))==1:
                    succList = list(g.successors(i))
                    nodeRepBB_n.append(succList[0])
                    nodeRepBB.append(nodeRepBB_n)
                    nodeRepBB_n=[]
                else:
                    succList = list(g.successors(i))
                    n1 = RD.randrange(0,len(succList))
                    nodeRepBB_n.append(succList[n1])
                    n2 = n1
                    while n2 == n1:
                        n2 = RD.randrange(0,len(succList))
                    nodeRepBB_n.append(succList[n2])
                    nodeRepBB.append(nodeRepBB_n)
                    nodeRepBB_n=[]
                
        for bbNodeRepClause in range(0,len(nodeRepBB)):
            for bbNodeRepClause_element in range(0, len(nodeRepBB[bbNodeRepClause])):
                f_sbb.write('%s ' % nodeRepBB[bbNodeRepClause][bbNodeRepClause_element])
            f_sbb.write('%s\n' % 0)
            
#MSBB node rep.....
        nodeRepBB =[]
        nodeRepBB_n = []
        
        for i in range(1,N+1):
            if int(len(list(g.successors(i))))==0:
                print("")
            else:
                nodeRepBB_n.append(-i)
                for j in range(0,len(list(g.successors(i)))):
                    succList = list(g.successors(i))
                    if (i!=succList[j]): 
                        nodeRepBB_n.append(succList[j])
                nodeRepBB.append(nodeRepBB_n)
                nodeRepBB_n=[]
    
        for bbNodeRepClause in range(0,len(nodeRepBB)):
            for bbNodeRepClause_element in range(0, len(nodeRepBB[bbNodeRepClause])):
                f_msbb.write('%s ' % nodeRepBB[bbNodeRepClause][bbNodeRepClause_element])
            f_msbb.write('%s\n' % 0)

#Cycles
        
        for i in range(0,len(the_biggest_cycle)-2):
            f_sbb.write('%s ' %  -the_biggest_cycle[i] )
            f_sbb.write('%s ' %  -the_biggest_cycle[i+1] )
            f_sbb.write('%s ' %  the_biggest_cycle[i+2] )
            f_sbb.write('%s\n' % 0)
            f_msbb.write('%s ' %  -the_biggest_cycle[i] )
            f_msbb.write('%s ' %  -the_biggest_cycle[i+1] )
            f_msbb.write('%s ' %  the_biggest_cycle[i+2] )
            f_msbb.write('%s\n' % 0)
        f_sbb.write('%s ' %  -the_biggest_cycle[N-2])
        f_sbb.write('%s ' %  -the_biggest_cycle[N-1])
        f_sbb.write('%s ' %  the_biggest_cycle[0])
        f_sbb.write('%s\n' % 0)
        f_sbb.write('%s ' %  -the_biggest_cycle[N-1])
        f_sbb.write('%s ' %  -the_biggest_cycle[0])
        f_sbb.write('%s ' %  the_biggest_cycle[1])
        f_sbb.write('%s\n' % 0)
        f_msbb.write('%s ' %  -the_biggest_cycle[N-2])
        f_msbb.write('%s ' %  -the_biggest_cycle[N-1])
        f_msbb.write('%s ' %  the_biggest_cycle[0])
        f_msbb.write('%s\n' % 0)
        f_msbb.write('%s ' %  -the_biggest_cycle[N-1])
        f_msbb.write('%s ' %  -the_biggest_cycle[0])
        f_msbb.write('%s ' %  the_biggest_cycle[1])
        f_msbb.write('%s\n' % 0)
        
        
#legnagyobb kör éleinek törlése
        for i in range(0,len(the_biggest_cycle)-1):
            if g.has_edge(the_biggest_cycle[i],the_biggest_cycle[i+1]):
                g.remove_edge(the_biggest_cycle[i],the_biggest_cycle[i+1])
            if g.has_edge(the_biggest_cycle[i+1],the_biggest_cycle[i]):
                g.remove_edge(the_biggest_cycle[i+1],the_biggest_cycle[i])
        if g.has_edge(the_biggest_cycle[N-1],the_biggest_cycle[0]):
            g.remove_edge(the_biggest_cycle[N-1],the_biggest_cycle[0])
        if g.has_edge(the_biggest_cycle[0],the_biggest_cycle[N-1]):
            g.remove_edge(the_biggest_cycle[0],the_biggest_cycle[N-1])


#Redukált gráf kirajzolása.... 
        if (isDraw):
            PL.figure()
            PL.plot()   
            PL.title('Communication graph - after deleting the edges of the largest circle')
            NX.draw(g,with_labels=True)
        if (isSave):
            PL.savefig(str(N)+"_"+str(g.number_of_edges())+"_"+str("%.2f" % float(graph_dens))+"_minus_main_cycle.png")    
 
        o = 0
        isCici=len(find_cycle(g)) 
        if isCici >=0:
            while isCici >= 2:
                o+=1
              #  all_cycles = list(NX.simple_cycles(g))
              #  the_biggest_cycle = []
              #  longest_cycle_len = 0
              #  for cycle in all_cycles:
              #      cycle_len = len(cycle)
              #      if cycle_len>longest_cycle_len:
              #          the_biggest_cycle =cycle
              #          longest_cycle_len = cycle_len
                #the_biggest_cycle = the_biggest_cycle.append(the_biggest_cycle[0])
                a_cycle =[]
                cic = find_cycle(g)
                for i in range(0,len(cic)):
                   a_cycle.append(cic[i][0])
                a_cycle.append(a_cycle[0])
                if len(a_cycle) == 3:  #pl 1-->3 , 3-->1
                    f_sbb.write('%s ' %  -a_cycle[0] )
                    f_sbb.write('%s ' %  -a_cycle[1])
                    f_msbb.write('%s ' %  -a_cycle[0] )
                    f_msbb.write('%s ' %  -a_cycle[1])
                    loc= original_cycle.index(a_cycle[0])
                    if loc+1 < len(original_cycle):
                        f_sbb.write('%s ' %  original_cycle[loc + 1] )    
                        f_msbb.write('%s ' %  original_cycle[loc + 1] )   
                    else:
                        f_sbb.write('%s ' %  original_cycle[0])
                        f_msbb.write('%s ' %  original_cycle[0])
                    f_sbb.write('%s\n' % 0)
                    f_msbb.write('%s\n' % 0)
                    if g.has_edge(a_cycle[0],a_cycle[1]):
                        g.remove_edge(a_cycle[0],a_cycle[1])
                    if g.has_edge(a_cycle[1],a_cycle[0]):
                        g.remove_edge(a_cycle[1],a_cycle[0])   
                else:
                    for i in range(0,len(a_cycle)-1):
                        f_sbb.write('%s ' %  -a_cycle[i] )
                        f_sbb.write('%s ' %  -a_cycle[i+1])
                        f_msbb.write('%s ' %  -a_cycle[i] )
                        f_msbb.write('%s ' %  -a_cycle[i+1])
                        loc= original_cycle.index(a_cycle[i])
                        if loc+1 < len(original_cycle):
                            f_sbb.write('%s ' %  original_cycle[loc + 1] )
                            f_msbb.write('%s ' %  original_cycle[loc + 1] )  
                        else:
                            f_sbb.write('%s ' %  original_cycle[0])
                            f_msbb.write('%s ' %  original_cycle[0])
                        f_sbb.write('%s\n' % 0)
                        f_msbb.write('%s\n' % 0)
                    for i in range(0,len(a_cycle)-1):
                        if g.has_edge(a_cycle[i],a_cycle[i+1]):
                            g.remove_edge(a_cycle[i],a_cycle[i+1])
                        if g.has_edge(a_cycle[i+1],a_cycle[i]):
                            g.remove_edge(a_cycle[i+1],a_cycle[i])
                    if g.has_edge(a_cycle[len(a_cycle)-1],a_cycle[0]):
                        g.remove_edge(a_cycle[len(a_cycle)-1],a_cycle[0])
                    if g.has_edge(a_cycle[0],a_cycle[len(a_cycle)-1]):
                        g.remove_edge(a_cycle[0],a_cycle[len(a_cycle)-1])  
                if (isDraw):
                    PL.figure()
                    PL.plot()   
                    PL.title('Communication graph - after deleting the edges of a circle')
                    NX.draw(g,with_labels=True)
                if (isSave):
                    PL.savefig(str(N)+"_"+str(g.number_of_edges())+"_"+str("%.2f" % float(graph_dens))+"_red_"+str(o)+".png") 
                if find_cycle(g):
                    isCici=len(find_cycle(g))
                else:
                    isCici = 0
#Constraints
            for m in range(1, N+1):
                f_sbb.write('%s ' % m)
            f_sbb.write('%s\n' % 0)
            for m in range(1, N+1):
                f_sbb.write('%s ' % -m)
            f_sbb.write('%s\n' % 0)
            for m in range(1, N+1):
                f_msbb.write('%s ' % m)
            f_msbb.write('%s\n' % 0)
            for m in range(1, N+1):
                f_msbb.write('%s ' % -m)
            f_msbb.write('%s\n' % 0)
            
            f_sbb.close()
            f_msbb.close()


#*****************************************************************
#Weak Model-VALID
#***************************************************************** 

#    #WM
#    
#    
#    f_wm = open(str(N)+"_WM.cnf", "w")
#    #f_sm = open(str(N)+"_UNKNOWN_"+str(6)+".cnf", "w")
#    f_wm.write('p cnf ')
#    f_wm.write('%s ' % N)
#    #f_wm.write('%s ' % str(kloz+2))    a klózok száma érdekes kérdés...
#    f_wm.write('\n')
#    
#    #NodeRep.......
#    nodeRep=[]
#    
#    for i in range(1,N+1):
#        if len(list(NX.neighbors(g,i)))!=0:
#            f_wm.write('%s ' % -i)
#            nodeRep=list(NX.neighbors(g,i))
#            nodeRep.sort()
#            for j in xrange(len(nodeRep)):
#                f_wm.write('%s ' % nodeRep[j])
#            f_wm.write('%s ' % 0)
#            f_wm.write('\n')
#    
#    #circleRep
#      
#    
#    paths = []
#    for i in xrange(1,N+1):
#        for j in xrange(1,N+1):
#            if i <> j:
#                s_path = NX.all_simple_paths(g,i,j)
#                for sp in list(s_path):
#                    paths.append(sp)
#    
#    notSimpleCycles = []
#    temp =[]
#    print len(paths)
#    
#    
#    for p in xrange(0, len(paths)):
#        sourceNode= paths[p][0]
#        targetNode= paths[p][len(paths[p])-1]
#        for pk in xrange(0, len(paths)):
#            if paths[pk][len(paths[pk])-1]==sourceNode and paths[pk][0]==targetNode:
#                temp = list(set(paths[p]+paths[pk]))
#                if temp not in notSimpleCycles:
#                   notSimpleCycles.append(temp)
#                temp=[]      
#    
#    fCycles = []
#    finalCycles = [[]]
#    tempList = []       
#    for fn in range(0, len(notSimpleCycles)):
#        print fn
#        for fn_element in range(0, len(notSimpleCycles[fn])):
#            elem = notSimpleCycles[fn][fn_element]
#            tempList = list(g.successors(elem))
#            inElement = False
#            for nb in range(0, len(list(g.successors(elem)))):
#                if -elem not in fCycles:
#                    fCycles.append(-elem)
#                if tempList[nb] not in list(notSimpleCycles[fn]):               
#                    inElement = True
#                    if inElement == True: 
#                        fCycles.append(tempList[nb])
#        finalCycles.append(fCycles)
#        fCycles = []
#        inElement = False
#
#    # create to final cycles clauses
#    
#    for fcCLause in range(1,len(finalCycles)):
#        for fcCLause_element in range(0, len(finalCycles[fcCLause])):
#            f_wm.write('%s ' % finalCycles[fcCLause][fcCLause_element])
#        f_wm.write('%s\n' % 0)
#    
#    
#    #Constraints
#    for m in range(1, N+1):
#       f_wm.write('%s ' % m)
#    f_wm.write('%s\n' % 0)
#    #f_sm.write('\n')
#    for m in range(1, N+1):
#       f_wm.write('%s ' % -m)
#    f_wm.write('%s\n' % 0)
#    
#    f_wm.close()
#

print("OK")

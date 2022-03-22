#250+os sorok BB modell.

#from networkx.algorithms.traversal.edgedfs import helper_funcs
from itertools import count
import matplotlib
matplotlib.use('TkAgg')
import random as RND
import networkx as NX
import math as MT
import pylab

from collections import defaultdict

def simple_cycles(G):
    # Yield every elementary cycle in python graph G exactly once
    # Expects a dictionary mapping from vertices to iterables of vertices
    def _unblock(thisnode, blocked, B):
        stack = set([thisnode])
        while stack:
            node = stack.pop()
            if node in blocked:
                blocked.remove(node)
                stack.update(B[node])
                B[node].clear()
    G = {v: set(nbrs) for (v,nbrs) in G.items()} # make a copy of the graph
    sccs = strongly_connected_components(G)
    while sccs:
        scc = sccs.pop()
        startnode = scc.pop()
        path=[startnode]
        blocked = set()
        closed = set()
        blocked.add(startnode)
        B = defaultdict(set)
        stack = [ (startnode,list(G[startnode])) ]
        while stack:
            thisnode, nbrs = stack[-1]
            if nbrs:
                nextnode = nbrs.pop()
                if nextnode == startnode:
                    yield path[:]
                    closed.update(path)
                elif nextnode not in blocked:
                    path.append(nextnode)
                    stack.append( (nextnode,list(G[nextnode])) )
                    closed.discard(nextnode)
                    blocked.add(nextnode)
                    continue
            if not nbrs:
                if thisnode in closed:
                    _unblock(thisnode,blocked,B)
                else:
                    for nbr in G[thisnode]:
                        if thisnode not in B[nbr]:
                            B[nbr].add(thisnode)
                stack.pop()
                path.pop()
        remove_node(G, startnode)
        H = subgraph(G, set(scc))
        sccs.extend(strongly_connected_components(H))

def strongly_connected_components(graph):
    # Tarjan's algorithm for finding SCC's
    # Robert Tarjan. "Depth-first search and linear graph algorithms." SIAM journal on computing. 1972.
    # Code by Dries Verdegem, November 2012
    # Downloaded from http://www.logarithmic.net/pfh/blog/01208083168

    index_counter = [0]
    stack = []
    lowlink = {}
    index = {}
    result = []
    
    def _strong_connect(node):
        index[node] = index_counter[0]
        lowlink[node] = index_counter[0]
        index_counter[0] += 1
        stack.append(node)
    
        successors = graph[node]
        for successor in successors:
            if successor not in index:
                _strong_connect(successor)
                lowlink[node] = min(lowlink[node],lowlink[successor])
            elif successor in stack:
                lowlink[node] = min(lowlink[node],index[successor])

        if lowlink[node] == index[node]:
            connected_component = []

            while True:
                successor = stack.pop()
                connected_component.append(successor)
                if successor == node: break
            result.append(connected_component[:])
    
    for node in graph:
        if node not in index:
            _strong_connect(node)
    
    return result

def remove_node(G, target):
    # Completely remove a node from the graph
    # Expects values of G to be sets
    del G[target]
    for nbrs in G.values():
        nbrs.discard(target)

def subgraph(G, vertices):
    # Get the subgraph of G induced by set vertices
    # Expects values of G to be sets
    return {v: G[v] & vertices for v in vertices}

""" def find_cycle(G, source=None, orientation='original'):

    out_edge, key, tailhead = helper_funcs(G, orientation)

    explored = set()
    cycle = []
    final_node = None
    for start_node in G.nbunch_iter(source): # returns nbunch of nodes that can be iterated. none = iterates through all nodes - Moha
        if start_node in explored: # Test it! #
            # No loop is possible.
            continue
        edges = []
        seen = {start_node}
        active_nodes = {start_node}
        previous_head = None

        for edge in NX.edge_dfs(G, start_node, orientation):
            tail, head = tailhead(edge)
            if head in explored: # Test it! #
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
 """

N=4  #Number of sensors

Scope = 10  #Homogenous sensor nodes Scope
MinScope = 20.0 #Minimum scope range
MaxScope = 40.0 #Maximum scope range
rangeX = (5, 19)
rangeY = (5, 19)

isDraw = True
isSave = True

scopeRad = (MinScope, MaxScope) #Scope interval - random sugar
NodeTypes = False #homogeneous or heterogeneous  True = homogenius False=heterogeneus
if NodeTypes == True:
    print("*****Undirected graph******")
else:
    print("*****Directed graph*******")
RND.seed() #Random seed
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
    pylab.rcParams['figure.figsize'] = 7, 7
    fig = pylab.gcf()
    ax = pylab.gca()
    ax.cla()
    ax.set_xlim((0,140))
    ax.set_ylim((0,140))
    pylab.figure(1, figsize=(14, 10))
    pylab.plot() #Plot WirelesSensorNetwork (WSN)


################################### Creating network ###################################

#**************************************************************************************************************
#Sensors placement and Graph
#**************************************************************************************************************


for i in range(1,N+1):
    x = float(RND.randrange(*rangeX))
    y = float(RND.randrange(*rangeY))
    positions = (x,y)
    rndRad = RND.randrange(*scopeRad)
    g.add_node(i,pos=(x,y)) 
    if NodeTypes == False:
        arrScope.append([i,rndRad])
        Scope = rndRad
    else: 
        arrScope.append([i,Scope])
    circle = pylab.Circle((x,y), Scope,  color="blue", fill=False)
    if (isDraw):
        fig.gca().add_artist(circle) 
    pos=NX.get_node_attributes(g,'pos')
    g.nodes
if (isDraw):
    NX.draw(g,pos, with_labels=True)
    pylab.title('Sensor nodes')
    

#**************************************************************************************************************
#Weak Model elkepzeles
#**************************************************************************************************************
'''
A semi-connected graph is a graph that for each pair of vertices u,v, there is either a path from u to v or a path from v to u. Give an algorithm to test if a graph is semi-connected.
   Given a graph G=(V,E)
   -Find strongly connected components in G
   -Replace each SCC with a vertex, G become a directed acrylic graph (DAG)
   -Topological sort on DAG
   -If there is an edge between each pair of vertices(v[i],v[i+1]) then the given graph is semi-connected
'''
#**************************************************************************************************************
#Strong Model-VALID
#**************************************************************************************************************

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
                NX.add_path(g,[i,j])
                clause.append(j)
                kloz= kloz+1
    creal = clause #original  sequence
    consistof = False
    for i in range(len(clauseSet)):
       if clause == clauseSet[i]:
           consistof = True           
    if consistof == False:
        clauseSet.append(clause)     
    clause = []
    creal = []

#**************************************************************************************************************
#Details
#**************************************************************************************************************

print("Number of nodes: " , N)
print("The maximum number of edges (if the graph is directed -default): ", N*(N-1))
print("Number of edges: " , g.number_of_edges())
graph_dens = float(g.number_of_edges()) / float((N*(N-1)))
print(" Graph density : %.2f (Coleman and More 1983)."  % (graph_dens))

isStrConn =  NX.is_strongly_connected(g)
print("G is strongly connected?  "  +str(isStrConn))

if (isSave):
    pylab.savefig(str(N)+"_"+str(g.number_of_edges())+"_"+str(float(graph_dens))+".png")


print(g)
d = simple_cycles(NX.to_dict_of_lists(g))
print(tuple(d))

#**************************************************************************************************************
#is_strongly_connected????
#**************************************************************************************************************


if not(isStrConn):
    is_cycle = False
    raise SystemExit
else:
    is_cycle = True 
    dfs_path = list(NX.dfs_preorder_nodes(g))
    the_biggest_cycle = original_cycle= dfs_path
    if (isDraw):
        pylab.figure()
        pylab.plot()   
        pylab.title('Communication graph - optimalized')
        NX.draw(g,with_labels=True)
    if (isSave):
        pylab.savefig(str(N)+"_"+str(g.number_of_edges())+"_"+str("%.2f" % float(graph_dens))+".png")   
    f_sm = open(str(N)+"_"+str(g.number_of_edges())+"_"+str("%.2f" % float(graph_dens))+"_SM.cnf", "w")
    f_sm.write('p cnf ')                #header
    f_sm.write('%s ' % N)
    f_sm.write('%s ' % str(kloz+2))
    f_sm.write('\n')                    #header vege
 
    for i in range(len(clauseSet)):
       for j in range(len(clauseSet[i])-1):
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
    
   
#**************************************************************************************************************
#BalatonBoglar Model-VALID
#**************************************************************************************************************
  
    f_bb = open(str(N)+"_"+str(g.number_of_edges())+"_"+str("%.2f" % float(graph_dens))+"_BB.cnf", "w")
    f_bb.write('p cnf ')
    f_bb.write('%s ' % N)
    f_bb.write('\n')
    
    #NodeRep......
    nodeRepBB =[]
    nodeRepBB_n = []

    #-++ t allitja elo a fileban
    for i in range(1,N+1):
        if int(len(list(g.successors(i))))==0: #legalabb egy leszarmazott
            print("")
        else:
            nodeRepBB_n.append(-i)
            if len(list(g.successors(i)))==1:
                succList = list(g.successors(i))
                nodeRepBB_n.append(succList[0])#Lehet ez ami a klozok szamat jeloli
                nodeRepBB.append(nodeRepBB_n)
                nodeRepBB_n=[]
            else:#tobb is van
                succList = list(g.successors(i)) #grafrol lekerdezo beepitett metodus
                n1 = RND.randrange(0,len(succList))
                nodeRepBB_n.append(succList[n1])#Lehet ez ami a klozok szamat jeloli
                n2 = n1
                while n2 == n1:
                    n2 = RND.randrange(0,len(succList))
                nodeRepBB_n.append(succList[n2])#Lehet ez ami a klozok szamat jeloli
                nodeRepBB.append(nodeRepBB_n)
                nodeRepBB_n=[]
    #Eddig a reszig
     
    for bbNodeRepClause in range(0,len(nodeRepBB)): #listaba gyujti, es a fajlba irja
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
                if succList_2_hop[k]  != i:
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
    
#**************************************************************************************************************
#Simplified BalatonBoglar Model es MSBB  -VALID only strongly connected graphs
#**************************************************************************************************************
    
   
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
                    n1 = RND.randrange(0,len(succList))
                    nodeRepBB_n.append(succList[n1])
                    n2 = n1
                    while n2 == n1:
                        n2 = RND.randrange(0,len(succList))
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
        
        
#legnagyobb kor eleinek torlese
        for i in range(0,len(the_biggest_cycle)-1):
            if g.has_edge(the_biggest_cycle[i],the_biggest_cycle[i+1]):
                g.remove_edge(the_biggest_cycle[i],the_biggest_cycle[i+1])
            if g.has_edge(the_biggest_cycle[i+1],the_biggest_cycle[i]):
                g.remove_edge(the_biggest_cycle[i+1],the_biggest_cycle[i])
        if g.has_edge(the_biggest_cycle[N-1],the_biggest_cycle[0]):
            g.remove_edge(the_biggest_cycle[N-1],the_biggest_cycle[0])
        if g.has_edge(the_biggest_cycle[0],the_biggest_cycle[N-1]):
            g.remove_edge(the_biggest_cycle[0],the_biggest_cycle[N-1])


#Redukalt graf kirajzolasa.... 
        if (isDraw):
            pylab.figure()
            pylab.plot()   
            pylab.title('Communication graph - after deleting the edges of the largest circle')
            NX.draw(g,with_labels=True)
        if (isSave):
            pylab.savefig(str(N)+"_"+str(g.number_of_edges())+"_"+str("%.2f" % float(graph_dens))+"_minus_main_cycle.png")    
 
        o = 0
        isCici=len(tuple(g))
        if isCici >=0:
            while isCici >= 2:
                o+=1
                a_cycle =[]
                cic = g
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
                    pylab.figure()
                    pylab.plot()   
                    pylab.title('Communication graph - after deleting the edges of a circle')
                    NX.draw(g,with_labels=True)
                if (isSave):
                    pylab.savefig(str(N)+"_"+str(g.number_of_edges())+"_"+str("%.2f" % float(graph_dens))+"_red_"+str(o)+".png") 
                if g:
                    isCici=len(list(g))
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

print("OK")

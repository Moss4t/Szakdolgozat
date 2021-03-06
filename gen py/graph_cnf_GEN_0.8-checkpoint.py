from collections import defaultdict
import matplotlib
matplotlib.use('TkAgg')
#import matplotlib.pyplot as plt
import random as rnd
import networkx as nx
import math as mt
import pylab


def _unblock(thisnode, blocked, B):
	stack = {thisnode}
	while stack:
		node = stack.pop()
		if node in blocked:
			blocked.remove(node)
			stack.update(B[node])
			B[node].clear()

def simple_cycles(G):
	# Johnson's algorithm requires some ordering of the nodes.
	# We assign the arbitrary ordering given by the strongly connected comps
	# There is no need to track the ordering as each node removed as processed.
	# Also we save the actual graph so we can mutate it. We only take the
	# edges because we do not want to copy edge and node attributes here.
	subG = type(G)(G.edges())
	sccStack = [scc for scc in nx.strongly_connected_components(subG) if len(scc) > 1]

	# Johnson's algorithm exclude self cycle edges like (v, v)
	# To be backward compatible, we record those cycles in advance
	# and then remove from subG
	for v in subG:
		if subG.has_edge(v, v):
			yield [v]
			subG.remove_edge(v, v)

	while sccStack:
		scc = sccStack.pop()
		sccG = subG.subgraph(scc)
		# order of scc determines ordering of nodes
		startnode = scc.pop()
		# Processing node runs "circuit" routine from recursive version ( recursive version = teljessen másik verzió/implementációból)
		path = [startnode]
		blocked = set() # vertex: blocked from search? # Maybe visited?
		closed = set() # nodes involved in a cycle
		blocked.add(startnode)
		B = defaultdict(set) # graph portions that yield no elementary circuit
		stack = [(startnode, list(sccG[startnode]))] # sccG gives comp neibrs # sccGraph gives component neighbors
		while stack:
			thisnode, neibrs = stack[-1]
			if neibrs:
				nextnode = neibrs.pop()
				if nextnode == startnode:
					yield path[:]
					closed.update(path)
#						print "Found a cycle", path, closed
				elif nextnode not in blocked:
					path.append(nextnode)
					stack.append((nextnode, list(sccG[nextnode])))
					closed.discard(nextnode)
					blocked.add(nextnode)
					continue
			# done with nextnode... look for more neighbors
			if not neibrs: # no more neibrs
				if thisnode in closed:
					_unblock(thisnode, blocked, B)
				else:
					for nbr in sccG[thisnode]:
						if thisnode not in B[nbr]:
							B[nbr].add(thisnode)
				stack.pop()
				#				assert path[-1] == thisnode
				path.pop()
		# done processing this node
		H = subG.subgraph(scc) # make smaller to avoid work in SCC routine
		sccStack.extend(scc for scc in nx.strongly_connected_components(H) if len(scc) > 1)

# CODE ABOVE is networkx original implementation

N=6 #Number of sensors

Scope = 10 #Homogenous sensor nodes Scope
MinScopeRange = 7
MaxScopeRange = 37
rangeX = (25, 65)
rangeY = (25, 65)

isDraw = False
isSave = False

scopeRad = (MinScopeRange, MaxScopeRange) #Scope interval - random sugar
NodeTypes = False #homogeneous or heterogeneous; True= homogenius False= heterogeneus
if NodeTypes == True:
	print("*****Undirected graph******")
else:
	print("*****Directed graph*******")
rnd.seed() #Random seed
clauseSet=[]
clauseSetReal = []
clause=[]
creal=[]
model1=[]
model1Set=[]
model2=[]
model2Set=[]
list_of_cliques = []
arrScope = [[]]
WMclause =[]
WMclauseSet = []




#Directed graph
# g = nx.DiGraph()

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


""" for i in range(1,N+1):
	x = float(rnd.randrange(*rangeX))
	y = float(rnd.randrange(*rangeY))
	positions = (x,y)
	rndRad = rnd.randrange(*scopeRad)
	g.add_node(i,pos=(x,y))
	if NodeTypes == False:
		arrScope.append([i,rndRad])
		Scope = rndRad
	else:
		arrScope.append([i,Scope])
	circle = pylab.Circle((x,y), Scope, color="blue", fill=False)
	if (isDraw):
		fig.gca().add_artist(circle)
	pos=nx.get_node_attributes(g,'pos')
	#g.node.values() # originaly debug data? Why run it for every node?
#print("Original placement of nodes on the field")
#print(g.nodes.data())
#These comments are not deleted, what if you ever need it...
if (isDraw):
	nx.draw(g,pos, with_labels=True)
	pylab.title('Sensor nodes') """

#**************************************************************************************************************
#Strong Model-VALID
#**************************************************************************************************************

kloz = 0
edges = []
# Generating graph & cnf file
""" for i in range(1,N+1):
	clause.append(i)
	for j in range(1,N+1):
		x1,y1 = pos[i]
		x2,y2 = pos[j]
		if i!=j:
			if NodeTypes == False:
				Comm = arrScope[i][1]+arrScope[j][1]
			else:
				Comm = 50
			if (mt.sqrt(mt.pow((x2-x1),2)+mt.pow((y2-y1),2)))<= arrScope[i][1]:
				edges.append((i,j))
				clause.append(j)
				kloz= kloz+1
	creal = clause #original sequence
	consistof = False
	for i in range(len(clauseSet)):
		if clause == clauseSet[i]:
			consistof = True
	if consistof == False:
		clauseSet.append(clause)
	clause = []
	creal = []
 """
edges.append((2,1))
edges.append((1,3))
edges.append((1,4))
edges.append((3,2))
edges.append((4,5))

g = nx.DiGraph(edges)
# print(list(nx.simple_cycles(g)))

#**************************************************************************************************************
#Weak Model elkepzeles
#**************************************************************************************************************
''' define the weak model
A semi-connected graph is a graph that for each pair of vertices u,v,
	there is either a path from u to v or a path from v to u.
	Give an algorithm to test if a graph is semi-connected.
 Given a graph G=(V,E)
	-Find strongly connected components in G
	-Replace each SCC with a vertex, G become a directed acyclic graph (DAG)
	-Topological sort on DAG
	-If there is an edge between each pair of vertices(v[i],v[i+1]) then
	the given graph is semi-connected

Egy félig összefüggő gráf olyan gráf, ami
	minden pár csúcs u, v közt van él u-ból v-be vagy v-ből u-ba.
	Adott egy algoritmus, ami leteszteli, ha egy gráf félig összefüggő.
 Adott egy gráf G = (V, E)
	- Találjuk meg G erősen összetett komponenseit (scc).
	- Cseréljük ki az összes scc-t egy csúcsra, és G
	egy irányított aciklikus gráf (DAG) lett.
	- Topológiailag rendezzük a kapott DAG-ot.
	- Ha van él minden adott csúcs közt (v[i], v[i+1]), akkor az adott gráf
	félig összefüggő.
	Side note: Az algráf minden éle legyen G-nek az éle, amivel össze van kötve = (v[i], v[i+1]).

	
	# Johnson algoritmusának szüksége van a csomópontok rendezésére. Az erősen összetett komponensek által megadott tetszőleges sorrendet rendelünk a csúcsokhoz.
	# Nem szükséges a rendezés számontartása, mivel minden csomópont feldolgozás után törölve lesz. Valamint az eredeti gráfot elmentjük, hogy változtathassuk. 
	# Csak az éleket vegyük ki, mert nincs szükség a tulajdonságaira.
'''
#stack-ben csak egyszer szerepelhet egy elem. Ezért lehetséges. Nem ismétlődnek az scc elemei.


def weak_model_gen(G):
	#? nem tudom biztosra, hogy kéne előre vizsgálni.
	# OK = nx.is_strongly_connected(G) & nx.is_semiconnected(G)
	# if not OK:
	# 	print("Not scc, or semiconnection")
		# print("Exited method: weak_model_gen, bad_args")
		# raise SystemExit

	negative_literals = []
	exitpoints = []
	all_clauses = []
	edges_plus = []
	edges = type(G)(G.edges())
	print("minden él:", edges.edges())
	# Todo: scc_count legyen a len(G.nodes()), mint alap érték, hogy nagyobb legyen bármelyik node számánál az scc-t helyettesítő node száma.
	# Todo: Lehet jobb, biztosabb megoldást kell erre kitalálni.
	scc_count = len(G.nodes())
	Graph = nx.DiGraph(G.edges())
	sccStack = [scc for scc in nx.strongly_connected_components(Graph) if len(scc) > 1]
	while sccStack:
		scc_Cycle = sccStack.pop()
		scc_count += 1
		for scc_elem_x in scc_Cycle:
			negative_literals.append(-scc_elem_x)		#! neg literal
			dads_one_far = [ des for des in nx.descendants_at_distance(Graph, scc_elem_x, 1)]
			print("next szomszéd:", dads_one_far)
			while dads_one_far:
				dad_element = dads_one_far.pop()
				for scc_elem_y in scc_Cycle:
					if dad_element != scc_elem_y:
						print("scc: %i, szomszédja: %i" % (scc_count, dad_element))
						edges_plus.append((scc_count, dad_element))
						exitpoints.append(dad_element)	#! pos literal
						break
					
					print("Törölt él:", (scc_elem_x, dad_element))
					# scc_Cycle.remove(scc_elem_x)
					edges.remove_edge(scc_elem_x, dad_element)
				# print("Neighbors %i. edge: " % dad_element + str(edges))
			exitpoints.append(0.1)
			for i in negative_literals:
				all_clauses.append(i)
			for i in exitpoints:
				all_clauses.append(i)
		print(negative_literals)
		print(exitpoints)

		negative_literals = []
		exitpoints = []

	# Todo: edges-nek átadni az összes élt. Az scc-k éleit törölni és kicserélni a scc_count + exitpoint kimenetre
	# edges és edges_plus-t rendezni. Hogy jó  wm  legyen tárolva.

	wm = nx.DiGraph(edges_plus)
	isDAG = nx.is_directed_acyclic_graph(wm)
	print("Is it a DAG? " + str(isDAG))
	print("Is it semiconnected? " + str(nx.is_semiconnected(wm)))
	if(isDAG):
		#! amíg hibás a kijövő adat, addig nem lesz jó ez se jó.
		# Todo: az éleket a kiválogatás után hozzá adni. És az kell a fileba.
		wm = nx.topological_sort(wm)
	print(wm)
	print(list(wm))

	# if isDraw:
	if True:
		pylab.savefig(str(N)+"_"+str(g.number_of_edges())+"_"+str("%.2f" % float(graph_dens))+"_WM.png")
	# if isSave:
		file_wm = open(str(N)+"_"+str(g.number_of_edges())+"_"+str("%.2f" % float(graph_dens))+"_WM.cnf", "w")
		file_wm.write('p cnf ')			#header
		file_wm.write('%s ' % N)
		file_wm.write('%s ' % str(len(all_clauses)))
		file_wm.write('\n')				#header vege

		print("\nTo file: ", end='')
		for i in all_clauses:
			if i != 0.1:
				file_wm.write('%s ' % str(i))
				print(str(i) + ' ', end='')
			else:
				file_wm.write('%s\n' % 0)

 		# Fekete és fehér hozzárendelés
		for n in range(1, N+1):
			file_wm.write('%s ' % n)
		file_wm.write('%s\n' % 0)
		for n in range(1, N+1):
			file_wm.write('%s ' % -n)
		file_wm.write('%s\n' % 0)
		file_wm.close()

	""" egyszerű wm leírás
	Kigyűjtjük az scc-ket.
		Bonyolultakat is kellene (Amíg van scc: ...), mert
		a-b kör, b-c kör. akkor lehet küldeni üzenetet a>b>c>b>a>...
		ha a-b X és b-c Y scc-k, valamint megakarjuk tartani a köztük lévő kapcsolatot, akkor
		megint egy scc-t hozunk létre X-Y kör formájában ...Nem jó!
		Akkor egy darab nagy Z scc-t kéne mondjuk létrehozni?
		Ha pedig teljes gráfról beszélünk, akkor az egészből nem csinálhatunk 1 db scc-t. Vagy igen?
	Kicseréljük az scc-ket csúcsokra
	Össze kötjük
		Iránynak merre? Legyen nem irányított? (undirected. Nem DAG? nem lehet topologiailag rendezni?)
	Topológiailag rendezzük a csúcsokat.
	"""

# Python implementation of Kosaraju's algorithm to print all SCCs
# Az összes scc-t megadja
def dfs_util(self, Graph, node, visited, sccs):
	visited[node] = True
	# Mark the current node as visited and print it
	sccs.append((node))
	print(node)
	# Recur for all the vertices adjacent to this vertex
	for i in range(len(Graph.nodes())):
		if visited[i] == False:
			dfs_util(self, Graph, i,visited, sccs)
	return sccs

nx.DiGraph.dfs_util = dfs_util # Monkey patch, it's kinda like delegates :)

def fill_order(Graph, node, visited, stack):
	visited[node] = True
	# Recur for all the vertices adjacent to this vertex
	for i in Graph.nodes(node):
		if visited[node] == False:
			fill_order(Graph, i, visited, stack)
	stack = stack.append(node)

nx.DiGraph.fill_order = fill_order

def get_transpose(Graph):
	g = nx.DiGraph(Graph)
	# Recur for all the vertices adjacent to this vertex
	for i in Graph.nodes():
		for j in Graph.nodes(i):
			g.add_edge(j,i)
	return g

nx.DiGraph.get_transpose = get_transpose

def get_all_scc(Graph):
	stack = []
	visited = [False]*Graph.number_of_nodes()
	for i in range(Graph.number_of_nodes()):
		if visited[i] == False:
			fill_order(Graph, i, visited, stack)

	# Create reversed graph
	gr = get_transpose(Graph)
	sccs = []

	# Mark all nodes as not visited (For second DFS)
	visited = [False]*len((Graph.nodes))

	# Process in order defined by the stack
	while stack:
		i = stack.pop()
		if not visited[i]:
			sccs = gr.dfs_util(Graph, i, visited, sccs)
			print("Gave every scc to you")
			return sccs

# Use it on the given graph.
# This code is contributed by Neelam Yadav.

nx.DiGraph.generate_all_scc = get_all_scc

#**************************************************************************************************************
#Details original
#**************************************************************************************************************

graph_dens = float(g.number_of_edges()) / float((N*(N-1)))
print("Number of nodes: " , N)
print("The maximum number of edges (if the graph is directed -default): ", N*(N-1))
print("Number of edges: " , g.number_of_edges())
print(" Graph density : %.2f (Coleman and More 1983)." % (graph_dens))

if (isSave):
	pylab.savefig(str(N)+"_"+str(g.number_of_edges())+"_"+str("%.2f" % float(graph_dens))+"_base.png")

#**************************************************************************************************************
# Details 1.0 - is_strongly_connected?????
#**************************************************************************************************************

isStrConn = nx.is_strongly_connected(g)
print("G is strongly connected? " +str(isStrConn))
copyG = type(g)(g)
# print(nx.condensation(copyG))
weak_model_gen(g)

#**************************************************************************************************************
#Strong model
#**************************************************************************************************************

if not(isStrConn):
	is_cycle = False
	raise SystemExit
else:
	is_cycle = True
	dfs_path = list(nx.dfs_preorder_nodes(g))
	the_biggest_cycle = original_cycle= dfs_path
	if (isDraw):
		pylab.figure()
		pylab.plot()
		pylab.title('Communication graph - optimalized')
		nx.draw(g,with_labels=True)
	if (isSave):
		pylab.savefig(str(N)+"_"+str(g.number_of_edges())+"_"+str("%.2f" % float(graph_dens))+"_SM.png")
		f_sm = open(str(N)+"_"+str(g.number_of_edges())+"_"+str("%.2f" % float(graph_dens))+"_SM.cnf", "w")
		f_sm.write('p cnf ')			#header
		f_sm.write('%s ' % N)
		f_sm.write('%s ' % str(kloz+2))
		f_sm.write('\n')				#header vege

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
		for m in range(1, N+1):
			f_sm.write('%s ' % -m)
		f_sm.write('%s\n' % 0)
		f_sm.close()


#**************************************************************************************************************
#BalatonBoglar Model-VALID
#**************************************************************************************************************
if(isSave):
	f_bb = open(str(N)+"_"+str(g.number_of_edges())+"_"+str("%.2f" % float(graph_dens))+"_BB.cnf", "w")
	f_bb.write('p cnf ')
	f_bb.write('%s ' % N)
	f_bb.write('\n')

	nodeRepBB =[]
	nodeRepBB_temp = []

	#-++ t allitja elo a fileban (npp literalokat)
	for i in range(1,N+1):
		if int(len(list(g.successors(i))))==0: #legalabb egy leszarmazott
			print("")
		else:
			nodeRepBB_temp.append(-i)
			if len(list(g.successors(i)))==1:
				succList = list(g.successors(i))
				nodeRepBB_temp.append(succList[0])
				nodeRepBB.append(nodeRepBB_temp)
				nodeRepBB_temp=[]
			else: #tobb leszarmazott is van
				succList = list(g.successors(i))
				n1 = rnd.randrange(0,len(succList))
				nodeRepBB_temp.append(succList[n1])
				n2 = n1
				while n2 == n1:
					n2 = rnd.randrange(0,len(succList))
				nodeRepBB_temp.append(succList[n2])
				nodeRepBB.append(nodeRepBB_temp)
				nodeRepBB_temp=[]
		
	for bbNodeRepClause in range(0,len(nodeRepBB)):
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

"""
#**************************************************************************************************************
#Simplified BalatonBoglar Model es MSBB-VALID only strongly connected graphs
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


#**************************************************************************************************************
#SBB node rep
#**************************************************************************************************************
nodeRepBB =[]
nodeRepBB_temp = []

for i in range(1,N+1):
	if int(len(list(g.successors(i))))==0:
		print("")
	else:
		nodeRepBB_temp.append(-i)
		if len(list(g.successors(i)))==1:
			succList = list(g.successors(i))
			nodeRepBB_temp.append(succList[0])
			nodeRepBB.append(nodeRepBB_temp)
			nodeRepBB_temp=[]
		else:
			succList = list(g.successors(i))
			n1 = rnd.randrange(0,len(succList))
			nodeRepBB_temp.append(succList[n1])
			n2 = n1
			while n2 == n1:
				n2 = rnd.randrange(0,len(succList))
			nodeRepBB_temp.append(succList[n2])
			nodeRepBB.append(nodeRepBB_temp)
			nodeRepBB_temp=[]
		
for bbNodeRepClause in range(0,len(nodeRepBB)):
	for bbNodeRepClause_element in range(0, len(nodeRepBB[bbNodeRepClause])):
		f_sbb.write('%s ' % nodeRepBB[bbNodeRepClause][bbNodeRepClause_element])
	f_sbb.write('%s\n' % 0)



#**************************************************************************************************************
#MSBB node rep
#**************************************************************************************************************
nodeRepBB =[]
nodeRepBB_temp = []

for i in range(1,N+1):
	if int(len(list(g.successors(i))))==0:
		print("")
	else:
		nodeRepBB_temp.append(-i)
		for j in range(0,len(list(g.successors(i)))):
			succList = list(g.successors(i))
			if (i!=succList[j]):
				nodeRepBB_temp.append(succList[j])
		nodeRepBB.append(nodeRepBB_temp)
		nodeRepBB_temp=[]

for bbNodeRepClause in range(0,len(nodeRepBB)):
	for bbNodeRepClause_element in range(0, len(nodeRepBB[bbNodeRepClause])):
		f_msbb.write('%s ' % nodeRepBB[bbNodeRepClause][bbNodeRepClause_element])
	f_msbb.write('%s\n' % 0)

#Cycles......
for i in range(0,len(the_biggest_cycle)-2):
	f_sbb.write('%s ' % -the_biggest_cycle[i] )
	f_sbb.write('%s ' % -the_biggest_cycle[i+1] )
	f_sbb.write('%s ' % the_biggest_cycle[i+2] )
	f_sbb.write('%s\n' % 0)
	f_msbb.write('%s ' % -the_biggest_cycle[i] )
	f_msbb.write('%s ' % -the_biggest_cycle[i+1] )
	f_msbb.write('%s ' % the_biggest_cycle[i+2] )
	f_msbb.write('%s\n' % 0)
f_sbb.write('%s ' % -the_biggest_cycle[N-2])
f_sbb.write('%s ' % -the_biggest_cycle[N-1])
f_sbb.write('%s ' % the_biggest_cycle[0])
f_sbb.write('%s\n' % 0)
f_sbb.write('%s ' % -the_biggest_cycle[N-1])
f_sbb.write('%s ' % -the_biggest_cycle[0])
f_sbb.write('%s ' % the_biggest_cycle[1])
f_sbb.write('%s\n' % 0)
f_msbb.write('%s ' % -the_biggest_cycle[N-2])
f_msbb.write('%s ' % -the_biggest_cycle[N-1])
f_msbb.write('%s ' % the_biggest_cycle[0])
f_msbb.write('%s\n' % 0)
f_msbb.write('%s ' % -the_biggest_cycle[N-1])
f_msbb.write('%s ' % -the_biggest_cycle[0])
f_msbb.write('%s ' % the_biggest_cycle[1])
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
	nx.draw(g,with_labels=True)
if (isSave):
	pylab.savefig(str(N)+"_"+str(g.number_of_edges())+"_"+str("%.2f" % float(graph_dens))+"_minus_main_cycle.png")

#error miatt kimarad a lentebbi kód, mert így hibás sbb és msbb modelleket generálok.
o = 0
isCici=len(tuple(g))
if isCici >=0:
	while isCici >= 2:
		o+=1
		a_cycle =[]
		print(g.nodes)
		print(g.edges)
		cic = g
		for i in range(0,len(cic)):

			# kis debug rész
			print(i)
			print(cic.edges[i])

			a_cycle.append(cic[i][0])
				# important line: error
				# a g [()]
				# cic [i][0] ? az melyik
				# g-re átírni. Most már [()] az edges változó és a
				# g = nx.DiGraph(edges)
				# list(nx.simple_cycles(g)) részek miatt más .append() kell
		a_cycle.append(a_cycle[0])
		if len(a_cycle) == 3: #pl 1-->3 , 3-->1
			f_sbb.write('%s ' % -a_cycle[0] )
			f_sbb.write('%s ' % -a_cycle[1])
			f_msbb.write('%s ' % -a_cycle[0] )
			f_msbb.write('%s ' % -a_cycle[1])
			loc= original_cycle.index(a_cycle[0])
			if loc+1 < len(original_cycle):
				f_sbb.write('%s ' % original_cycle[loc + 1] )
				f_msbb.write('%s ' % original_cycle[loc + 1] )
			else:
				f_sbb.write('%s ' % original_cycle[0])
				f_msbb.write('%s ' % original_cycle[0])
			f_sbb.write('%s\n' % 0)
			f_msbb.write('%s\n' % 0)
			if g.has_edge(a_cycle[0],a_cycle[1]):
				g.remove_edge(a_cycle[0],a_cycle[1])
			if g.has_edge(a_cycle[1],a_cycle[0]):
				g.remove_edge(a_cycle[1],a_cycle[0])
		else:
			for i in range(0,len(a_cycle)-1):
				f_sbb.write('%s ' % -a_cycle[i] )
				f_sbb.write('%s ' % -a_cycle[i+1])
				f_msbb.write('%s ' % -a_cycle[i] )
				f_msbb.write('%s ' % -a_cycle[i+1])
				loc= original_cycle.index(a_cycle[i])
				if loc+1 < len(original_cycle):
					f_sbb.write('%s ' % original_cycle[loc + 1] )
					f_msbb.write('%s ' % original_cycle[loc + 1] )
				else:
					f_sbb.write('%s ' % original_cycle[0])
					f_msbb.write('%s ' % original_cycle[0])
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
			nx.draw(g,with_labels=True)
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
"""
print("Ended")

from itertools import tee, islice, chain
import networkx as nx
import pylab

#**************************************************************************************************************
# Weak Model elkepzeles
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
'''


#**************************************************************************************************************
# Strong Model
#**************************************************************************************************************
# source: https://stackoverflow.com/questions/1011938/loop-that-also-accesses-previous-and-next-values
# original implementation by: https://stackoverflow.com/users/17160/nosklo
# editor: https://stackoverflow.com/users/4495634/zaidrehman
def previous_and_next(some_iterable):
	prevs, items, nexts = tee(some_iterable, 3)
	prevs = chain([None], prevs)
	nexts = chain(islice(nexts, 1, None), [None]) # -1 -2 -3 1 0
	return zip(prevs, items, nexts)
# here is one of my modifications:
def previous(some_iterable):
	prevs, items = tee(some_iterable, 2)
	prevs = chain([None], prevs)
	return zip(prevs, items)
	
#Todo: csinálj teszteket a tesztelő file-al. Csinálj még több tesztet, hogy biztosan jól működjön.

def strong_model_literal_gen(G):
	clause = []
	# bw_clause = []
	for i, j in G.edges():
		clause.append(-i)
		clause.append(j)
		clause.append(0.1)
	# for i in G.nodes():
	# 	bw_clause.append(i)
	# for i in bw_clause:
	# 	clause.append(-i)
	# clause.append(0.1)
	# for i in bw_clause:
	# 	clause.append(i)
	# clause.append(0.1)
	return clause


#**************************************************************************************************************
# Expanded Weak Model elkepzeles
#**************************************************************************************************************
def expanded_strong_model_literal_gen(G):
	"""Returns the expanded strong model of a graph. 

	The expanded strong model of a graph gives a list of literals.
	Each clause is separated with the unique value 0.1.

	Parameters
	----------
	G: Networkx DiGraph
		A directed graph

	Returns
	-------
	Clause: A single iterable list
		Every negative literal represents a cycle, and every positive 
		literal is an exit point of it. A cycle does not include the 
		same value twice.

	Example
	-------
	DiGraph's edges: 
		((1,2),(2,1),
		(1,3),
		(3,4),(4,3),(5,3),(5,4),(4,5),(3,5))
	Literals generated:
		-1 -2 6
		-3 -4 -5 7
		-6 7
	
	Note
	----
	There can't be any self loops, like (1,1). It will be deleted.
	"""
	
	""" szükségtelen, hiszen minden node-ot csak egyszer rak bele egy scc-be. A self loop így értelmét veszti.
	subG = G
	for v in subG:
		if subG.has_edge(v, v):
			yield [v]
			subG.remove_edge(v, v) """
	
	dagG = condensation(G, None, G.number_of_nodes() + 1)

	mem = nx.get_node_attributes(dagG, "members")
	print("members: ",mem)
	# members:  {0: {5}, 1: {4}, 2: {1, 2, 3}}
	# indecies:	[0] [1],[0] [1],[0] [	1	]
	clause = []
	if len(dagG.edges()) == 0:
		for cycle in mem.items[1]:
			clause.append(-cycle)
		#clause.append(mem.items[0])
		#érdekes. Kell külön átvinni, hogy egy scc-vel helyettesítek? Vagy ha csak 1 scc van, akkor annak elemei + f-f klóz és kész. Vagy csak a f-f klózok, hiszen az az egyedüli megoldás
		clause.append(0.1)
		return clause
	else:
		for prev, current in previous(mem.items()):
			for cycle in current[1]:
				clause.append(-cycle)
			clause.append(current[0])
			clause.append(0.1)
			if prev == None:
				continue
			if (prev[0], current[0]) in dagG.edges():
				clause.append(-prev[0])
				clause.append(current[0])
				clause.append(0.1)
			elif (current[0], prev[0]) in dagG.edges():
				clause.append(-current[0])
				clause.append(prev[0])
				clause.append(0.1)
		return clause

def condensation(G, scc=None, offset=0):
	"""Returns the condensation of G.
	The condensation of G is the graph with each of the strongly connected
	components contracted into a single node.
	Parameters
	----------
	G : NetworkX DiGraph
		A directed graph.
	scc: list or generator (optional, default=None)
		Strongly connected components. If provided, the elements in
		`scc` must partition the nodes in `G`. If not provided, it will be
		calculated as scc=nx.strongly_connected_components(G).
	Returns
	-------
	C : NetworkX DiGraph
		The condensation graph C of G. The node labels are integers
		corresponding to the index of the component in the list of
		strongly connected components of G. C has a graph attribute named
		'mapping' with a dictionary mapping the original nodes to the
		nodes in C to which they belong. Each node in C also has a node
		attribute 'members' with the set of original nodes in G that
		form the SCC that the node in C represents.
	Raises
	------
	NetworkXNotImplemented
		If G is undirected.
	Notes
	-----
	After contracting all strongly connected components to a single node,
	the resulting graph is a directed acyclic graph.
	"""
	if scc is None:
		scc = nx.strongly_connected_components(G)
	mapping = {}
	members = {}
	C = nx.DiGraph()
	#Nm = G.number_of_nodes()
	#?component az ami meghatározza, hanyadik scc, ezt kell átírni Node + num_scc
	# Add mapping dict as graph attribute
	C.graph["mapping"] = mapping
	if len(G) == 0:
		return C
	for i, component in enumerate(scc, offset):
		members[i] = component
		mapping.update((n, i) for n in component)
	number_of_components = i + 1
	C.add_nodes_from(range(number_of_components))
	C.add_edges_from(
		(mapping[u], mapping[v]) for u, v in G.edges() if mapping[u] != mapping[v]
	)
	# Add a list of members (ie original nodes) to each node (ie scc) in C.
	nx.set_node_attributes(C, members, "members")
	return C


def model_to_picture():
	""" Unfinnished method! """
	print("Nothing")
#todo
""" 	N = G.number_of_nodes()
	E = G.number_of_edges()
	D = nx.density(G)

	pylab.title("Weak Model's Starting Graph")
	nx.draw(G, with_labels = True)
	pylab.savefig(str(N)+"_"+str(E)+"_"+str("%.2f" % float(D))+"_WM.png") """

def model_to_cnf_file(G, Literals, Title):
	"""Creates the cnf model of a graph, adds the black and white clauses to the end of it, and puts it all in a file.

	By the original graph, the list of literals and the type of model we want
	it creates a cnf file. 
	It gives the file name by node count _ edge count _ density _ type or title .cnf

	Parameters
	----------
	G: Networkx DiGraph
		A directed graph

	Literals: List
		A list of every literal in the graph. For separation of clauses 
		it uses the value 0.1

	Title: string
		This differates the files.		

	Returns
	-------
	None: It creates a file next to the .py, in wich you called this function

	Notes
	-----
	If you give the same parameters to this method, it will override 
	the previous file with the same name.

	"""
	N = G.number_of_nodes()
	E = G.number_of_edges()
	D = nx.density(G)
	C = 2 # BB and WW clauses.
	for i in Literals:
		if i == 0.1:
			C += 1

	file_wm = open(str(N)+"_"+str(E)+"_"+str("%.2f" % float(D))+"_"+Title+".cnf", "w")
	file_wm.write('p cnf ')			#header
	file_wm.write('%s ' % N)
	file_wm.write('%s ' % C)
	file_wm.write('\n')				#header vege

	print("\nTo file: ", end='')
	for i in Literals:
		if i != 0.1:
			file_wm.write('%s ' % str(i))
			print(str(i) + ' ', end='')
		else:
			file_wm.write('%s\n' % 0)
			print("0 ", end='')
	print()

	# Fekete és fehér hozzárendelés
	for n in range(1, N+1):
		file_wm.write('%s ' % -n)
	file_wm.write('%s\n' % 0)
	for n in range(1, N+1):
		file_wm.write('%s ' % n)
	file_wm.write('%s\n' % 0)
	file_wm.close()

def main():
	edges = []
	# Geeks for Geeks graph example:
	edges.append((2,1))
	edges.append((1,3))
	edges.append((1,4))
	edges.append((3,2))
	edges.append((4,5))
	edges.append((5,4))
	# mapping:  {5: 0, 4: 1, 1: 2, 2: 2, 3: 2}
	# members:  {0: {5}, 1: {4}, 2: {1, 2, 3}}


	# SYNASC2020_submission_77_v20.pdf Fig. 1. example:
	# a=1, b=2, c=3, d=4
	# edges.append((1,2))
	# edges.append((2,1))
	# edges.append((1,3))
	# edges.append((3,1))
	# edges.append((2,3))
	# edges.append((2,4))
	# edges.append((3,4))
	# mapping:  {4: 0, 1: 1, 2: 1, 3: 1}
	# members:  {0: {4}, 1: {1, 2, 3}}
	######################################
	# Általánosíotott SM:
	######################################
	""" 
	Minden scc-ből legyen strong modell.
	cnf dimacs file
	kiterjesztett erős modell:
	p cnf 4 ?
 	-1 2 0
	-2 1 0
	-1 3 0
	-3 1 0
	-2 3 0
	-1 -2 -3 4 0
	-1 -2 -3 -4 0
	1 2 3 4 0
	"""
	""" erős modell:
	p cnf 4 ?
	-1 2 0
	-2 1 0
	-1 3 0
	-3 1 0
	-2 3 0
	-2 4 0
	-3 4 0
	-1 -2 -3 -4 0
	1 2 3 4 0
	 """

	# A 4. node-ba csak befele mennek élek. Nincs szomszédja.
	# Todo Mennyi szomszédot ad vissza a 3. csúcs?

	# SYNASC2020_submission_77_v20.pdf Fig. 3. example:
	# a=1, b=2, c=3, d=4
	#! Only this example should generate BW SAT problem, since it is strongly connected.
	""" Theorem 1. Let D be a communication graph. Let WM be
	the weak model of D. Then WM is a Black-and-White SAT
	problem iff D is strongly connected.
 	"""
	# edges.append((1,2))
	# edges.append((2,1))
	# edges.append((2,3))
	# edges.append((3,2))
	# edges.append((3,4))
	# edges.append((4,1))
	# mapping:  {1: 0, 2: 0, 3: 0, 4: 0}
	# members:  {0: {1, 2, 3, 4}}

	#from thesis work
	# edges.append((1,2))
	# edges.append((2,1))
	# edges.append((1,3))
	# edges.append((3,4))
	# edges.append((4,5))
	# edges.append((5,3))

	g = nx.DiGraph(edges)
	# algo_check(g)
	# model_to_picture()
	Literals = expanded_strong_model_literal_gen(g)
	model_to_cnf_file(g, Literals, "ESM")
	Literals = strong_model_literal_gen(g)
	model_to_cnf_file(g, Literals, "SM")

	#!golden rule: Always define new nodes with the next lowest real number, for the reason of correct .cnf output!
	#Adding nodes and edges like so ((13,17),(17,14),(14,6),(14,13),(6,1)) is FORBIDDEN!
main()
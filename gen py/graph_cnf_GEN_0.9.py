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
	
#Todo: csinálj teszteket a tesztelő file-al

def strong_model_literal_gen(G):
	clause = []
	bw_clause = []
	for i, j in G.edges():
		clause.append(-i)
		clause.append(j)
		clause.append(0.1)
	for i in G.nodes():
		bw_clause.append(i)
	for i in bw_clause:
		clause.append(-i)
	clause.append(0.1)
	for i in bw_clause:
		clause.append(i)
	clause.append(0.1)
	return clause


#**************************************************************************************************************
# Expanded Weak Model elkepzeles
#**************************************************************************************************************
#Todo Egészítsd ki a leírást példákkal
# The model does not compute with self loops (because in our use it is not possible)
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
	"""
	OK = nx.is_strongly_connected(G)
	if not OK:
		print("Not strongly connected")
		# print("Exited method: expanded_strong_model_literal_gen, bad_args")
		# raise SystemExit

	dagg = nx.condensation(G)
	map = dagg.graph["mapping"]
	mem = nx.get_node_attributes(dagg, "members")
	print("mapping: ",map)
	print("members: ",mem)
	# mapping:  {5: 0, 4: 1, 1: 2, 2: 2, 3: 2}
	# members:  {0: {5}, 1: {4}, 2: {1, 2, 3}}
	# indecies:	[0] [1],[0] [1],[0] [   1   ]

	# Todo: neighbors-t használva. nézze meg a csúcsokból kimutató nyilakat. Azok is literálok neg amiből, poz mindenhova, ahova mutat. 
	# Todo  Ha van két csomópont közt él, akkor mindkettőt neg-el adom hozzá, és egyesével a szomszédait, kivéve a közös élen lévőt (self loop)
	clause = []
	edges = list(dagg.edges())
	if len(edges) == 0:
		# go through nodes add every node as negative literal. Mark it, so later it will be known.
		for i in mem.values():
			while i:
				clause.append(-i.pop())
		clause.append(0.1)
		print("Careful! All are negative literals.")
		return(clause)
	else:
		# goes through every element in the form of:	number: {number}
		for prev, curr in previous(mem.items()):
			if len(curr[1]) > 1:
				# goes through every element in the form of:	{number, number, ...}
				for pre, cu in previous(curr[1]):
					if pre == None:
						firs = cu
						continue
					if (pre, cu) in G.edges():
						clause.append(-pre)
						clause.append(cu)
						clause.append(0.1)
					if (cu, pre) in G.edges():
						clause.append(-cu)
						clause.append(pre)
						clause.append(0.1)
					if (cu, firs) in G.edges() and pre != firs:
						clause.append(-cu)
						clause.append(firs)
						clause.append(0.1)
					if (firs, cu) in G.edges() and pre != firs:
						clause.append(-firs)
						clause.append(cu)
						clause.append(0.1)
			if prev == None:
				continue
			if (prev[0], curr[0]) in edges:
				print("edge goes from previous to current")
				for i in prev[1]:
					clause.append(-i)
				for i in curr[1]:
					clause.append(i)
				clause.append(0.1)

			if (curr[0], prev[0]) in edges:
				print("edge goes from current to previous")
				for i in curr[1]:
					clause.append(-i)
				for i in prev[1]:
					clause.append(i)
				clause.append(0.1)

	print("Before sort:",dagg.nodes)
	print(dagg.edges())
	copy_dagg = nx.topological_sort(dagg)
	print("After sort:",list(copy_dagg))
	
	return(clause)
	# todo nodeokat rendezni, és a fileba sorrendben kiírni.
	# élekkel az eredetihez kötni a dagg elemei szerint. Utána a sorrend a dagg csúcsait rendezi. Ez alapján lehet a fileba a sorrnedet kiírni.

""" 
# Todo nehezebb? simple-el sccket kigyűjteni, azokat klózokba. Majd a maradék elemeket is.
# Todo: Ebbe bele rakni a klóz halmazok gyártását?
def simple_cycles(G):
	print("not in use") """
	
def model_to_picture():
	""" Unfinnished method! """
	print("Nothing")
""" 	N = G.number_of_nodes()
	E = G.number_of_edges()
	D = nx.density(G)

	pylab.title("Weak Model's Starting Graph")
	nx.draw(G, with_labels = True)
	pylab.savefig(str(N)+"_"+str(E)+"_"+str("%.2f" % float(D))+"_WM.png") """

def model_to_cnf_file(G, Literals, Title):
	"""Creates the cnf model of a graph, and puts it in a file.

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

def algo_check(G):
	""" Tried to make the order topologicly sorted. Unfinished method! """
	dagg = nx.condensation(G)
	edges = dagg.edges()
	wm = nx.topological_sort(dagg)
	for ed in edges:
		print("try", ed)

def main():
	edges = []
	# Geeks for Geeks graph example:
	# edges.append((2,1))
	# edges.append((1,3))
	# edges.append((1,4))
	# edges.append((3,2))
	# edges.append((4,5))
	# mapping:  {5: 0, 4: 1, 1: 2, 2: 2, 3: 2}
	# members:  {0: {5}, 1: {4}, 2: {1, 2, 3}}

	# edges.append((5,4))

	# SYNASC2020_submission_77_v20.pdf Fig. 1. example:
	# a=1, b=2, c=3, d=4
	edges.append((1,2))
	edges.append((2,1))
	edges.append((1,3))
	edges.append((3,1))
	edges.append((2,3))
	edges.append((2,4))
	edges.append((3,4))
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

	g = nx.DiGraph(edges)
	# algo_check(g)
	model_to_picture()
	Literals = expanded_strong_model_literal_gen(g)
	model_to_cnf_file(g, Literals, "ESM")
	Literals = strong_model_literal_gen(g)
	model_to_cnf_file(g, Literals, "SM")

main()
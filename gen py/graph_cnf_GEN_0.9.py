from itertools import tee, chain
import networkx as nx

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
'''
# source: https://stackoverflow.com/questions/1011938/loop-that-also-accesses-previous-and-next-values
# original implementation by: https://stackoverflow.com/users/17160/nosklo
# editor: https://stackoverflow.com/users/4495634/zaidrehman
# and here is my modification:
def previous(some_iterable):
    prevs, items = tee(some_iterable, 2)
    prevs = chain([None], prevs)
    return zip(prevs, items)
	
#Todo: csinálj teszteket a tesztelő file-al

#Todo Egészítsd ki a leírást példákkal
# The model does not compute with self loops (because in our use it is not possible)
def weak_model_gen(G):
	"""Returns the weak model of a graph. 

	The weak model of a graph gives a list of literals.
	Each clause is separated with the unique value 0.1.

	Parameters
	----------
	G : Networkx DiGraph
		A directed graph

	Returns
	-------
	Clause : A single iterable list
		Every negative literal represents a cycle, and every positive 
		literal is an exit point of it. A cycle does not include the 
		same value twice.
	"""
	dagg = nx.condensation(G)
	map = dagg.graph["mapping"]
	mem = nx.get_node_attributes(dagg, "members")
	print("mapping: ",map)
	print("members: ",mem)
	# {eredeti : dagg} dictben lévő node
	# mapping:  {5: 0, 4: 1, 1: 2, 2: 2, 3: 2}
	# members:  {0: {5}, 1: {4}, 2: {1, 2, 3}}
	# previndex [0],[1],[0],[1],[0],[   1   ]

	#!  Nem ad vissza minden scc-t. Csak a legnagyobbakat.
	# Todo: neighbours-t használva. nézze meg a csúcsokból kimutató nyilakat. Azok is literálok neg amiből, poz mindenhova, ahova mutat. 
	# Todo  Ha van két csomópont közt él, akkor mindkettőt neg-el adom hozzá, és egyesével a szomszédait, kivéve a közös élen lévőt (self loop)
	# mapping:  {1: 0, 2: 0, 3: 0, 4: 0}
	# members:  {0: {1, 2, 3, 4}}
	clause = []
	edges = list(dagg.edges())
	if len(edges) == 0:
		# go through nodes add every node as negative literal. Mark it, so later it will be known.
		for i in mem.values():
			while i:
				clause.append(-i.pop())
		print("Careful! All are negative literals.")
		print(clause)
	else:
		for prev, curr in previous(mem.items()):
			if prev == None:
				continue
			if (prev[0], curr[0]) in edges:
				print("edge: prev to curr")
				for i in prev[1]:
					clause.append(-i)
				for i in curr[1]:
					clause.append(i)
				clause.append(0.1)

			elif (curr[0], prev[0]) in edges:
				print("edge: curr to prev")
				for i in curr[1]:
					clause.append(-i)
				for i in prev[1]:
					clause.append(i)
				clause.append(0.1)

		print(clause)
		
	
	# todo nodeokat rendezni, és a fileba sorrendben kiírni.
	# élekkel az eredetihez kötni a dagg elemei szerint. Utána a sorrend a dagg csúcsait rendezi. Ez alapján lehet a fileba a sorrnedet kiírni.
	
	print("Before sort:",dagg.nodes)
	print(dagg.edges())
	copy_dagg = nx.topological_sort(dagg)
	print("After sort:",list(copy_dagg))

""" 
# Todo nehezebb? simple-el sccket kigyűjteni, azokat klózokba. Majd a maradék elemeket is.
# Todo: Ebbe bele rakni a klóz halmazok gyártását?
def simple_cycles(G):
	print("not in use") """
	
def weak_model_to_cnf_file(cl):
	print("not implemented yet.")

def main():
	edges = []
	# Geeks for Geeks graph example:
	# edges.append((2,1))
	# edges.append((1,3))
	# edges.append((1,4))
	# edges.append((3,2))
	# edges.append((4,5))

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

	# SYNASC2020_submission_77_v20.pdf Fig. 3. example:
	# a=1, b=2, c=3, d=4
	# edges.append((1,2))
	# edges.append((2,1))
	# edges.append((2,3))
	# edges.append((3,2))
	# edges.append((3,4))
	# edges.append((4,1))

	g = nx.DiGraph(edges)
	
	weak_model_gen(g)
	# cl = []
	# weak_model_to_cnf_file(cl)

main()
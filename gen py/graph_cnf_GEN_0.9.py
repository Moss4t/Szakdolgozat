from collections import defaultdict
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
# https://stackoverflow.com/questions/1011938/loop-that-also-accesses-previous-and-next-values
# original implementation by: https://stackoverflow.com/users/17160/nosklo
# editor: https://stackoverflow.com/users/4495634/zaidrehman
# and here is my modification:
def previous(some_iterable):
    prevs, items = tee(some_iterable, 2)
    prevs = chain([None], prevs)
    return zip(prevs, items)
	
#Todo: csinálj teszteket a tesztelő file-al
def weak_model_gen(G):
	""" 
	The condensation graph C of G. The node labels are integers corresponding to the index of the component in the list of strongly connected components of G.
	C has a graph attribute named 'mapping' with a dictionary mapping the original nodes to the nodes in C to which they belong. 
	Each node in C also has a node attribute 'members' with the set of original nodes in G that form the SCC that the node in C represents 
	
	A kondenzált C gráf G-ből. A csomópontok cimkéi számokkal vannak jelölve, a hozzájuk tartozó komponens indexével, az SCC-k listájából G-ből.
	C-nek van egy gráf tulajdonsága 'mapping' néven, egy szótárral, ami feltérképezi az eredeti csomópontokat és a C-ben megfelelő csomópontokhoz rendeli.
	Minden csomópontnak C-ben van egy tulajdonsága 'members' néven, ami az eredeti csomópontok halmazával G-ben, az eredeti SCC-hez tartozó csomópontokat 
	a C-ben lévő csomópont reprezentállja."""
	# negative_literals = []
	# positive_literals = []
	# Todo nehezebb? simple-el sccket kigyűjteni, azokat klózokba. Majd a maradék elemeket is.
	""" all_scc = simple_cycles(G)
	print("all scc")
	for cycle in all_scc:
		for element in cycle:
			print(element) 
			negative = -element
			posotive = element"""
	# Todo egyszerű verzió: condens-el map, és members segítségével klózokat gyártani.
	# after sort itarate through list. Each node check in the dagg : original, if original len() > 1, then add every member as negative literal, and then
	# the exitpoint. Which should be the edge in the sorted list.
	dagg = nx.condensation(G)
	map = dagg.graph["mapping"]
	mem = nx.get_node_attributes(dagg, "members")
	print("mapping: ",map)
	print("members: ",mem)
	# {eredeti : dagg} dictben lévő node
	# mapping:  {5: 0, 4: 1, 1: 2, 2: 2, 3: 2} 
	# members:  {0: {5}, 1: {4}, 2: {1, 2, 3}}
	# previndex [0],[1],[0],[1],[0],[   1   ]

	clause = []
	edges = list(dagg.edges())
	# todo Összehasonlítani az élek szerint.
	for prev, curr in previous(mem.items()):
		if prev == None:
			continue
		if (prev[0], curr[0]) in edges:
			print("edge: prev to curr")
			for i in prev[1]:
				clause.append(-i)
			for i in curr[1]:
				clause.append(i)

		elif (curr[0], prev[0]) in edges:
			print("edge: curr to prev")
			for i in curr[1]:
				clause.append(-i)
			for i in prev[1]:
				clause.append(i)
	
	print(clause)
	# todo rendezés előtt megcsinálni a klózokat. Utána rendezni, és a fileba sorrendben kiírni. 
	# élekkel az eredetihez kötni a dagg elemei szerint. Utána a sorrend a dagg csúcsait rendezi. Ez alapján lehet a fileba a sorrnedet kiírni.
	
	print("Before sort:",dagg.nodes)
	print(dagg.edges())
	dagg = nx.topological_sort(dagg)
	print("After sort:",list(dagg))
	
def _unblock(thisnode, blocked, B):
	stack = {thisnode}
	while stack:
		node = stack.pop()
		if node in blocked:
			blocked.remove(node)
			stack.update(B[node])
			B[node].clear()

# Todo: Ebbe bele rakni a klóz halmazok gyártását?
def simple_cycles(G):
	# Johnson's algorithm requires some ordering of the nodes.
	# We assign the arbitrary ordering given by the strongly connected comps
	# There is no need to track the ordering as each node removed as processed.
	# Also we save the actual graph so we can mutate it. We only take the
	# edges because we do not want to copy edge and node attributes here.	

	# Johnson algoritmusának szüksége van a csomópontok rendezésére. Az erősen összetett komponensek által megadott tetszőleges sorrendet rendelünk a csúcsokhoz.
	# Nem szükséges a rendezés számontartása, mivel minden csomópont feldolgozás után törölve lesz. Valamint az eredeti gráfot elmentjük, hogy változtathassuk. 
	# Csak az éleket vesszük ki, mert nincs szükség a tulajdonságaira.

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

def main():
	edges = []
	edges.append((2,1))
	edges.append((1,3))
	edges.append((1,4))
	edges.append((3,2))
	edges.append((4,5))
	# edges.append((5,4))

	g = nx.DiGraph(edges)
	
	weak_model_gen(g)

main()
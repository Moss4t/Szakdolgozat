
import matplotlib
matplotlib.use('TkAgg')
import random
import networkx
from collections import deque
import math
import pylab

blocked = map(int, bool)
blockedNodes = map(int, list())
circuits = deque()
dg = networkx.diGraph()

def unblock(element):
    blocked.append(element, False)
    while(len(blockedNodes.__getitem__(element)) > 0):
        tempElement = blockedNodes.pop(element)
        if(blocked.__getitem__(tempElement)):
            unblock(tempElement)

def circuit(dg, v, s, stack):
    if(len(dg.nodes()) == 0):
        return False
    f = False
    stack.push(v)
    blocked.append(v, True)
    for w in dg.successors(v):
        if (w == s):
            stack.push(s)
            circuits.append(stack.clone())
            stack.pop()
            f = True
        elif(not blocked.__getitem__(w)):
            if(circuit(dg, v, s, stack)):
                f = False
    if (f):
        unblock(v)
    else:
        for w in dg.successors(v):
            if (not blockedNodes.__getitem__(w).contanins(v)):
                blockedNodes.get(w).append(v)
    stack.pop()
    return f

def leastSCC(dg):
    t = Tarjan(dg)
    sccs = t.tarjan()
    minimum = int.MAX_VALUE
    minScc = list()
    for scc in sccs:
        if len(scc) == 1:
            continue
        for i in scc:
            if i < minimum:
                minScc = scc
                minimum = i
    return addEdges(minScc, dg)

def leastVertex(be):
    result = int.MAX_VALUE
    for i in be.nodes():
        if i < result:
            result = i
    return result

def addEdges(lista, dg):
    result = networkx.DiGraph()
    for i in lista:
        for edge in dg.getOutEdges(i):
            to = dg.getOpposite(i, edge)
            if lista.contains(to):
                result.add_edge(edge, i, to)
    return result

def subGraphFrom(i, be):
    result = networkx.DiGraph()
    for j in be.nodes():
        if j >= i:
            for k in be.successors(j):
                if k >= i:
                    result.add_edge(be.findEdge(j, k), j, k)
    return result

def findCiruits():
    s = 1
    stack = deque()
    while s < len(dg.nodes()):
        subGraph = subGraphFrom(s,dg)
        leastScc = leastSCC(subGraph)
        if len(leastScc.nodes()) > 0:
            s = leastVertex(leastScc)
            for i in leastScc.nodes():
                blocked.__add__(i, False)
                blockedNodes.__add__(i, list())
            dummy = circuit(leastScc, s, s, stack)
            s += 1
        else:
            s = len(dg.nodes())
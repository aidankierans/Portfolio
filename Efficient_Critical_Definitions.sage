#PROPERTIES

#this list updated when new property added:
#properties = [is_2_bootstrap_good, has_blocks_property, Graph.is_clique, Graph.is_tree, Graph.is_chordal, diameter_no_more_than_two, is_dirac, Graph.is_cograph, girth_less_than_five, Graph.is_split]

def has_blocks_property(g):

    if g.is_connected() and len(g.blocks_and_cut_vertices()[0]) <= 2:
        return True
    else:
        return False

#is_chordal
#is_tree

#is cograph (means no induced p4)
#see: https://en.wikipedia.org/wiki/Cograph

#is_split, see: https://en.wikipedia.org/wiki/Split_graph


#is diameter no more than 2
def diameter_no_more_than_two(g):
    if g.diameter() <= 2:
        return True
    else:
        return False

def is_dirac(g):
    if min_degree(g) >= 0.5*g.order():
        return True
    else:
        return False

def girth_less_than_five(g):
    if g.girth() < 5:
        return True
    else:
        return False

#Def. If a vertex has 2 infected neighbors then it is/becomes infected.
#A graph is 2-bootstrap-good (2BG or simply "good") IF there is a
#choice of 2 initially infected vertices so that every vertex becomes infected.

def is_2_bootstrap_good(G):
    G.relabel()
    return ktBootstrappable(G,2,2)

#Def. A graph is 2B critical if it is 2BG and it would not be 2BG if any of its edges were removed.
def is_2_bootstrap_critical(G):
    if ktBootstrappable(G,2,2):
        for e in G.edges(labels=False):
            G.delete_edge(e)
            if is_2_bootstrap_good(G):
                print "This edge is unnecessary: " + e
                return false
            G.add_edge(e)
    return true

#AUXILLIARY FUNCTIONS

# k is the number of adjacent infected cells it takes to become infected, t is the number of initially infected cells
def ktBootstrappable(G,k,t):
    n=G.order()
    V=G.vertices()
    if n <= t: # If all vertices can be infected initially...
        return true # ... the graph must be good.

    iVerts=sortaIsolatedVertices(G,k,t,V)
    if iVerts.cardinality >= t: # If there are more cells that must be initially infected than there are initially infected cells...
        return false # ... no subset of vertices can infect every cell.
    S=Subsets(G.vertices().difference(iVerts), t-iVerts.cardinality) # S is the set of subsets of G's vertices that we can infect initially, not including any "isolated" cells
    for s in S:
        s=s.union(iVerts) # s includes all "isolated" cells, which we know must be included because they can't be reached otherwise (by definition)
        if percolate(k,G,s,n,V):
            return true
    return false

# This does not use the actual definition for "isolated" in graph theory
def sortaIsolatedVertices(G,k,t,V):
    iVerts=graphs.EmptyGraph # we want to keep track of (and return) which vertices have few enough neighbors that they can't be infected by them
    count=0 # count of "isolated" vertices, which is what we might call them
    for v in V:
        if v.degree() < k:
            iVerts += v;
            count += 1
        if count > t: # If there are "isolated" vertices that aren't infected initially...
            break # ... it's impossible to bootstrap this graph, so give up.
    return iVerts

def percolate(k,G,initial,n,V):
    G.relabel()
    neighbs=[0]*n
    uninfected=[]
    for v in V:
        if v in initial:
            for s in G.neighbors(v):
                neighbs[s]=neighbs[s]+1
        else:
            uninfected.append(v)
    while not len(uninfected)==0:
        flaggity=0
        for v in uninfected:
            if neighbs[v]>k-1:
                flaggity=1
                uninfected.remove(v)
                for s in G.neighbors(v):
                    neighbs[s]=neighbs[s]+1
        if len(uninfected)==0:
            return true
        if not flaggity:
            return false
    return true

def min_degree(g):
    return min(g.degree())

#GRAPHS

#objects list updated as graphs are added:
#build = [Graph(x) for x in G6] #G6 is a list of strings for 2BG graphs
#objects = [pete, k3, pentagon_star, diamond, paw, glasses, pent_chords, grid4, paw4, clebsch, p4, apex] + build

#CE to is_3_connected and has_kite => 2BG
ugly_kite = Graph("L?GO@cMoeCuGRG")

#CE to locally_connected or genghua_fan => 2BG
c4s_k4_center = Graph('G~OXCC')

#CE to has_kite & is_dart_free => 2BG
kissing_kites = Graph('O_C?_oH`A@C?OIH@?aHCG')

#CE to has_dart and is_kite_free => 2BD
kissing_darts = Graph('OOSo@?G?dAHU?D?EC_@G?')

#CE to "If ((is_apex)&(diameter_no_more_than_two)) then is_2_bootstap_good".
apex = Graph("GhdHKc")

#a graph with diameter 2 that is not a cograph (and not 2BG)
big_house = Graph("ECxo")

#p4 is a path on 4 vertices
#p4 is bad but has more than 2 blocks
p4 = graphs.PathGraph(4)

#clebsch graph, see: https://en.wikipedia.org/wiki/Clebsch_graph
#clebsch has girth = 4, diameter = 2, not-2BG
clebsch = graphs.ClebschGraph()

#an n-paw is an n-cycle with a single pendant
paw4 = Graph('Dl_')

#the strong product of p4 with itself (is 2BG and has diameter 3)
grid4 = Graph('OcG@JN?@q@L@YrcSGDEbe')

#the omnipresent Petersen graph
pete = graphs.PetersenGraph()

#a triangle attached to a pendant
paw = Graph("CV")

#5-cycle surrounded by 5 triangles,
#CE to: if every vertex in a triangle then graph is 2BG
pentagon_star = Graph('IhfB@_Wa?')

#complete graph on 3 vertices
k3 = graphs.CompleteGraph(3)

#4-cycle with chord
diamond = Graph('C|')

#2 c4s joined at a vertex
glasses = Graph('Fla?W')

#2BG g6 strings - need to build these still
G6 = ['DrK', 'Cl', 'Dl{', 'Dls']

#a pentagon with 2 chords (has an induced p4 and is 2BG)
pent_chords = Graph("Ks_?BLUR`wFO")

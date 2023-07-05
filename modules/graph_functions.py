import numpy as np
import networkx as nx

class Node:
    def __init__(self,node_type=0, neighbours = [],name=''):
        '''
        type: int; 0 = qubit, 1 = traced, 2 = open wire
        neighbours: list[*Node]
        '''
        self.name = str(name)
        self.node_type = node_type
        if len(neighbours)==0:
            self.neighbours = [] 
        else:
            self.neighbours = neighbours
    def __str__(self):
        s = f"{self.name}({self.node_type}), neighbours:"
        for i in self.neighbours:
            s+= i.name + ", "
        return s
    
    def connect(self, *another_nodes):
        for n in another_nodes:
            if n != self and n not in self.neighbours:
                self.neighbours.append(n)
                n.neighbours.append(self)
    def disconnect(self, *another_nodes):
        for n in another_nodes:
            if n != self and n in self.neighbours:
                self.neighbours.remove(n)
                n.neighbours.remove(self)

    def change_type(self, new_type):
        self.node_type = new_type


class Graph:
    def __init__(self, nodes=[], rules=[],name=""):
        self.name = name
        if len(nodes)!=0:
            self.nodes = nodes
        else:
            self.nodes = []
        if len(rules)!=0:
            self.rules = rules
        else:
            self.rules = []
        self.wires = []
        starred = []
        for i in range(len(self.nodes)):
            if self.nodes[i].node_type==1:
                starred.append(self.nodes[i])
        self.starred = starred
        self.changed  = True
        self.can_simplify = False
        
    def add_wires(self, *wires):
        for w in wires:
            self.wires.append(w)

    def __str__(self):
        return f"{self.name}: nodes({len(self.nodes)}, starred({len(self.starred)}); was changed? {self.changed}; Simplified? {len(self.nodes)==len(self.starred)}"
    
    def simplify_step(self):
        any_change = False
        for n in self.starred:
            for r in self.rules:
                if r(n,self):
                    any_change = True
        if any_change:
            self.changed = True
        else:
            self.changed = False
        return self.changed
    def simplify(self):
        while self.changed:
            self.simplify_step()
            # print(self)
        if len(self.starred) == len(self.nodes):
            self.can_simplify = True
            # print("Simplified!")
    
        else:
            self.can_simplify = False
            # print("Cannot be simplified!")
        return self.can_simplify
        
    def set_rules(self, *rules):
        for r in rules:
            self.rules.append(r)
    def print_nodes(self,):
        for i in self.nodes:
            print(i)
    def plot_graph(self,):
        G = nx.Graph()
        for i in range(len(self.nodes)):
            G.add_node(self.nodes[i].name)

        for i in range(len(self.nodes)):
            for j in range(i+1,len(self.nodes)):
                if self.nodes[i] in self.nodes[j].neighbours:
                    G.add_edge(self.nodes[i].name,self.nodes[j].name)


        color_map = []
        for node in self.nodes:
            if node.node_type == 0:
                color_map.append('pink')
            elif node.node_type == 1: 
                color_map.append('blue') 
                
        if len(self.wires) != 0:
            for w in self.wires:
                G.add_node(w.name)
                G.add_edge(w.name, w.neighbours[0].name)
                color_map.append('gray')


        nx.draw(G, node_color=color_map,with_labels=True, font_weight='bold')

# TODO rename to generate_graph
def generate_random_graph( N, adj_mat):
    nodes = []
    for i in range(N):
        nodes.append(Node(1,name=i))
    for i in range(N):
        for j in range(i+1,N):
            # print( adj_mat[i][j],end=' ')
            if adj_mat[i][j]==1:
                nodes[i].connect(nodes[j])
        # print()
    G = Graph(nodes)
    return G
    
# TODO rename genereate_given_state
def generate_state_for_qubits(G,qubits):
    counter = 0
    for i in qubits:
        if G.nodes[i].node_type != 0:
            G.nodes[i].change_type(0)
            wire = Node(2,name='wire{}'.format(counter))
            G.nodes[i].connect(wire)
            G.starred.remove(G.nodes[i])
            G.add_wires(wire)   
            counter+=1
    

def generate_random_state(G,r):
    qubits = np.random.choice(len(G.nodes),r,replace=False)
    
    counter = 0
    for i in qubits:
        if G.nodes[i].node_type != 0:
            G.nodes[i].change_type(0)
            wire = Node(2,name='wire{}'.format(counter))
            G.nodes[i].connect(wire)
            G.starred.remove(G.nodes[i])
            G.add_wires(wire)  
            counter+=1
    return qubits

def spread(node, G):
    if node.node_type == 1 and len(node.neighbours)==1 and node.neighbours[0].node_type == 0:
        node.neighbours[0].change_type(1)
        G.starred.append(node.neighbours[0])
        
        node.neighbours[0].disconnect(node)
        G.starred.remove(node)
        G.nodes.remove(node)
        return True
    else:
        return False
        
def disconnect(node, G):
    buf = False
    if node.node_type == 1:
        for n in node.neighbours:
            if n.node_type == 1:
                node.disconnect(n)
                buf = True
    return buf

def adjacency_matrix_binomial(N,prob=0.5):
    return np.random.binomial(1,prob, size=(N,N))

def adjacency_matrix_regular(N,d=3):
    G = nx.random_regular_graph(d,N)
    return nx.to_numpy_array(G)
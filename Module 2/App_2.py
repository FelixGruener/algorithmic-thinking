"""
Algorithmic Thinking - Module 2
09-21-2014

Beadth-First Seach and Connected Components
Analysis of a Computer Network
Application File
"""

# general imports
import urllib2
import random
import time
import math

# Desktop imports
import matplotlib.pyplot as plt
import Project_2 as prj2
import Project_1 as prj1
import DPA


############################################
# Provided code

def copy_graph(graph):
    """
    Make a copy of a graph
    """
    new_graph = {}
    for node in graph:
        new_graph[node] = set(graph[node])
    return new_graph

def delete_node(ugraph, node):
    """
    Delete a node from an undirected graph
    """
    neighbors = ugraph[node]
    ugraph.pop(node)
    for neighbor in neighbors:
        ugraph[neighbor].remove(node)
    
def targeted_order(ugraph):
    """
    Compute a targeted attack order consisting
    of nodes of maximal degree
    
    Returns:
    A list of nodes
    """
    # copy the graph
    new_graph = copy_graph(ugraph)
    
    order = []    
    while len(new_graph) > 0:
        max_degree = -1
        for node in new_graph:
            if len(new_graph[node]) > max_degree:
                max_degree = len(new_graph[node])
                max_degree_node = node
        
        neighbors = new_graph[max_degree_node]
        new_graph.pop(max_degree_node)
        for neighbor in neighbors:
            new_graph[neighbor].remove(max_degree_node)

        order.append(max_degree_node)
    return order
    


##########################################################
# Code for loading computer network graph

NETWORK_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt"


def load_graph(graph_url):
    """
    Function that loads a graph given the URL
    for a text representation of the graph
    
    Returns a dictionary that models a graph
    """
    graph_file = urllib2.urlopen(graph_url)
    graph_text = graph_file.read()
    graph_lines = graph_text.split('\n')
    graph_lines = graph_lines[ : -1]
    
    print "Loaded graph with", len(graph_lines), "nodes"
    
    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        for neighbor in neighbors[1 : -1]:
            answer_graph[node].add(int(neighbor))

    return answer_graph
    
##########################################################
# Code for loading UPA graph

class UPATrial:
    """
    Simple class to encapsulate optimizated trials for the UPA algorithm
    
    Maintains a list of node numbers with multiple instance of each number.
    The number of instances of each node number are
    in the same proportion as the desired probabilities
    
    Uses random.choice() to select a node number from this list for each trial.
    """

    def __init__(self, num_nodes):
        """
        Initialize a UPATrial object corresponding to a 
        complete graph with num_nodes nodes
        
        Note the initial list of node numbers has num_nodes copies of
        each node number
        """
        self._num_nodes = num_nodes
        self._node_numbers = [node for node in range(num_nodes) for dummy_idx in range(num_nodes)]


    def run_trial(self, num_nodes):
        """
        Conduct num_nodes trials using by applying random.choice()
        to the list of node numbers
        
        Updates the list of node numbers so that each node number
        appears in correct ratio
        
        Returns:
        Set of nodes
        """
        
        # compute the neighbors for the newly-created node
        new_node_neighbors = set()
        for _ in range(num_nodes):
            new_node_neighbors.add(random.choice(self._node_numbers))
        
        # update the list of node numbers so that each node number 
        # appears in the correct ratio
        self._node_numbers.append(self._num_nodes)
        for dummy_idx in range(len(new_node_neighbors)):
            self._node_numbers.append(self._num_nodes)
        self._node_numbers.extend(list(new_node_neighbors))
        
        #update the number of nodes
        self._num_nodes += 1
        return new_node_neighbors
    
############################################################
# Code for application

def make_ER_graph(num_nodes, p):
    """
    Takes number of nodes and returns dictionary with an ER graph
    
    num_nodes (int) - number of nodes to build into graph
    return: graph (dict)
    """
    graph = {}
    for node in xrange(num_nodes):
        graph[node] = set([])
        for to_node in xrange(num_nodes):
            chance = random.random()
            if node != to_node and chance < p:
                if to_node in graph:
                    graph[node].add(to_node)
                    graph[to_node].add(node)
                else:
                    graph[to_node] = set()
                    graph[node].add(to_node)
                    graph[to_node].add(node)
    return graph 
    
def UPA_graph(num_nodes, exist_nodes):
    """
    
    
    num_nodes (int) - number of nodes to add
    exist_nodes (int) - number of existing nodes to connect to
    return: digraph (dict)
    """
    ugraph = prj1.make_complete_graph(exist_nodes)
    for new_node in xrange(exist_nodes, num_nodes):
        total_in = prj1.compute_in_degrees(ugraph)
        total_indegrees = 0
        for node in total_in:
            total_indegrees += total_in[node]
        trial = UPATrial(total_indegrees)
        to_connect = trial.run_trial(exist_nodes)
        ugraph[new_node] = to_connect
    return ugraph 

def random_order(num_nodes, graph):
    """
    Creates an attacking order
    """
    choices = graph.keys()
    order = set(random.sample(choices, num_nodes))
    return order

def question_one():
    graph_network = load_graph(NETWORK_URL)
    graph_ER = make_ER_graph(1347, .0025)
    #graph_UPA
    graphs = [graph_network, graph_ER]
    
    y_vals = []
    x_vals = []
    for each in graphs:
        order = random_order(len(each) - 1, each)
        print order
        res = prj2.compute_resilience(each, order)
        y_vals.append(res)
        x_vals.append([x for x in xrange(len(order))])

    plt.plot(x_vals[0], y_vals[0])
    plt.xlabel("Number of Nodes Removed")
    plt.ylabel("Largest Connected Component")
    plt.title("Largest Connected Components as Nodes Removed")
    plt.show()


def edge_tester(ugraph):
    total_ins = prj1.compute_in_degrees(ugraph)
    sum = 0
    for node in total_ins:
        sum += total_ins[node]
    print sum/2

#graph_network = load_graph(NETWORK_URL) #1347 nodes, 3112 edges
#graph_ER = make_ER_graph(1347, .0025) #1347 nodes, .25% change of edge between node
#graph_UPA = DPA.UPA_graph(100, 19)

question_one()
























    

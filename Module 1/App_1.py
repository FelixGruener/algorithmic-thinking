"""
Algorithmic Thinking - Module 1
Mark Hess
09-07-2014

Degree Distributions for graphs
Application file
"""

# general imports
import urllib2
import random
import Project_1 as P1
import DPA
import matplotlib.pyplot as plt

###################################
# Code for loading citation graph

CITATION_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_phys-cite.txt"

QUESTION_ONE = False
QUESTION_TWO = False
FINAL = False

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

######## Question 1 ##########

def normalize_distribution(digraph):
    """
    Normalizes the digraph
    
    return: dictionary with degrees normalized
    """
    distribution = P1.in_degree_distribution(digraph)
    sum_nodes = len(digraph)
    normalized = dict.fromkeys(distribution)
    for degree in distribution:
        normalized[degree] = distribution[degree] / float(sum_nodes)
    return normalized
    
def plot_normalized(normal_distrib):
    x_vals = []
    y_vals = []
    for degree in normal_distrib:
        x_vals.append(degree)
        y_vals.append(normal_distrib[degree])
    plt.loglog(x_vals, y_vals, color="black", linestyle='None', marker=".", markersize=6)
    plt.xlabel("Log of Number of Degrees")
    plt.ylabel("Log of Distribution")
    plt.title("Log/log Normalized Distribution of High Energy Physics Theory Papers")
    plt.show()
    
if QUESTION_ONE:
    print "Loading citation graph..."
    citation_graph = load_graph(CITATION_URL)
    out_degrees = 0
    print "Calculating average out degrees for citation graph..."
    for node in citation_graph:
        out_degrees += len(citation_graph[node])
    print out_degrees / len(citation_graph)
    print "Calculating normalized distribution of in degrees..."  
    n = normalize_distribution(citation_graph)
    print "Plotting normalized distibution..."
    plot_normalized(n)
    
####### Question 2 #########
    
def digraph_rand(num_nodes, prob):
    """
    Function for creating a random directional graph with a specified number of nodes per
    a given probability.
    
    num_nodes (int) - number of nodes
    prob (int) - probability
    return: digraph (dict)
    """
    digraph = {}
    for node_i in xrange(num_nodes):
        edges = []
        for node_j in xrange(num_nodes):
            a = random.random()
            if a < prob and node_i != node_j:
                edges.append(node_j)
        digraph[node_i] = edges
    return digraph

def plot_question_2():
    x_d0, y_d0 = [], []
    d0 = digraph_rand(10000, .5)
    norm_0 = normalize_distribution(d0)
    for degree in norm_0:
        x_d0.append(degree)
        y_d0.append(norm_0[degree])        
    
    x_d1, y_d1 = [], []
    d1 = digraph_rand(10000, .8)
    norm_1 = normalize_distribution(d1)
    for degree in norm_1:
        x_d1.append(degree)
        y_d1.append(norm_1[degree])
        
    x_d2, y_d2 = [], []
    d2 = digraph_rand(10000, .3)
    norm_2 = normalize_distribution(d2)
    for degree in norm_2:
        x_d2.append(degree)
        y_d2.append(norm_2[degree])

    plt.loglog(x_d0, y_d0, color="black", linestyle='None', marker=".", markersize=6)
    plt.loglog(x_d1, y_d1, color="blue", linestyle='None', marker=".", markersize=6)
    plt.loglog(x_d2, y_d2, color="red", linestyle='None', marker=".", markersize=6)
    plt.xlabel("Log of Number of Degrees")
    plt.ylabel("Log of Distribution")
    plt.title("Log/log Normalized Distribution for Random Generated Digraphs")
    plt.show()

if QUESTION_TWO:
    plot_question_2()
    
    
########### Question 3-5 ###############

N = 200
M = 12

def plot_final():
    DPA_graph = DPA.DPA_algo(N, M)
    print len(DPA_graph) 
#    x_vals = []
#    y_vals = []
#    for degree in normal_distrib:
#        x_vals.append(degree)
#        y_vals.append(normal_distrib[degree])
#    plt.loglog(x_vals, y_vals, color="black", linestyle='None', marker=".", markersize=6)
#    plt.xlabel("Log of Number of Degrees")
#    plt.ylabel("Log of Distribution")
#    plt.title("Log/log Normalized Distribution of High Energy Physics Theory Papers")
#    plt.show()

if FINAL:
    plot_final()
    
    
    
    
    
    
    
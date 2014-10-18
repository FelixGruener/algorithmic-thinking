"""
Algorithmic Thinking - Module 1
Mark Hess
09-07-2014

Degree Distributions for graphs
Provided Helper class for implementing efficient version
of DPA algorithm
"""

# general imports
import random
import Project_1 as prj1


class DPATrial:
    """
    Simple class to encapsulate optimized trials for DPA algorithm
    
    Maintains a list of node numbers with multiple instances of each number.
    The number of instances of each node number are
    in the same proportion as the desired probabilities
    
    Uses random.choice() to select a node number from this list for each trial.
    """

    def __init__(self, num_nodes):
        """
        Initialize a DPATrial object corresponding to a 
        complete graph with num_nodes nodes
        
        Note the initial list of node numbers has num_nodes copies of
        each node number
        """
        self._num_nodes = num_nodes
        self._node_numbers = [node for node in xrange(num_nodes) for dummy_idx in xrange(num_nodes)]


    def run_trial(self, num_nodes):
        """
        Conduct num_node trials using by applying random.choice()
        to the list of node numbers
        
        Updates the list of node numbers so that the number of instances of
        each node number is in the same ratio as the desired probabilities
        
        Returns:
        Set of nodes
        """
        
        # compute the neighbors for the newly-created node
        new_node_neighbors = set()
        for dummy_idx in xrange(num_nodes):
            new_node_neighbors.add(random.choice(self._node_numbers))
        
        # update the list of node numbers so that each node number 
        # appears in the correct ratio
        self._node_numbers.append(self._num_nodes)
        self._node_numbers.extend(list(new_node_neighbors))
        
        #update the number of nodes
        self._num_nodes += 1
        return new_node_neighbors

        
def DPA_algo(num_nodes, exist_nodes):
    """
    
    
    num_nodes (int) - number of nodes to add
    exist_nodes (int) - number of existing nodes to connect to
    return: digraph (dict)
    """
    #initialize variables for direction graph
    digraph = prj1.make_complete_graph(exist_nodes)
    
    #create DPA graph
    for new_node in xrange(exist_nodes, num_nodes):
        total_in = prj1.compute_in_degrees(digraph)
        total_indegrees = 0
        for node in total_in:
            total_indegrees += total_in[node]
        trial = DPATrial(total_indegrees)
        to_connect = trial.run_trial(exist_nodes)
        digraph[new_node] = to_connect
    
    #return direction DPA graph
    return digraph
        
       
        
        
        
        
        
        
        
        
        
        
        
        
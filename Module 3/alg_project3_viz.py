"""
Algorithmic Thinking - Module 3
10-5-2014

Divide and Conquer Method and Clustering
Comparison of Clustering Algorithms
Application File

Note that you must download the file
http://www.codeskulptor.org/#alg_clusters_matplotlib.py
to use the matplotlib version of this code
"""

# Flavor of Python - desktop or CodeSkulptor
DESKTOP = True

import math
import random
import urllib2
import time
import alg_cluster
import matplotlib.pyplot as plt


# conditional imports
if DESKTOP:
    import Project_3 as prj3      # desktop project solution
    import alg_clusters_matplotlib
else:
    #import userXX_XXXXXXXX as prj3   # CodeSkulptor project solution
    import alg_clusters_simplegui
    import codeskulptor
    codeskulptor.set_timeout(30)


###################################################
# Code to load data tables

# URLs for cancer risk data tables of various sizes
# Numbers indicate number of counties in data table

DIRECTORY = "http://commondatastorage.googleapis.com/codeskulptor-assets/"
DATA_3108_URL = DIRECTORY + "data_clustering/unifiedCancerData_3108.csv"
DATA_896_URL = DIRECTORY + "data_clustering/unifiedCancerData_896.csv"
DATA_290_URL = DIRECTORY + "data_clustering/unifiedCancerData_290.csv"
DATA_111_URL = DIRECTORY + "data_clustering/unifiedCancerData_111.csv"


def load_data_table(data_url):
    """
    Import a table of county-based cancer risk data
    from a csv format file
    """
    data_file = urllib2.urlopen(data_url)
    data = data_file.read()
    data_lines = data.split('\n')
    print "Loaded", len(data_lines), "data points"
    data_tokens = [line.split(',') for line in data_lines]
    return [[tokens[0], float(tokens[1]), float(tokens[2]), int(tokens[3]), float(tokens[4])] 
            for tokens in data_tokens]


############################################################
# Code to create sequential clustering
# Create alphabetical clusters for county data

def sequential_clustering(singleton_list, num_clusters):
    """
    Take a data table and create a list of clusters
    by partitioning the table into clusters based on its ordering
    
    Note that method may return num_clusters or num_clusters + 1 final clusters
    """
    
    cluster_list = []
    cluster_idx = 0
    total_clusters = len(singleton_list)
    cluster_size = float(total_clusters)  / num_clusters
    
    for cluster_idx in range(len(singleton_list)):
        new_cluster = singleton_list[cluster_idx]
        if math.floor(cluster_idx / cluster_size) != \
           math.floor((cluster_idx - 1) / cluster_size):
            cluster_list.append(new_cluster)
        else:
            cluster_list[-1] = cluster_list[-1].merge_clusters(new_cluster)
            
    return cluster_list
                

#####################################################################
# Code to load cancer data, compute a clustering and 
# visualize the results


def run_example():
    """
    Load a data table, compute a list of clusters and 
    plot a list of clusters

    Set DESKTOP = True/False to use either matplotlib or simplegui
    """
    algo_used = 1  # 1: sequential clusters, 2: hierarchical clusters, 3: k-means clusters
    
    data_urls = [DATA_3108_URL, DATA_896_URL, DATA_290_URL, DATA_111_URL]
    source = 3 # pick which data source url
    data_table = load_data_table(data_urls[source - 1]) 
    

    
    def clustering(algo_used, num_clusters, num_iter = 5):
        """
        Uses specified algorithm to cluster data
        
        input: int for specified algorithm, data_table
        output: cluster_list
        """     
        singleton_list = []
        for line in data_table:
            singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
        
        if algo_used == 1:
            cluster_list = sequential_clustering(singleton_list, num_clusters)
            print "Displaying", len(cluster_list), "sequential clusters"
        elif algo_used == 2:
            cluster_list = prj3.hierarchical_clustering(singleton_list, num_clusters)
            print "Displaying", len(cluster_list), "hierarchical clusters"
        elif algo_used == 3:
            cluster_list = prj3.kmeans_clustering(singleton_list, num_clusters, num_iter)
            print "Displaying", len(cluster_list), "k-means clusters"
        
        return cluster_list


    def gen_random_clusters(num_clusters):
        """
        Creates a list of clusters where each cluster in this list corresponds to one randomly generated point in the 2 x 2 square
        Input: number of clusters (int)
        Output: list of random clusters that is num_clusters long (list)
        """
        cluster_list = []
        for cluster in xrange(num_clusters):
            x = random.choice([1, -1]) * random.random()
            y = random.choice([1, -1]) * random.random()
            cluster_list.append(alg_cluster.Cluster(set([]), x, y, 1, 0))
        return cluster_list
        
        
    def question_one():
        """
        Function for answering first question
        """
        xvals = range(2, 200)
        slow_yvals = []
        fast_yvals = []
        for num in xvals:
            cluster_list = gen_random_clusters(num)
            initial = time.time()
            answer = prj3.slow_closest_pairs(cluster_list)
            final = time.time()
            slow_yvals.append(final - initial)
        for num in xvals:
            cluster_list = gen_random_clusters(num)
            initial = time.time()
            answer = prj3.fast_closest_pair(cluster_list)
            final = time.time()
            fast_yvals.append(final - initial)
        slow_line = plt.plot(xvals, slow_yvals, color='r', label="Slow Closest Pair")
        fast_line = plt.plot(xvals, fast_yvals, color='b', label="Fast Closest Pair")
        plt.legend(loc=2)
        plt.title("Efficiency of Slow and Fast Closest Pairs Algorithms")
        plt.xlabel("Number of Clusters")
        plt.ylabel("Run Times in Milliseconds")
        plt.show()
    
    
    def compute_distortion(cluster_list):
        """
        Takes a list of clusters and uses cluster_error to compute its distortion.
        
        input: list of clusters, original data table
        output: cluster distortion int
        """
        distortion = 0
        for cluster in cluster_list:
            distortion += cluster.cluster_error(data_table)
        return distortion
    
    def question_ten():
        """
        Function for answering question 10
        """
        xvals = xrange(6, 21)
        kmeans_y = []
        high_y = []
        
        for clusters in xvals:
            kmeans_y.append(compute_distortion(clustering(3, clusters)))
        for clusters in xvals:
            high_y.append(compute_distortion(clustering(2, clusters)))
        
        kmeans_line = plt.plot(xvals, kmeans_y, color='r', label="K-Means Clustering")
        high_line = plt.plot(xvals, high_y, color='b', label="Hierarchical Clustering")
        plt.legend()
        plt.title("Distortion Comparison Between Clustering Methods on 290 County Data Set")
        plt.xlabel("Number of Output Clusters")
        plt.ylabel("Distortion")
        plt.show()

    #question_one()
    #question_ten()

    # draw the clusters using matplotlib or simplegui
    cluster_list = clustering(1, 5)
    if DESKTOP:
        alg_clusters_matplotlib.plot_clusters(data_table, cluster_list, True)
    else:
        alg_clusters_simplegui.PlotClusters(data_table, cluster_list)
        
        
    
run_example()





    





  
        






        






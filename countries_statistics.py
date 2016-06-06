import networkx as nx
import pandas
import operator
import matplotlib.pyplot as plt 
import sys
import csv
from glob import glob


def save_png(plot, path):
    fig = plot.get_figure()
    fig.savefig(path)
    plt.close(fig)


if __name__ == '__main__':
    graph_files = glob('images/*/*.gv')
    print len(graph_files)
    print graph_files
    for graph_file in graph_files:
        print 'Reading %s' % graph_file
        # Note: you need to have a graph instead of multigraph to compute eigenvector centrality and page rank
        G = nx.Graph(nx.read_dot(graph_file))
        #G = nx.read_dot(graph_file)
        #print G.nodes()
        #print G.edges()
        degree = nx.degree_centrality(G)
        #print 'degree:', degree
        #eigen = nx.eigenvector_centrality(G, max_iter=1000)
        #print 'eigen:', eigen
        closeness = nx.closeness_centrality(G)
        #print 'closeness:', closeness
        betweenness = nx.betweenness_centrality(G)
        #print 'betweenness:', betweenness
        #pagerank = nx.pagerank(G, max_iter=100000)
        #print 'pagerank:', pagerank
        with open(graph_file.replace('.gv', '.csv'), 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['Country', 'Degree', 'Closeness', 'Betweenness'])
            for node in G.nodes():
                writer.writerow([node, degree[node], closeness[node], betweenness[node]])

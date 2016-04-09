
import networkx as nx
import pandas
import operator
import matplotlib.pyplot as plt

PATH = 'graphs/top_1000_keywords.graphml'

def save_png(plot, path):
    fig = plot.get_figure()
    fig.savefig(path)
    plt.close(fig)


if __name__ == '__main__':

    G = nx.read_graphml(PATH, unicode)

    degree = nx.degree_centrality(G)
    cDegree = pandas.Series(degree)
    eigen = nx.eigenvector_centrality(G)
    cEigen = pandas.Series(eigen)
    closeness = nx.closeness_centrality(G)
    cCloseness = pandas.Series(closeness)
    betweenness = nx.betweenness_centrality(G)
    cBetweeness = pandas.Series(betweenness)
    pagerank = nx.pagerank(G)
    cPagerank = pandas.Series(pagerank)

    print("Degree c. distribution\n")
    print(cDegree.describe())
    print("Max: %s" % max(degree.iteritems(), key=operator.itemgetter(1))[0])
    print("Min: %s" % min(degree.iteritems(), key=operator.itemgetter(1))[0])
    print("Eigenvector c. distribution\n")
    print(cEigen.describe())
    print("Max: %s" % max(eigen.iteritems(), key=operator.itemgetter(1))[0])
    print("Min: %s" % min(eigen.iteritems(), key=operator.itemgetter(1))[0])
    print("Closeness c. distribution\n")
    print(cCloseness.describe())
    print("Max: %s" % max(closeness.iteritems(), key=operator.itemgetter(1))[0])
    print("Min: %s" % min(closeness.iteritems(), key=operator.itemgetter(1))[0])
    print("Betweenness c. distribution\n")
    print(cBetweeness.describe())
    print("Max: %s" % max(betweenness.iteritems(), key=operator.itemgetter(1))[0])
    print("Min: %s" % min(betweenness.iteritems(), key=operator.itemgetter(1))[0])
    print("PageRank c. distribution\n")
    print(cPagerank.describe())
    print("Max: %s" % max(pagerank.iteritems(), key=operator.itemgetter(1))[0])
    print("Min: %s" % min(pagerank.iteritems(), key=operator.itemgetter(1))[0])

    save_png(cDegree.plot.hist(bins=100), 'images/top_1000_keywords/degree.png')
    save_png(cEigen.plot.hist(bins=100), 'images/top_1000_keywords/eigenvector.png')
    save_png(cCloseness.plot.hist(bins=100), 'images/top_1000_keywords/closeness.png')
    save_png(cBetweeness.plot.hist(bins=100), 'images/top_1000_keywords/betweenness.png')
    save_png(cPagerank.plot.hist(bins=100), 'images/top_1000_keywords/pagerank.png')


    # communities = list(nx.k_clique_communities(G, 6))
    # communities = sorted(communities, key = lambda c: len(c), reverse = True)[:10]
    # print communities

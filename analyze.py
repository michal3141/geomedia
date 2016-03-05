#!/usr/bin/env python

import os

from graphviz import Graph, Digraph
from collections import defaultdict
from parse import get_by_pattern
from operator import itemgetter

styles = { 
    'graph': {
        'label': 'Graph',
        'fontsize': '12',
        'fontcolor': 'white',
        'bgcolor': '#888888',
        'overlap': 'prism',
        'outputorder': 'edgesfirst'
        # 'rankdir': 'BT'
    },  
    'nodes': {
        'fontname': 'Helvetica',
        'shape': 'hexagon',
        'fontcolor': 'white',
        'color': 'white',
        'style': 'filled',
        'fillcolor': '#006699',
    },  
    'edges': {
        'color': 'black',
        'arrowhead': 'open',
        'fontname': 'Courier',
        'fontsize': '12',
        'fontcolor': 'white',
    }   
}

# Visualizing countries that appear together in one item as a graph
def visualize_countries_together_in_item(data):
    countries_together_dict = _get_countries_together_in_items(data)
    # print 'countries_together_dict:', countries_together_dict
    dot = Graph(comment='Countries together in item graph', engine='sfdp')
    seen_countries = set()
    edges_between_countries = defaultdict(int)

    ## Building the graph
    for ID, countries in countries_together_dict.iteritems():
        for country in countries:
            if country != '' and country not in seen_countries:
                dot.node(country, label=country)
                seen_countries.add(country)
        for i in xrange(len(countries)):
            for j in xrange(i+1, len(countries)):
                edges_between_countries[(countries[i], countries[j])] += 1

    for edge_endpoints, edge_weight in edges_between_countries.iteritems():
        dot.edge(edge_endpoints[0], edge_endpoints[1], weight=str(edge_weight))

    print 'seen_countries:', seen_countries
    print 'edges_between_countries:', edges_between_countries

    
    dot = _apply_styles(dot, styles)
    # print dot.source
    dot.render(os.path.join('images', 'countries_together_in_item.gv'), view=True)

def _get_countries_together_in_items(data):
    ID_to_country_list = defaultdict(list)
    for d in data:
        ID_to_country_list[d['ID']].append(d['TAG_country'])
    return ID_to_country_list

def _apply_styles(graph, styles):
    graph.graph_attr.update(
        ('graph' in styles and styles['graph']) or {}
    )
    graph.node_attr.update(
        ('nodes' in styles and styles['nodes']) or {}
    )
    graph.edge_attr.update(
        ('edges' in styles and styles['edges']) or {}
    )
    return graph

def main():
    data = get_by_pattern('*/*/*/rss_unique_TAG_country_Ebola.csv')
    visualize_countries_together_in_item(data)
    # data.sort(key=itemgetter('ID'))
    # for d in data:
    #    print d['ID']

if __name__ == '__main__':
    main()

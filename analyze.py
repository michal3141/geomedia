#!/usr/bin/env python

import os, sys, datetime

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
def visualize_countries_together_in_item(data, start_time_str=None, end_time_str=None, newspaper_str='*'):
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
    out_dirname = newspaper_str.replace('*', '')
    out_filename = ('countries_together_in_item_%s_%s.gv' % (start_time_str, end_time_str)).replace(':', '-')
    dot.render(os.path.join('images', out_dirname, out_filename), view=False)

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
    DATETIME_FMT = '%Y-%m-%d %H:%M:%S' 
    # Restricting analyzed data to particular timespan (timerange: <start_time -> end_time>)
    start_time, end_time, start_time_str, end_time_str = None, None, None, None
    if len(sys.argv) >= 3:
        # Example usage: ./analyze.py '2014-01-01 00:00:00' '2015-02-01 00:00:00' 'en_AUS_austra_int'

        start_time_str = sys.argv[1]
        end_time_str = sys.argv[2]
        try: 
            newspaper_str = sys.argv[3]
            print 'Using newspaper: %s' % newspaper_str
        except:
            newspaper_str = '*'
            print 'No provided newspaper - using all newspapers'

        start_time = datetime.datetime.strptime(start_time_str, DATETIME_FMT)
        end_time = datetime.datetime.strptime(end_time_str, DATETIME_FMT)
        print 'Using start_time:', start_time
        print 'Using end_time:', end_time
         
    data = get_by_pattern('*/*/%s/rss_unique_TAG_country_Ebola.csv' % newspaper_str)

    data_filtered_by_time = []
    print 'Starting filtering by time...'
    for item in data:
        if start_time:
            if datetime.datetime.strptime(item['time'], DATETIME_FMT) < start_time:
                continue
        if end_time:
            if datetime.datetime.strptime(item['time'], DATETIME_FMT) >= end_time:
                continue
        data_filtered_by_time.append(item)
    print 'Filtering by time has finished.'

    visualize_countries_together_in_item(data_filtered_by_time, start_time_str=start_time_str, end_time_str=end_time_str, newspaper_str=newspaper_str)
    # data.sort(key=itemgetter('ID'))
    # for d in data:
    #    print d['ID']

if __name__ == '__main__':
    main()

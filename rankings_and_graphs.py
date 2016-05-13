#!/usr/bin/env python

import csv
import sys
import glob
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from collections import defaultdict

MONTHS = ['2014-01', '2014-02', '2014-03', '2014-04', '2014-05', '2014-06', '2014-07', '2014-08', '2014-09',
          '2014-10', '2014-11', '2014-12', '2015-01', '2015-02', '2015-03', '2015-04', '2015-05', '2015-06']


def parse_spreadsheets(spreadsheet_files, metric_name):
    metrics = []
    for i in xrange(len(spreadsheet_files)):
        metrics.append([])
        with open(spreadsheet_files[i], 'r') as csvfile:
            csvreader = csv.DictReader(csvfile, delimiter=',')
            if i == 0:
                print 'fieldnames:', csvreader.fieldnames
            for row in csvreader:
                metrics[i].append((row['Label'], float(row[metric_name])))
            metrics[i] = sorted(metrics[i], key=lambda x: -x[1])
            print metrics[i]
    return metrics


def dump_metrics_to_file(metrics, metric_name, top_count):
    for i in xrange(len(MONTHS)):
        with open('metrics/%s_top%d_%s' % (metric_name, top_count, MONTHS[i]), 'w') as f:
            for j in xrange(top_count):
                lab, val = metrics[i][j]
                f.write(lab + ' ' + str(val) + '\n')

def plot(metrics, metric_name, top_count):
    d = defaultdict(list)
    top_count_labs = set()

    for i in xrange(len(MONTHS)):
        for j in xrange(len(metrics[i])):
            lab, val = metrics[i][j]
            print lab, '-->', val
            if j < top_count:
                if lab not in top_count_labs:
                    print 'Adding label: %s' % lab
                    top_count_labs.add(lab)
            d[lab].append(val)

    colors = iter(cm.rainbow(np.linspace(0, 1, len(top_count_labs))))
    for lab in top_count_labs:
        print lab, len(MONTHS), len(d[lab])
        if len(MONTHS) == len(d[lab]):
            plt.scatter(range(len(MONTHS)), d[lab], color=next(colors), label=lab)
    plt.legend(loc='upper left')
    plt.savefig('metrics/%s_top%d.png' % (metric_name, top_count))
    plt.show()


def main():
    spreadsheet_files = sorted(glob.glob('spreadsheets/countries_together_by_months*'))

    metric_name = sys.argv[1]
    top_count = int(sys.argv[2])

    metrics = parse_spreadsheets(spreadsheet_files, metric_name)

    dump_metrics_to_file(metrics, metric_name, top_count)

    plot(metrics, metric_name, top_count)

    # print spreadsheet_files
    # print len(spreadsheet_files)

if __name__ == '__main__':
    main()

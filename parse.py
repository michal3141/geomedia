#!/usr/bin/env python

import csv
import glob
import sys

def get_by_pattern(pattern):
    return _parse(_get_filenames_by_pattern(pattern))

def _get_filenames_by_pattern(pattern):
    return glob.glob(pattern)

def _parse(filenames):
    all_items = []
    for filename in filenames:
        with open(filename, 'r') as csvfile:
            csvreader = csv.DictReader(csvfile, delimiter='\t')
            print 'Reading: %s ...' % filename
            # print csvreader.fieldnames
            for row in csvreader:
                all_items.append(row)
                # print row['ID'] #    "feed"  "time"  "text1" "text2" "TAG_country"   "TAG_ebola"
                # print ', '. join(row)
    return all_items

def main():
    #filenames = _get_filenames_by_pattern('Geomedia_extract_AGENDA/Geomedia_extract_AGENDA/*/rss_unique_TAG_country_Ebola.csv')
    #filenames = _get_filenames_by_pattern('*/*/*/rss_unique_TAG_country_Ebola.csv')
    #data = _parse(filenames)
    data = get_by_pattern('*/*/*/rss_unique_TAG_country_Ebola.csv')

    print len(data)

if __name__ == '__main__':
    main()

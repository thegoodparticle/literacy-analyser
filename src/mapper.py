#!/usr/bin/env python3

import sys

# iterate through all the inputs from the streaming file
for line in sys.stdin:
    # strip unnecessary whitespaces
    line = line.strip()
    columns = line.split(',')
    
    # we are interested in Census Year 2001 and 2011 only
    if len(columns) == 29 and (columns[0] in ('2001', '2011')):
        # print the output as key-value pair separated by a tab
        # Key: District,Census Year
        # Value: Total Literates, Total Population
        print('%s,%s\t%s,%s' % (columns[1], columns[0], columns[17], columns[5]))

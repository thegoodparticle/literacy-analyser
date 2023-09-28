#!/usr/bin/env python3

import sys

current_key = None
literate_population = 0
total_population = 0
literacy_rate = None

for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()

    # split the key and value using tab separator
    # key: District,Census Year
    # value: literates,population
    key, value = line.split('\t', 1)

    # convert the values (literates, population) to int values
    try:
        literates, population = value.split(',', 1)
        literates = int(literates)
        population = int(population)
    except ValueError:
        # ignore/discard this line in case of type conversion errors
        continue

    # find the cummulative sum of literates and total population for the key
    if current_key == key:
        literate_population += literates
        total_population += population
    else:
        # if new key, write the existing reduced result to STDOUT
        if current_key:
            # check added to avoid divide by zero exception
            try:
                literacy_rate = f"{literate_population/total_population:.2%}"
            except ZeroDivisionError:
                literacy_rate = None
            
            print('%s\t%s' % (current_key, literacy_rate))
        
        # initialize global values for first key or new keys
        literate_population = literates
        total_population = population
        current_key = key

# output the last reduced value
if current_key == key:
    literacy_rate = f"{literate_population/total_population:.2%}"
    print('%s\t%s' % (current_key, literacy_rate))
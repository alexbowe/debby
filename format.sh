#!/bin/bash

# This script is just for splitting the edge into node and edge label, and reversing the node label ready to be sorted
# in colex order by unix sort

# Ruby is nice for this one liner since it provides a $_ variable for stdin
# Python one liners don't accept stdin like this
ruby -lane 'print $_[0..-2].reverse, " ", $_[-1]'

# To get de bruijn graph, feed this into | sort -u | ./reduce.py
# Could maybe use GNU Parallel for a simple parallel version.


#! /usr/local/bin/python

import sys
import itertools as it
import operator as op
from collections import defaultdict
from utility import *

# Taken from http://docs.python.org/2/library/itertools.html
# Add a threshold here for "solid" kmers
def unique(iterable, key=None):
  "List unique elements, preserving order. Remember only the element just seen."
  return it.imap(next, it.imap(op.itemgetter(1), it.groupby(iterable, key)))

def flag_edge((suffix, edges)):
  seen = set()
  for _,e in edges:
    if e in seen:
      yield 1
    else:
      seen.add(e)
      yield 0

def group(pairs, key=lambda (v,e): v):
  return it.groupby(pairs, key=key)

def group_suffixes(pairs):
  return group(pairs, key=lambda (v,e):v[1:])

def flag_last((node, edges)):
  edges.next()
  return it.chain((0 for e in edges), [1])

lines = (clean(line).split() for line in sys.stdin)
lines = ((reverse(v),e) for v,e in lines)
lines = unique(lines)

w,x,y,z = it.tee(lines, 4)

f_column = ((v[-1], 1) for v,_ in x)
edges = (e for _,e in w)
outgoing_flags = flatten(it.imap(flag_edge, group_suffixes(y)))
last = flatten(it.imap(flag_last, group(z)))

g = it.izip(f_column, last, edges, outgoing_flags)

counts = defaultdict(int)

for (c,v), last_flag, edge, out_flag in g:
  counts[c] += v
  print last_flag, edge, out_flag

print [0] + list(accumulate(v for _,v in sorted(counts.items())))[:-1]

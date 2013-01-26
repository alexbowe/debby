#! /usr/local/bin/python

import sys
from utility import *

def split(s):
  return (s[:-1], s[-1])

for line in sys.stdin:
  v,e = split(line.strip())
  v = reverse(v)
  print v,e

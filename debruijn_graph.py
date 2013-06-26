import itertools as it
from utility import *
from bisect import bisect_left, bisect_right

def rank(symbol, sequence, i):
  return sequence[:i+1].count(symbol)

def select(symbol, sequence, i):
  if i <= 0: return -1
  ranks = (rank(symbol, sequence, i) for i in xrange(len(sequence)))
  return next(it.dropwhile(lambda (_,x): x<i, enumerate(ranks)), (None,None))[0]

class debruijn_graph:
  def __init__(self, k, F, last, edges, edge_flags):
    alphabet = sorted(list(set(edges)))
    self._F = dict(zip(alphabet, F))
    self._F_inv = lambda i: alphabet[bisect_left(F, i, 0, bisect_right(F, i) - 1)]
    self._last = last
    self._edges = [c + ("","-")[x] for c,x in it.izip(edges,edge_flags)]
    self.num_edges = len(edges)
    self.num_nodes = sum(last)
    self.k = k

  def _fwd(self, i):
    c = self._edges[i][0] # [0] to remove minus flag
    if c == "$": return -1
    base_c = self._F[c]
    rank_c = rank(c, self._edges, i) # how many Cs away from base, but only if they are marked as last
    prev_1s = rank(1, self._last, base_c - 1)
    return select(1, self._last, prev_1s + rank_c)

  def _bwd(self, i):
    c = self._F_inv(i)
    if c == "$": return -1
    base_c = self._F[c] # find the base first, then find how many cs, then select to it
    pre_base_rank = rank(1, self._last, base_c - 1)
    prev_rank = rank(1, self._last, i - 1)
    n = prev_rank - pre_base_rank + 1 # nth edge with label c
    return select(c, self._edges, n)

  def _first_edge(self, v):
    return select(1, self._last, v) + 1

  def _last_edge(self, v):
    return select(1, self._last, v + 1)

  def _node_range(self, v):
    return (self._first_edge(v), self._last_edge(v))

  def _edge_to_node(self, i):
    if i == 0: return 0
    return rank(1, self._last, i - 1)

  def outdegree(self, v):
    first, last = self._node_range(v)
    return last - first + 1

  def outgoing(self, v, c):
    if c == "$": return -1
    first, last = self._node_range(v)
    for x in (c, c + "-"):
      prev_cs = rank(x, self._edges, last)
      last_c_pos = select(x, self._edges, prev_cs)
      if first <= last_c_pos <= last:
        return rank(1, self._last, self._fwd(last_c_pos)) - 1
    return -1

  def successors(self, v):
    first, last = self._node_range(v)
    for x in xrange(first, last + 1):
      yield rank(1, self._last, self._fwd(x)) - 1

  def indegree(self, v):
    i = self._last_edge(v)
    first_pred = self._bwd(i)
    if first_pred == -1: return 0
    c = self._edges[first_pred]
    next_node = select(c, self._edges, first_pred + 1) or self.num_edges - 1
    return rank(c+"-", self._edges, next_node) - rank(c+"-", self._edges, first_pred) + 1

  def incoming(self, v, c):
    i = self._last_edge(v)
    first_pred = self._bwd(i)
    if first_pred == -1: return -1
    e = self._edges[first_pred]
    next_node = select(e, self._edges, first_pred + 1) or self.num_edges - 1
    flags_before_base = rank(e+"-", self._edges, first_pred)
    number_flags = rank(e+"-", self._edges, next_node) - flags_before_base
    indices = [first_pred] + [select(e+"-", self._edges, flags_before_base + x) for x in xrange(1, number_flags + 1)]
    accessor = lambda i: self.label(self._edge_to_node(indices[i]))[0]
    a = array_adaptor(accessor, len(indices))
    sub_idx = get_index(a, c)
    if sub_idx == -1: return -1
    return self._edge_to_node(indices[sub_idx])

  def _label_iter(self, v):
    i = self._first_edge(v)
    while True:
      yield self._F_inv(i)
      i = self._bwd(i)

  def label(self, v):
    return "".join(take(self.k, self._label_iter(v))[::-1])

  @staticmethod
  def load(filename):
    with open(filename, "r") as f:
      lines = f.readlines()
    edges = [(int(l),e,int(f)) for l,e,f in (x.strip().split() for x in lines[:-2])]
    last, edges, flags = map(list, zip(*edges))
    F = map(int, lines[-2].split())
    k = int(lines[-1])
    return debruijn_graph(k, F, last, edges, flags)

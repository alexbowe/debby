
class de_bruijn_graph:
  def __init__(self, f_column, last_flags, edges, edge_flags):
    # zip them up and go crazy
    pass

  def _fwd(self, i):
    c = edges[i]
    r = rank(c, edges, i)
    x = F[c] + r - 1
    return select(1, last, x)

  def _bwd(self, i):
    x = rank(1, last, j)
    c = F_inv[x]
    r = x - F[c] + 1
    return select(c, W, r)

  def outdegree(v): pass
  def outgoing(v,c): pass
  def indegree(v): pass
  def incoming(v,c): pass
  def node(v):
    pass

# TODO: make a commandline tool for this that streams the
# other program output into the datastructures for this
# TODO: just use python's counting function to implement rank and select atm
# TODO: isnt there a O(N) BWT construction alg?
# TODO: implement de bruijn rank

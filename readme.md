Debby
=====

Debby is a *demonstration* of the succinct de Bruijn Graph implementation, in Python.
Details can be found on my [blog post][blog].

As it is only a demonstration, it doesn't use any efficient data structures for compression or rank/select, and some operations could be shaved off.
Perhaps one day Debby will grow up, and I will write tests for, refactor, and optimize her.

Usage
-----

1. First you need to stream (k+1)-mers (that is, a kmer and an edge label) into `format.sh`. So, if you want to make a
   de Bruijn graph with 3-mers, you would need to break your reads into 4-mers. Also, they reads must be padded with $
   signs (see the [blog][blog] for why). I'll leave this up to you, but for testing I have included the file `sample-edges`.

2. These need to be sorted, and filtered for unique nodes.

3. Finally, run `reduce.py` on the output to format the graph correctly (in plaintext) and output to a file. The format
   is that the last line is the k value, the second last line is the F-array (how we represent the node labels), and the
   previous lines represent a (last-flag, edge-label, shared-outgoing-node-flag) tuple, for each edge.

Here is how to do so with the supplied `sample-edges` file:

    $ cat sample-edges | ./format.sh | sort -u | ./reduce.py > my-graph

The reason I split it into stages (and made my Python code operate entirely on streams in a map-reduce fashion)
was to demonstrate that these parts can be easily distributed, or the sort phase can be replaced with a more sophisticated
k-mer counting method (e.g. bloom filters).

After you have your graph file, you can open a python interpreter, import debby, and play with the interface:

    >>> import debby as db
    >>> g = db.debruijn_graph.load("my-graph")
    >>> g.label(4)
    'TAC'
    >>> g.indegree(4)
    1

and so on...

[blog]: http://www.alexbowe.com/succinct-debruijn-graph

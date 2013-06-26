import itertools as it
from bisect import bisect_left

def reverse(s):
  return s[-1::-1]

def clean(s):
  return s.strip()

def flatten(listOfLists):
  "Flatten one level of nesting"
  return it.chain.from_iterable(listOfLists)

def take(n, iterable):
  "Return first n items of the iterable as a list"
  return list(it.islice(iterable, n))

def accumulate(iterable, func=lambda a,b: a+b):
  'Return running totals'
  # accumulate([1,2,3,4,5]) --> 1 3 6 10 15
  # accumulate([1,2,3,4,5], operator.mul) --> 1 2 6 24 120
  iterable = iter(iterable)
  total = next(iterable)
  yield total
  for element in iterable:
    total = func(total, element)
    yield total

def get_index(a, x):
  'Locate the leftmost value exactly equal to x'
  i = bisect_left(a, x)
  if i != len(a) and a[i] == x:
    return i
  return -1

class array_adaptor:
  def __init__(self, lam, n):
    self.lam = lam
    self.n = n

  def __getitem__(self, idx):
    return self.lam(idx)

  def __len__(self):
    return self.n

import itertools as it

def reverse(s):
  return s[-1::-1]

def clean(s):
  return s.strip()

def flatten(listOfLists):
  "Flatten one level of nesting"
  return it.chain.from_iterable(listOfLists)

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

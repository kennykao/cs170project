#!/usr/bin/env python

from __future__ import division
import argparse


"""
===============================================================================
  Please complete the following function.
===============================================================================
"""
def alg3(P, M, N, C, items, constraints):
  sorted_by_second = sorted(items, key=lambda tup: tup[5])
  print(sorted_by_second)
  i = N - 1
  sack = [P,M]
  insack = []
  while i > 0:
    if sack[0] == 0: 
      break
    elif 
      insack.append(items[i])
      i -= 1




def solve(P, M, N, C, items, constraints):
  """
  Write your amazing algorithm here.

  Return: a list of strings, corresponding to item names.
  """
  '''
  Basically just regular knapsack except with added dimension
  so instead of a 2-D table have a 3-D table.
  if resale < cost: dont buy
  base cost off of resale - cost; always have a positive value
  '''
  d = dict()
  i = 0
  while i<N:
    d[i] = set()
    i += 1
  for constraint in constraints:
    for i in constraint:
      d[i] = d[i].union(constraint)
      d[i].remove(i)
  i = 0
  while i < N:
    if items[i][3] > items[i][4]:
      del items[i]
      i += 1
    else:
      items[i] = items[i] + (items[i][4] - items[i][3],)
      print(items[i])
      i += 1

  alg3(P,M,N,C,items,constraints)





"""
===============================================================================
  No need to change any code below this line.
===============================================================================
"""

def read_input(filename):
  """
  P: float
  M: float
  N: integer
  C: integer
  items: list of tuples
  constraints: list of sets
  """
  with open(filename) as f:
    P = float(f.readline())
    M = float(f.readline())
    N = int(f.readline())
    C = int(f.readline())
    items = []
    constraints = []
    for i in range(N):
      name, cls, weight, cost, val = f.readline().split(";")
      items.append((name, int(cls), float(weight), float(cost), float(val)))
    for i in range(C):
      constraint = set(eval(f.readline()))
      constraints.append(constraint)
  return P, M, N, C, items, constraints

def write_output(filename, items_chosen):
  with open(filename, "w") as f:
    for i in items_chosen:
      f.write("{0}\n".format(i))

if __name__ == "__main__":

  parser = argparse.ArgumentParser(description="PickItems solver.")
  parser.add_argument("input_file", type=str, help="____.in")
  parser.add_argument("output_file", type=str, help="____.out")
  args = parser.parse_args()

  P, M, N, C, items, constraints = read_input(args.input_file)
  items_chosen = solve(P, M, N, C, items, constraints)
  write_output(args.output_file, items_chosen)

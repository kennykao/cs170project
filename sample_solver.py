#!/usr/bin/env python

from __future__ import division
import argparse
from multiprocessing import Process
from multiprocessing.pool import ThreadPool
from os import getpid 

"""
===============================================================================
  Please complete the following function.
===============================================================================
"""

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

  # INITIALIZING DATA STRUCTURES
  
  d = dict()                  # Dictionary of Constraints { item_class : {constraints set} }
  item_val_lst = []           # List of Item Net Values  [ (resale value - cost, item_name) ]
  item_weight_lst = []        # List of Item Weights [ (weight, item_name) ]
  item_ratio_lst = []
  item_combined = []
  weight_zero = []
  item_cost_val_dict = dict() # Dictionary of Items { item_name : (cost, resale value, weight, class) }

  i = 0
  while i < N:
    curr_item = items[i]
    d[i] = set()
    if (curr_item[4] - curr_item[3] <= 0):
      i += 1
      continue

    item_val_lst.append( (curr_item[4] - curr_item[3], curr_item[0]) )
    item_weight_lst.append((curr_item[2], curr_item[0]))
    item_combined.append((curr_item[4] - curr_item[3], curr_item[2], curr_item[0]))
    item_cost_val_dict[curr_item[0]] = (curr_item[3], curr_item[4], curr_item[2], curr_item[1]) 
    i += 1
    if (curr_item[2] == 0):
      item_ratio_lst.append(((curr_item[4]-curr_item[3])/.01, curr_item[0]))
    else:
      item_ratio_lst.append(((curr_item[4]-curr_item[3])/curr_item[2], curr_item[0]))


 
  for constraint in constraints:
    for i in constraint:
      d[i] = d[i].union(constraint)
      d[i].remove(i)
  i = 0 


  # MAX VALUE GREEDY ALGORITHM
  # Choose the item that has the maximum value from the remaining items
  def max_val_greedy(P, M, lst):
    lst = lst[:]
    lst_classes = set()
    result = []
    total_resale = 0

    while (lst):
      lst.sort(reverse = True)
      curr_max = lst[0]
      curr_max_cost = item_cost_val_dict[curr_max[1]][0]
      curr_max_weight = item_cost_val_dict[curr_max[1]][2]
      curr_max_class = item_cost_val_dict[curr_max[1]][3]
      if (M == 0) or (P == 0):
        break
      elif (curr_max_cost <= M) and (curr_max_weight <= P) and (curr_max_class not in lst_classes):
        result.append(curr_max[1])
        for c in d[curr_max_class]:
          lst_classes.add(c)
        total_resale += curr_max[0]
        lst.remove(curr_max)
        M = M - curr_max_cost 
        P = P - curr_max_weight
      else:
        lst.remove(curr_max)

    return (total_resale, result)


  # MIN WEIGHT GREEDY ALGORITHM
  # Choose the lightest item from the remaining items
  def min_weight_greedy(P, M, lst):
    lst = lst[:]
    lst_classes = set()
    result = []
    total_resale = 0

    while (lst):
      curr_min = min(lst)
      curr_min_cost = item_cost_val_dict[curr_min[1]][0]
      curr_min_weight = item_cost_val_dict[curr_min[1]][2]
      curr_min_class = item_cost_val_dict[curr_min[1]][3]

      if (M == 0) or (P == 0):
        break
      elif (curr_min_cost <= M) and (curr_min_weight <= P) and (curr_min_class not in lst_classes):
        result.append(curr_min[1])
        for c in d[curr_min_class]:
          lst_classes.add(c)
        total_resale += item_cost_val_dict[curr_min[1]][1]
        lst.remove(curr_min)
        M = M - curr_min_cost 
        P = P - curr_min_weight 
      else:
        lst.remove(curr_min)

    return (total_resale, result)


  # VALUE TO WEIGHT RATION GREEDY ALGORITHM
  # Choose the items with as high a value per weight as possible
  def val_to_weight_greedy(P, M, lst):
    lst = lst[:]
    lst_classes = set()
    result = []
    total_resale = 0

    while (lst):
      curr_max = max(lst)
      curr_max_cost = item_cost_val_dict[curr_max[1]][0]
      curr_max_weight = item_cost_val_dict[curr_max[1]][2]
      curr_max_class = item_cost_val_dict[curr_max[1]][3]
      if (M == 0) or (P == 0):
        break
      elif (curr_max_cost <= M) and (curr_max_weight <= P) and (curr_max_class not in lst_classes):
        result.append(curr_max[1])
        for c in d[curr_max_class]:
          lst_classes.add(c)
        total_resale += curr_max[0]
        lst.remove(curr_max)
        M = M - curr_max_cost 
        P = P - curr_max_weight
      else:
        lst.remove(curr_max)
    return (total_resale, result)

  # HYBRID GREEDY ALGORITHM
  # Choose max value until 90% full, then switch to min weight. Then sweep down from 90% - ~50%? 
  def hybrid_greedy(P, M, lst):
    lst = lst[:]
    lst_classes = set()
    result = []
    total_resale = 0

    reduced_P = P * 0.7
    reduced_P2 = P - reduced_P 
    while (lst):
      curr_max = max(lst)
      curr_max_cost = item_cost_val_dict[curr_max[2]][0]
      curr_max_weight = item_cost_val_dict[curr_max[2]][2]
      curr_max_class = item_cost_val_dict[curr_max[2]][3]
      if (M == 0) or (reduced_P == 0):
        break
      elif (curr_max_cost <= M) and (curr_max_weight <= reduced_P) and (curr_max_class not in lst_classes):
        result.append(curr_max[2])
        for c in d[curr_max_class]:
          lst_classes.add(c)
        total_resale += item_cost_val_dict[curr_max[2]][0]
        lst.remove(curr_max)
        M = M - curr_max_cost 
        reduced_P = reduced_P - curr_max_weight
      else:
        lst.remove(curr_max)
    while (lst):
      lst.sort(key=lambda x: x[1])
      curr_min = min(lst)
      curr_min_cost = item_cost_val_dict[curr_min[2]][0]
      curr_min_weight = item_cost_val_dict[curr_min[2]][2]
      curr_min_class = item_cost_val_dict[curr_min[2]][3]
      if (M == 0) or (reduced_P2 == 0):
        break
      elif (curr_min_cost <= M) and (curr_min_weight <= reduced_P2) and (curr_min_class not in lst_classes):
        result.append(curr_min[2])
        for c in d[curr_min_class]:
          lst_classes.add(c)
        total_resale += item_cost_val_dict[curr_min[2]][0]
        lst.remove(curr_min)
        M = M - curr_min_cost 
        reduced_P2 = reduced_P2 - curr_min_weight
      else:
        lst.remove(curr_min)   
    print(result)
    return (total_resale, result)


  # Take max of all algorithms

  pool = ThreadPool(processes = 8)
  async_pool = pool.apply_async(min_weight_greedy,(P,M,item_weight_lst))
  return_val1 = async_pool.get()

  pool = ThreadPool(processes = 8)
  async_pool = pool.apply_async(max_val_greedy,(P,M,item_val_lst))
  return_val2 = async_pool.get()

  pool = ThreadPool(processes = 8)
  async_pool = pool.apply_async(val_to_weight_greedy,(P,M,item_ratio_lst))
  return_val3 = async_pool.get()

  pool = ThreadPool(processes = 8)
  async_pool = pool.apply_async(hybrid_greedy,(P,M,item_combined))
  return_val4 = async_pool.get()
  
  return max([return_val1,return_val2,return_val3,return_val4])[1]
  '''
  alg_one = Process(target=max_val_greedy(P,M,item_val_lst))
  alg_one.start()
  alg_two = Process(target=min_weight_greedy(P,M,item_weight_lst))
  alg_two.start()
  alg_one.join()
  alg_two.join()
  return max([alg_one,alg_two])[1]
  '''
  '''
  #alg_one = max_val_greedy(P, M, item_val_lst)
  #alg_two = min_weight_greedy(P, M, item_weight_lst)
  alg_three = val_to_weight_greedy(P,M,item_ratio_lst)
  alg_four = hybrid_greedy(P,M,item_combined)

  return max([alg_one, alg_two, alg_three, alg_four])[1]
  '''
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
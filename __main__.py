# -*- coding: utf-8 -*-
"""101803010_Harshit_Assig6.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Cm_XDHoz4DC01i6umEk5SWjkAmbJPZ5T
"""

def main():
  import sys
  arguments = sys.argv
  if len(arguments) != 5:
    print("Not correct number of arguments")
    exit(0)
  if len(arguments[2]) % 2 != 1 and len(arguments[3]) % 2 != 1:
    print("Not correct number of weights or impacts")
    exit(0)
  if len(arguments[2]) != len(arguments[3]):
    print("Number of weights and impacts should be equal")
    exit(0)
  input_file = arguments[1]
  try:
    import pandas as pd
    import numpy as np
    import math
    """
    Reading Input file
    """
    open_file = pd.read_csv(input_file, index_col=False)
    colnames = open_file.columns
    if len(colnames) < 3:
      print("There should be atleast 3 columns")
      exit(0)
    """
    Converting Dataframe column values to numpy arrays and Root mean square of values
    """
    attribute = []
    j = 0
    for i in range(1, len(colnames)):
      lt = []
      lt = open_file[colnames[i]]
      attribute.append(np.array(lt))
      sum1 = math.sqrt(sum(attribute[j] ** 2))
      attribute[j] = attribute[j] / sum1
      j += 1
    """
    Multiplying values with their corresponding weights
    """
    weights_str = arguments[2]
    weights_raw = weights_str.split(',')
    if '' in weights_raw:
      print("Incorrect number of comma separators")
      exit(0)

    if len(weights_raw) != (len(colnames) - 1):
      print("Number of weights should be attribute columns")
      exit(0)

    weights = []
    num = []
    for w in range(len(weights_raw)):
      if ord(weights_raw[w]) not in range(48, 58):
        print("Weights should only be numeric")
        exit(0)
      else:
        weights.append(float(weights_raw[w]))

    for i in range(len(attribute)):
      attribute[i] *= weights[i]

    """
    Multiplying impacts with values
    """
    impact_str = arguments[3]
    impact = impact_str.split(",")
    if '' in impact:
      print("Incorrect number of comma separators")
      exit(0)

    if len(impact) != (len(colnames) - 1):
      print("Number of impacts should be attribute columns")
      exit(0)
    for i in range(len(impact)):
      if impact[i] not in ['+', '-']:
        print("Imacts should be either \"+\" or \"-\"")
        exit(0)
      else:
        if impact[i] == "-":
          attribute[i] = -1 * attribute[i]
    """
    Finding best and worst values among columns and corresponding Euclidean distance  
    """
    V_worst = []
    V_best = []
    for i in range(len(attribute)):
      V_worst.append(min(attribute[i]))
      V_best.append(max(attribute[i]))
    Euc_dist_from_worst = []
    Euc_dist_from_best = []
    for i in range(len(attribute[0])):
      w = 0
      b = 0
      for j in range(len(attribute)):
        w += (attribute[j][i] - V_worst[j]) ** 2
        b += (attribute[j][i] - V_best[j]) ** 2
      Euc_dist_from_worst.append(math.sqrt(w))
      Euc_dist_from_best.append(math.sqrt(b))
    """
    Calculating performance
    """
    performance = []
    for i in range(len(attribute[0])):
      performance.append(Euc_dist_from_worst[i] / (Euc_dist_from_worst[i] + Euc_dist_from_best[i]))
    rank = np.zeros((len(performance)))
    j = 1

    pp = performance.copy()
    for i in range(len(performance)):
      m = max(pp)
      ind = np.where(np.array(performance) == m)
      for k in range(len(ind[0])):
        rank[ind[0][k]] = j
        tt = np.where(np.array(pp) == performance[ind[0][k]])
        for t in tt[0]:
          del pp[t]
      j += 1
    names = list(open_file[colnames[0]])
    name = str(arguments[4])
    pd.DataFrame({str(colnames[0]): names}).to_csv("ex1.csv", index=False)
    r1 = pd.read_csv("ex1.csv")
    k = 1
    for i in range(len(attribute)):
      r1.insert(k, colnames[i + 1], list(attribute[i]))
      k += 1
    r1.insert(k, "Performance", performance)
    k += 1
    r1.insert(k, "Rank", rank)
    r1 = r1.loc[:, ~r1.columns.str.contains('^Unnamed')]
    r1.to_csv(name, index=False)
  except:
    print("File not found")

if __name__ == '__main__':
    main()

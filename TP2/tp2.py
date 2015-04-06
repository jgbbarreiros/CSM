# imports
import numpy as np

# functions

def bin_code_shannon_fano(symb, prob):

  #sorted(prob, reverse=True)
  #sorted_symb = np.array(len(symb))
  sorted_symb = np.zeros(len(symb))

  b = 0
  s = 0
  l = 0

  for i in range(len(prob)):
    if (prob[i] > b):
      b = prob[i]

  while(l < len(symb)):
    for i in range(len(prob)):
      if (prob[i] == b):
        sorted_symb[l] = i
        l += 1

    for i in range(len(prob)):
      if (s < prob[i] < b):
          s = prob[i]
    b = s
    s = 0

  

  return sorted_symb


# main

if __name__ == "__main__":
  
  # variables

  document_text = "babe"
  symbols = ["a","b","c","d","e"]
  #symbols = [1,2,3,4,5]
  probability = [.25,.5,.0,.0,.25]

  # function calls

  bin_table = bin_code_shannon_fano(symbols, probability)

  print bin_table
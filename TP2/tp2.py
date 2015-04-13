# imports
import numpy as np

# functions

def bin_code_shannon_fano(symb, prob):

  #sorted(prob, reverse=True)
  #sorted_symb = np.array(len(symb))
  # sorted_symb = np.zeros(len(symb))

  # b = 0
  # s = 0
  # l = 0

  # for i in range(len(prob)):
  #   if (prob[i] > b):
  #     b = prob[i]

  # while(l < len(symb)):
  #   for i in range(len(prob)):
  #     if (prob[i] == b):
  #       sorted_symb[l] = prob[i]
  #       l += 1

  #   for i in range(len(prob)):
  #     if (s < prob[i] < b):
  #         s = prob[i]
  #   b = s
  #   s = 0
  s = sorted(prob, reverse=True)
  print s
  return a(s)


  # [.20, .20, .20, .10, .10, .10, .5, .5]
def a(prob):
  print "(-----------------"
  for i in range(len(prob)):
    l = prob[:i+1]
    r = prob[i+1:]
    if (sum(l) >= sum(r)):
      break
  print "l = " + str(l)
  print "r = " + str(r)
  if len(l) == 1:
    fl = np.array(["0"])
    print "fim l"
  else:
    fl = a(l)
    for i in range(len(fl)):
      fl[i] = "0" + fl[i]
    print "fl = " + str(fl)

  if len(r) == 1:
    fr = np.array(["1"])
    print "fim r"
  else:
    fr = a(r)
    print "fr = " + str(fr)
    for i in range(len(fr)):
      fr[i] = "1" + fr[i]
    print "fr = " + str(fr)
  print np.hstack((fl, fr))
  print "-----------------)"
  return np.hstack((fl, fr))

# main

if __name__ == "__main__":
  
  # variables
  document_text = "babe"
  symbols = ["a","b","c","d","e"]
  #symbols = [1,2,3,4,5]
  probability = [.25,.5,.25]
  # .20, .20, .20, .10, .10, .10, .5, .5

  # function calls

  bin_table = bin_code_shannon_fano(symbols, probability)

  print bin_table
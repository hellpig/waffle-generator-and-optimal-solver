#!/usr/bin/env python3.11
#
# Generate rectangular Waffle solutions of any size,
#   but make them "solid" (without "holes").
# Any word size greater than 1 is currently supported!
#
# Some examples of puzzles online...
#   https://wafflegame.net/daily       5×5
#   https://wafflegame.net/deluxe      7×7
#   https://wordwaffle.org/unlimited   3×3 can be found here
# I cannot find any non-square rectangular puzzles online.
# I cannot find any "solid" puzzles online.
#
# For square waffles...
#  - I prevent symmetrically identical puzzles.
#  - I remove waffles with repeated words.
#
# For non-square Waffles, I put the longer words vertical.
# If desired, transposing rows and columns is a trivial next step.
#
# First, generate the words#.json files as described in README.md
#
# (c) 2023 Bradley Knockel



# Set number of letters per word along each dimension.
# Each must be an odd number greater than 1.
#  n1 <= n2
n1 = 4
n2 = 4


import json

#################################################
###### prepare
#################################################

if n1 > n2:
  print("  Error: n1 > n2.")
  exit()

if n1 < 2:
  print("  Error: only sizes greater than 1!")
  exit()


n1p = 2*n1   # useful
n2p = 2*n2


# load first word list
with open('words' + str(n1) + '.json') as f:
  data1 = json.load(f)

# load 2nd word list
if n1==n2:
  data2 = data1
else:
  with open('words' + str(n2) + '.json') as f:
    data2 = json.load(f)
  

print("\n  Word list 1 is", len(data1), str(n1) + "-letter words.")
print("  Word list 2 is", len(data2), str(n2) + "-letter words.")


#################################################
###### place words one by one in all possible ways
#################################################

# For numbering the words, word on top is 0,
#   and the vertical word on the left is 1.
#   It keeps alternating between horizontal and vertical.
#   If there are no vertical words remaining,
#     the word is still counted but is equal to ''.



# recursive function to handle the variable number of for loops (number of loops depends on nl)
def loop_recursive(w, n, nHalf):

  if n < n2p:

    if n < n1p:
      temp1 = "".join([ w[i][nHalf] for i in range(1,n,2) ])

    for w1 in data1:   # horizontal word

      if n < n1p:   # if there are still more vertical words to be placed

        if w1[:nHalf] != temp1:
          continue

        nn = n + 1
        nnHalf = nHalf + 1
        ww = w + [w1]

        temp2 = "".join([ ww[i][nHalf] for i in range(0,nn,2) ])

        for w2 in data2:    # vertical word

          if w2[:nnHalf] != temp2:
            continue

          loop_recursive(ww + [w2], nn + 1, nnHalf)

      else:

        if [ w1[i] for i in range(0,n1) ] != [ w[i][nHalf] for i in range(1,n1p,2) ]:
          continue

        loop_recursive(w + [w1, ''], n + 2, nHalf + 1)


  else:     # w now contains all the words in the waffle

      # check for repeated words in square waffle
      if n1==n2 and len(w) != len(set(w)):
        return

      waffle = '\n'.join([w[i] for i in range(0,n2p,2)])

      print()
      print(waffle)
      print("      " + " ".join([word for word in w]))
      print()


# prevent symmetrically identical puzzles by doing the first two words here to enforce w1 < w2,
#   but only for square waffles

for w1 in data1:
  print("  Now starting with " + w1 + " as the first word")

  if n1==n2:   # square waffles
    for w2 in data2:
      if w2[0]==w1[0] and w1 < w2:
        loop_recursive([w1,w2], 2, 1)
  else:
    for w2 in data2:
      if w2[0]==w1[0]:
        loop_recursive([w1,w2], 2, 1)


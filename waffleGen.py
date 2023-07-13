#!/usr/bin/env python3.11
#
# Generate all Waffle grids of a certain size...
#   https://wafflegame.net/daily       5×5
#   https://wafflegame.net/deluxe      7×7
#   https://wordwaffle.org/unlimited   3×3 can be found here
# Any odd word size greater than 1 is currently supported!
#
# I remove waffles with repeated words.
#
# I prevent symmetrically identical puzzles. 
#
# First, download freq_map.json (5-letter-word frequencies) from
#   https://github.com/3b1b/videos/tree/master/_2022/wordle/data
# and/or download words_alpha.txt from
#   https://github.com/dwyl/english-words
#
# words_alpha.txt works for any size words.
# freq_map.json is better, but only has 5-letter words,
#   and my code assumes you will use it for 5-letter words
#
# (c) 2023 Bradley Knockel



# Set number of letters per word
# Must be an odd number greater than 1
nl = 17


#################################################
###### prepare
#################################################


if nl < 3 and not nl&1:   # only odds greater than 1
  print("  Error: only 3×3, 5×5, 7×7, ... puzzles are currently supported!")
  exit()


# useful (assuming odd nl)
half = nl//2 + 1
full = nl + 1   # the number of words


# load word list
isFrequencyMap = False
if nl==5:   # this list is better, but only has 5-letter words

  import json
  isFrequencyMap = True
  with open('freq_map.json') as f:
    data = json.load(f)

else:

  with open('words_alpha.txt') as f:
    dataLong = f.read().split()

  data = []
  for word in dataLong:
    if len(word)==nl:
      data.append(word)
  del dataLong   # free up RAM


print("\n  Word list is", len(data), str(nl) + "-letter words.")


#################################################
###### place words one by one in all possible ways
#################################################

# For numbering the words, word on top is 0,
#   and the vertical word on the left is 1.
#   It keeps alternating between horizontal and vertical.



# recursive function to handle the variable number of for loops (number of loops depends on nl)
def loop_recursive(w, n):

  if n < full:
    for w1 in data:   # horizontal word

      if [ w1[i] for i in range(0,n,2) ] != [ w[i][n] for i in range(1,n,2) ]:
        continue

      nn = n + 1
      ww = w + [w1]

      for w2 in data:    # vertical word

        if [ w2[i] for i in range(0,nn,2) ] != [ ww[i][n] for i in range(0,nn,2) ]:
          continue

        loop_recursive(ww + [w2], nn + 1)

  else:     # w now contains all the words in the waffle

      # check for repeated words in waffle
      if len(w) != len(set(w)):
        return

      waffle = ''.join(["\n"+" ".join( [w[j][i] for j in range(1,full,2)] )+"\n" if i&1 else w[i] for i in range(nl)])  # oof

      print()
      print(waffle)
      print("      " + " ".join([word for word in w]))
      print()


# Prevent symmetrically identical puzzles by doing the first two words here and enforcing w1 < w2
for w1 in data:
  print("  Now starting with " + w1 + " as the first word")
  for w2 in data:
    if w2[0]==w1[0] and w1 < w2:
      loop_recursive([w1,w2], 2)



#!/usr/bin/env python3.11
#
# Generate rectangular Waffle solutions of any size...
# Any odd word size greater than 1 is currently supported!
#
# Some examples of puzzles online...
#   https://wafflegame.net/daily       5×5
#   https://wafflegame.net/deluxe      7×7
#   https://wordwaffle.org/unlimited   3×3 can be found here
# I cannot find any non-square rectangular puzzles online.
#
# For square waffles...
#  - I prevent symmetrically identical puzzles.
#  - I remove waffles with repeated words.
#
# For non-square Waffles, I put the longer words vertical.
# If desired, transposing rows and columns is a trivial next step.
#
# First, download freq_map.json (5-letter-word frequencies) from
#   https://github.com/3b1b/videos/tree/master/_2022/wordle/data
# and/or download words_alpha.txt from
#   https://github.com/dwyl/english-words
#
# words_alpha.txt works for any size words.
#   However, you will want to reduce it to more common words.
# freq_map.json is better, but only has 5-letter words,
#   and my code assumes you will use it for 5-letter words,
#   and that you want to use its frequency data to reduce
#   the size of the word list.
#
# (c) 2023 Bradley Knockel



# Set number of letters per word along each dimension.
# Each must be an odd number greater than 1.
#  n1 <= n2
n1 = 5
n2 = 7


# for when using freq_map.json (when an n is 5)
freqCutoff = 0.0001



# for when not using freq_map.json (when an n is not 5)

wordListFile1 = "words_alpha.txt"
wordListFile1 = "wordsCommon3.txt"

wordListFile2 = "words_alpha.txt"
wordListFile2 = "wordsCommon7.txt"




#################################################
###### prepare
#################################################

if n1 > n2:
  print("  Error: n1 > n2.")
  exit()

if n1 < 3 or not n1&1 or n2 < 3 or not n2&1:
  print("  Error: only odd sizes greater than 1!")
  exit()


n1p = n1+1   # useful


# load first word list
if n1==5:   # this list is better, but only has 5-letter words

  import json
  with open('freq_map.json') as f:
    dataLong = json.load(f)

  data1 = []
  for word in dataLong:
    if dataLong[word] > freqCutoff:
      data1.append(word)
  del dataLong   # try to free up RAM

else:

  with open(wordListFile1) as f:
    dataLong = f.read().split()

  data1 = []
  for word in dataLong:
    if len(word)==n1:
      data1.append(word)
  del dataLong   # try to free up RAM



# load 2nd word list
if n1==n2:
  data2 = data1
else:
  if n2==5:   # this list is better, but only has 5-letter words

    import json
    with open('freq_map.json') as f:
      dataLong = json.load(f)

    data2 = []
    for word in dataLong:
      if dataLong[word] > freqCutoff:
        data2.append(word)
    del dataLong   # try to free up RAM

  else:

    with open(wordListFile2) as f:
      dataLong = f.read().split()

    data2 = []
    for word in dataLong:
      if len(word)==n2:
        data2.append(word)
    del dataLong   # try to free up RAM
  



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
def loop_recursive(w, n):

  if n < n2:
    for w1 in data1:   # horizontal word

      if n < n1p:   # if there are still more vertical words to be placed

        if [ w1[i] for i in range(0,n,2) ] != [ w[i][n] for i in range(1,n,2) ]:
          continue

        nn = n + 1
        ww = w + [w1]

        for w2 in data2:    # vertical word

          if [ w2[i] for i in range(0,nn,2) ] != [ ww[i][n] for i in range(0,nn,2) ]:
            continue

          loop_recursive(ww + [w2], nn + 1)

      else:

        if [ w1[i] for i in range(0,n1,2) ] != [ w[i][n] for i in range(1,n1p,2) ]:
          continue

        loop_recursive(w + [w1, ''], n + 2)


  else:     # w now contains all the words in the waffle

      # check for repeated words in square waffle
      if n1==n2 and len(w) != len(set(w)):
        return

      waffle = ''.join(["\n"+" ".join( [w[j][i] for j in range(1,n1p,2)] )+"\n" if i&1 else w[i] for i in range(n2)])  # oof

      print()
      print(waffle)
      print("      " + " ".join([word for word in w]))
      print()


# prevent symmetrically identical puzzles by doing the first two words here to enforce w1 < w2,
#   but only for square waffles

for w1 in data1:
  #print("  Now starting with " + w1 + " as the first word")

  if n1==n2:   # square waffles
    for w2 in data2:
      if w2[0]==w1[0] and w1 < w2:
        loop_recursive([w1,w2], 2)
  else:
    for w2 in data2:
      if w2[0]==w1[0]:
        loop_recursive([w1,w2], 2)


#!/usr/bin/env python3.11
#
# Given a "solid" solution, make a rectangular Waffle puzzle.
# Any word size greater than 1 is currently supported!
#
# First, generate the words#.json files as described in README.md
#
# Enter the solution in the first section of the code.
# To change the waffle-making strategy, edit the final "main code" section.
# Keep rerunning the code until you get a puzzle you like!
#
# (c) 2023 Bradley Knockel


from itertools import permutations
# Note that product(*perms) where perms is a list of permutations could use a lot of RAM,
#   so I don't import product from itertools
# Instead, I do the product myself using a recursive function that loops over permutations.

from random import shuffle, sample

import json


#################################################
###### enter the solution
#################################################



sol = """

draw
rare
idea
liar
loss

""".strip().lower()


sol = """

drill
radio
areas
wears

""".strip().lower()





#################################################
###### prepare
#################################################


# get number of letters per word (n1 and n2)
n1 = len(sol.split()[0])    # length of horizontal words
n2 = len(sol.split('\n'))   # length of vertical words

if n1 < 2 or n2 < 2:
  print("  Error: only sizes greater than 1!")
  exit()


# useful
full = n1 + n2    # the number of words
n1p = n1 + 1
n1d = 2*n1
n2d = 2*n2

# useful
fullNew = max(n1,n2) * 2
limits = [2*n2, 2*n1]
wordListAllNew = [[] for i in range(fullNew)]

# make blank board
temp = "." * n1 + "\n"
blank = temp * (n2-1) + "." * n1


# check for consistency
if len(sol) != n2*n1p-1:
  print("  Error: sol has an invalid shape!")
  exit()
for i in range(len(sol)):   # check against structure of blank
  b =  blank[i] == "\n" and sol[i] != "\n"
  c =  blank[i] == "." and not sol[i].isalpha()
  if b or c:
    print("  Error: invalid input!")
    exit()




# load first word list
with open('words' + str(n1) + '.json') as f:
  data1 = json.load(f)

# load 2nd word list
if n1==n2:
  data2 = data1
else:
  with open('words' + str(n2) + '.json') as f:
    data2 = json.load(f)





# make countsAll
countsAll = {}
goodLetters = sol.replace('\n', '').lower()
for i in 'abcdefghijklmnopqrstuvwxyz':
  countsAll[i] = goodLetters.count(i)



# make a list of words, where each word is a list of letters
wordsAll = []

for wordNum in range(full):

  if wordNum < n2:   # horizontal words
    start = wordNum * n1p
    wordsAll.append( list( sol[ start : start+n1 ] ) )
  else:
    start = wordNum - n2
    wordsAll.append( list( sol[ start :: n1p ] ) )




#################################################
###### colorPuzzle() function that makes greenMaskAll and lettersAll from puzzle
#################################################


def colorPuzzle(puzzle):

  # For numbering the words...
  # Initially, horizontal are first (word on top is 0),
  #   then vertical (word on right is last).

  # deep copy wordsAll[]; greens will later be removed; then yellows will be removed
  wordsLists = []
  for i in wordsAll:
    wordsLists.append(i[:])


  # make greenMaskAll
  greenMaskAll = list(blank)
  for i,l in enumerate(puzzle):
    if l.isalpha() and sol[i]==l:
      greenMaskAll[i] = l

      # remove greens from wordsLists[]
      wordNum = i//n1p   # horizontal word
      wordsLists[ wordNum ].remove(l)
      wordNum = n2 + i%n1p   # vertical word
      wordsLists[ wordNum ].remove(l)



  # find yellow candidates
  # Due to the various ways that yellows could be colored in, I am trying to add extra organization
  #   before choosing where any yellows go.
  yellowCandidates = []     # [ [ letter, index, words list, trivial? ], ... ]
  for i,l in enumerate(puzzle):
    if greenMaskAll[i].isalpha() or not l.isalpha():
      continue

    countMatches = 0
    length = 0    # the max number of places the player might think that the yellow goes to
    words = []

    wordNum = i//n1p   # horizontal word
    length += len(wordsLists[wordNum]) - 1
    countMatches += wordsLists[wordNum].count(l)
    words.append(wordNum)

    wordNum = n2 + i%n1p   # vertical word
    length += len(wordsLists[wordNum]) - 1
    countMatches += wordsLists[wordNum].count(l)
    words.append(wordNum)

    if countMatches:
      yellowCandidates.append( (l, i, words, length==1) )



  # put yellows in lettersAll by making yellow letters upper case
  lettersAll = puzzle[:]
  trivialPuzzle = False

  candidates =  [(a,b,c,d) for a,b,c,d in yellowCandidates if len(c)==2]   # shared locations

  indices = []   # marking indices to go back to
  for i,(a,b,c,d) in enumerate(candidates):    # first, do only locations that are inW1 and inW2
    w1 = c[0]  # wordNum1
    w2 = c[1]  # wordNum2
    inW1 = a in wordsLists[w1]
    inW2 = a in wordsLists[w2]
    if inW1 and inW2:

      lettersAll[b] = lettersAll[b].upper()
      if d:
        trivialPuzzle = True

      wordsLists[w1].remove(a)
      wordsLists[w2].remove(a)

    else:
      indices.append(i)

  for i in indices:    # do the skipped locations
    a,b,c,d = candidates[i]
    w1 = c[0]  # wordNum1
    w2 = c[1]  # wordNum2
    inW1 = a in wordsLists[w1]
    inW2 = a in wordsLists[w2]
    if inW1 or inW2:

      lettersAll[b] = lettersAll[b].upper()
      if d:
        trivialPuzzle = True

      if inW1:
        wordsLists[w1].remove(a)
      if inW2:
        wordsLists[w2].remove(a)






  return "".join(greenMaskAll), "".join(lettersAll), trivialPuzzle




#################################################
###### solver function, which returns number of solutions
#################################################


def count_solutions(greenMaskAll, lettersAll):
  global solCount    # needs to be global for loop_recursive()

  wordListAll = []

  for wordNum in range(full):   # find the possibilities for each of the words


    # For numbering the words...
    # Initially, horizontal are first (word on top is 0),
    #   then vertical (word on right is last).
    # The numbering system will later be changed.

    # take the correct slice and get correct word list (data) and number of letters (nl)
    if wordNum < n2:   # horizontal words
      start = wordNum * n1p
      greenMask = greenMaskAll[ start : start+n1 ]
      letters = lettersAll[ start : start+n1 ]
      data = data1
      nl = n1
    else:
      start = wordNum - n2
      greenMask = greenMaskAll[ start :: n1p ]
      letters = lettersAll[ start :: n1p ]
      data = data2
      nl = n2


    # make counts
    # I should probably reduce this further by looking at yellows in other words!?
    #   Though it doesn't really matter to do it here, because countsAll is checked later.
    counts = countsAll.copy()
    for i in 'abcdefghijklmnopqrstuvwxyz':
      greensInOtherWords = greenMaskAll.count(i) - greenMask.count(i)
      counts[i] = counts[i] - greensInOtherWords
    for i in letters:
      if i.islower() and i not in greenMask and i.upper() not in letters:
        counts[i] = 0



    # make wordNoGreen
    wordNoGreen = list(letters)
    for k in range(nl):
      if letters[k]==greenMask[k]:
        wordNoGreen[k] = '.'
    wordNoGreen = "".join(wordNoGreen)



    #######################
    ###### make letterList[]
    #######################

    # letterList[] = [ [letter, badLocations, countMax] , ...]
    letterList = []

    for i,j in enumerate(letters):   # j is a letter

        # is j the first yellow of that letter in the word?
        if j.isupper() and j not in letters[:i]:

          count = letters.count(j)  # yellows for now; greens added next
          for k in range(nl):
            if letters[k]==j.lower() and letters[k]==greenMask[k]:
              count += 1

          badLocations = [k for k in range(nl) if wordNoGreen.upper()[k] == j]

          if j.lower() in wordNoGreen:   # if there is a grey of the letter
            letterList.append([ j.lower(), badLocations, count ])
          else:
            letterList.append([ j.lower(), badLocations, counts[j.lower()] ])

        # is j is a green with no yellows of the same letter
        elif j==greenMask[i] and j.upper() not in letters:

          # we only need the first green in word
          if j in greenMask[:i]:
            continue

          # we only care if we learn that there aren't any more of the letter in the word
          if j in wordNoGreen:

            count = 0
            for k in range(nl):
              if letters[k]==j and letters[k]==greenMask[k]:
                count += 1

            letterList.append([ j, [], count ])




    #######################
    ###### search through all words in word list
    #######################

    wordList = []

    for word in data:

      # greenMask[]
      if any( g.isalpha() and g!=w for (g, w) in zip(greenMask, word)):
        continue

      # counts[]
      if any(word.count(i)>counts[i] for i in word):
        continue

      # letterList[]
      go = True
      for entry in letterList:
        if word.count(entry[0]) > entry[2] or entry[0] in [word[i] for i in entry[1]]:
          go = False
          break

      if go:

          # do not print words with low frequency (optional)
          #if data[word] <= 1e-7:
          #  continue

          wordList.append((data[word], word))

    wordListAll.append(wordList)



  #######################
  ###### see which combinations work
  #######################

  # New numbering system...
  #   Word on top is 0,
  #   and the vertical word on the left is 1.
  #   It keeps alternating between horizontal and vertical.
  #   If there are no vertical or horizontal words remaining,
  #   the word is still counted but is equal to ''.

  for i in range(n2):
    wordListAllNew[i*2] = wordListAll[i]
  for i in range(n1):
    wordListAllNew[i*2 + 1] = wordListAll[n2 + i]



  # recursive function to handle the variable number of for loops (number of loops depends on n1 and n2)
  def loop_recursive(w, n):
    global solCount     # this is the "returned" output of the function

    if n < fullNew:

      if wordListAllNew[n]:

        nHalf = n >> 1
        nHalf2 = (n+1) >> 1    # round up
        temp0 = (n+1)&1   # 1, 0, 1, 0, 1, 0, ...
        temp = "".join( [w[j][nHalf] for j in range(temp0, min(n, limits[temp0]), 2)] )

        for _,word in wordListAllNew[n]:
          if word[0:nHalf2] == temp :
            loop_recursive(w + [word], n + 1)

      else:
        loop_recursive(w + [''], n + 1)

    else:    # w is now a permutation that contains all (n1 + n2)/2 + 1 words and some ''

      # check counts
      letters = ''.join( [w[i] for i in range(0,fullNew,2)] )
      for i in set(letters):    # is this faster than:  i in letters
        if letters.count(i) != countsAll[i]:
          return

      solCount += 1




  solCount = 0

  loop_recursive([], 0)

  return solCount




#################################################
###### define function get_optimal_swaps(), which counts optimal swaps
#################################################


def get_optimal_swaps(greenMaskAll, lettersAll):

  # remove greens and other garbage from sol and lettersAll
  solution = list(sol)
  lettersTemp = list(lettersAll.lower())
  for i in range(len(greenMaskAll)):
    if greenMaskAll[i].isalpha():
      solution[i] = " "
      lettersTemp[i] = " "
  solution_string = "".join(solution).replace(' ', '').replace('\n', '')
  lettersAll_string = "".join(lettersTemp).replace(' ', '').replace('\n', '')

  counts = {}
  for i in solution_string:
    counts[i] = solution_string.count(i)

  solution_list = list(solution_string)
  letters_list = list(lettersAll_string)




  # Does swaps that make 2 new greens. This is optional but can GREATLY speed up the permutation part of the code.
  # I am not sure if this will always allow me to find the optimal solution!
  # Modifies: solution_list, letters_list, and counts
  def swapToTwoGreens():

    swaps = 0

    indices = []   # for marking indices that are already solved
    for i in range(len(solution_list)):
      for j in range(i+1, len(solution_list)):
        if i in indices or j in indices:   # I do not worry about preferentially trying to reduce the letters that have the most duplicates
          continue
        if solution_list[j] == letters_list[i] and solution_list[i] == letters_list[j]:
          indices.append(i)
          indices.append(j)
          swaps += 1

    indices.sort(reverse=True)
    for ind in indices:

      # update counts
      letter = solution_list[ind]
      if counts[letter] == 1:
        counts.pop(letter)
      else:
        counts[letter] -= 1

      # remove from lists
      solution_list.pop(ind)
      letters_list.pop(ind)

    return swaps



  # The following is optional but safe. It will speed up the permutation part of the code.
  # Does all swaps that swap a letter to its correct position if there is only one swappable instance of that letter
  # Modifies: solution_list, letters_list, and counts
  def swapSafe():

    swaps = 0

    toDelete = []   # for marking letters that are already solved
    for letter in counts:
      if counts[letter] == 1:

        i = solution_list.index(letter)
        j = letters_list.index(letter)

        if i!=j:
          swaps += 1
          letters_list[j] = letters_list[i]   # swap

        # remove the now green letter
        toDelete.append(letter)
        solution_list.pop(i)
        letters_list.pop(i)

    for letter in toDelete:
      counts.pop(letter)

    return swaps



  # If no duplicates, you just mindlessly move things to where they belong and you'll get the optimal number of swaps.
  # Functions for this, minSwapsToSort() and minSwapToMakeArraySame(), are below.
  # The above swapSafe() would also do it.
  #
  # With duplicates, the problem is harder...
  #   https://stackoverflow.com/questions/18292202/finding-the-minimum-number-of-swaps-to-convert-one-string-to-another-where-the
  #
  # Let's say there are 3 r's in solution_list. I will instead call them r0, r1, and r2 in solution_list.
  # Then I will make many versions of letters_list (called letters) that have permutations of r0, r1, and r2.
  # Then, I use the above no-duplicate code for each version of letters_list until I find an optimal one!
  # The coding of this is lengthy because there could be many different letters that are repeated.
  #
  # Modifies solution_list a bit by adding numbers after the letters then clobbering it.
  # Requires letters_list and counts.

  def permuteToGetMinSwaps():
    global bestSwaps    # what this function "returns"


    #   https://www.geeksforgeeks.org/minimum-number-swaps-required-sort-array/
    #  Duplicates are not allowed

    def minSwapsToSort(arr, n):
      ans = 0
      temp = arr.copy()
      h = {}
      temp.sort()
      for i in range(n):
          h[arr[i]] = i
      init = 0
      for i in range(n):
          if (arr[i] != temp[i]):
              ans += 1
              init = arr[i]
              new = h[temp[i]]
              arr[i], arr[new] = arr[new], arr[i]
              h[init] = new
              h[temp[i]] = i
      return ans



    #   https://www.geeksforgeeks.org/minimum-swaps-to-make-two-array-identical/

    def minSwapToMakeArraySame(a, b, n):
      mp = {}
      for i in range(n):
          mp[b[i]] = i
      for i in range(n):
          b[i] = mp[a[i]]
      return minSwapsToSort(b, n)



    permStarts = []
    for letter,count in counts.items():

      # I can't make a list of permutations themselves because they are generators
      #   that can only be used once.
      # I wonder if itertools' cycle(permutations()) would be faster??
      permStarts.append( [ letter+str(i) for i in range(count) ] )

      # modify solution_list
      ind = 0
      for i in range(count):
        for j in range(ind, len(solution_list)):
          if solution_list[j]==letter:
            ind = j
            break
        solution_list[ind] = letter + str(i)


    # Recursive function to handle the variable length of perms to loop through
    def loop_recursive_perms(p, n):
      global bestSwaps    # what this function "returns"

      if n < len(permStarts):
        for perm in permutations(permStarts[n]):
          loop_recursive_perms(p + [perm], n + 1)
  
      else:    # p is now a list of specific permutations

        # create letters from letters_list, but now with specific permutations
        letters = letters_list[:]
        for perm in p:
          ind = 0
          for i in range(len(perm)):

            # find the index, ind
            for j in range(ind, len(letters)):
              if letters[j]==perm[0][0]:
                ind = j
                break

            letters[ind] = perm[i]

        temp = letters[:]   # minSwapToMakeArraySame() clobbers letters[]
        swapsTemp = minSwapToMakeArraySame( solution_list, letters, len(solution_list) )

        if swapsTemp < bestSwaps:
          bestSwaps = swapsTemp


    bestSwaps = 1000000    # any large enough number
    loop_recursive_perms([], 0)





  ######## do everything!

  swaps = 0
  #swaps += swapToTwoGreens()
  swaps += swapSafe()

  permuteToGetMinSwaps()
  swaps += bestSwaps

  return swaps





#################################################
###### main code
#################################################


### Strategy 1: randomly shuffle everything
#  This strategy does not work well for large waffles that take a long time to solve without many greens

def strategy1():

  puzzle = list(sol)

  temp = list("".join(puzzle).replace('\n', ''))
  shuffle(temp)

  # put temp back into puzzle
  j=0
  for i,l in enumerate(puzzle):
    if l.isalpha():
      puzzle[i] = temp[j]
      j += 1

  return puzzle





### Strategy 2: randomly shuffle some things

greenMask = """

m..
...
...

""".strip().lower()    # warning: not checked for consistency with sol


def strategy2():

  puzzle = list(sol)

  temp = list(sol)
  for i in range(len(puzzle)-1,-1,-1):
    if greenMask[i].isalpha():
      temp.pop(i)

  temp = list("".join(temp).replace('\n', ''))
  shuffle(temp)

  # put temp back into puzzle
  j=0
  for i,l in enumerate(puzzle):
    if l.isalpha() and not greenMask[i].isalpha():
      puzzle[i] = temp[j]
      j += 1

  return puzzle




### Strategy 3: do random swaps until swap goal is met or exceeded (or until multiple solutions are found)

swapGoal = 15   # desired optimal swaps in puzzle

def strategy3():

  puzzle = list(sol)

  solCount = 1
  swaps = 0
  while solCount==1 and swaps < swapGoal:

    temp = list("".join(puzzle).replace('\n', ''))

    # do a random swap
    i1, i2 = sample(range(len(temp)), 2)
    temp[i1], temp[i2] = temp[i2], temp[i1]

    # put temp back into puzzle
    j=0
    for i,l in enumerate(puzzle):
      if l.isalpha():
        puzzle[i] = temp[j]
        j += 1

    greenMaskAll, lettersAll, trivial = colorPuzzle(puzzle)
    solCount = count_solutions(greenMaskAll, lettersAll)
    swaps = get_optimal_swaps(greenMaskAll, lettersAll)

    print(".")

  return puzzle




### make and analyze puzzle

trivial = True

while trivial or solCount!=1:

  puzzle = strategy3()    # choose strategy here

  greenMaskAll, lettersAll, trivial = colorPuzzle(puzzle)

  print()
  print(sol)
  print()
  print(greenMaskAll)   # print greens
  print("  There are", greenMaskAll.count('.'), "unsolved locations.")
  print()
  print(lettersAll)     # yellows are capitalized
  print()
  print("  Puzzle has a trivial move?", trivial)
  print()

  solCount = count_solutions(greenMaskAll, lettersAll)

  print("  solution count =", solCount)
  print()

  swaps = get_optimal_swaps(greenMaskAll, lettersAll)

  print("  optimal swaps =", swaps)
  print()


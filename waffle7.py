#!/usr/bin/env python3.11
#
# Find optimal (fewest swap) solutions for deluxe Waffle puzzles...
#   https://wafflegame.net/deluxe
#
# (c) 2023 Bradley Knockel

# For numbering the 8 words...
#   .0.0.0.
#   4 5 6 7
#   .1.1.1.
#   4 5 6 7
#   .2.2.2.
#   4 5 6 7
#   .3.3.3.


# First, download words_alpha.txt from
#   https://github.com/dwyl/english-words
with open('words_alpha.txt') as f:
  dataLong = f.read().split()

from itertools import permutations, product

# number of letters per word
nl = 7


data = []
for word in dataLong:
  if len(word)==nl:
    data.append(word)
dataLong.clear()  # free up RAM




#################################################
###### enter greenMaskAll and lettersAll for your specific Waffle puzzle
#################################################

# A '.' is a placeholder for when the letter is unknown.
# The spaces (' ') are for the holes in the waffle shape.
greenMaskAll = '''

..t.n..
. . . .
e.p.a.n
. p r .
e.i.e.t
. . . .
..g.t..

'''


# Capital letters mean yellow
# Warning: I never check for consistency with greenMaskAll
lettersAll = '''

UotsnTi
d N x D
eLpvadn
o p r s
eNieeet
e a E g
HlgEtIS

'''




#################################################
###### find the possibilities for each of the words
#################################################

greenMaskAll = greenMaskAll.strip().lower()
lettersAll = lettersAll.strip()

# make countsAll
countsAll = {}
goodLetters = lettersAll.replace(' ', '').replace('\n', '').lower()
for i in 'abcdefghijklmnopqrstuvwxyz':
  countsAll[i] = goodLetters.count(i)



wordListAll = []

for wordNum in range(nl+1):


    # take the correct slice
    if wordNum == 0:
      greenMask = greenMaskAll[0:nl]
      letters = lettersAll[0:nl]
    elif wordNum == 1:
      greenMask = greenMaskAll[2*nl+2:3*nl+2]
      letters = lettersAll[2*nl+2:3*nl+2]
    elif wordNum == 2:
      greenMask = greenMaskAll[4*nl+4:5*nl+4]
      letters = lettersAll[4*nl+4:5*nl+4]
    elif wordNum == 3:
      greenMask = greenMaskAll[6*nl+6:7*nl+6]
      letters = lettersAll[6*nl+6:7*nl+6]
    elif wordNum == 4:
      greenMask = greenMaskAll[0::nl+1]
      letters = lettersAll[0::nl+1]
    elif wordNum == 5:
      greenMask = greenMaskAll[2::nl+1]
      letters = lettersAll[2::nl+1]
    elif wordNum == 6:
      greenMask = greenMaskAll[4::nl+1]
      letters = lettersAll[4::nl+1]
    else:   #7
      greenMask = greenMaskAll[6::nl+1]
      letters = lettersAll[6::nl+1]


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

    # letterList[] = [ [letter, badLocations, countMin, countMax] , ...]
    letterList = []

    for i,j in enumerate(letters):   # j is a letter

        # is j the first yellow of that letter in the word?
        if j.isupper() and j not in letters[:i]:

          count = letters.count(j)  # yellows for now; greens added next
          for k in range(nl):
            if letters[k]==j.lower() and letters[k]==greenMask[k]:
              count += 1

          countEven = letters[0::2].count(j)   # yellows that could be part of another word instead
          # I assume that the game will prefer to make a non-shared spot yellow.
          # I am assuming that if both words have a yellow of the same letter not in the shared location,
          #   and the solution to each word only has one of that letter,
          #   then that letter would NOT be yellow if also in the shared location???
          # Does it matter what I assume???

          badLocations = [k for k in range(nl) if wordNoGreen.upper()[k] == j]

          if j.lower() in wordNoGreen:   # if there is a grey of the letter
            letterList.append([ j.lower(), badLocations, count - countEven, count ])
          else:
            letterList.append([ j.lower(), badLocations, count - countEven, counts[j.lower()] ])

        # is j is a green with no yellows of the same letter
        elif j==greenMask[i] and j.upper() not in letters:

          # we only need the first green in word
          if j in greenMask[:i]:
            continue

          count = 0
          for k in range(nl):
            if letters[k]==j and letters[k]==greenMask[k]:
              count += 1

          # we only care if we learn that there aren't any more of the letter in the word
          if j in wordNoGreen:
            letterList.append([ j, [], count, count ])




    #######################
    ###### search through all words in dictionary
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
        if word.count(entry[0]) < entry[2] or word.count(entry[0]) > entry[3] or entry[0] in [word[i] for i in entry[1]]:
          go = False
          break

      if go:
        wordList.append((1, word))   # frequency is unknown, so I put 1. Mathematica's (or WolframAlpha's ??) WordFrequencyData[] could add frequencies to words_alpha.txt


    wordListAll.append(wordList)


    '''
    #######################
    ###### sort matches according to frequency and print
    #######################

    print("\n word " + str(wordNum) + ":", greenMask, letters)
    #print(letterList)

    for entry in sorted(wordList, reverse=True):   # sorting is for when there is frequency data

      # do not print words with low frequency
      if entry[0] <= 1e-7:
        break

      print("  " + entry[1])
      #print("  " + entry[1], entry[0])
    '''



#################################################
###### see which combinations work to get solution
#################################################

solution = False

for _,w0 in wordListAll[0]:
  for _,w1 in wordListAll[1]:
    for _,w2 in wordListAll[2]:
      for _,w3 in wordListAll[3]:
        for _,w4 in wordListAll[4]:
          for _,w5 in wordListAll[5]:
            for _,w6 in wordListAll[6]:
              for _,w7 in wordListAll[7]:

                # check waffle shape
                if w0[0::2] != w4[0] + w5[0] + w6[0] + w7[0]:
                  continue
                if w1[0::2] != w4[2] + w5[2] + w6[2] + w7[2]:
                  continue
                if w2[0::2] != w4[4] + w5[4] + w6[4] + w7[4]:
                  continue
                if w3[0::2] != w4[6] + w5[6] + w6[6] + w7[6]:
                  continue

                # check counts
                letters = w0 + w1 + w2 + w3 + w4[1::2] + w5[1::2] + w6[1::2] + w7[1::2]
                works = True
                for i in 'abcdefghijklmnopqrstuvwxyz':
                  if letters.count(i) != countsAll[i]:
                    works = False
                    break
                if works:
                  print()
                  print(" ", w0)
                  print(" ", w4[1] + " " + w5[1] + " " + w6[1] + " " + w7[1])
                  print(" ", w1)
                  print(" ", w4[3] + " " + w5[3] + " " + w6[3] + " " + w7[3])
                  print(" ", w2)
                  print(" ", w4[5] + " " + w5[5] + " " + w6[5] + " " + w7[5])
                  print(" ", w3)
                  print("      ", w0, w1, w2, w3, w4, w5, w6, w7)
                  print()

                  solution = w0 + "\n" + w4[1] + " " + w5[1] + " " + w6[1] + " " + w7[1] + "\n" + w1 + "\n" + w4[3] + " " + w5[3] + " " + w6[3] + " " + w7[3] + "\n" + w2 + "\n" + w4[5] + " " + w5[5] + " " + w6[5] + " " + w7[5] + "\n" + w3


if not solution:
  exit()


#################################################
###### work out the optimal number of swaps to get to the solution
#################################################

# remove greens from solution and lettersAll and make them into lists
solution = list(solution)
lettersAll = list(lettersAll.lower())
waffleIndices = []   # used for printing the Waffle
for i in range(len(greenMaskAll)):
  if greenMaskAll[i].isalpha():
    solution[i] = " "
    lettersAll[i] = " "
  elif lettersAll[i].isalpha():
    waffleIndices.append(i)
solution_string = "".join(solution).replace(' ', '').replace('\n', '')
lettersAll_string = "".join(lettersAll).replace(' ', '').replace('\n', '')
solution = list(solution_string)
lettersAll = list(lettersAll_string)

blank = ".......\n. . . .\n.......\n. . . .\n.......\n. . . .\n......."

def printSwap(li, lj, i, j):
  li = li[0]
  lj = lj[0]
  i = waffleIndices[i]
  j = waffleIndices[j]
  if i<j:
    print( blank[:i] + li + blank[i+1:j] + lj + blank[j+1:] )
  else:
    print( blank[:j] + lj + blank[j+1:i] + li + blank[i+1:] )



#   https://www.geeksforgeeks.org/minimum-number-swaps-required-sort-array/

def minSwapsToSort(arr, n, mp, printBool):
    ans = 0
    temp = arr.copy()
    h = {}
    temp.sort()
    for i in range(n):
        h[arr[i]] = i
    init = 0
    if printBool:
      keyList = list(mp.keys())
      valueList = list(mp.values())
    for i in range(n):
        if (arr[i] != temp[i]):
            ans += 1
            init = arr[i]
            new = h[temp[i]]
            arr[i], arr[new] = arr[new], arr[i]
            if printBool:
              #print( [keyList[valueList.index(j)] for j in arr] )
              printSwap(keyList[valueList.index(arr[i])], keyList[valueList.index(arr[new])] , i, new)
              print()
            h[init] = new
            h[temp[i]] = i
    return ans



#   https://www.geeksforgeeks.org/minimum-swaps-to-make-two-array-identical/

def minSwapToMakeArraySame(a, b, n, printBool):
    mp = {}
    for i in range(n):
        mp[b[i]] = i
    for i in range(n):
        b[i] = mp[a[i]]
    return minSwapsToSort(b, n, mp, printBool)




# If no duplicates, you just mindlessly move things to where they belong and you'll get the optimal number of swaps.
# Functions for this are above.
#
# With duplicates, the problem is harder...
#   https://stackoverflow.com/questions/18292202/finding-the-minimum-number-of-swaps-to-convert-one-string-to-another-where-the
#
# Let's say there are 3 r's in solution. I will instead call them r0, r1, and r2 in solution.
# Then I will make many versions of lettersAll that have permutations of r0, r1, and r2...
# Then, I could use the above no-duplicate code for each version of lettersAll until I find the best one(s)!
# The coding of this will be more lengthy because there could be many different letters that are repeated.


counts = {}
for i in solution_string:
  counts[i] = solution_string.count(i)

perms = []
for letter,count in counts.items():
  perms.append(permutations( [ letter+str(i) for i in range(count) ] ))

  # modify solution[]
  ind = 0
  for i in range(count):
    for j in range(ind, len(solution)):
      if solution[j]==letter:
        ind = j
        break
    solution[ind] = letter + str(i)

prod = product(*perms)    # might take a lot of RAM ?!

bestSwaps = 1000
best = False
for p in prod:

  letters = lettersAll[:]
  for perm in p:
    ind = 0
    for i in range(len(perm)):
      for j in range(ind, len(letters)):
        if letters[j]==perm[0][0]:
          ind = j
          break
      letters[ind] = perm[i]

  temp = letters[:]   # minSwapToMakeArraySame() clobbers letters[]
  swaps = minSwapToMakeArraySame( solution, letters, len(solution), False )

  if swaps < bestSwaps:
    bestSwaps = swaps
    best = temp[:]

print("  At best, this will take", bestSwaps, "swaps.\n")

# print the swaps
minSwapToMakeArraySame( best,  solution, len(solution), True )


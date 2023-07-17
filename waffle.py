#!/usr/bin/env python3.11
#
# Find optimal (fewest swap) solutions for rectangular Waffle puzzles.
# Any odd word size greater than 1 is currently supported!
#
# Some examples of square puzzles online...
#   https://wafflegame.net/daily       5×5
#   https://wafflegame.net/deluxe      7×7
#   https://wordwaffle.org/unlimited   3×3 can be found here
# I cannot find any non-square rectangular puzzles online.
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


from itertools import permutations
# Note that product(*perms) where perms is a list of permutations could use a lot of RAM,
#   so I don't import product from itertools
# Instead, I do the product myself using a recursive function that loops over permutations.



#################################################
###### enter greenMaskAll and lettersAll for your specific Waffle puzzle
#################################################


##########   set greenMaskAll   ##########
### A '.' is a placeholder for when the letter is unknown.
### The spaces (' ') are for the holes in the waffle shape.


greenMaskAll = """

m..
. .
...

""".strip().lower()


greenMaskAll = """

w...f
. . r
..t..
. . .
t...e

""".strip().lower()


greenMaskAll = """

..t.n..
. . . .
e.p.a.n
. p r .
e.i.e.t
. . . .
..g.t..

""".strip().lower()


greenMaskAll = """

a...t
. . .
..t..
. c .
..ow.
. . .
s...s

""".strip().lower()



##########   set lettersAll   ##########
### Capital letters mean yellow.


lettersAll = """

mhA
h a
APS

""".strip()


lettersAll = """

wIHnf
h s r
zetIN
o R r
tfERe

""".strip()


lettersAll = """

UotsnTi
d N x D
eLpvadn
o p r s
eNieeet
e a E g
HlgEtIS

""".strip()


lettersAll = """

amUOt
a E r
nhtem
T c T
ToowL
S b i
sauEs

""".strip()




#################################################
###### prepare
#################################################


# get number of letters per word (n1 and n2)
n1 = len(greenMaskAll.split()[0])    # length of horizontal words
n2 = len(greenMaskAll.split('\n'))   # length of vertical words

if n1 < 3 or not n1&1 or n2 < 3 or not n2&1:
  print("  Error: only odd sizes greater than 1!")
  exit()


# useful
half = n2//2 + 1         # the number of horizontal words
full = (n1 + n2)//2 + 1   # the number of words
n1p = n1+1

# make blank board (eventually also used for printing swaps)
temp = "." * n1 + "\n" + ". " * (n1//2) + ".\n"
blank = temp * (n2//2) + "." * n1


# check for consistency
if len(greenMaskAll) != n2*(n1+1)-1:
  print("  Error: greenMaskAll has an invalid shape!")
  exit()
if len(greenMaskAll) != len(lettersAll):
  print("  Error: len(greenMaskAll) does not match len(lettersAll)!")
  exit()
for i in range(len(greenMaskAll)):
  if greenMaskAll[i].isalpha() and lettersAll[i] != greenMaskAll[i]:
    print("  Error: greenMaskAll does not match lettersAll!")
    exit()
for i in range(len(greenMaskAll)):   # check against structure of blank
  a =  blank[i] == " " and (greenMaskAll[i] != " " or lettersAll[i] != " ")
  b =  blank[i] == "\n" and (greenMaskAll[i] != "\n" or lettersAll[i] != "\n")
  c =  blank[i] == "." and not (greenMaskAll[i] == "." or greenMaskAll[i].isalpha())
  d =  blank[i] == "." and not lettersAll[i].isalpha()
  if a or b or c or d:
    print("  Error: invalid input!")
    exit()



dataLong = False



# load first word list
isFrequencyMap1 = False
if n1==5:   # this list is better, but only has 5-letter words

  import json
  isFrequencyMap1 = True
  with open('freq_map.json') as f:
    data1 = json.load(f)

else:

  with open('words_alpha.txt') as f:
    dataLong = f.read().split()

  data1 = []
  for word in dataLong:
    if len(word)==n1:
      data1.append(word)



# load 2nd word list

if n1==n2:
  data2 = data1
  isFrequencyMap2 = isFrequencyMap1
else:
  isFrequencyMap2 = False
  if n2==5:   # this list is better, but only has 5-letter words

    import json
    isFrequencyMap2 = True
    with open('freq_map.json') as f:
      data2 = json.load(f)

  else:

    if not dataLong:
      with open('words_alpha.txt') as f:
        dataLong = f.read().split()

    data2 = []
    for word in dataLong:
      if len(word)==n2:
        data2.append(word)


if dataLong:
  del dataLong   # try to free up RAM




# make countsAll
countsAll = {}
goodLetters = lettersAll.replace(' ', '').replace('\n', '').lower()
for i in 'abcdefghijklmnopqrstuvwxyz':
  countsAll[i] = goodLetters.count(i)



#################################################
###### find the possibilities for each of the words
#################################################

# For numbering the words, horizontal are first (word on top is 0),
#   then vertical (word on right is last).


wordListAll = []

for wordNum in range(full):


    # take the correct slice and get correct word list (data), number of letters (nl), and isFrequencyMap
    if wordNum < half:   # horizontal words
      start = 2 * wordNum * n1p
      greenMask = greenMaskAll[ start : start+n1 ]
      letters = lettersAll[ start : start+n1 ]
      data = data1
      nl = n1
      isFrequencyMap = isFrequencyMap1
    else:
      start = 2 * (wordNum - half)
      greenMask = greenMaskAll[ start :: n1p ]
      letters = lettersAll[ start :: n1p ]
      data = data2
      nl = n2
      isFrequencyMap = isFrequencyMap2


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

          # assume that the other word has not had all of its other letters solved
          countEven = letters[0::2].count(j)   # yellows that could be part of another word instead

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

          # we only care if we learn that there aren't any more of the letter in the word
          if j in wordNoGreen:

            count = 0
            for k in range(nl):
              if letters[k]==j and letters[k]==greenMask[k]:
                count += 1

            letterList.append([ j, [], count, count ])




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
        if word.count(entry[0]) < entry[2] or word.count(entry[0]) > entry[3] or entry[0] in [word[i] for i in entry[1]]:
          go = False
          break

      if go:
        if isFrequencyMap:

          # do not print words with low frequency (optional)
          #if data[word] <= 1e-7:
          #  continue

          wordList.append((data[word], word))

        else:
          # frequency is unknown, so I put 1. Mathematica's (or WolframAlpha's ??) WordFrequencyData[] could add frequencies to words_alpha.txt
          wordList.append((1, word))

    wordListAll.append(wordList)


    
    #######################
    ###### sort matches according to frequency and print
    #######################

    print("\n word " + str(wordNum) + ":   " + greenMask + "   " + letters)
    #print(letterList)

    for entry in wordList:   #sorted(wordList, reverse=True):   # sorting only does something when there is frequency data for both word lists

      print("  " + entry[1])
      #print("  " + entry[1], entry[0])
    



#################################################
###### see which combinations work to get solution
#################################################


# recursive function to handle the variable number of for loops (number of loops depends on n1 and n2)
def loop_recursive(w, n):
  global solution     # this is the "returned" output of the function

  if n < full:
      for _,word in wordListAll[n]:
        loop_recursive(w + [word], n + 1)

  else:    # w is now a permutation that contains all (n1 + n2)/2 + 1 words

      # check waffle shape
      for i in range(half):   # loop over the horizontal words
        if w[i][0::2] != "".join( [w[j][i*2] for j in range(half, full)] ) :
          return

      # check counts
      letters = ''.join( [w[i] if i<half else w[i][1::2] for i in range(full)] )
      for i in set(letters):    # is this faster than:  i in letters
        if letters.count(i) != countsAll[i]:
          return

      solution = ''.join(["\n"+" ".join( [w[j][i] for j in range(half, full)] )+"\n" if i&1 else w[i>>1] for i in range(n2)])  # oof

      print()
      print(solution)
      print("      " + " ".join([word for word in w]))
      print()


solution = False

loop_recursive([], 0)

if not solution:
  print("  No solution found!")
  exit()



#################################################
###### work out the optimal number of swaps to get to the solution
#################################################

# remove greens and other garbage from solution and lettersAll, and create waffleIndices[]
solution = list(solution)
lettersAll = list(lettersAll.lower())
waffleIndices = []   # used for printing swaps on the Waffle
for i in range(len(greenMaskAll)):
  if greenMaskAll[i].isalpha():
    solution[i] = " "
    lettersAll[i] = " "
  elif lettersAll[i].isalpha():
    waffleIndices.append(i)
solution_string = "".join(solution).replace(' ', '').replace('\n', '')
lettersAll_string = "".join(lettersAll).replace(' ', '').replace('\n', '')

counts = {}
for i in solution_string:
  counts[i] = solution_string.count(i)

solution_list = list(solution_string)
letters_list = list(lettersAll_string)



def printSwap(li, lj, i, j):
  li = li[0]
  lj = lj[0]
  i = waffleIndices[i]
  j = waffleIndices[j]
  if i<j:
    print( blank[:i] + li + blank[i+1:j] + lj + blank[j+1:] )
  else:
    print( blank[:j] + lj + blank[j+1:i] + li + blank[i+1:] )
  print()



# Does swaps that make 2 new greens. This is optional but can GREATLY speed up the permutation part of the code.
# I am not sure if this will always allow me to find the optimal solution!
# Modifies: solution_list, letters_list, counts, and waffleIndices
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
        printSwap(letters_list[i], letters_list[j], i, j)
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
    waffleIndices.pop(ind)

  return swaps



# The following is optional but safe. It will speed up the permutation part of the code.
# Does all swaps that swap a letter to its correct position if there is only one swappable instance of that letter
# Modifies: solution_list, letters_list, counts, and waffleIndices
def swapSafe():

  swaps = 0

  toDelete = []   # for marking letters that are already solved
  for letter in counts:
    if counts[letter] == 1:

      i = solution_list.index(letter)
      j = letters_list.index(letter)

      if i!=j:
        printSwap(letters_list[i], letters_list[j], i, j)
        swaps += 1
        letters_list[j] = letters_list[i]   # swap

      # remove the now green letter
      toDelete.append(letter)
      solution_list.pop(i)
      letters_list.pop(i)
      waffleIndices.pop(i)

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
  global bestSwaps, best    # these are what this function "returns"


  #   https://www.geeksforgeeks.org/minimum-number-swaps-required-sort-array/
  #  Duplicates are not allowed

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
              printSwap(keyList[valueList.index(arr[i])], keyList[valueList.index(arr[new])] , new, i)
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
    global bestSwaps, best    # these are what this function "returns"

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
      swapsTemp = minSwapToMakeArraySame( solution_list, letters, len(solution_list), False )

      if swapsTemp < bestSwaps:
        bestSwaps = swapsTemp
        best = temp[:]


  bestSwaps = 1000000    # any large enough number
  loop_recursive_perms([], 0)

  # print the bestSwaps swaps
  minSwapToMakeArraySame( best, solution_list, len(solution_list), True )




######## do everything!

swaps = 0
#swaps += swapToTwoGreens()
swaps += swapSafe()

permuteToGetMinSwaps()
swaps += bestSwaps

print("  At best, this took", swaps, "swaps.\n")


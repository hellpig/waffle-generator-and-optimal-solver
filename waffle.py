#!/usr/bin/env python3.11
#
# Find optimal (fewest swap) solutions for square Waffle puzzles...
#   https://wafflegame.net/daily       5×5
#   https://wafflegame.net/deluxe      7×7
#   https://wordwaffle.org/unlimited   3×3 can be found here
# Any odd word size greater than 1 is supported!
#
# First, download freq_map.json (5-letter-word frequencies) from
#   https://github.com/3b1b/videos/tree/master/_2022/wordle/data
# and/or download words_alpha.txt from
#   https://github.com/dwyl/english-words
# words_alpha.txt works for any size words. freq_map.json is better, but only has 5-letter words.
#
# (c) 2023 Bradley Knockel


from itertools import permutations, product



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




#################################################
###### prepare
#################################################


# get number of letters per word (nl)
nl = len(greenMaskAll.split()[0])

if nl < 3 and not nl&1:   # only odds greater than 1
  print("  Error: only 3×3, 5×5, 7×7, ... puzzles are currently supported!")
  exit()


# useful (assuming odd nl)
half = nl//2 + 1
full = nl + 1   # the number of words

# make blank board (eventually also used for printing swaps) (assume odd nl)
temp = "." * nl + "\n" + ". " * (nl//2) + ".\n"
blank = temp * (nl//2) + "." * nl


# check for consistency
if len(greenMaskAll) != nl*(nl+1)-1:
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
  dataLong.clear()  # free up RAM


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


    # take the correct slice
    if wordNum < half:   # horizontal words
      start = 2 * wordNum * full
      greenMask = greenMaskAll[ start : start+nl ]
      letters = lettersAll[ start : start+nl ]
    else:
      start = 2 * (wordNum - half)
      greenMask = greenMaskAll[ start :: full ]
      letters = lettersAll[ start :: full ]


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
        if isFrequencyMap:
          wordList.append((data[word], word))
        else:
          # frequency is unknown, so I put 1. Mathematica's (or WolframAlpha's ??) WordFrequencyData[] could add frequencies to words_alpha.txt
          wordList.append((1, word))

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


# recursive function to handle the variable number of for loops (number of loops depends on nl)
def loop_recursive(w, n):
  global solution

  if n < full:
      for _,word in wordListAll[n]:
        temp = w[:]
        temp.append(word)
        loop_recursive(temp, n + 1)

  else:

      # check waffle shape
      for i in range(half):   # loop over first half of the words
        if w[i][0::2] != "".join( [w[j][i*2] for j in range(half, full)] ) :
          return

      # check counts
      letters = ''.join( [w[i] if i<half else w[i][1::2] for i in range(full)] )
      for i in set(letters):    # is this faster than:  i in letters
        if letters.count(i) != countsAll[i]:
          return

      solution = ''.join(["\n"+" ".join( [w[j][i] for j in range(half, full)] )+"\n" if i&1 else w[i//2] for i in range(nl)])  # oof

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

# remove greens from solution and lettersAll and make them into lists
solution = list(solution)
lettersAll = list(lettersAll.lower())
waffleIndices = []   # used for printing on the Waffle
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

prod = product(*perms)    # might take a lot of RAM ?

bestSwaps = 1000
best = False
for p in prod:

  # create letters from lettersAll, but now with specific permutations
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


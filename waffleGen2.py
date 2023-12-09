#!/usr/bin/env python3.11
#
# Given a solution, make a rectangular Waffle puzzle.
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
# Enter the solution in the first section of the code.
# To change the waffle-making strategy, edit the final "main code" section.
# Keep rerunning the code until you get a puzzle you like!
#
# (c) 2023 Bradley Knockel


from random import shuffle, sample


# The following import is only needed if using permuteToGetMinSwaps(),
#   which is not the default.
# Note that product(*perms) where perms is a list of permutations could use a lot of RAM,
#   so I don't import product from itertools
# Instead, I do the product myself using a recursive function that loops over permutations.
#from itertools import permutations



#################################################
###### enter the solution
#################################################


### spaces (' ') are for the holes in the waffle shape.


sol = """

mas
a h
pah

""".strip().lower()


sol = """

whiff
r n r
intro
s e z
three

""".strip().lower()


sol = """

attuned
g o e e
explain
l p r o
evident
s n s e
sighted

""".strip().lower()


sol = """

about
r u a
total
i c e
shown
t m t
seems

""".strip().lower()


sol = """

artists
b o h e
outcome
u a w m
talents

""".strip().lower()





#################################################
###### prepare
#################################################


# get number of letters per word (n1 and n2)
n1 = len(sol.split()[0])    # length of horizontal words
n2 = len(sol.split('\n'))   # length of vertical words

if n1 < 3 or not n1&1 or n2 < 3 or not n2&1:
  print("  Error: only odd sizes greater than 1!")
  exit()


# useful
half = n2//2 + 1         # the number of horizontal words
halfVer = n1//2 + 1      # the number of vertical words
full = (n1 + n2)//2 + 1   # the number of words
n1p = n1+1

# useful
fullNew = max(half,halfVer) * 2
limits = [2*half, 2*halfVer]
wordListAllNew = [[] for i in range(fullNew)]

# make blank board
temp = "." * n1 + "\n" + ". " * (n1//2) + ".\n"
blank = temp * (n2//2) + "." * n1


# check for consistency
if len(sol) != n2*n1p-1:
  print("  Error: sol has an invalid shape!")
  exit()
for i in range(len(sol)):   # check against structure of blank
  a =  blank[i] == " " and sol[i] != " "
  b =  blank[i] == "\n" and sol[i] != "\n"
  c =  blank[i] == "." and not sol[i].isalpha()
  if a or b or c:
    print("  Error: invalid input!")
    exit()



dataLong = False   # do not change



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



del dataLong   # try to free up RAM




# make countsAll
countsAll = {}
goodLetters = sol.replace(' ', '').replace('\n', '').lower()
for i in 'abcdefghijklmnopqrstuvwxyz':
  countsAll[i] = goodLetters.count(i)



# make a list of words, where each word is a list of letters
wordsAll = []

for wordNum in range(full):

  if wordNum < half:   # horizontal words
    start = 2 * wordNum * n1p
    wordsAll.append( list( sol[ start : start+n1 ] ) )
  else:
    start = 2 * (wordNum - half)
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
      if not (i//n1p)&1:   # if in a horizontal word (when row is even)
        wordNum = (i//n1p)//2
        wordsLists[ wordNum ].remove(l)
      if not i&1:    # if in vertical word (when i is even)
        wordNum = half + (i%n1p)//2
        wordsLists[ wordNum ].remove(l)



  # find yellow candidates
  # Due to the various ways that yellows could be colored in, I am trying to add extra organization
  #   before choosing where any yellows go.
  yellowCandidates = []     # [ [ letter, index, words list, trivial? ], ... ]
  for i,l in enumerate(puzzle):
    if greenMaskAll[i].isalpha():
      continue

    countMatches = 0
    length = 0    # the max number of places the player might think that the yellow goes to
    words = []
    if not (i//n1p)&1:   # if in a horizontal word (when row is even)
      wordNum = (i//n1p)//2
      length += len(wordsLists[wordNum]) - 1
      countMatches += wordsLists[wordNum].count(l)
      words.append(wordNum)
    if not i&1:    # if in vertical word (when i is even)
      wordNum = half + (i%n1p)//2
      length += len(wordsLists[wordNum]) - 1
      countMatches += wordsLists[wordNum].count(l)
      words.append(wordNum)

    if countMatches:
      yellowCandidates.append( (l, i, words, length==1) )



  # put yellows in lettersAll by making yellow letters upper case
  lettersAll = puzzle[:]
  trivialPuzzle = False

  candidates =  [(a,b,c,d) for a,b,c,d in yellowCandidates if len(c)==2]   # shared locations
  candidates2 = [(a,b,c,d) for a,b,c,d in yellowCandidates if len(c)==1]   # non-shared locations

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

  for a,b,c,d in candidates2:
    w1 = c[0]  # wordNum
    if a in wordsLists[w1]:

      lettersAll[b] = lettersAll[b].upper()
      if d:
        trivialPuzzle = True

      wordsLists[w1].remove(a)

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
          # frequency is unknown, so I put 1
          wordList.append((1, word))

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

  for i in range(half):
    wordListAllNew[i*2] = wordListAll[i]
  for i in range(halfVer):
    wordListAllNew[i*2 + 1] = wordListAll[half + i]



  # recursive function to handle the variable number of for loops (number of loops depends on n1 and n2)
  def loop_recursive(w, n):
    global solCount     # this is the "returned" output of the function

    if n < fullNew:

      if wordListAllNew[n]:

        temp = (n//2)*2   # 0, 0, 2, 2, 4, 4, ...
        temp2 = (n+1)&1   # 1, 0, 1, 0, 1, 0, ...
        temp3 = "".join( [w[j][temp] for j in range(temp2, min(n, limits[temp2]), 2)] )

        for _,word in wordListAllNew[n]:
          if word[0:n:2] == temp3 :
            loop_recursive(w + [word], n + 1)

      else:
        loop_recursive(w + [''], n + 1)

    else:    # w is now a permutation that contains all (n1 + n2)/2 + 1 words and some ''

      # check counts
      letters = ''.join( [w[i][1::2] if i&1 else w[i] for i in range(fullNew)] )
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

    # cleanup a bit
    for i in range(len(letters_list)-1, -1, -1):
      if letters_list[i] == solution_list[i]:  # if puzzle equals solution
        if counts[letters_list[i]] == 1:
          counts.pop(letters_list[i])
        else:
          counts[letters_list[i]] -= 1
        letters_list.pop(i)
        solution_list.pop(i)

    return swaps



  '''
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
  '''



  # Requires letters_list and solution_list

  def findCyclesToGetMinSwaps():

    leng = len(letters_list)

    # the following is explicitly needed because Python's max() doesn't like empty lists
    if leng==0:
      return 0


    ### find and print all the cycles

    def loop_recursive_cycles(cyc, depth):
      # "globals": n, leng, cycle[], and cycles[]

      # did you find a cycle that has not yet been found?
      if cyc[-1][0]==cyc[0][1] and cyc not in cycles:
        cyclesGood.append(cyc[:])
        cycles.append(cyc[:])
        for c in range(depth-1):
            cyc.append(cyc.pop(0))  # cycle the cycle
            cycles.append(cyc[:])
        return

      if depth < leng-n:

        for j in zip(letters_list[n+1:], solution_list[n+1:]):

          if j[1] != cyc[-1][0] or j in cyc:
            continue

          loop_recursive_cycles(cyc + [j], depth+1)
    
    cycles = []      # to not collect repeats
    cyclesGood = []  # will list all the cycles

    for n,i in enumerate(zip(letters_list[:-1], solution_list[:-1])):
      loop_recursive_cycles([i],1)

    # sort by length to speed up later code a bit
    cyclesGood = sorted(cyclesGood, key=len)

    # optionally print cycles
    #for cyc in cyclesGood:
    #  print()
    #  print("".join([i[0] for i in cyc]))
    #  print("".join([i[1] for i in cyc]))



    ### go through cycles and fit them together in every possible way

    def loop_recursive_combine_cycles(cycList, currentSituation):
      # "globals": cycListAll[]

      # did you find a combination that has not yet been found?
      if len(currentSituation)==0 and cycList not in cycListAll:
        cycListAll.append(cycList[:])
        return

      index = cycList[-1] - 1
      for cyc in cyclesGood[cycList[-1]:]:   # allows repeats of the same cycle
        index += 1

        # trying to speed things up (only works if cyclesGood is sorted by length)
        if len(cyc) > len(currentSituation):
          break

        currentSituationNew = currentSituation[:]
        try:
          for j in cyc:
            currentSituationNew.remove(j)
        except:
          continue   # cyc could not be removed

        loop_recursive_combine_cycles(cycList + [index], currentSituationNew)

    cycListAll = []   # to collect combinations of cycles

    for i,cyc in enumerate(cyclesGood):

      # convert to a different data structure
      currentSituation = list(zip( letters_list, solution_list ))

      # remove cyc
      for j in cyc:
        currentSituation.remove(j)

      loop_recursive_combine_cycles([i], currentSituation)

    # optionally print
    #for l in cycListAll:
    #  print()
    #  print(l)
    #  print("swaps =", leng - len(l) )



    # each cycle takes its length minus 1 swaps
    return leng - len(max(cycListAll, key=len))






  ######## do everything!

  swaps = 0
  swaps += swapToTwoGreens()
  swaps += swapSafe()

  #permuteToGetMinSwaps()
  #swaps += bestSwaps
  swaps += findCyclesToGetMinSwaps()

  return swaps





#################################################
###### main code
#################################################


### Strategy 1: randomly shuffle everything
#  This strategy does not work well for large waffles that take a long time to solve without many greens

def strategy1():

  puzzle = list(sol)

  temp = list("".join(puzzle).replace(' ', '').replace('\n', ''))
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
. .
...

""".strip().lower()    # warning: not checked for consistency with sol


def strategy2():

  puzzle = list(sol)

  temp = list(sol)
  for i in range(len(puzzle)-1,-1,-1):
    if greenMask[i].isalpha():
      temp.pop(i)

  temp = list("".join(temp).replace(' ', '').replace('\n', ''))
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

    temp = list("".join(puzzle).replace(' ', '').replace('\n', ''))

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


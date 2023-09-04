# waffle-generator-and-optimal-solver
Waffle puzzles are basically 2D Wordle puzzles for which you must swap letters. I find optimal (fewest swap) solutions to waffles of various rectangular sizes! I can also generate waffles!

All the rectangular ones that I can find online are square. The puzzles...  
[https://wafflegame.net/daily](https://wafflegame.net/daily) is 5×5  
[https://wafflegame.net/deluxe](https://wafflegame.net/deluxe) is 7×7  
[https://wordwaffle.org/unlimited](https://wordwaffle.org/unlimited) has 3×3 Waffle puzzles


# waffle.py is the optimal solver

To run the code, enter the initial puzzle into the top section of the code in the format provided within the code. That is, you need to set two and only two variables. You will also need to download the word-list file(s) in the links specified at the top of the code. The solution and step-by-step optimal swaps will be output to a terminal (or, in Windows, PowerShell or whatever).

The word lengths must be an odd number larger than 1. Note that 5-letter words use a better word list, but the list only has 5-letter words. The word list used for other sizes has lowercase English words of all lengths.

Waffle puzzles are not super difficult by hand. Though, writing the code was a bit tricky (that is to say, fun!).

Trying to then minimize the number of swaps was most interesting. This is [trivial if there are no duplicates](https://www.geeksforgeeks.org/number-of-transpositions-in-a-permutation/) of initially-non-green letters (just put letters where they belong), but duplicates often occur. If duplicates occur in a puzzle, swapping the letters that do not have duplicates is also trivial (safely put them where they go at any time). For remaining duplicates, I brute force all permutations of where duplicates should go because [the problem is NP-hard](https://arxiv.org/abs/1011.1157). See comments in the code for more details on my technique.

My code has a call to swapToTwoGreens() that can greatly speed up the permutations. The idea is to swap two letters if they both become green after. Starting from the upper left then going right, it swaps the first pairs that work. I was not sure if this would affect my code's ability to find optimal swaps, so I did extensive experimental testing, and swapToTwoGreens() seemed to be safe, but I wanted a proof. I especially wanted a proof because the claim "a swap that creates no greens is always bad" is *not* true because, taking *abcd* as the correct order, *dcab* optimally has 3 swaps, and *cdab*, which is obtained from *dcab* after a single no-green-producing swap, optimally takes 2 swaps. However, "a swap that creates no greens can be required for the optimal score" is also *not* true because a swap mixing two cycles always makes a larger single cycle, and a no-green-producing swap within a cycle always splits the cycle into two, where cycles are defined [here](https://www.geeksforgeeks.org/minimum-number-swaps-required-sort-array/). Let's prove that it is always safe to swap to two new greens. With duplicates, there are many ways of drawing cycles that include all numbers. Let us consider only those that give optimal swaps. For the cycles that contain the swap-to-two-new-greens as a cycle, the swap is obviously safe. For the cycles that don't, the swap will merge two cycles into one but also will remove two letters (instead of just one letter) from that cycle, so the effects cancel.

Next steps...
* Other shapes? I believe the whole idea of a waffle is to have maximal shared letters given a word size without having parallel words "touch". A 3-letter word square waffle could be made with two words (it would be a plus sign), but two words do not have maximal shared letters so would be very boring (I suppose a yellow in the center spot would be a curiosity). I suppose that 4-letter words could make 4-word square waffles in various ways, and it would not be hard to modify my code to handle this, but I have never seen these. If I were to do another shape, it might be [this](https://wafflegame.net/royale), though I would think that a 5-letter-word by 7-letter-word rectangle, which my code can already solve, would be more interesting!


# waffleGen.py

I made waffleGen.py to generate all possible waffle solutions of any rectangular size.

**Reducing the size of a word list *greatly* helps runtime and is always crucial**. Without reducing the word list, nearly all printed puzzles are garbage because they have at least one ridiculously uncommon word. I suppose the user could always hand select the desired sublist then run the generator code!

If the length of a word list is not changed, the length of the word does not greatly affect runtime. This is because few scenarios make it past 3 or 4 words. Regardless of word size, word lists should be less than 1000 if you want to finish them in a reasonable amount of time. If you want to use multiple CPU cores, quickly modify my code so that each core could be assigned different starting words, keeping in mind that starting words with a starting letter that is a common starting letter in the word list will likely take longer to run.

If n1 and n2 are the number of letters per word, the number of words of length n1 in the waffle is (n2 + 1)/2, and the number of shared letters is (n2 + 1)(n1 + 1)/4. If num1 is the number of words in the n1 word list, and num2 is the number of words in the n2 word list, then, assuming that letters appear in a word independent of nearby letters, the number of puzzles found should be roughly...
$$\frac{num1^{\frac{n2 + 1}{2}} num2^{\frac{n1 + 1}{2}}}{2.01^{(n2 + 1)(n1 + 1)}}$$
Note that, for square waffles, the numerator is an approximation instead of using the permutation formula. The denominator arises because the probability that a valid waffle can be made from a permutation is 0.06124^(number of shared letters), and (1/0.06124)^(1/4) equals 2.01. In the case of square waffles, you should get less than this because then symmetric and repeated-word solutions are prevented.

Where did the 0.06124 come from? I first got [letter frequencies in the dictionary](https://www3.nd.edu/~busiforc/handouts/cryptography/letterfrequencies.html). I will assume that all word lists have the same frequencies and that the location of the letters in the word (odd vs. even letter location) makes no difference. By summing the squares of the frequencies, I get 0.06124.

My current interesting results for *square* waffles are...
* Because I have frequency data for 5-letter words, I can easily reduce the word list, which is a very successful strategy! With a list of 156 words (from a frequency cutoff of 0.0001), all 31 waffle solutions were printed within seconds! The prediction for the 31 seems to be 174, which is (156/66)^6, where the 66 is 2.01^6. If using the actual permutation formula instead of 156^6, the prediction becomes 158. Dividing by 2 to remove symmetric solutions gives 79, which is between 31 and 92, where 92 is the number of solutions that my code prints if words are allowed to be repeated within a puzzle. I would expect the prediction to be between 31 and 92 because the 31 does not include repeats, but, when including repeats, you can get more waffles than you should (as can be seen from the ratio of 92 to 31) because repeated words can fit together in a waffle shape with high probability.
* For 9-letter words, I found a [list of 215 common words](https://www.unscramblerer.com/common-nine-letter-words/). After making all of the words lowercase, in about half a minute, the search was completed and no puzzle solutions were found. I then found a [sublist of 1180 words](https://7esl.com/9-letter-words/), however the words are not exactly common. It finished running after over a day, but no puzzles were found.
* For 7-letter words, I found a [list of 1371 common words](https://github.com/powerlanguage/word-lists/blob/master/common-7-letter-words.txt). After making all of the words lowercase, many solutions were found after several minutes, though, with such a long list, running on a single core would take at least a week.
* Here is a good [list of 404 common 3-letter words](https://7esl.com/common-three-letter-words/#3_Letter_Words_with_Q). Though, I had to remove a couple 4-letter words and remove capitalization on the words with *q*, and I noticed that *que* is not an English word.
* Using the full 7-letter-word list, after many minutes, solutions do eventually start to print. After roughly an hour, solutions started to print for 9-letter words! Though some of the words were stupidly uncommon. The first to print was *aardvarks aaronical rabatting rabbanist nearabout vitiation chibinite rhinolite latinless sightless* followed shortly by *aardvarks aaronical rabatting rabbanist nearabout vitiation chilicote rhizopods lutanists sightsees*. Of course, neither search was any real progress through the entire search space.
* There are no 21-letter-or-larger-word waffles. After roughly an hour when I stopped the code, no puzzle solutions were found for 19-letter words or 17-letter words. The 19-letter words at least made significant progress through the search space, and, if I cared, I could have finished it.

I want to get frequency data for words of all lengths. Mathematica's (or WolframAlpha's??) WordFrequencyData[] could add frequencies to words_alpha.txt, but I don't have access to Mathematica. I then was talking with [https://github.com/CodingKraken](https://github.com/CodingKraken), and he gave me the idea to use the Python *wordfreq* module and use its word list file found at [https://github.com/rspeer/wordfreq/tree/master/wordfreq/data](https://github.com/rspeer/wordfreq/tree/master/wordfreq/data). Here is my code to make frequency lists of correct size...
```
from msgpack import unpackb 
from wordfreq import word_frequency
import json

# first, download file from https://github.com/rspeer/wordfreq/tree/master/wordfreq/data
with open("large_en.msgpack", 'rb') as f:
  dataLong = unpackb(f.read())

lengths = [3, 5, 7, 9]       # choose word lengths
freqCutoffs = [1E-5, 1E-5, 1E-6, 1E-6]   # set frequency cutoffs

data = [{} for i in range(len(lengths))]
for wordGroup in dataLong[1:]:
  for word in wordGroup:
    freq = word_frequency(word, 'en')
    if word.islower() and word.isalpha() and word.isascii():
      for j in range(len(lengths)):
        if len(word)==lengths[j] and freq > freqCutoffs[j]:
          data[j][word] = freq

for j in range(len(lengths)):
  print(lengths[j], len(data[j]))
  with open("words" + str(lengths[j]) + ".json", "w") as f:
    json.dump(data[j], f)
```
I believe you need at least Python 3.7 to run the above code since isascii() was introduced in 3.7. I was using 3.11. I haven't changed my 3 waffle files to use these word lists yet, but feel free to use the resulting .json files for even 5-letter words! Note that I exclusively use the above word lists in my 3 solidWaffle files.

Next steps...
* Maybe I could make the code faster by placing words in the hardest locations first. For example, if it is time to place a horizontal word, and the leftmost vertical word has the letter *z* in it, place the horizontal word where the *z* is (if possible). I am not convinced that this would even be faster.
* Insisting that a certain word be a pre-decided thing could be fun, and it probably wouldn't take much coding, though, for speed, you would want to place it first, which would make the coding more tricky (unless it is placed as the 0th word).


# waffleGen2.py

I wrote waffleGen2.py to take a solution and makes a puzzle by swapping the letters. It uses the same solver and swap counting algorithm as waffle.py (basically copied and pasted). Currently, it is a toolbox for you to edit the final "main code" section. You can select between strategies...
* completely shuffling all the letters, which, for large puzzles, can produce puzzles that take forever for the code to solve due to not having many greens (especially greens in shared locations)
* force certain locations to be green then shuffle all the letters
* keep doing random swaps until you get a certain number of optimal swaps or more (or until multiple solutions occur)
* write your own strategies!

The final puzzle should ideally not have trivial moves where a yellow letter has only one letter that it could swap with by only thinking about colors of letters (without even taking into account what the actual letters are). My code currently makes sure that there is one solution and that there are no immediate trivial swaps. The significant new code in waffleGen2.py is the colorPuzzle() function (besides what I copied from waffle.py), which colors the yellow letters after coloring all green letters.

A way to color yellow letters is, first, look at all non-green shared locations to try to color in every shared location we can. Once all shared locations are handled, fill in yellows in non-shared locations, but always count a shared yellow towards both words. This could be considered "hard mode", when the idea is to use the fewest possible non-shared yellows. "Easy mode" would be doing the non-shared locations first.

When coloring the *shared* locations, the order that the locations are considered can affect the number of solutions and the number of yellows (non-shared locations aren't an issue). Only the number of *shared* yellows can be affected by the coloring order of the shared yellows. To think about such things, we only need to think about a single letter—let's say, *n*—at a time because other letters being yellow cannot affect any *n* being yellow. The number of solutions could be affected because, for a horizontal word with a single *n* in its solution (and no green *n*s yet), *N-n--* and *n-N--*, where capital *N* means yellow, allow a different number of *n*s in the vertical words. The number of yellows can also be affected. In the following 2 puzzles, a • means the location of the *n* in the solution...
```
  N•N--        n•N--
  | | •   or   | | •
  N-•--        N-•--

  N•N        n•N
  • |   or   • |
  N-•        N-•
```
In either puzzle above, depending on color ordering, coloring all 3 *n*s can occur, but you could also only color the two *n*s not on the upper left. If this is something you care about, in "hard mode", I believe a good thing to do is: first color the shared locations that removes a letter from a single word (in "easy mode", do the ones that affect both words first). I suggest this strategy because I believe that more shared yellows makes the puzzle harder. It may be the case that all permutations of a letter on non-green shared locations must be considered to get the optimal most or least shared letters. The second 2D example above shows that it is likely that all permutations must be considered since each of the three *n*s would initially remove the *n* from two words. 

Perhaps, when doing the shared locations, the best choice is to aim for the minimum amount of yellows (prioritize the locations that remove the letter from both words). In a word with a single *n*, *N-N•-* is always a valid coloring, even if neither vertical word has an *n* (note that my code would never do this), but it is needlessly confusing (gross!). Perhaps extra yellows on shared locations are always needlessly confusing. In both of the 2D examples drawn above, the one with the least yellows is the easier puzzle and is the less gross puzzle. My coloring code prioritizes coloring shared locations that remove a letter from two words. I don't check all permutations, but I just start with coloring the yellows that remove a letter from two words.

Actually, I believe that minimum yellows is always the best choice. If I start adding non-shared *n*s to the examples above, some especially gross situations arise unless always going for minimum yellows. My code tries to color shared-locations that remove a letter from two words before coloring anything else yellow.

After doing the letters that remove from two words, I choose to do the non-shared locations before doing the rest of the shared locations (making the puzzle less gross and easier), but this would be very easy to change.

I was curious how [https://wafflegame.net/daily](https://wafflegame.net/daily) and [https://wordwaffle.org/unlimited](https://wordwaffle.org/unlimited) handle certain situations, so I did some limited testing.
* If the solution for a word has a single instance of a letter, but two of the squares—one shared and one not—have that letter (and the other word's solution does not contain that letter), the game did not prefer to make a shared letter yellow, and it also did not prefer to make a non-shared letter yellow. The game should either consistently choose to make the shared letter yellow or the non-shared letter yellow.
* If a shared letter is yellow and appears once in both words' solution, a duplicate of that letter wasn't yellow if in one of the words, but was yellow if in the other word. This might be thought to be a bug because the game should either consistently try to color the fewest possible non-shared letters yellow or consistently try to color the most possible non-shared letters yellow.
* Both online games seem to just color in the first yellow that can be made yellow and associating it with the first letter it can while using the normal left-to-right top-to-bottom order. For simplicity and runtime, I recommend such a strategy eventually (it certainly will eventually be necessary to decide between equivalent choices for non-shared locations), but I also recommend starting with either shared or non-shared locations.

Next steps...
* Prove whether or not a simple pre-determined coloring order (without exploring all permutations) for shared locations that remove from two words exists to make the puzzle have the fewest yellows. If so, consider coding it! Even if not, consider coding the permutations! Regardless, each letter can be done separately.


# "solid" waffles

I define "solid" waffle as those with no "holes". See the 3 files whose names start with *solid*. These files are nearly the same as the non-solid files. They use the words#.json file lists described above, though now word lengths can be even numbers.

For solidWaffleGen.py, the approximate number-of-puzzles formula now becomes...
$$\frac{num1^{n2} num2^{n1}}{16.33^{n1 n2}}$$

Square waffles should have a bit less (due to things like removing symmetric solutions). In general, the above prediction is over 10 times larger than what is observed! Perhaps this is due to the most common words favoring common letters less than general words. I wrote the following code to find out (only valid for square waffles)...
```
import json

file = "words5.json"
with open(file, 'rb') as f:
  data = json.load(f)

# get counts
count = 0
counts = [0 for i in range(26)]
for word in data:
  for letter in word:
    count += 1
    counts[ord(letter) - ord('a')] += 1

# print the sum of the squares of frequencies
sum = 0
for c in counts:
  sum += c**2

print(sum / count**2)  # chance that a random letter matches another random letter
```
I learn that, given my frequency cutoffs, 3-letter and 4-letter words have a more uniform distribution of letter frequencies (the chance of a random letter matching another random letter is less than 0.06), but 5-letter, 6-letter, and 7-letter words have certain letters be quite common.

For 4×5, the following are most of the few good puzzles...
```
draw
rare
idea
liar
loss

ages
draw
mate
idea
tent

cats
hurt
idea
liar
lots

odds
wrap
note
even
rest

caps
hurt
idea
list
dose

caps
hurt
idea
list
lose

caps
hurt
idea
list
loss
```

For 3×6, the following is most of the few good puzzles...
```
dog
era
far
end
age
ten
```
Here is a good 3×7...
```
its
net
see
one
far
age
red
```

Ignoring a word length of 2, this leaves 3×3, 3×4, 3×5, and 4×4.

There are no longer non-shared locations in puzzles.

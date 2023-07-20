# waffle-generator-and-optimal-solver
Waffle puzzles are basically 2D Wordle puzzles for which you must swap letters. I find optimal (fewest swap) solutions to waffles of various rectangular sizes! I can also generate waffles!

All the rectangular ones that I can find online are square. The puzzles...  
[https://wafflegame.net/daily](https://wafflegame.net/daily) is 5×5  
[https://wafflegame.net/deluxe](https://wafflegame.net/deluxe) is 7×7  
[https://wordwaffle.org/unlimited](https://wordwaffle.org/unlimited) has 3×3 Waffle puzzles


# waffle.py is the optimal solver

Waffle puzzles are not super difficult by hand. Though, writing the code was a bit tricky (that is to say, fun!).

Trying to then minimize the number of swaps was most interesting. This is trivial if there are no duplicates of initially-non-green letters, but duplicates often occur. I brute force all permutations in the case of duplicates. See comments in the code for more details.

My code has a commented-out call to swapToTwoGreens() that can greatly speed up the permutations. The idea is to swap two letters if they both become green after. Starting from the upper left then going right, it swaps the first pairs that work. I am not sure if this will affect my code's ability to find optimal swaps! I have done extensive experimental testing, and swapToTwoGreens() seems to be safe, but I would like a proof.

To run the code, enter the initial puzzle into the top section of the code in the format provided within the code. That is, you need to set two and only two variables. You will also need to download the word-list file(s) in the links specified at the top of the code. The solution and step-by-step optimal swaps will be output to a terminal (or, in Windows, PowerShell or whatever).

The word lengths must be an odd number larger than 1. Note that 5-letter words use a better word list, but the list only has 5-letter words. The word list used for other sizes has lowercase English words of all lengths.

Next steps...
* Other shapes? I believe the whole idea of a waffle is to have maximal shared letters given a word size without having parallel words "touch". A 3-letter word square waffle could be made with two words (it would be a plus sign), but two words do not have maximal shared letters so would be very boring (I suppose a yellow in the center spot would be a curiosity). I suppose that 4-letter words could make 4-word square waffles in various ways, and it would not be hard to modify my code to handle this, but I have never seen these. If I were to do another shape, it might be [this](https://wafflegame.net/royale), though I would think that a 5-letter-word by 7-letter-word rectangle, which my code can already solve, would be more interesting!


# waffleGen.py

I made waffleGen.py to generate all possible waffle solutions of any rectangular size.

**Reducing the size of a word list *greatly* helps runtime and is always crucial**. Without reducing the word list, nearly all printed puzzles are garbage because they have at least one ridiculously uncommon word. I suppose the user could always hand select the desired sublist then run the generator code!

If the length of a word list is not changed, the length of the word does not greatly affect runtime. This is because few scenarios make it past 3 or 4 words. Regardless of word size, word lists should be less than 1000 if you want to finish them in a reasonable amount of time. If you want to use multiple CPU cores, quickly modify my code so that each core could be assigned different starting words, keeping in mind that starting words with a starting letter that is a common starting letter in the word list will likely take longer to run.

If n1 and n2 are the number of letters per word, the number of words of length n1 in the waffle is (n2 + 1)/2, and the number of shared letters is (n2 + 1)(n1 + 1)/4. If num1 is the number of words in the n1 word list, and num2 is the number of words in the n2 word list, then the number of puzzles found should be roughly...
$$\frac{num1^{\frac{n2 + 1}{2}} num2^{\frac{n1 + 1}{2}}}{2.01^{(n2 + 1)(n1 + 1)}}$$
Note that I used approximations in the numerator instead of using the permutation formula. The denominator arises because the probability that a valid waffle can be made from a permutation is 0.06124^(number of shared letters), and (1/0.06124)^(1/4) equals 2.01. In the case of square waffles, you should get less than this because then symmetric and repeated-word solutions are prevented.

Where did the 0.06124 come from? I first got [letter frequencies in the dictionary](https://www3.nd.edu/~busiforc/handouts/cryptography/letterfrequencies.html). I will assume that all word lists have the same frequencies and that the location of the letters in the word (middle vs beginning vs end) makes no difference. By summing the squares of the frequencies, I get 0.06124.

My current interesting results for *square* waffles are...
* Because I have frequency data for 5-letter words, I can easily reduce the word list, which is a very successful strategy! With a list of 156 words (from a frequency cutoff of 0.0001), all 31 waffle solutions were printed within seconds! The prediction for the 31 seems to be 174, which is (156/66)^6, where the 66 is 2.01^6. If using the actual permutation formula instead of 156^6, the prediction becomes 158. Dividing by 2 to remove symmetric solutions gives 79, which is between 31 and 92, where 92 is the number of solutions that my code prints if words are allowed to be repeated within a puzzle. I would expect the prediction to be between 31 and 92 because the 31 does not include repeats, but, when including repeats, you can get more waffles than you should (as can be seen from the ratio of 92 to 31) because repeated words can fit together in a waffle shape with high probability.
* For 9-letter words, I found a [list of 215 common words](https://www.unscramblerer.com/common-nine-letter-words/). After making all of the words lowercase, in about half a minute, the search was completed and no puzzle solutions were found. I then found a [sublist of 1180 words](https://7esl.com/9-letter-words/), however the words are not exactly common. It finished running after over a day, but no puzzles were found.
* For 7-letter words, I found a [list of 1371 common words](https://github.com/powerlanguage/word-lists/blob/master/common-7-letter-words.txt). After making all of the words lowercase, many solutions were found after several minutes, though, with such a long list, running on a single core would take at least a week.
* Here is a good [list of 404 common 3-letter words](https://7esl.com/common-three-letter-words/#3_Letter_Words_with_Q). Though, I had to remove a couple 4-letter words and remove capitalization on the words with *q*, and I noticed that *que* is not an English word.
* Using the full 7-letter-word list, after many minutes, solutions do eventually start to print. After roughly an hour, solutions started to print for 9-letter words! Though some of the words were stupidly uncommon. The first to print was *aardvarks aaronical rabatting rabbanist nearabout vitiation chibinite rhinolite latinless sightless* followed shortly by *aardvarks aaronical rabatting rabbanist nearabout vitiation chilicote rhizopods lutanists sightsees*. Of course, neither search was any real progress through the entire search space.
* There are no 21-letter-or-larger-word waffles. After roughly an hour when I stopped the code, no puzzle solutions were found for 19-letter words or 17-letter words. The 19-letter words at least made significant progress through the search space, and, if I cared, I could have finished it.

Next steps...
* Get frequency data for words of all lengths. Mathematica's (or WolframAlpha's??) WordFrequencyData[] could add frequencies to words_alpha.txt, but I don't have access to Mathematica.
* Maybe I could make the code faster by placing words in the hardest locations first. For example, if it is time to place a horizontal word, and the leftmost vertical word has the letter *z* in it, place the horizontal word where the *z* is (if possible). I am not convinced that this would even be faster.


# waffleGen2.py

I wrote waffleGen2.py to take a solution and makes a puzzle by swapping the letters. It uses the same solver and swap counting algorithm as waffle.py. Currently, it is a toolbox for you to edit the final "main code" section. The only strategy I put in the code is just shuffling all the letters, which can produce puzzles that take forever for the code to solve due to not having many greens, so you should write your own strategies that have more greens, perhaps to shoot for a certain number of optimal swaps. You could just do one random(ish) swap at a time then check the optimal swaps until the desired optimal swaps is obtained, while also making sure that there is just the one solution. The final puzzle should ideally also not have obvious moves where a yellow letter has only one letter that it could swap with by only thinking about colors of letters (without even taking into account what the actual letters are). My code currently makes sure that there is one solution and that there are no trivial swaps. I first needed to figure out how to color the yellow letters after coloring all green letters.

I believe that the way to color yellow letters is, first, look at all non-green shared locations to try to color in every shared location we can. Once all shared locations are handled, fill in yellows in non-shared locations, but always count a shared yellow towards both words.

I was curious how [https://wafflegame.net/daily](https://wafflegame.net/daily) and [https://wordwaffle.org/unlimited](https://wordwaffle.org/unlimited) handle certain situations, so I did some limited testing.
* If the solution for a word has a single instance of a letter, but two of the squares—one shared and one not—have that letter (and the other word's solution does not contain that letter), the game did not prefer to make a shared letter yellow, and it also did not prefer to make a non-shared letter yellow. The game should either consistently choose to make the shared letter yellow or the non-shared letter yellow.
* If a shared letter is yellow and appears once in both words' solution, a duplicate of that letter wasn't yellow if in one of the words, but was yellow if in the other word. This might be thought to be a bug because the game should either consistently try to color the fewest possible non-shared letters yellow or consistently try to color the most possible non-shared letters yellow.
* Both online games seem to just color in the first yellow that can be made yellow and associating it with the first letter it can while using the normal left-to-right top-to-bottom order. For simplicity and runtime, I recommend such a strategy eventually, though I still recommend trying to start with shared locations.



# waffle-optimal-solver
Waffle puzzles are basically 2D Wordle puzzles for which you must swap letters. I find optimal (fewest swap) solutions to waffles of various sizes!

The puzzles...  
[https://wafflegame.net/daily](https://wafflegame.net/daily) is 5×5  
[https://wafflegame.net/deluxe](https://wafflegame.net/deluxe) is 7×7  
[https://wordwaffle.org/unlimited](https://wordwaffle.org/unlimited) has 3×3 Waffle puzzles

Waffle puzzles are not super difficult by hand. Though, writing the code was a bit tricky (that is to say, fun!).

Trying to then minimize the number of swaps was most interesting. This is trivial if there are no duplicates of initially-non-green letters, but duplicates often occur. I brute force all permutations in the case of duplicates. See comments in the code for more details.

My code has a commented-out section that can greatly speed up the permutations. The idea is to swap two letters if they both become green after. I am not sure if this will affect my codes ability to find optimal swaps!

To run the code, enter the initial puzzle into the top of the code in the format provided within the code. That is, you need to set two and only two variables. You will also need to download the word-list file(s) in the links specified at the top of the code. The solution and step-by-step optimal swaps will be output to a terminal (or, in Windows, PowerShell).

The word length of the square waffle must be an odd number larger than 1. Note that 5×5 waffles use a better word list, but the list only has 5-letter words. The word list used for other sizes has lowercase English words of all lengths.

Next steps...
* Other shapes? I believe the whole idea of a waffle is to have maximal shared letters given a word size without having parallel words "touch". A 3-letter word waffle could be made with two words (it would be a plus sign), but two words would be very boring (I suppose a yellow in the center spot would be a curiosity). I suppose that 4-letter words could make 4-word waffles in various ways, and it would not be hard to modify my code to handle this, but I have never seen these. A non-square rectangular waffle would be fun, but I have never seen these. If I were to do another shape, it might be [this](https://wafflegame.net/royale). I would think that a 5-letter word by 7-letter word rectangle would be more interesting, and generalizing my code to handle this would be easy, but I cannot find any of these puzzles.
* When solving the waffle, I currently do not reduce counts[] as much as I could, which could exponentially affect runtime when the code checks all combinations of possible words. Certain yellow letters in the waffle are guaranteed to not be in certain words, so counts[] could be reduced further. However, I do not believe that this is the speed bottleneck. If this speed does every become the bottleneck, I could also not generate every combination of possible words by checking for waffle compatibility when adding each word to the current combination list.


# waffleGen.py

I was wondering how many interesting 9-letters-per-word (10-lowercase-word) waffle solutions exist. Assuming that the chance that a letter in a word is the same as a letter in another word is 1/10 (not 1/26 since not all letters are equally frequent), I get the approximate result that we should expect there to be a waffle solution if the number of words in the list is larger than 1.78^(n+1), where n is the number of letters per word and 1.78 is 10^(1/4). To get the result, compare the number of permutations of the word list, which is approximately (number of words in the list)^(n+1), with the chances that a valid waffle can be made from that permutation, which is (1/10)^((n+1)^2/4), where (n+1)^2/4 is the number of shared squares in the waffle.

A number better than 1/10 can be found by [looking at letter frequencies in the dictionary](https://www3.nd.edu/~busiforc/handouts/cryptography/letterfrequencies.html). I will assume that all word lists have the same frequencies. By summing the squares of the frequencies, I get 0.06124, so 1.78 should actually be (1/0.06124)^(1/4), which is 2.01. Since 2.01^10 is 1076, there are most likely many 9-letter-word waffles!

I made waffleGen.py to generate all possible waffle solutions. Due to the nature of exponentially growing runtime, the code (1) spits out seemingly endless solutions for 3-letter or 5-letter words, (2) takes seemingly forever to find a single solution for longer words, or (3) quickly proves that there are no solutions for very long words.

My current interesting results are...
* Because I have frequency data for 5-letter words, I can reduce the word list, which is a very successful strategy! All waffle solutions are printed in a short amount of time! Regardless of word size, this strategy is crucial because, nearly all printed puzzles are garbage because they have at least one ridiculously uncommon word.
* There are no 21-letter-or-larger-word waffles. After roughly an hour, no puzzle solutions were found for 19-letter words or 17-letter words. The 19-letter words at least made significant progress through the search space, and, if I cared, I could have finished it.
* For 7-letter words, after many minutes, solutions do eventually start to print. After roughly an hour, solutions started to print for 9-letter words! Neither was any real progress through the entire search space.

Next steps...
* Generate non-square rectangular waffles. 3×5 or maybe 5×7 would be the way to go while removing low-frequency 5-letter words.
* Get frequency data for words of all lengths. Mathematica's (or WolframAlpha's??) WordFrequencyData[] could add frequencies to words_alpha.txt, but I don't have access to Mathematica.
* Write a new code that takes a solution and makes a puzzle by swapping the letters


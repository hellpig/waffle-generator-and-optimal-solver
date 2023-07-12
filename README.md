# waffle-optimal-solver
Waffle puzzles are basically 2D Wordle puzzles for which you must swap letters. I find optimal (fewest swap) solutions to waffles of various sizes!

The puzzles...  
[https://wafflegame.net/daily](https://wafflegame.net/daily) is 5×5  
[https://wafflegame.net/deluxe](https://wafflegame.net/deluxe) is 7×7  
[https://wordwaffle.org/unlimited](https://wordwaffle.org/unlimited) has 3×3 Waffle puzzles

Waffle puzzles are not super difficult by hand. Though, writing the code was a bit tricky (that is to say, fun!).

Trying to then minimize the number of swaps was most interesting. This is trivial if there are no duplicates of initially-non-green letters, but duplicates often occur. I just brute force all permutations in the case of duplicates. See comments in the code for more details.

To run the code, enter the initial puzzle into the top of the code in the format provided within the code. That is, you need to set two and only two variables. You will also need to download the word-list file(s) in the links specified at the top of the code. The solution and step-by-step optimal swaps will be output to a terminal (or, in Windows, PowerShell).

The word length of the square waffle must be an odd number larger than 1. Note that 5×5 waffles use a better word list, but the list only has 5-letter words. The word list used for other sizes has lowercase English words of all lengths.

Next steps...
* Other shapes? I believe the whole idea of a waffle is to have maximal shared letters given a word size without having parallel words "touch". A 3-letter word waffle could be made with two words (it would be a plus sign), but two words would be very boring (I suppose a yellow in the center spot would be a curiosity). I suppose that 4-letter words could make 4-word waffles in various ways, and it would not be hard to modify my code to handle this, but I have never seen these. A non-square rectangular waffle would be fun, but I have never seen these. If I were to do another shape, it might be [this](https://wafflegame.net/royale), though I would think that a 5-letter word by 7-letter word rectangle would be more interesting.
* When solving the waffle, I currently do not reduce the dictionary counts[] as much as I could, which could exponentially affect runtime when the code checks all combinations of possible words. Certain yellow letters in the waffle are guaranteed to not be in certain words, so counts[] could be reduced further.
* I wonder how many interesting 9-letters-per-word 10-lowercase-word waffle solutions exist? I might try to *generate* 9×9 puzzles. As for solving a 9×9 puzzle, for the final step of finding the optimal swaps, a ton of RAM might be required if there are many not-intially-green duplicates of the same letter (number of permutations is *n* factorial for each repeated letter). If so, I'm not sure exactly how itertools' permutations() and product() work, but, if either produces something with a lot of RAM instead of just a [generator](https://www.geeksforgeeks.org/generators-in-python/), I bet you could write your own functions that are generators?? Though runtime would likely also be an issue. However, I have a guess of a different strategy for finding optimal swaps. I believe that you can always safely (1) swap a letter to its correct position if there is only one swappable instance of that letter and (2) swap two letters if they both become green after. If this is true, this could be used before or perhaps even instead of trying all permutations.

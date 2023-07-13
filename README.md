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
* When solving the waffle, I currently do not reduce counts[] as much as I could, which could exponentially affect runtime when the code checks all combinations of possible words. Certain yellow letters in the waffle are guaranteed to not be in certain words, so counts[] could be reduced further. However, I do not believe that this is the speed bottleneck.
* I wonder how many interesting 9-letters-per-word 10-lowercase-word waffle solutions exist. Now that I have a solver, I might try to *generate* 9×9 puzzles or puzzles of any size. Maybe I could generate non-square rectangular waffles too!

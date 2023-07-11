# waffle-optimal-solver
Waffle puzzles are basically 2D Wordle puzzles for which you must swap letters. I find optimal (fewest swap) solutions to waffles of various sizes!

The puzzles...  
[https://wafflegame.net/daily](https://wafflegame.net/daily) is solved by waffle5.py  
[https://wafflegame.net/deluxe](https://wafflegame.net/deluxe) is solved by waffle7.py  
[https://wordwaffle.org/unlimited](https://wordwaffle.org/unlimited) has 3×3 Waffle puzzles, which are solved by waffle3.py

The three files are very similar. Running the *diff* command (or, on Windows, I am told that the *FC* command works) on them to see the specific differences. Note that waffle5.py uses a better word list, but the list only has 5-letter words. The word list used by waffle3.py and waffle7.py has lowercase English words of all lengths.

Waffle puzzles are not super difficult by hand. Though, writing the code was a bit tricky (that is to say, fun!).

What I found most interesting was trying to minimize the number of swaps. This is trivial if there are no duplicates of initially-non-green letters, but duplicates often occur. I just brute force all permutations in the case of duplicates. See comments in the code for more details.

To run the code, enter the initial puzzle into the top of the code in the format provided within the code. You will also need to download the word-list file in the link specified at the top of the code. The solution and step-by-step optimal swaps will be output to a terminal (or, in Windows, PowerShell).

I wonder how many interesting 9-letters-per-word 10-lowercase-word waffle solutions exist? Generalizing waffle7.py to waffle9.py is trivial. Just compare waffle3.py to waffle7.py to see how it can be done. For the final step of finding the optimal swaps, waffle9.py might require a ton of RAM if there are many not-intially-green duplicates of the same letter (number of permutations is *n* factorial for each repeated letter).

Next steps...
* If I merge the files into a single file, it could auto-detect the size of the puzzle then choose the correct word list and other things. This would make maintaining the code easier, but I don't really care about that for such a small project. If anything, I might try to automate more things in each of the files to reduce the differences between them.
* Other shapes? I believe the whole idea of a waffle is to have maximal shared letters given a word size without having parallel words "touch". A 3-letter word waffle could be made with two words (it would be a plus sign), but two words would be very boring (I suppose a yellow in the center spot would be a curiosity). I suppose that 4-letter words could make 4-word waffles in various ways, and it would not be hard to modify my code to handle this, but I have never seen these. A non-square rectangular waffle would be fun, but I have never seen these. If I were to do another shape, it would be [this](https://wafflegame.net/royale), though I would think that a 5-word by 7-word rectangle would be more interesting.
* I might try to generate puzzles for what a waffle9.py might try to solve.

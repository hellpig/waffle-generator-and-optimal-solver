# waffle-optimal-solver
Waffle puzzles are basically 2D Wordle puzzles for which you must swap letters. I find optimal (fewest swap) solutions to waffles of various sizes!

The puzzles...  
[https://wafflegame.net/daily](https://wafflegame.net/daily) is solved by waffle5.py  
[https://wafflegame.net/deluxe](https://wafflegame.net/deluxe) is solved by waffle7.py  
[https://wordwaffle.org/unlimited](https://wordwaffle.org/unlimited) has 3×3 Waffle puzzles, which are solved by waffle3.py

Waffle puzzles are not super difficult by hand, though writing the code was a bit tricky (that is to say, fun!).

What I found most interesting was trying to minimize the number of swaps. This is trivial if there are no duplicates of initially-non-green letters, but duplicates often occur. I just brute forced all permutations in the case of duplicates. See comments in the code for more details.

To run the code, enter the initial puzzle into the top of the code in the format provided within the code. You will also need to download the word-list file in the link specified at the top of the code. The solution and step-by-step optimal swaps will be output to a terminal (or, in Windows, PowerShell).

I wonder how many interesting 9-letters-per-word 10-lowercase-word waffles exist? Generalizing waffle7.py to waffle9.py is trivial. Just compare waffle3.py to waffle7.py to see how it can be done. Note that waffle5.py uses a better word list, but the list only has 5-letter words. The word list used by waffle3.py and waffle7.py has lowercase English words of all lengths.

This tetromino tiler will place every piece in every orientation until it
finds a solution, then it will tell the user what that solution is. If no
solution is found, it will tell the user that too.

My original naieve solution took 80 seconds on my laptop to find a solution
for a 6X8 board with OOI22TTLLPPP tetrominos. An improvement made was
implementing an undo function and making it so I didn't copy the board and
tetrominos at each recursion. Then I made it so that if one tetromino was
unable to be placed in a position, it wouldn't try the same type in that
spot. I implemented several versions of empty space checkers to make sure
that any cut off spaces are of a size that is divisible by 4, but even the
version that only checked one empty region and only checked it if the
tetromio laid touched one of the sides of the board, made the tests
significantly slower. So none of those are in the final program.

The biggest speedups came from my huristics however. I chose a ordering of
tetrominos to try the simplest pieces first. The rotations of each tetromino
were ordered by which ones took up the most space in the top row. By the time
I implemented these orderngs my 6X8 test was taking 20 seconds and afterwards
they were being done in about half a second.

To run my program:

cat <inputfile.txt> | python3 tetromino-tiler.py

or

python3 tetromino-tiler.py
and enter:
"number_of_rows_as_int number_of_cols_as_int
list_of_tetrominos_as_IOLPT25"

or

python3 tetromino-tiler.py <number_of_rows_as_int> <number_of_cols_as_int> <list_of_tetrominos> <number of tests>




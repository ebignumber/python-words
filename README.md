
# Python Words

## What is Python Words?

Word Finder is a game that is supposed to be like those word puzzle games on Google Play, only here, you play in a terminal, and you can create your own puzzles if you really wanted to.

## How do you start the game?

To play the game just go to the game directory and run the wordfinder.py file like you would any other python file.

## Dependencies

This game requires Python; I made this using Python 3.12.3, and it will likely work on other version, but I haven't tested Word Finder on any of them.

## How to play?

Once you run the wordfinder.py file you will be greeted with this screen:

    Do you want to play a custom level or select a numbered lever?
    c. Custom Level
    s. Sample Level

Type s, to play sample puzzles, and c if you want to play custom puzzles. After that, type a number or the name of the puzzle to play it.

Next, you will see a screen like this:

       #       
       #         
    #####        
     #  ##       
     ## #        
                
                
                
                
                
                
                
                
                
    Letters: ['O', 'G', 'E', '2D']
    Guess a word:

On the top of the screen, you will see the puzzle that you need to solve. Below that, you can see every letter that is used in the puzzle.

\* If you see a number on the left of the letter, that means there is at least one word left in the puzzle that has that many instances of that letter.

## How can I create a puzzle?

You have two ways of doing this. You can make a text file with the necessary data and put it in the Custom-Puzzles directory or use the puzzle creator named "puzzle-creator.py".

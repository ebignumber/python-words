
# Python Words

## What is Python Words?

Word Finder is a game that is supposed to be like those word puzzle games on Google Play, only here, you play in a terminal, and you can create your own puzzles if you really wanted to.

## How do you start the game?

To play the game just go to the game directory and run the wordfinder.py file like you would any other python file.

## Dependencies

This game requires Python; I made this using Python 3.12.3, and it will likely work on other version, but I haven't tested Word Finder on any of them.

## How to play?

Once you run the wordfinder.py file you will be greeted with this screen:

    1: Sample
    2: Custom
    Select a series you want to play:


you may not see the Custom option when you first use it, since this option only appears when you make a puzzle in that directory.

Next, you enter the puzzle number you want to play. This will lead you to a screen like this one:

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

Open a file named "puzzle-creator.py" and start work.

When you first start, you will be greeted by this screen:

    Type "help" for help

    puzzle_creator/Custom$ 

Here you type commands to make puzzles and write them to files. The data is stored in a series of strings in a text file once you save it.

## How are my puzzles stored?

sample puzzle data will look something like this:

    r:1:1:HAPPY d:2:0:PAY d:5:1:YAP r:5:2:APP

Here we can see that words, coordinates, and direction are shown. We can take the first string from here "r:1:1:HAPPY" and tell that this word is horizontal (r for right), has an x and a y coordinate of 1, and the word is "HAPPY"


import os
puzzle_creation = []
autodisplay = False

#Help string

help_string = '''
add. Syntax: add "direction":"x":"y":"word" | Adds a word to the puzzle

addword. Syntax: addword "word" | Adds a word to the puzzle at position 0,0 going right

autodisplay. Syntax: autodisplay | toggles the autodisplay setting

display. Syntax: display | displays the puzzle and the words in it.

exit. Syntax: exit. | exits the program

help. Syntax: help | prints this help

load Syntax: load "name" | loads a puzzle to edit

mv. Syntax: move "word" "x" "y" | moves a word in the puzzle

rm. Syntax: rm "word" | remove a word from the puzzle

reset. Syntax: reset | resets the puzzle and removes all words from it

rotate. Syntax: rotate "word" | rotates a word in the puzzle

save. Syntax: save "name" saves the puzzle with a name that doesn\'t contain whitespaces

shift. Syntax: shift "word" "x" "y" | moves a word by x and y coordinates
'''

#creates 15 by 15 block
def reset_list():
    global my_list
    my_list = []
    n = 15
    while n > 0:
        my_list.append([])
        x = 15
        while x > 0:
            my_list[15 - n].append(' ')
            x -= 1
        n -= 1
reset_list()

#Prints words to the my_list variable
def print_word_to_puzzle(opt, x, y, w):
    for index, i in enumerate(w):
        if opt == 'r':
            my_list[y][index + x] = i
        else:
            my_list[index + y][x] = i

#Displays the puzzle and gives details about it
def display_puzzle():
    print('\n_______________')
    for i in puzzle_creation:
        i = i.split(':')
        print_word_to_puzzle(i[0], int(i[1]), int(i[2]), i[3])
    n = 15
    while n > 0:
        print(f"{''.join(my_list[15 - n])}{15 - n}")
        n -= 1
    print('012345678901234')
    reset_list()
    print(f'words: {puzzle_creation}\n')

#Checks the word for issues, then, if successful, adds it to puzzle_creation variable
def add_word(word):
    word_test = word.split(':')
    if not len(word_test) == 4:
        print('You must input a 4 colon-separated values')
        return
    elif not word_test[0] in 'rd' or len(word_test[0]) != 1:
        print('The direction value must be either r or d')
        return
    try:
        int(word_test[1])
        int(word_test[2])
    except:
        print("x and y coordinates must be integers")
        return
    if int(word_test[1]) < 0 or int(word_test[1]) > 14:
        print("x coordinate must be between 0 and 14")
        return
    elif int(word_test[2]) < 0 or int(word_test[2]) > 14:
        print('y coordinate must be between 0 and 14')
    elif not word_test[3].isalpha():
        print('Your word can only contain letters in the English alphabet')
        return
    #removes word if it is out of bounds
    elif (len(word_test[3]) + int(word_test[1]) - 1 > 14 and word_test[0] == 'r') or (len(word_test[3]) + int(word_test[2]) - 1 > 14 and word_test[0] == 'd'):
        print(f'could not print {word_test[3]} in x coordinate {word_test[1]} and y coordinate {word_test[2]}\ntry adding it in a different direction or adding it to a different position')
        return
    #checks if the word is in the puzzle
    for i in puzzle_creation:
        i = i.split(':')
        if i[3] == word_test[3].upper():
            print('This word is already in the puzzle')
            return
    word_test[3] = word_test[3].upper()
    puzzle_creation.append(':'.join(word_test))

def move_word(word, x, y):
    try:
        int(x)
        int(y)
    except:
        print("x and y coordinates must be integers")
        return
    if int(x) < 0 or int(x) > 14:
        print("x coordinate must be between 0 and 14")
        return
    elif int(y) < 0 or int(y) > 14:
        print('y coordinate must be between 0 and 14')
        return
    for index, i in enumerate(puzzle_creation):
        i = i.split(':')
        if word.upper() == i[3]:
            #test if word is out of bounds if moved
            if (len(i[3]) + int(x) - 1 > 14 and i[0] == 'r') or (len(i[3]) + int(y) - 1 > 14 and i[0] == 'd'):
                print(f'Could not move {word}, it would go out of bounds')
                return
            #moves the word
            i[1] = x
            i[2] = y
            puzzle_creation[index] = ':'.join(i)
            return
    print(f'Could not find the word to move {word}')

def rotate_word(word):
    for index, i in enumerate(puzzle_creation):
        i = i.split(':')
        if word.upper() == i[3]:
            #test if word is out of bounds if rotated
            if (len(i[3]) + int(i[1]) - 1 > 14 and i[0] == 'd') or (len(i[3]) + int(i[2]) - 1 > 14 and i[0] == 'r'):
                print(f'Could not rotate {word}, it would go out of bounds')
                return
            #rotates the word
            if i[0] == 'r':
                i[0] = 'd'
            else:
                i[0] = 'r'
            puzzle_creation[index] = ':'.join(i)
            return
    print(f'Could not find the word to rotate {word}')



def remove_word(word):
    for index, i in enumerate(puzzle_creation):
        i = i.split(':')
        if word.upper() == i[3]:
            puzzle_creation.pop(index)
            return
    print(f'Could not find the word to {word}')

#Saves the puzzle with a name and offers to overwrite it if a puzzle with that name.  
def save_puzzle(name):
    try:
        with open(f'Custom-Puzzles{os.path.sep}{name}.txt', 'x') as f:
            f.write(' '.join(puzzle_creation))
            print(f'Successfully created {name}')
    except:
        overwrite = input('That puzzle already exists, would you like to overwrite it? y/yes\n')
        if overwrite.lower() == 'y':
            with open(f'Custom-Puzzles{os.path.sep}{name}.txt', 'w') as f:
                f.write(' '.join(puzzle_creation))
                print(f'Puzzle {name} was overwritten')

#Shifts a word coordinate by a certain amount
def shift_word(word, x, y):
    move_word(word, str(int(x) + int(x)), str(int(y) + int(y)))

#Loads a puzzle with a name
def load_puzzle(name):
    try:
        with open(f'Custom-Puzzles{os.path.sep}{name}.txt', 'r') as f:
            global puzzle_creation
            puzzle_creation = f.read().split(' ')
            #Removes \n from puzzles if present
            if puzzle_creation[-1].find('\n'):
                puzzle_creation[-1] = puzzle_creation[-1][0:-1]
    except:
        print(f'Puzzle {name} doesn\'t exist')

#Reads user command
def read_command(command):
    command = command.split(' ')
    match command[0]:
        case 'add':
            try:
                add_word(command[1])
            except:
                print('You need to add an argument to this command')
        case 'addword':
            try: add_word(f'r:0:0:{command[1]}')
            except: print('You need to add an argument to this command')
        case 'autodisplay':
            global autodisplay
            autodisplay = not autodisplay
        case 'display':
            display_puzzle()
        case 'exit':
            exit()
        case 'help':
            print(help_string)
        case 'load':
            try:
                load_puzzle(command[1])
            except:
                print('You need to add an argument to this command')
        case 'mv':
            try:
                move_word(command[1], command[2], command[3])
            except:
                print('You need to add 3 arguments to this command')
        case 'rm':
            remove_word(command[1])
        case 'reset':
            global puzzle_creation
            puzzle_creation = []
        case 'rotate':
            rotate_word(command[1])
        case 'save':
            try:
                save_puzzle(command[1])
            except:
                print('You need to add an argument to this command')
        case 'shift':
            try:
                shift_word(command[1], command[2], command[3])
            except:
                print('You need to add 3 arguments to this command')
        case _:
            print(f'Could not find command {command}')
  
  #runs display puzzle function if autodisplay is on
    if autodisplay:
        display_puzzle()


#Allows user to input commands
print('Type "help" for help')
while True:
    command = input("\npuzzle_creator$ ")
    read_command(command)

import os
puzzle_creation = []
autodisplay = False
series = "Custom"
puzzle_path = f'Puzzles{os.path.sep}{series}'
#Help string

help_string = '''
add. Syntax: add "direction":"x":"y":"word" | Adds a word to the puzzle

add_word. Syntax: add_word "word" | Adds a word to the puzzle at position 0,0 going right

autodisplay. Syntax: autodisplay | toggles the autodisplay setting

display. Syntax: display | displays the puzzle and the words in it.

delete. Syntax: delete "puzzle number" | deletes a puzzle in the series you are editing

exit. Syntax: exit. | exits the program

help. Syntax: help | prints this help

load Syntax: load "puzzle number" | loads a puzzle to edit

mv. Syntax: mv "word" "x" "y" | moves a word in the puzzle

rm. Syntax: rm "word" | remove a word from the puzzle

reset. Syntax: reset | resets the puzzle and removes all words from it

rotate. Syntax: rotate "word" | rotates a word in the puzzle

save. Syntax: save | saves the puzzle as the final end level

save_as. Syntax save "puzzle number" | overwrites a puzzle with the number given with the current puzzle 

series. Syntax series "series" | moves to a new series to edit puzzles in that series

shift. Syntax: shift "word" "x" "y" | moves a word by x and y coordinates
'''

#creates 15 by 15 block
def reset_list():
    global my_list
    my_list = []
    for i in range(15):
        my_list.append([])
        for j in range(15):
            my_list[i].append(' ')
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
    for j in range(15):
        print(f"{''.join(my_list[j])}{j}")
    print('012345678901234')
    reset_list()
    print(f'words: {puzzle_creation}\n')

def change_series(new_series):
    global series
    series = new_series
    global puzzle_path
    puzzle_path = f'Puzzles{os.path.sep}{series}'
    try: print(f'Changed series to {new_series}!\nPuzzles: {len(os.listdir(puzzle_path))}')
    except: print(f'NEW SERIES\n\nChanged series to {new_series}!\nPuzzles: 0')

def delete_puzzle(puzzle_number):
    try: puzzle_number = int(puzzle_number)
    except: print('the argument must be an integer')
    try: os.remove(f'{puzzle_path}{os.path.sep}{puzzle_number}.txt')
    except: 
        print("puzzle does not exist!")
        return
    puzzles = os.listdir(puzzle_path)
    n = puzzle_number
    while n <= len(puzzles):
        try: os.rename(f'{puzzle_path}{os.path.sep}{n + 1}.txt', f'{puzzle_path}{os.path.sep}{n}.txt')
        except: print(f"an error occurred: could not find puzzle {n + 1} in {series}\nPlease make sure that all the puzzles in the series are integers and that no numbers are missing") 
        n += 1

def move_puzzle(puzzle_number, location):
    try: 
        puzzle_number = int(puzzle_number)
        location = int(location)
    except: print('the arguments must be integers')
    try: os.rename(f'{puzzle_path}{os.path.sep}{puzzle_number}.txt', f'{puzzle_path}{os.path.sep}moving.txt')
    except: 
        print("puzzle does not exist!")
        return
    puzzles = os.listdir(puzzle_path)
    if location > len(puzzles):
        print("move puzzle to that location. location out of bounds")
    #Renames puzzles in front of puzzle
    i = puzzle_number
    while i < len(puzzles):
        try: os.rename(f'{puzzle_path}{os.path.sep}{i + 1}.txt', f'{puzzle_path}{os.path.sep}{i}.txt')
        except: print(f"an error occurred: could not find puzzle {i + 1} in {series}\nPlease make sure that all the puzzles in the series are integers and that no numbers are missing") 
        i += 1
    #Renames puzzles in front of new puzzle location
    n = len(puzzles) - 1
    while n >= location:
        print(os.listdir(puzzle_path))
        try: os.rename(f'{puzzle_path}{os.path.sep}{n}.txt', f'{puzzle_path}{os.path.sep}{n + 1}.txt')
        except: print(f"an error occurred: could not find puzzle {n} in {series}\nPlease make sure that all the puzzles in the series are integers and that no numbers are missing") 
        n -= 1
    try: os.rename(f'{puzzle_path}{os.path.sep}moving.txt', f'{puzzle_path}{os.path.sep}{location}.txt')
    except: print("ERROR")

    
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
def save_puzzle(puzzle_integer):
    try: os.listdir(puzzle_path)
    except: os.mkdir(puzzle_path)

    try:
        if len(os.listdir(puzzle_path)) + 1 < int(puzzle_integer):
            print("The integer is too big!, try just save instead")
            return
    except:
        print("the puzzle needs to be saved as an integer")
        return
    try:
        with open(f'{puzzle_path}{os.path.sep}{puzzle_integer}.txt', 'x') as f:
            f.write(' '.join(puzzle_creation))
            print(f'Successfully created {puzzle_integer}')
    except:
        overwrite = input('That puzzle already exists, would you like to overwrite it? y/yes\n')
        if overwrite.lower() == 'y':
            with open(f'{puzzle_path}{os.path.sep}{puzzle_integer}.txt', 'w') as f:
                f.write(' '.join(puzzle_creation))
                print(f'Puzzle {puzzle_integer} was overwritten')

#Shifts a word coordinate by a certain amount
def shift_word(word, x, y):
    for index, i in enumerate(puzzle_creation):
        i = i.split(':')
        if word.upper() == i[3]:
            move_word(word, str(int(x) + int(i[1])), str(int(y) + int(i[2])))
            break

#Loads a puzzle with a name
def load_puzzle(name):
    try:
        with open(f'Puzzles{os.path.sep}{series}{os.path.sep}{name}.txt', 'r') as f:
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
        case 'add_word':
            try: add_word(f'r:0:0:{command[1]}')
            except: print('You need to add an argument to this command')
        case 'autodisplay':
            global autodisplay
            autodisplay = not autodisplay
        case 'delete':
            try: delete_puzzle(command[1])
            except: print('this command needs 1 argument')
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
        case 'move_puzzle':
            try: move_puzzle(command[1], command[2])
            except: print('You need to add 2 arguments to this command')
        case 'rm':
            remove_word(command[1])
        case 'reset':
            global puzzle_creation
            puzzle_creation = []
        case 'rotate':
            rotate_word(command[1])
        case 'save':
            try:
                save_puzzle(len(os.listdir(puzzle_path)) + 1 )
            except:
                save_puzzle(1)
        case 'save_as':
            try:
                save_puzzle(command[1])
            except:
                print('could not save puzzle')
        case 'series':
            change_series(command[1])
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
    command = input(f"\npuzzle_creator/{series}$ ")
    read_command(command)

import os, json
os.chdir(os.path.dirname(__file__))

puzzle_creation = {}
autodisplay = False
series = "Custom"
puzzle_path = f'..{os.path.sep}Puzzles{os.path.sep}{series}{os.path.sep}'
#Help string

help_string = '''
add. Syntax: add "direction":"x":"y":"word" | Adds a word to the puzzle

aw. Syntax: aw "word" | Adds a word to the puzzle at position 0,0 going right

autodisplay. Syntax: autodisplay | toggles the autodisplay setting

display. Syntax: display opt("puzzle number") | displays the puzzle and the words in it.

delete. Syntax: delete "puzzle number" | deletes a puzzle in the series you are editing

exit. Syntax: exit. | exits the program

help. Syntax: help | prints this help

load. Syntax: load "puzzle number" | loads a puzzle to edit

move_puzzle. Syntax move_puzzle "puzzle_number" "location" | moves a puzzle to a different location in the series

mv. Syntax: mv "word" "x" "y" | moves a word in the puzzle

rm. Syntax: rm "word" | remove a word from the puzzle

reset. Syntax: reset | resets the puzzle and removes all words from it

rotate. Syntax: rotate "word" | rotates a word in the puzzle

save. Syntax: save | saves the puzzle as the final end level

save_as. Syntax save "puzzle number" | overwrites a puzzle with the number given with the current puzzle 

series. Syntax series opt("series") | moves to a new series to edit puzzles in that series

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
def display_puzzle(command):
    if len(command) == 1:
        puzzle = puzzle_creation
    else:
        try:
            with open(f'{puzzle_path}{command[1]}.json', 'r') as f:
                puzzle = json.load(f)
        except:
            print('Could not read that puzzle.')
            return

    words = []
    print('\n_______________')
    for i in list(puzzle.keys()):
        print_word_to_puzzle(puzzle[i]['direction'], puzzle[i]['x'], puzzle[i]['y'], i)
        words.append(i)
    for j in range(15):
        print(f"{''.join(my_list[j])}{j}")
    print('012345678901234')
    reset_list()
    print(f'words: {puzzle}\n')

    #Prints letters used in the puzzle
    letters = []
    mixed_words = ''.join(words)
    legal_letters = set(mixed_words)
    for i in legal_letters:
        occurrences = []
        for j in words:
            occurrences.append(j.count(i))
        if max(occurrences) == 1:
            letters.append(i)
        else:
            letters.append(f'{max(occurrences)}{i}')
    print(f"Letters: {letters}")

     
def change_series(new_series):
    global series
    series = new_series
    global puzzle_path
    puzzle_path = f'..{os.path.sep}Puzzles{os.path.sep}{series}{os.path.sep}'
    try: print(f'Changed series to {new_series}!\nPuzzles: {len(os.listdir(puzzle_path))}')
    except: print(f'NEW SERIES\n\nChanged series to {new_series}!\nPuzzles: 0')

def delete_puzzle(puzzle_number):
    try: puzzle_number = int(puzzle_number)
    except: print('the argument must be an integer')
    try: os.remove(f'{puzzle_path}{puzzle_number}.json'); print('Puzzle deleted, moving files...')
    except: 
        print("puzzle does not exist!")
        return
    puzzles = os.listdir(puzzle_path)
    n = puzzle_number
    while n <= len(puzzles):
        try: os.rename(f'{puzzle_path}{n + 1}.json', f'{puzzle_path}{n}.json'); print(f'moving {n + 1} to {n}')
        except: print(f"an error occurred: could not find puzzle {n + 1} in {series}\nPlease make sure that all the puzzles in the series are integers and that no numbers are missing"); return
        n += 1
    print("deletion successful")
    if len(os.listdir(puzzle_path)) == 0:
        os.rmdir(puzzle_path)


def move_puzzle(puzzle_number, location):
    puzzles = os.listdir(puzzle_path)
    try: 
        puzzle_number = int(puzzle_number)
        location = int(location)
        if location < 1:
            print('the location integer must be positive')
    except: print('the arguments must be integers')

    if location > len(puzzles):
        print("can't move puzzle to that location. location out of bounds")
        return

    try: os.rename(f'{puzzle_path}{puzzle_number}.json', f'{puzzle_path}moving.json')
    except: 
        print("puzzle does not exist!")
        return
    print('Moving Puzzles...')
    #Renames puzzles in front of puzzle
    i = puzzle_number
    while i < len(puzzles):
        try: os.rename(f'{puzzle_path}{i + 1}.json', f'{puzzle_path}{i}.json'); print(f'Moved puzzle {i + 1} to {i}')
        except: print(f"an error occurred: could not find puzzle {i + 1} in {series}\nPlease make sure that all the puzzles in the series are integers and that no numbers are missing") 
        i += 1
    #Renames puzzles in front of new puzzle location
    n = len(puzzles) - 1
    while n >= location:
        try: os.rename(f'{puzzle_path}{n}.json', f'{puzzle_path}{n + 1}.json'); print(f'Moved puzzle {n} to {n + 1}')
        except: print(f"an error occurred: could not find puzzle {n} in {series}\nPlease make sure that all the puzzles in the series are integers and that no numbers are missing") 
        n -= 1
    try: os.rename(f'{puzzle_path}moving.json', f'{puzzle_path}{location}.json'); print(f'Successfully moved {puzzle_number} to {location}')
    except: print("an error occurred changing the name of the moving.json file, you may need to do this manually")

    
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
    for i in list(puzzle_creation.keys()):
        if i == word_test[3].upper():
            print('This word is already in the puzzle')
            return
    word_test[3] = word_test[3].upper()
    puzzle_creation.__setitem__(word_test[3], {'direction':word_test[0], 'x':int(word_test[1]), 'y':int(word_test[2])})

def move_word(word, x, y):
    try:
       x =  int(x)
       y = int(y)
    except:
        print("x and y coordinates must be integers")
        return
    if x < 0 or x > 14:
        print("x coordinate must be between 0 and 14")
        return
    elif y < 0 or y > 14:
        print('y coordinate must be between 0 and 14')
        return

        #test if word is out of bounds if moved
    if (len(word) + x - 1 > 14 and puzzle_creation[word.upper()]['direction'] == 'r') or (len(word) + y - 1 > 14 and puzzle_creation[word.upper()]['direction'] == 'd'):
        print(f'Could not move {word}, it would go out of bounds')
        return
    #moves the word
    try:
        puzzle_creation[word.upper()]['x'] = x
        puzzle_creation[word.upper()]['y'] = y
    except:
        print(f'Could not find the word to move {word}')

def rotate_word(word):
    #test if word is out of bounds if rotated
    if (len(word) + puzzle_creation[word.upper()]['x'] - 1 > 14 and puzzle_creation[word.upper()]['direction'] == 'd') or (len(word) + puzzle_creation[word.upper()]['y'] - 1 > 14 and puzzle_creation[word.upper()]['direction'] == 'r'):
        print(f'Could not rotate {word}, it would go out of bounds')
        return
    #rotates the word
    if puzzle_creation[word.upper()]['direction'] == 'r':
        puzzle_creation[word.upper()]['direction'] = 'd'
    else:
        puzzle_creation[word.upper()]['direction'] = 'r'
    return
    #print(f'Could not find the word to rotate {word}')



def remove_word(word):
    try:
        puzzle_creation.pop(word.upper())
        return
    except:
        print(f'Could not find the word to {word}')

#Saves the puzzle with a name and offers to overwrite it if a puzzle with that name.  
def save_puzzle(puzzle_integer):
    try: os.listdir(puzzle_path)
    except: os.mkdir(puzzle_path)

    try:
        if len(os.listdir(puzzle_path)) + 1 < int(puzzle_integer):
            print("The integer is too big!, try just 'save' instead")
            return
        elif int(puzzle_integer) < 1:
            print("The integer is too small!, try just 'save' instead")
            return
    except:
        print("the puzzle needs to be saved as an integer")
        return
    try:
        with open(f'{puzzle_path}{puzzle_integer}.json', 'x') as f:
            json.dump(puzzle_creation, f, indent=4)
            print(f'Successfully created {puzzle_integer}')
    except:
        overwrite = input('That puzzle already exists, would you like to overwrite it? y/yes\n')
        if overwrite.lower() == 'y':
            with open(f'{puzzle_path}{puzzle_integer}.json', 'w') as f:
                json.dump(puzzle_creation, f, indent=4)
                print(f'Puzzle {puzzle_integer} was overwritten')

#Shifts a word coordinate by a certain amount
def shift_word(word, x, y):
    move_word(word, str(int(x) + puzzle_creation[word.upper()]['x']), str(int(y) + puzzle_creation[word.upper()]['y']))

def shift_all(x, y):
    try: x = int(x); y = int(y)
    except: print('x and y must be integers'); return
    for i in list(puzzle_creation.keys()):
        if (len(puzzle_creation[i]) + x + puzzle_creation[i]['x'] - 1 > 14 and puzzle_creation[i]['direction'] == 'r') or (len(puzzle_creation[i]) + y + puzzle_creation[i]['y'] - 1 > 14 and puzzle_creation[i]['direction'] == 'd') or (x + puzzle_creation[i]['x'] < 0 and puzzle_creation[i]['direction'] == 'r') or (y + puzzle_creation[i]['y'] < 0 and puzzle_creation[i]['direction'] == 'd'):
            print(f'Could not shift word "{i}". That word must be move before running the command')
            return
    for i in list(puzzle_creation.keys()):
        shift_word(i, str(x), str(y))
    return

#Loads a puzzle with a name
def load_puzzle(name):
    try:
        with open(f'{puzzle_path}{name}.json', 'r') as f:
            global puzzle_creation
            puzzle_creation = json.load(f)
            #Removes \n from puzzles if present
            print(f"loaded {name}")
    except:
        print(f'Puzzle {name} doesn\'t exist')


#Reads user command
def read_command(command):
    global puzzle_creation
    command = command.split(' ')
    match command[0]:
        case 'add':
            try:
                add_word(command[1])
            except:
                print('You need to add an argument to this command')
        case 'aw':
            try: add_word(f'r:0:0:{command[1]}')
            except: print('You need to add an argument to this command')
        case 'autodisplay':
            global autodisplay
            autodisplay = not autodisplay
        case 'delete':
            try: delete_puzzle(command[1])
            except: print('this command needs 1 argument')
        case 'display':
            display_puzzle(command)
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
            if len(command) >= 2: remove_word(command[1])
            else: print('You need to add 2 arguments to this command')
        case 'reset':
            puzzle_creation = []
        case 'rotate':
            try: rotate_word(command[1])
            except: print('You need to add 1 argument to this command')
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
            if len(command) == 1:
                change_series(series)
            else:
                change_series(command[1])
        case 'shift':
            try:
                shift_word(command[1], command[2], command[3])
            except:
                print('You need to add 3 arguments to this command')
        case 'shift_all':
            try:
                shift_all(command[1], command[2])
            except:
                print('You need to add 2 arguments to this command')
        case _:
            print(f'Could not find command "{command[0]}"')
  
  #runs display puzzle function if autodisplay is on
    if autodisplay:
        display_puzzle(['display'])


#Allows user to input commands
print('Type "help" for help')
while True:
    command = input(f"\npuzzle_creator/{series} $ ")
    read_command(command)

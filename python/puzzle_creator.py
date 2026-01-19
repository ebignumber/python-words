import os; import json
os.chdir(os.path.dirname(__file__))

class State:
    def __init__(self, puzzle, message, selected, series):
        self.puzzle = puzzle
        self.message = message
        self.selected = selected
        self.series = series
    def get_puzzle_path(s, series):
        return f'..{os.path.sep}Puzzles{os.path.sep}{series}{os.path.sep}'

#Displays the puzzle and gives details about it
def display_puzzle(puzzle):
    displayed_puzzle = ''
    def print_selected_word_to_puzzle(opt, x, y, w):
        for index, i in enumerate(w):
            if opt == 'r':
                display[y][index + x] = f'\033[31m{i}\033[0m'
            else:
                display[index + y][x] = f'\033[31m{i}\033[0m'



    def print_word_to_puzzle(opt, x, y, w):
        for index, i in enumerate(w):
            if opt == 'r':
                display[y][index + x] = i
            else:
                display[index + y][x] = i



    display = [[' ' for _ in range(15)] for _ in range(15)]
    words = []
    displayed_puzzle += '_______________'
    for word in list(puzzle.keys()):
        if word == user_state.selected:
            print_selected_word_to_puzzle(puzzle[word]['direction'], puzzle[word]['x'], puzzle[word]['y'], word)
        else:
            print_word_to_puzzle(puzzle[word]['direction'], puzzle[word]['x'], puzzle[word]['y'], word)
        words.append(word)
    for j in range(15):
        displayed_puzzle += f"\n{''.join(display[j])}{j}"
    displayed_puzzle += '\n012345678901234'
    displayed_puzzle += f'\nwords: {user_state.puzzle}\n'

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
    displayed_puzzle += f"\nLetters: {letters}\n"
    return displayed_puzzle

def add_word(word):
    user_state.puzzle.__setitem__(word.upper(), {'direction':'r', 'x':0, 'y':0})

def remove_word(word):
    if user_state.selected == word.upper():
        user_state.selected = word.upper()
    try:
        user_state.puzzle.pop(word.upper())
        return
    except:
        user_state.message = f'Could not find the word {word} to remove'



def select_word(word):
    if not word.upper() in user_state.puzzle:
        return
    user_state.selected = word.upper() 

def save_puzzle(puzzle_integer):
    puzzle_path = user_state.get_puzzle_path(user_state.series)
    print(puzzle_path)
    try: os.listdir(puzzle_path)
    except: 
        if puzzle_integer == 1:
            os.mkdir(puzzle_path)

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
            json.dump(user_state.puzzle, f, indent=4)
            user_state.message = f'Successfully created {puzzle_integer}'
    except:
        with open(f'{puzzle_path}{puzzle_integer}.json', 'r') as f:
            display_puzzle(json.load(f))
        overwrite = input('Are you sure you want to overwrite this puzzle? y/yes\n')
        if overwrite.lower() == 'y':
            with open(f'{puzzle_path}{puzzle_integer}.json', 'w') as f:
                json.dump(user_state.puzzle, f, indent=4)
                print(f'Puzzle {puzzle_integer} was overwritten')

def load_puzzle(name):
    puzzle_path = user_state.get_puzzle_path(user_state.series)
    try:
        with open(f'{puzzle_path}{name}.json', 'r') as f:
            user_state.puzzle = json.load(f)
            user_state.message = f"loaded {name}"
            user_state.selected = ''
    except:
        user_state.message = f'Puzzle {name} doesn\'t exist'

def move_puzzle(puzzle_number, location):
    puzzle_path = user_state.get_puzzle_path(user_state.series)
    puzzles = os.listdir(puzzle_path)
    try: 
        puzzle_number = int(puzzle_number)
        location = int(location)
        if location < 1:
            print('the location integer must be positive')
    except: print('the arguments must be integers')

    if location > len(puzzles):
        user_state.message = "can't move puzzle to that location. location out of bounds"
        return

    try: os.rename(f'{puzzle_path}{puzzle_number}.json', f'{puzzle_path}moving.json')
    except: 
        user_state.message = f"puzzle {puzzle_number} does not exist!"
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



def move_word(word, x, y):
    if not user_state.selected:
        user_state.message = "Cannot move word. Word not selected"
        return
    try:
       x =  int(x)
       y = int(y)
    except:
        print("x and y coordinates must be integers")
        return
    #test if word is out of bounds if moved
    word_x = user_state.puzzle[user_state.selected]['x']
    word_y = user_state.puzzle[user_state.selected]['y']
    word_direction = user_state.puzzle[word.upper()]['direction']
    OUT_OF_BOUNDS = (len(word) + x + word_x - 1 > 14 and word_direction == 'r') or (len(word) + y + word_y - 1 > 14 and word_direction == 'd') or (x + word_x < 0 or x + word_x > 14) or (y + word_y < 0 or y + word_y > 14)
    print(len(word) + x + word_x - 1)
    if OUT_OF_BOUNDS:
        print(f'Could not move {word}, it would go out of bounds')
        return
    #moves the word
    try:
        user_state.puzzle[word.upper()]['x'] = user_state.puzzle[word.upper()]['x'] + x
        user_state.puzzle[word.upper()]['y'] = user_state.puzzle[word.upper()]['y'] + y
    except:
        print(f'Could not find the word to move {word}')

def rotate_word(word):
    word_x = user_state.puzzle[word.upper()]['x']
    word_y = user_state.puzzle[word.upper()]['y']
    word_direction = user_state.puzzle[word.upper()]['direction']

    #test if word is out of bounds if rotated
    if (len(word) + word_x - 1 > 14 and word_direction == 'd') or (len(word) + word_y - 1 > 14 and word_direction == 'r'):
        user_state.message = f'Could not rotate {word}, it would go out of bounds'
        return
    #rotates the word
    if user_state.puzzle[word.upper()]['direction'] == 'r':
        user_state.puzzle[word.upper()]['direction'] = 'd'
    else:
        user_state.puzzle[word.upper()]['direction'] = 'r'
    return
 

def delete_puzzle(puzzle_number):
    puzzle_path = user_state.get_puzzle_path(user_state.series)
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

def view_series(series):
    puzzle_path = user_state.get_puzzle_path(user_state.series)
    try: os.listdir(puzzle_path)
    except: user_state.message = "This series doesn't have any puzzles in it!"; return
    number_of_puzzles_in_series = len(os.listdir(puzzle_path))
    report = f'Levels in {series}\n\nNumber of puzzles: {number_of_puzzles_in_series}\n\n'
    for puzzle in range(number_of_puzzles_in_series):
        with open(f'{puzzle_path}{puzzle + 1}.json', 'r') as f:
            report += f"Level {puzzle + 1}\n\n{display_puzzle(json.load(f))}\n"
    os.system(f'echo "{report}" | more' if os.name == 'nt' else f'echo "{report}" | less')





def read_input(user_input):
    multiplier = user_input[0]
    try:
        multiplier = int(multiplier)
    except:
        multiplier = 1
    if len(user_input) > 2:
        return
    match user_input[-1]:
    #WORD COMMANDS
        case 'a':
            word = input("What word do you want to add? ")
            if len(word) > 15:
                user_state.message = "Word must be less than 16 characters long!"
                return
            add_word(word)
            select_word(word)
        case 'd':
            word = input("What word do you want to delete? ")
            if not word.upper() in user_state.puzzle:
                user_state.message = f"Can't delete {word}. word not in puzzle"
                return
            remove_word(word)
        case 's':
            word = input("Select a word ")
            if not word.upper() in user_state.puzzle:
                user_state.message = f"Can't select {word}. word not in puzzle"
                return
            select_word(word)
    #MOVEMENT COMMANDS
        case 'h':
            move_word(user_state.selected, -1 * multiplier, 0)
        case 'j':
            move_word(user_state.selected, 0, 1 * multiplier)
        case 'k':
            move_word(user_state.selected, 0, -1 * multiplier)
        case 'l':
            move_word(user_state.selected, 1 * multiplier, 0)
        case 'r':
            rotate_word(user_state.selected)
    #SERIES COMMANDS 
        case 'c':
            user_state.series = input("Enter the name of a series you want to create/edit: ")
        case 'o':
            puzzle_integer = input('Enter a puzzle number to load: ')
            load_puzzle(puzzle_integer)
        case 'q':
            exit()
        case 'v':
            view_series(user_state.series)
        case 'w':
            try:
                save_puzzle(len(os.listdir(user_state.get_puzzle_path(user_state.series))) + 1)
            except:
                save_puzzle(1)
        case 'W':
            try: requested_integer = int(input("Enter a puzzle number to overwrite: "))
            except: user_state.message = "Not a number"; return
            save_puzzle(requested_integer)
        case 'x':
            puzzle_integer = input("What puzzle do you want to delete?: ")
            delete_puzzle(puzzle_integer)
        case 'm':
            try: puzzle_integer = int(input('Where puzzle do you want to move?: '))
            except: user_state.message = "Not a number"; return
            try: location = int(input('Where do you want to move the puzzle? :'))
            except: user_state.message = "Not a number"; return
            move_puzzle(puzzle_integer, location)
        case '?':
            os.system('more ..\\docs\\creating-puzzles.txt' if os.name == 'nt' else 'less ../docs/creating-puzzles.txt')
        case _:
            user_state.message = "Invalid Input"


#Allows user to input commands
user_state = State({}, 'Welcome to Python Words! Type "?" for help', '', 'Custom')
while True:
    os.system('cls' if os.name == 'nt' else 'clear')
    print(display_puzzle(user_state.puzzle))
    print(f"SERIES: {user_state.series}")
    print(f"{user_state.message}\n\n")
    user_input = input()
    if user_input:
        read_input(user_input)

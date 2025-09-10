import os
has_played_a_round = False

#reads input as 'n' or 'c' from player
while True:
    if not has_played_a_round:
        print('Do you want to play a custom level or select a numbered lever?\nc. Custom Level\ns. Sample Level\n')
        response = input('')
    if response in 'sc' and response.isalpha() and len(response) == 1:
        break
    else: print('Invalid Response')


#Select the puzzle
def select_puzzle():
    global puzzle_number

    #reads puzzle_number
    if response == 's' and not has_played_a_round:
        while True:
            try:
                puzzle_number = int(input('Enter a puzzle number: '))
                if puzzle_number < 1 or puzzle_number > 10:
                    puzzle_number = input('Level Number must be between 1 and 10')
                else:
                    global c_or_n
                    c_or_n = 'Puzzles'
                    break
            except:
                print('not a number')
    elif response == 's' and has_played_a_round:
        puzzle_number += 1
    else:
        while True:
            if response == 'c':
                try:
                    puzzle_number = input('Enter the name of your puzzle: ')
                    with open(f'Custom-Puzzles{os.path.sep}{puzzle_number}.txt', 'r') as f:
                        c_or_n = 'Custom-Puzzles'
                        break
                except:
                    print(f'Puzzle {puzzle_number} not found!')
                    exit()

select_puzzle()
#converts puzzle to a list of lists
def empty_puzzle_list():
    global puzzle_list
    puzzle_list = []
    n = 225
    while n > 0:
        if n % 15 == 0:
            puzzle_list.append([' '])
        puzzle_list[(225 - n) // 15].append(' ')
        n -= 1
empty_puzzle_list()

#adds words to the puzzle and collects them in an list to guess
def add_word_to_puzzle(opt, x, y, w, word_found):
    for index, i in enumerate(w):
        if word_found == False:
            if opt == 'r':
                puzzle_list[y][index + x] = '#'
            else:
                puzzle_list[index + y][x] = '#'
        else:
            if opt == 'r':
                puzzle_list[y][index + x] = i
            else:
                puzzle_list[index + y][x] = i
      
    n = 15
    while n > 0:
        n -= 1

#Gets new puzzle to play
def get_puzzle():
    with open(f'{c_or_n}{os.path.sep}{puzzle_number}.txt', 'r') as f:
        global puzzle_data
        puzzle_data = f.read()
        puzzle_data = puzzle_data.split(' ')
        if puzzle_data[-1].find('\n') != -1:
            puzzle_data[-1] = puzzle_data[-1][0:-1]
    global word_list
    word_list = []
    for data in puzzle_data:
        data = data.split(':')
        word_list.append(data[3])
        add_word_to_puzzle(data[0], int(data[1]), int(data[2]), data[3], False)

get_puzzle()

#updates the puzzle to add the puzzle
found_words = []
def update_puzzle(word):
    searching_word = puzzle_data[word_list.index(word)]
    result = searching_word.split(':')
    add_word_to_puzzle(result[0], int(result[1]), int(result[2]), result[3], True)
    found_words.append(word)
    puzzle_data.pop(word_list.index(word))
    word_list.pop(word_list.index(word))

#Displays the puzzle
def display_puzzle(puzzle):
    n = 15
    while n > 0:
        print(''.join(puzzle[15 - n]))
        n -= 1

#Adds the letters that are used in the puzzle
def collect_legal_letters(list):
    letters = []
    list = ''.join(list)
    legal_letters = set(list)
    for i in legal_letters:
        ocurrences = []
        for j in word_list:
            ocurrences.append(j.count(i))
        if max(ocurrences) == 1:
            letters.append(i)
        else:
            letters.append(f'{max(ocurrences)}{i}')
    print(f"Letters: {letters}")
            
#Tries to find the guessed word in the list of words 
def guess_word():
    guess = input('Guess a word:\n').upper()
    print('\n')
    if guess in found_words:
        print('Word Already Guessed')
    elif guess in word_list:
        update_puzzle(guess)
        print('Word Found')
    else:
        print('Word Not Found')

#Plays the game
def play_game():
    global current_puzzle
    current_puzzle = puzzle_list
    while len(word_list) != 0:
        display_puzzle(current_puzzle)
        collect_legal_letters(word_list)
        guess_word()
    display_puzzle(current_puzzle)
    print(f'You completed puzzle {puzzle_number}!')

#The loop calling the other functions
while True:
    play_game()
    yes_or_no = input('Would you like to play the next level? n/no')
    if yes_or_no == 'n':
        break
    else:
        has_played_a_round = True
        select_puzzle()
        empty_puzzle_list()
        get_puzzle()
        found_words.clear()

# This a finished hangman game that works entirely in the command line.

HANGMAN_ASCII_ART = """  _    _                                         
 | |  | |                                        
 | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __  
 |  __  |/ _` | '_ \ / _` | '_ ` _ \ / _` | '_ \ 
 | |  | | (_| | | | | (_| | | | | | | (_| | | | |
 |_|  |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                      __/ |                      
                     |___/"""

HANGMAN_PHOTOS = {
    0: "x-------x",
    1: "x-------x\n|\n|\n|\n|\n|",
    2: "x-------x\n|       |\n|       0\n|\n|\n|",
    3: "x-------x\n|       |\n|       0\n|       |\n|\n|",
    4: "x-------x\n|       |\n|       0\n|      /|\\\n|\n|",
    5: "x-------x\n|       |\n|       0\n|      /|\\\n|      /\n|",
    6: "x-------x\n|       |\n|       0\n|      /|\\\n|      / \\\n|"
}

MAX_TRIES = 6


def choose_word(file_path, index):
    file = open(file_path, "r")
    strings = file.read().split(' ')
    words_amount = len(set(strings))
    print(strings)
    res = (words_amount, strings[(index - 1) % words_amount])
    return res


def show_hidden_word(hidden_word, old_letters_guessed):
    res = ' '.join(hidden_word)
    for c in hidden_word:
        if c not in old_letters_guessed:
            res = res.replace(c, '_')
    return res


def check_win(hidden_word, old_letters_guessed):
    for c in list(dict.fromkeys(hidden_word)):
        if c not in old_letters_guessed:
            return False
    return True


def check_valid_input(letter_guessed, old_guesses):
    if len(letter_guessed) != 1:
        return False
    if not letter_guessed.isalpha():
        return False
    if letter_guessed in old_guesses:
        return False
    return True


def try_update_letter_guessed(letter_guessed, old_letters_guessed):
    letter_guessed = letter_guessed.lower()
    if not check_valid_input(letter_guessed, old_letters_guessed):
        print('X')
        if len(old_letters_guessed) > 0:
            old_keys = list(dict.fromkeys(old_letters_guessed))
            res = ""
            for c in old_keys:
                if len(res) > 0:
                    res = res + ' -> '
                res = res + str(c)
            print(res)
        return False
    old_letters_guessed.append(letter_guessed)
    return True


def print_open_screen():
    print(HANGMAN_ASCII_ART)
    print(MAX_TRIES)


print_open_screen()
current_file_path = input("Please enter the path where your words file is: ")
current_index = int(input("Please enter the index of the word inside the file: "))
current_hidden_word = choose_word(current_file_path, current_index)[1]

triedLetters = []
currentTries = 0
won = False

print(HANGMAN_PHOTOS[currentTries])
print(show_hidden_word(current_hidden_word, triedLetters))

while currentTries < MAX_TRIES and not won:
    letter = input("Please enter a letter: ")
    if try_update_letter_guessed(letter, triedLetters):
        print(show_hidden_word(current_hidden_word, triedLetters))
        if letter not in current_hidden_word:
            currentTries += 1
            print("):")
            print(HANGMAN_PHOTOS[currentTries])
        else:
            won = check_win(current_hidden_word, triedLetters)

if won:
    print("WIN")
else:
    print("LOSE")

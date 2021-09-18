import random


class HangManGame:
    FILE_PATH = ".\\files\\words.txt"
    GAME_LOST = 1
    GAME_WON = 2
    SUCCESS = 3

    ERROR_RANGE = range(11,16)
    UNKNOWN_ERROR = 10
    NO_INPUT_ERROR = 11
    LONG_INPUT_ERROR = 12
    NOT_LETTER_INPUT_ERROR = 13
    LETTER_ALREADY_GUESSED = 14
    GAME_NOT_RUNNING_ERROR = 15

    STARTING_TRIES_LEFT = 6

    def get_error_message(error_number=UNKNOWN_ERROR):
        if error_number not in HangManGame.ERROR_RANGE:
            return "Unknown error occurred."
        if error_number == HangManGame.NO_INPUT_ERROR:
            return "You need to type a letter in the input box."
        if error_number == HangManGame.LONG_INPUT_ERROR:
            return "You can only type exactly one letter and nothing more."
        if error_number == HangManGame.NOT_LETTER_INPUT_ERROR:
            return "You can only type letters and no other character."
        if error_number == HangManGame.LETTER_ALREADY_GUESSED:
            return "The letter you typed was already guessed earlier."
        if error_number == HangManGame.GAME_NOT_RUNNING_ERROR:
            return "Game is finished."


    def init_game(self, hidden_word="", hidden_index=0):
        self.current_tries_left = HangManGame.STARTING_TRIES_LEFT
        if hidden_word != "" and hidden_word.isalpha():
            self.current_hidden_word = hidden_word
        elif hidden_index > 0:
            self.current_hidden_word = HangManGame.choose_indexed_word(hidden_index)
        else:
            self.current_hidden_word = HangManGame.choose_random_word()
        self.current_hidden_word = self.current_hidden_word.lower()
        self.letters_guessed = []
        self.is_game_running = True

    def choose_random_word():
        file = open(FILE_PATH, "r")
        strings = file.read().split(' ')
        return strings[random.randrange(0, len(strings) - 1)]

    def choose_indexed_word(index):
        file = open(HangManGame.FILE_PATH, "r")
        strings = file.read().split(' ')
        return strings[(index - 1) % len(strings)]

    def __init__(self, hidden_word="", hidden_index=-1):
        self.current_tries_left = 0
        self.current_hidden_word = None
        self.letters_guessed = []
        self.init_game(hidden_word=hidden_word, hidden_index=hidden_index)

    def choose_random_word():
        file = open(HangManGame.FILE_PATH, "r")
        strings = file.read().split(' ')
        return strings[random.randrange(0, len(strings) - 1)]

    def show_hidden_word(self):
        res = ' '.join(self.current_hidden_word)
        for c in self.current_hidden_word:
            if c not in self.letters_guessed:
                res = res.replace(c, '_')
        return res

    def check_win(self):
        for c in list(dict.fromkeys(self.current_hidden_word)):
            if c not in self.letters_guessed:
                return False
        return True

    def try_update_letter_guessed(self, letter_guessed):
        if not self.is_game_running:
            return HangManGame.GAME_NOT_RUNNING_ERROR

        if len(letter_guessed) < 1:
            return HangManGame.NO_INPUT_ERROR

        if len(letter_guessed) > 1:
            return HangManGame.LONG_INPUT_ERROR

        if not letter_guessed.isalpha():
            return HangManGame.NOT_LETTER_INPUT_ERROR

        letter_guessed = letter_guessed.lower()
        if letter_guessed in self.letters_guessed:
            return HangManGame.LETTER_ALREADY_GUESSED

        self.letters_guessed.append(letter_guessed)
        if letter_guessed not in self.current_hidden_word:
            self.current_tries_left -= 1
            if self.current_tries_left == 0:
                self.is_game_running = False
                return HangManGame.GAME_LOST

        if self.check_win():
            self.is_game_running = False
            return HangManGame.GAME_WON

        return HangManGame.SUCCESS

    def guessed_letters(self):
        return ', '.join(self.letters_guessed)

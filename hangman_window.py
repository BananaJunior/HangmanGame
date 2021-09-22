from tkinter import messagebox

from PIL import ImageTk, Image
from hangman_game import *


class HangmanWindow:
    DEF_FONT = ("Ariel", 16)
    INDEX_REQUEST = 1
    CUSTOM_REQUEST = 2

    CANVAS_WIDTH = 300
    CANVAD_HEIGHT = CANVAS_WIDTH

    HANGMAN_IMAGES = {
        0: Image.open(".\\files\\images\\0.png"),
        1: Image.open(".\\files\\images\\1.png"),
        2: Image.open(".\\files\\images\\2.png"),
        3: Image.open(".\\files\\images\\3.png"),
        4: Image.open(".\\files\\images\\4.png"),
        5: Image.open(".\\files\\images\\5.png"),
        6: Image.open(".\\files\\images\\6.png"),
    }

    COLUMNS_AMOUNT_CENTER = 3;

    def get_input_from_popup(self):
        if self.input_popup == None or self.popup_input_field == None:
            return
        input_text = self.popup_input_field.get()
        if len(input_text) <= 0:
            return

        self.input_popup.destroy()
        self.input_popup = None
        self.popup_input_field = None

        if self.input_popup_type == HangmanWindow.INDEX_REQUEST:
            if input_text.isnumeric() and int(input_text) > 0:
                self.hangman_game.init_game(hidden_index=int(input_text))
            else:
                messagebox.showerror(title="Input Error", message="Please enter a number larger than zero.")
        elif self.input_popup_type == HangmanWindow.INDEX_REQUEST:
            if input_text.isalpha():
                input_text = input_text.lower()
                self.hangman_game.init_game(hidden_word=input_text)
            else:
                messagebox.showerror(title="Input Error",
                                     message="Please enter a word using only letters and no spaces")
        else:
            messagebox.showerror(title="Input Error", message="Unknown input request", font=HangmanWindow.DEF_FONT)
        self.update_window()

    def new_game_input_popup(self, current_input_type=0):
        label_text = "Unkown input request"
        if current_input_type == HangmanWindow.INDEX_REQUEST:
            label_text = "Please enter the dsired index of the word in the file that you want to play: "
        elif current_input_type == HangmanWindow.CUSTOM_REQUEST:
            label_text = "Please enter the word you want to play: "
        else:
            messagebox.showerror(title="Input Error", message="Unknown input request", font=HangmanWindow.DEF_FONT)
            return

        self.input_popup_type = current_input_type
        self.input_popup = Toplevel(self.window)
        self.input_popup.title("Input Request")
        label = Label(self.input_popup, text=label_text, font=HangmanWindow.DEF_FONT)
        label.pack()
        self.popup_input_field = Entry(self.input_popup, font=HangmanWindow.DEF_FONT)
        self.popup_input_field.pack()
        button = Button(self.input_popup, text="Submit", font=HangmanWindow.DEF_FONT, command=self.get_input_from_popup)
        button.pack()

    def update_window(self):
        self.missing_word_text.set(self.hangman_game.show_hidden_word())
        self.guessed_letters_text.set(self.hangman_game.guessed_letters())
        image_index = self.hangman_game.current_tries_left
        if image_index > 6:
            image_index = 6
        img = HangmanWindow.HANGMAN_IMAGES[image_index]
        img = img.resize((HangmanWindow.CANVAS_WIDTH, HangmanWindow.CANVAD_HEIGHT))
        self.current_img = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, anchor=NW, image=self.current_img)

    def new_random_game_action(self):
        self.hangman_game.init_game()
        self.update_window()

    def new_indexed_game_action(self):
        self.new_game_input_popup(HangmanWindow.INDEX_REQUEST)

    def new_custom_game_action(self):
        self.new_game_input_popup(HangmanWindow.CUSTOM_REQUEST)

    def input_action(self):
        current_input = self.input_field.get()
        self.input_field.delete(0, 'end')
        result = self.hangman_game.try_update_letter_guessed(current_input)
        self.update_window()
        if result in HangManGame.ERROR_RANGE:
            error_message = HangManGame.get_error_message(result)
            messagebox.showerror(title="Game Error", message=error_message)
        elif result == HangManGame.GAME_WON:
            messagebox.showinfo(title="Game End", message="Congratulations! You won the game!")
        elif result == HangManGame.GAME_LOST:
            messagebox.showinfo(title="Game End", message="That's too bad, you lost the game, better luck next time!")

    def __init__(self):
        self.input_popup = None
        self.input_popup_field = None
        self.input_popup_type = 0
        self.current_image = None
        self.hangman_game = HangManGame()

        self.window = Tk()
        self.missing_word_text = StringVar()
        self.guessed_letters_text = StringVar()
        self.canvas = Canvas(self.window, width=HangmanWindow.CANVAS_WIDTH, height=HangmanWindow.CANVAD_HEIGHT)

        self.title = Label(self.window, text="Hangman", font=("Ariel", 30))
        self.missing_word = Label(self.window, textvariable=self.missing_word_text, font=("Ariel", 15))
        self.guessed_letters_title = Label(self.window, text="Letters you already guessed: ", font=("Ariel", 15))
        self.guessed_letters = Label(self.window, textvariable=self.guessed_letters_text, font=("Ariel", 15))
        self.input_field = Entry(self.window, font=("Ariel", 16))
        self.input_button = Button(self.window, text="enter", command=self.input_action, font=("Ariel", 16))
        self.random_new_game_button = Button(self.window, text="Random new game", command=self.new_random_game_action,
                                             font=("Ariel", 12))
        self.indexed_new_game_button = Button(self.window, text="Index new game", command=self.new_indexed_game_action,
                                              font=("Ariel", 12))
        self.custom_new_game_button = Button(self.window, text="Custuom new game", command=self.new_custom_game_action,
                                             font=("Ariel", 12))

        cmc = HangmanWindow.COLUMNS_AMOUNT_CENTER
        self.title.grid(row=0, column=0, columnspan=cmc)
        self.canvas.grid(row=1, column=0, columnspan=cmc)
        self.missing_word.grid(row=2, column=0, columnspan=cmc)
        self.guessed_letters_title.grid(row=3, column=0, columnspan=cmc)
        self.guessed_letters.grid(row=4, column=0, columnspan=cmc)
        self.input_field.grid(row=5, column=0, columnspan=cmc - 1)
        self.input_button.grid(row=5, column=cmc - 1)
        self.random_new_game_button.grid(row=6, column=0)
        self.indexed_new_game_button.grid(row=6, column=1)
        self.custom_new_game_button.grid(row=6, column=2)
        self.update_window()

    def show_window(self):
        self.window.mainloop()


window = HangmanWindow()
window.show_window()

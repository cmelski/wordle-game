from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
import random
from wordle_logic import evaluate_guess

def get_random_word(path="words.txt"):
    with open(path) as f:
        words = [w.strip().lower() for w in f if len(w.strip()) == 5]
    return random.choice(words)


secret_word = get_random_word().upper()
print(secret_word)


class GuessRow(GridLayout):
    def __init__(self, word_length=5, **kwargs):
        super().__init__(**kwargs)
        self.cols = word_length
        self.spacing = 5
        self.size_hint_y = None
        self.height = 70
        self.labels = []
        for _ in range(word_length):
            lbl = Label(
                text="",
                font_size=50,
                size_hint=(None, None),
                size=(90, 90),
                halign='center',
                valign='middle'
            )
            lbl.bind(size=lbl.setter('text_size'))
            self.add_widget(lbl)
            self.labels.append(lbl)

    def update_guess(self, guess, solution):
        result = evaluate_guess(solution, guess)

        for i, letter in enumerate(guess):
            lbl = self.labels[i]
            lbl.text = letter
            lbl.canvas.before.clear()
            with lbl.canvas.before:
                from kivy.graphics import Color, Rectangle
                if result[i] == "G":
                    Color(0, 1, 0, 1)
                elif result[i] == "Y":
                    Color(1, 1, 0, 1)
                else:
                    Color(0.83, 0.83, 0.83, 1)
                Rectangle(pos=lbl.pos, size=lbl.size)

    def clear(self):
        for lbl in self.labels:
            lbl.text = ""


class Keyboard(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.rows = [
            "QWERTYUIOP",
            "ASDFGHJKL",
            "ZXCVBNM"
        ]
        self.buttons = {}  # map letter to button
        self.on_letter_click = None  # callback

        # Create three horizontal rows for the keyboard
        for row_letters in self.rows:
            row_layout = BoxLayout(size_hint_y=None, height=70, spacing=2)
            for c in row_letters:
                btn = Button(text=c, size_hint=(None, None), size=(50, 70))
                btn.bind(on_press=self._make_click_handler(c))
                self.buttons[c] = btn
                row_layout.add_widget(btn)
            self.add_widget(row_layout)

    def _make_click_handler(self, letter):
        def handler(instance):
            if self.on_letter_click:
                self.on_letter_click(letter)

        return handler

    def disable_letter(self, letter):
        btn = self.buttons.get(letter.upper())
        if btn:
            btn.disabled = True
            btn.background_color = (0.5, 0.5, 0.5, 1)


class WordleGame(App):
    def build(self):
        self.word_length = 5
        self.max_attempts = 6
        self.attempt = 0
        self.solution = secret_word
        print(f'Solution: {self.solution}')
        self.current_guess = []

        main = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Guess grid
        self.grid_layouts = []
        for _ in range(self.max_attempts):
            row = GuessRow(word_length=self.word_length)
            main.add_widget(row)
            self.grid_layouts.append(row)

        # Keyboard with 3 rows stacked vertically
        self.keyboard = Keyboard()
        self.keyboard.on_letter_click = self.add_letter
        main.add_widget(self.keyboard)

        # Submit button
        submit_btn = Button(
            text='Submit Guess',
            size_hint=(None, None),
            size=(170, 70)
        )
        submit_btn.bind(on_press=self.submit_guess)
        main.add_widget(submit_btn)

        return main

    def add_letter(self, letter):
        if len(self.current_guess) < self.word_length:
            self.current_guess.append(letter)
            self.update_display()

    def update_display(self):
        row = self.grid_layouts[self.attempt]
        row.clear()
        for i in range(self.word_length):
            if i < len(self.current_guess):
                row.labels[i].text = self.current_guess[i]
            else:
                row.labels[i].text = ""

    def submit_guess(self, *args):
        if len(self.current_guess) != self.word_length:
            return  # incomplete guess
        guess = "".join(self.current_guess).upper()
        row = self.grid_layouts[self.attempt]
        row.update_guess(guess, self.solution)
        # disable letters used
        for letter in guess:
            if letter not in self.solution:
                self.keyboard.disable_letter(letter)
        self.attempt += 1
        self.current_guess = []

        if guess == self.solution:
            print("Congratulations! Correct Guess.")
        elif self.attempt >= self.max_attempts:
            print(f"Game Over! The word was {self.solution}.")


if __name__ == '__main__':
    WordleGame().run()

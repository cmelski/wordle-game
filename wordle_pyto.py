import ui
from wordle_logic import evaluate_guess
from random import choice

WORDS = ["CRANE", "SLATE", "APPLE", "PLANT"]

solution = choice(WORDS)
attempts = 0
current_guess = ""

label = ui.Label(text="Wordle", font=('Helvetica-Bold', 24), alignment=ui.ALIGN_CENTER)
status = ui.Label(text="", alignment=ui.ALIGN_CENTER)

def submit(sender):
    global attempts, current_guess
    if len(current_guess) != 5:
        return

    result = evaluate_guess(solution, current_guess)
    status.text = f"{current_guess} → {result}"
    attempts += 1
    current_guess = ""

def add_letter(sender):
    global current_guess
    if len(current_guess) < 5:
        current_guess += sender.title

v = ui.View(bg_color='white')
v.add_subview(label)
v.add_subview(status)

label.frame = (0, 20, 375, 40)
status.frame = (0, 70, 375, 40)

for i, c in enumerate("QWERTYUIOP"):
    b = ui.Button(title=c)
    b.frame = (10 + i*35, 130, 32, 40)
    b.action = add_letter
    v.add_subview(b)

submit_btn = ui.Button(title="Submit")
submit_btn.frame = (120, 200, 120, 44)
submit_btn.action = submit
v.add_subview(submit_btn)

v.present('sheet')

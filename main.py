from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}
try:
    data = pandas.read_csv("Words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)

    canvas.itemconfig(card_title, text=f"{current_card['Kanji']}, (Level:{current_card['JLPT']}) ", fill = "black")
    canvas.itemconfig(card_word, text=f"Onyomi: {current_card['Onyomi']}\n\nKunyomi: {current_card['Kunyomi']} "
                      , fill = "black", )
    canvas.itemconfig(card_background, image = card_front_img)
    flip_timer = window.after(5000, func=flip_card)

def flip_card():
    canvas.itemconfig(card_title, text="", fill = "white")
    canvas.itemconfig(card_word, text=f"{current_card['Kanji Meaning']}",fill = "white")
    canvas.itemconfig(card_background,image= card_back_img)

def is_known():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("Words_to_learn.csv", index = False)

    next_card()




window = Tk()
window.title("Flashcards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(5000, func=flip_card)

canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file="card_front.png")
card_back_img = PhotoImage(file="card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 30, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 25, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=2)

tickphoto = PhotoImage(file="right.png")
tick_button = Button(image=tickphoto, highlightthickness=0, command=next_card)
tick_button.grid(row=1, column=1)

xphoto = PhotoImage(file="wrong.png")
x_button = Button(image=xphoto, highlightthickness=0, command=is_known)
x_button.grid(row=1, column=0)

next_card()

window.mainloop()

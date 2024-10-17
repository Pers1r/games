import tkinter as tk
import random


# window
window = tk.Tk()
window.geometry('500x500')
window.title('Memorizer')

# game staff
colors = ['red', 'blue', 'yellow', 'green']
score = 0
game = []
temp = []
click = 0
max_score = [0]


def game_start():
    global game, score, temp, click

    start.config(state='disabled')
    label_score.config(text='Score: ' + str(score))
    temp = []
    click = 0
    finish_text.place_forget()
    game.append(random.choice(colors))
    disable_buttons()
    show(0)


def show(index):
    if index < len(game):
        update(game[index])

        window.after(1000, lambda: show(index + 1))
    else:
        enable_buttons()


def update(color):
    if color == 'red':
        red_button.configure(background='white')
        window.after(500, lambda: red_button.configure(background=btn_red))
    elif color == 'blue':
        blue_button.configure(background='white')
        window.after(500, lambda: blue_button.configure(background=btn_blue))
    elif color == 'yellow':
        yellow_button.configure(background='white')
        window.after(500, lambda: yellow_button.configure(background=btn_yellow))
    elif color == 'green':
        green_button.configure(background='white')
        window.after(500, lambda: green_button.configure(background=btn_green))


def check():
    global click, score

    if click < len(game):
        if temp[click] == game[click]:
            click += 1
            if click == len(game):
                disable_buttons()
                score += 1
                label_score.config(text='Score: ' + str(score))
                window.after(1000, game_start)
        else:
            game_over()
    else:
        score += 1
        game_start()


def red():
    temp.append('red')
    check()


def blue():
    temp.append('blue')
    check()


def yellow():
    temp.append('yellow')
    check()


def green():
    temp.append('green')
    check()


def game_over():
    global game, score, temp, click

    disable_buttons()
    max_score.append(score)
    finish_text.config(text='You lose! Score: ' + str(score))
    finish_text.place(anchor='center', relx=0.5, rely=0.5, relwidth=0.7, relheight=0.3)
    able_start()
    start.config(text='Restart')
    score_max.config(text='Max score: ' + str(max(max_score)))

    game = []
    temp = []
    click = 0
    score = 0


def disable_buttons():
    red_button.config(state='disabled')
    blue_button.config(state='disabled')
    yellow_button.config(state='disabled')
    green_button.config(state='disabled')


def enable_buttons():
    red_button.config(state='normal')
    blue_button.config(state='normal')
    yellow_button.config(state='normal')
    green_button.config(state='normal')


def able_start():
    start.config(state='normal')


# colors
bg_blue = '#0a0a1a'
grey_blue = '#33324d'
btn_red = '#c70202'
btn_blue = '#0081eb'
btn_yellow = '#eb7100'
btn_green = '#08cf15'

# background
bg = tk.Label(window, text='', background=bg_blue)
bg.place(relx=0, rely=0, relwidth=1, relheight=1)

# frames
menu_frame = tk.Frame(window, background=grey_blue, relief='solid')
main_frame = tk.Frame(window, background=grey_blue, relief='solid')
btn_frame = tk.Frame(main_frame)
menu_frame.place(relx=0.05, rely=0.02, relwidth=0.9, relheight=0.1)
main_frame.place(relx=0.05, rely=0.15, relwidth=0.9, relheight=0.8)

# layout
main_frame.columnconfigure((0, 1), weight=1, uniform='a')
main_frame.rowconfigure((0, 1), weight=1, uniform='a')

# buttons
start = tk.Button(menu_frame, text='Start', background=bg_blue, foreground='white', font='15', command=game_start)
red_button = tk.Button(main_frame, text='', background=btn_red, command=red)
blue_button = tk.Button(main_frame, text='', background=btn_blue, command=blue)
yellow_button = tk.Button(main_frame, text='', background=btn_yellow, command=yellow)
green_button = tk.Button(main_frame, text='', background=btn_green, command=green)
red_button.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
blue_button.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)
yellow_button.grid(row=1, column=1, sticky='nsew', padx=10, pady=10)
green_button.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
start.place(relx=0.5, rely=0.5, relwidth=0.3, relheight=0.90, anchor='center')

# info
label_score = tk.Label(menu_frame, text='Score: ' + str(score), foreground='white', background=grey_blue, font='18')
label_score.place(relx=0.1, rely=0.5, anchor='center', relwidth=0.3, relheight=0.9)
finish_text = tk.Label(main_frame,
                       text='You Lose! Score: ' + str(score),
                       background=bg_blue,
                       foreground='white',
                       font='Consolas 20')
score_max = tk.Label(menu_frame,
                     text='Max score: ' + str(max(max_score)),
                     foreground='white',
                     background=grey_blue,
                     font=18)
score_max.place(relx=0.85, rely=0.5, anchor='center')

# run
window.mainloop()

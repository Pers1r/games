import tkinter as tk


# vars
playerX = 'X'
playerO = 'O'
currPlayer = playerX
game_over = False
board = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0]]

big_board = [0, 0, 0,
             0, 0, 0,
             0, 0, 0]

# colors
bg_blue = '#0a0a1a'
grey_blue = '#33324d'

# window
window = tk.Tk()
window.title('Ultimate Tic Tac Toe')
window.geometry('600x600')

# frames
text_frame = tk.Frame(window, background=bg_blue, borderwidth=0)
main_frame = tk.Frame(window, background=bg_blue, borderwidth=0, pady=10, padx=10)
text_frame.place(relx=0, rely=0, relwidth=1, relheight=0.2)
main_frame.place(relx=0, rely=0.2, relwidth=1, relheight=0.8)

# labels
label = tk.Label(text_frame,
                 text=currPlayer + "'s turn",
                 foreground='yellow',
                 background=bg_blue,
                 font='Consolas 20 bold')
label.place(anchor='center', relx=0.5, rely=0.5, relwidth=0.5, relheight=1)
finish_label = tk.Label(window, text='', background=bg_blue, foreground='yellow', font='Consolas 25 bold')

# main frame layout layout
main_frame.columnconfigure((0, 1, 2), weight=1, uniform='a')
main_frame.rowconfigure((0, 1, 2), weight=1, uniform='a')


def set_title(x, y):
    global currPlayer, big_board
    if game_over:
        return
    if board[x][y]['text'] != '':
        return
    if currPlayer == 'X':
        board[x][y]['text'] = currPlayer
        board[x][y]['foreground'] = 'blue'
        board[x][y]['disabledforeground'] = 'blue'
        if check_win(board[x]):
            big_board[x] = currPlayer
            print('win')
            mark_won(x)
            big_win()
        currPlayer = playerO
        possible_moves()
        move(y)
    else:
        board[x][y]['text'] = currPlayer
        board[x][y]['foreground'] = 'red'
        board[x][y]['disabledforeground'] = 'red'
        if check_win(board[x]):
            big_board[x] = currPlayer
            print('win')
            mark_won(x)
            big_win()
        currPlayer = playerX
        possible_moves()
        move(y)
    label.config(text=currPlayer + "'s turn")


def disable_buttons():
    for i in range(9):
        if big_board[i] == 0:
            for x in range(9):
                board[i][x].config(state='disabled')
                board[i][x].config(background=grey_blue)


def able_buttons():
    for i in range(9):
        if big_board[i] == 0:
            for x in range(9):
                board[i][x].config(state='normal')
                board[i][x].config(background='lime green')


def move(y):
    disable_buttons()
    if big_board[y] == 0:
        for i in range(9):
            board[y][i].config(state='normal')
            board[y][i].config(background='lime green')
    else:
        able_buttons()


def check_win(arr):
    for m in range(0, 7, 3):
        if arr[0+m]['text'] == arr[1+m]['text'] == arr[2+m]['text'] != '':
            return True
    for n in range(3):
        if arr[n]['text'] == arr[n+3]['text'] == arr[n+6]['text'] != '':
            return True
    if arr[0]['text'] == arr[4]['text'] == arr[8]['text'] != '':
        return True
    if arr[2]['text'] == arr[4]['text'] == arr[6]['text'] != '':
        return True
    return False


def mark_won(x):
    if currPlayer == 'X':
        for i in range(9):
            if i in range(0, 9, 2):
                board[x][i].config(background='blue', text='')
            else:
                board[x][i].config(background=grey_blue, text='')
    else:
        for i in range(9):
            if i == 4:
                board[x][i].config(background=grey_blue, text='')
            else:
                board[x][i].config(background='red', text='')


def big_win():
    global game_over

    if game_over:
        return
    for i in range(3):
        if big_board[i] == big_board[i+3] == big_board[i+6] != 0 != 'T':
            big_winner()
    for i in range(0, 7, 3):
        if big_board[0+i] == big_board[1+i] == big_board[2+i] != 0 != 'T':
            big_winner()
    if big_board[0] == big_board[4] == big_board[8] != 0 != 'T':
        big_winner()
    if big_board[2] == big_board[4] == big_board[6] != 0 != 'T':
        big_winner()


def possible_moves():
    moves = 0
    for x in range(9):
        if big_board[x] != 0:
            pass
        else:
            temp = 0
            for i in range(9):
                if board[x][i]['text'] == '':
                    temp += 1
                    moves += 1
                if temp == 0 and big_board == 0:
                    big_board[x] = 'T'
    if moves == 0:
        tie()


def tie():
    global game_over
    game_over = True
    disable_buttons()
    finish_label.config(text="It's a Tie!")
    finish_label.place(anchor='center', relx=0.5, rely=0.5, relwidth=0.5, relheight=0.3)


def restart():
    global board, game_over, big_board, currPlayer
    board = [[0 for _ in range(9)] for _ in range(9)]
    big_board = [0 for _ in range(9)]
    game_over = False
    currPlayer = playerX
    finish_label.place_forget()
    btn_res.place_forget()

    index = 0
    # buttons
    for row in range(3):
        for column in range(3):
            frame = tk.Frame(main_frame, background=grey_blue)
            frame.grid(row=row, column=column, sticky='nsew', padx=10, pady=10)
            frame.columnconfigure((0, 1, 2), weight=1, uniform='a')
            frame.rowconfigure((0, 1, 2), weight=1, uniform='a')
            btn = 0
            for row_ in range(3):
                for column_ in range(3):
                    board[index][btn] = tk.Button(frame,
                                                  text='',
                                                  background=grey_blue,
                                                  font='Consolas 15',
                                                  command=lambda x=index, y=btn: set_title(x, y))
                    board[index][btn].grid(row=row_, column=column_, sticky='nsew')
                    btn += 1
            index += 1


# restart button
btn_res = tk.Button(window,
                    text='Restart',
                    background=grey_blue,
                    foreground='yellow',
                    font='Consolas 15 bold',
                    command=restart)


def big_winner():
    disable_buttons()
    finish_label.config(text=' Player ' + currPlayer + ' wins')
    finish_label.place(anchor='center', relx=0.5, rely=0.5, relwidth=0.5, relheight=0.3)
    btn_res.place(anchor='center', relx=0.5, rely=0.60, relwidth=0.2, relheight=0.05)


index = 0
# buttons
for row in range(3):
    for column in range(3):
        frame = tk.Frame(main_frame, background=grey_blue)
        frame.grid(row=row, column=column, sticky='nsew', padx=10, pady=10)
        frame.columnconfigure((0, 1, 2), weight=1, uniform='a')
        frame.rowconfigure((0, 1, 2), weight=1, uniform='a')
        btn = 0
        for row_ in range(3):
            for column_ in range(3):
                board[index][btn] = tk.Button(frame,
                                              text='',
                                              background=grey_blue,
                                              font='Consolas 15',
                                              command=lambda x=index, y=btn: set_title(x, y))
                board[index][btn].grid(row=row_, column=column_, sticky='nsew')
                btn += 1
        index += 1

# run
window.mainloop()

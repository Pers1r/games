import tkinter as tk
import random as r

title_size = 25


class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y


# window setup
window = tk.Tk()
window.title('Snake')
window.resizable(False, False)

canvas = tk.Canvas(window, bg='black', width=625, height=625, borderwidth=0, highlightthickness=0)
canvas.pack()

window.update()

window.geometry(f'625x625+{int(window.winfo_screenwidth()/2-311)}+{int(window.winfo_screenheight()/2-311)}')

# variables
snake = Tile(5 * title_size, 5 * title_size)
food = Tile(10 * title_size, 10 * title_size)
snake_body = []
velocityX = 0
velocityY = 0
game_over = False
score = 0
height_score = [0]


# functions
def new_game():
    global game_over, velocityY, velocityX, score, snake_body, snake

    # reset all values
    height_score.append(score)
    game_over = False
    velocityX = 0
    velocityY = 0
    score = 0
    snake.x = 125
    snake.y = 125
    snake_body = []
    canvas.delete('all')
    food.x = r.randint(0, 24) * title_size
    food.y = r.randint(0, 24) * title_size


def place_food():
    global snake_body, food
    # placing food
    food.x = r.randint(0, 24) * title_size
    food.y = r.randint(0, 24) * title_size
    # check if food is in snake's body
    for snake_ in snake_body:
        if food.x == snake_.x and food.y == snake_.y:
            place_food()


def change_direction(event):
    global velocityX, velocityY, game_over, score, snake_body

    if event.keysym == "Up" and velocityY != 1:
        velocityY = -1
        velocityX = 0
    elif event.keysym == "Down" and velocityY != -1:
        velocityY = 1
        velocityX = 0
    elif event.keysym == "Left" and velocityX != 1:
        velocityX = -1
        velocityY = 0
    elif event.keysym == "Right" and velocityX != -1:
        velocityX = 1
        velocityY = 0
    elif event.keysym == 'space' and game_over:
        new_game()

    if game_over:
        return


def move():
    global snake, food, game_over, snake_body, score

    if game_over:
        return
    # collide with borders
    if snake.x < 0 or snake.x > 600 or snake.y < 0 or snake.y > 600:
        game_over = True
        return
    # collide with body
    for tile in snake_body:
        if tile.x == snake.x and tile.y == snake.y:
            game_over = True
            return
    # eating food
    if snake.x == food.x and snake.y == food.y:
        snake_body.append(Tile(food.x, food.y))
        place_food()
        score += 1
    # body follows the snake
    for i in range(len(snake_body)-1, -1, -1):
        tile = snake_body[i]
        if i == 0:
            tile.x = snake.x
            tile.y = snake.y
        else:
            prev_tile = snake_body[i-1]
            tile.x = prev_tile.x
            tile.y = prev_tile.y
    # actual movement
    snake.x += velocityX * title_size
    snake.y += velocityY * title_size


def draw():
    global snake, score
    # making move
    move()

    canvas.delete('all')

    # drawing food
    canvas.create_rectangle(food.x,
                            food.y,
                            food.x + title_size,
                            food.y + title_size,
                            fill='red')
    # drawing snake's head
    canvas.create_rectangle(snake.x,
                            snake.y,
                            snake.x + title_size,
                            snake.y + title_size,
                            fill='lime green',
                            outline='lime green')
    # drawing snake's body
    for tile in snake_body:
        canvas.create_rectangle(tile.x,
                                tile.y,
                                tile.x + title_size,
                                tile.y + title_size,
                                fill='lime green',
                                outline='lime green')
    # score
    canvas.create_text(50, 10, text=f'Score: {score}', fill='yellow', font='Comic_sans 15')
    # max score
    canvas.create_text(530, 10, text=f'Highest score: {max(height_score)}', font='Comic_sans 15', fill='yellow')
    # game over
    if game_over:
        canvas.create_text(313, 300, font='Consolas 30 bold', text=f'Game over: {score}', fill='yellow')
        canvas.create_text(313, 340, font='Consolas 20 bold', text='Press Space to restart', fill='yellow')
    # looping everything in 1/10 frames per second
    window.after(100, draw)


draw()

# checking for key press
window.bind('<KeyRelease>', change_direction)
window.bind('<Escape>', lambda x: window.quit())

# run
window.mainloop()

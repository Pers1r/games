from tkinter import *
from random import *


class App(Tk):
    def __init__(self, title):
        super().__init__()
        self.title(title)
        self.geometry('500x500')

        self.update()

        self.width = self.winfo_width()
        self.height = self.winfo_height()

        self.game = Game(self)
        self.game.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.game_over_text = None
        self.restart_button = Button(self, text='Restart', font='consolas 20 bold', command=self.restart)

        self.score = 0
        self.score_text = self.score_text = self.game.canvas.create_text(
            self.width//2, self.height * 0.2, anchor='center', fill='yellow',  text=self.score, font='Consolas 40 bold'
        )
        self.fall = False
        self.walls = []
        self.velocity = -1
        self.gravity = 0.1
        self.jump_strength = -2
        self.step = 5

        self.wall_timer = None
        self.move_timer = None

        self.player = self.game.canvas.create_oval(100, 230, 120, 250, width=1, outline='orange', fill='orange')
        self.move()
        self.wall()
        self.move_walls()

        self.mainloop()

    def move(self):
        if self.fall:
            return
        self.velocity += self.gravity
        self.game.canvas.move(self.player, 0, self.velocity * self.step)

        for x in self.walls:
            top = self.game.canvas.coords(x[0])[3]
            bottom = self.game.canvas.coords(x[1])[1]
            left = self.game.canvas.coords(x[0])[0]
            right = self.game.canvas.coords(x[0])[2]
            p_x_1 = self.game.canvas.coords(self.player)[0]
            p_y_1 = self.game.canvas.coords(self.player)[1]
            p_x_2 = self.game.canvas.coords(self.player)[2]
            p_y_2 = self.game.canvas.coords(self.player)[3]
            if left < p_x_1 < right:
                if top < p_y_1 < bottom:
                    pass
                else:
                    self.game_over()
            if left < p_x_2 < right:
                if top < p_y_2 < bottom:
                    pass
                else:
                    self.game_over()
            if right == p_x_1:
                self.score += 1
                self.game.canvas.itemconfig(self.score_text, text=self.score)
                self.game.canvas.tag_raise(self.score_text)

        if self.game.canvas.coords(self.player)[3] > self.height:
            self.game_over()

        self.move_timer = self.after(16, self.move)

        self.bind('<space>', lambda x_: self.up())
        self.bind('<ButtonPress-1>', lambda x_: self.up())

    def up(self):
        self.velocity = self.jump_strength

    def game_over(self):
        self.fall = True
        self.game_over_text = self.game.canvas.create_text(
            self.width//2, self.height//2, anchor='center', text='You lose', font='Consolas 40 bold'
        )
        self.restart_button.place(anchor='center', relx=0.5, rely=0.65)

    def restart(self):
        self.fall = False
        if self.wall_timer:
            self.after_cancel(self.wall_timer)
            self.wall_timer = None
        if self.move_timer:
            self.after_cancel(self.move_timer)
            self.move_timer = None
        for x in self.walls:
            self.game.canvas.delete(x[0])
            self.game.canvas.delete(x[1])
        self.velocity = -1
        self.gravity = 0.1
        self.jump_strength = -2
        self.step = 5
        self.walls = []
        self.score = 0

        self.game.canvas.delete('all')

        self.restart_button.place_forget()
        self.score_text = self.score_text = self.game.canvas.create_text(
            self.width // 2, self.height * 0.2, anchor='center', fill='yellow', text=self.score, font='Consolas 40 bold'
        )
        self.game.canvas.tag_raise(self.score_text)
        self.player = self.game.canvas.create_oval(100, 230, 120, 250, width=1, outline='orange', fill='orange')
        self.move()
        self.wall()
        self.move_walls()

    def wall(self):
        if self.fall:
            return
        top = self.width * choice([x/1000 for x in range(300, 601)])
        wall_up = self.game.canvas.create_rectangle(self.width, 0, self.width + 100, top, fill='green')
        wall_down = self.game.canvas.create_rectangle(self.width, top+150, self.width + 100, self.height, fill='green')
        self.walls.append((wall_up, wall_down))
        self.game.canvas.tag_raise(self.score_text)
        self.wall_timer = self.after(3000, self.wall)

    def move_walls(self):
        if self.fall:
            return
        for x in self.walls:
            if self.game.canvas.coords(x[0])[2] <= 0:
                self.game.canvas.delete(x[0])
                self.game.canvas.delete(x[1])
                self.walls.remove(x)
            self.game.canvas.move(x[0], -2, 0)
            self.game.canvas.move(x[1], -2, 0)
        self.game.canvas.tag_raise (self.score_text)
        self.after(16, self.move_walls)


class Game(Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.canvas = Canvas(self, background='light blue')
        self.canvas.place(relx=0, rely=0, relwidth=1, relheight=1)


App('Flappy bird')

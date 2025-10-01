import os
from pathlib import Path
from tkinter import PhotoImage
import random
import tkinter.messagebox
from fractions import Fraction
from tkinter import *
from tkinter import messagebox


# Hallo

CELL_SIZE = 90
GRID_LENGTH = 9
CANVAS_SIZE = 840
CANVAS_CENTER = CANVAS_SIZE // 2
DIRECTION_TO_INDEX = {'up': 0, 'right': 1, 'down': 2, 'left': 3}

GRID_PIXEL_SIZE = CELL_SIZE * GRID_LENGTH
GRID_OFFSET = (CANVAS_SIZE - GRID_PIXEL_SIZE) // 2
MIN_COORD = GRID_OFFSET
MAX_COORD = GRID_OFFSET + GRID_PIXEL_SIZE

current_snake = None
direction = 'down'

class Snake:

    def __init__(self, start_direction: str):
        self.body_size = 3
        self.coordinates: list[list[int]] = []
        self.squares: list[int] = []
        self.orientations: list[int] = []

        initial_orientation = DIRECTION_TO_INDEX[start_direction]

        start_x = GRID_OFFSET
        start_y = GRID_OFFSET

        for _ in range(self.body_size):
            self.coordinates.append([start_x, start_y])
            self.orientations.append(initial_orientation)

        for x, y in self.coordinates:
            square = canvas.create_image(x, y, image=BODY_IMAGE, anchor='nw')
            self.squares.append(square)


class Food:

    def __init__(self):
        x = GRID_OFFSET + random.randint(0, GRID_LENGTH - 1) * CELL_SIZE
        y = GRID_OFFSET + random.randint(0, GRID_LENGTH - 1) * CELL_SIZE
        self.coordinates = [x, y]
        self.position = canvas.create_rectangle(x, y, x + CELL_SIZE, y + CELL_SIZE, fill="#FF0000", tags="food")


def gameover():
    canvas.delete("all")
    label.config(text=f"Pascal died", fg="red")

    play_again = Button(root, text="Play Again", font=("Helvetica", 20), width=15, command=play)
    canvas.create_window(CANVAS_CENTER, CANVAS_CENTER + CELL_SIZE // 2, window=play_again)
    canvas.create_text(CANVAS_CENTER, CANVAS_CENTER + CELL_SIZE, text=f"{score}", font=("Helvetica", 20), fill="white")

def draw_player(snake: Snake) -> None:
    for index, square in enumerate(snake.squares):
        orientation = snake.orientations[index]
        if index == 0:
            canvas.itemconfig(square, image=head_list[orientation])
        elif index == len(snake.squares) - 1:
            canvas.itemconfig(square, image=feet_list[orientation])
        else:
            canvas.itemconfig(square, image=body_list[orientation])


def next_turn(snake, food):
    x, y = snake.coordinates[0]

    if direction == 'up':
        y -= CELL_SIZE
    if direction == 'down':
        y += CELL_SIZE
    if direction == 'left':
        x -= CELL_SIZE
    if direction == 'right':  #####################################################
        x += CELL_SIZE

    snake.coordinates.insert(0, [x, y])
    snake.orientations.insert(0, DIRECTION_TO_INDEX[direction])
    new_square = canvas.create_image(x, y, image=BODY_IMAGE, anchor='nw')
    snake.squares.insert(0, new_square)

    ate_food = x == food.coordinates[0] and y == food.coordinates[1]

    if ate_food:
        global score
        score += 1
        label.config(text=f"Score is : {score}")

        canvas.delete(food.position)
        del food.coordinates
        food = Food()
    else:
        tail_square = snake.squares.pop()
        canvas.delete(tail_square)
        snake.coordinates.pop()
        snake.orientations.pop()

    draw_player(snake)

    if check_collision(snake):
        gameover()
    else:
        root.after(100, next_turn, snake, food)

def change_direction(new_direction):
    global direction, current_snake

    opposite = {'left': 'right', 'right': 'left', 'up': 'down', 'down': 'up'}
    if new_direction != opposite.get(direction):
        direction = new_direction
        if current_snake:
            current_snake.orientations[0] = DIRECTION_TO_INDEX[new_direction]
            draw_player(current_snake)

def check_collision(snake):
    x, y = snake.coordinates[0]

    for x_pos, y_pos in snake.coordinates[1:]:
        if x_pos == x and y_pos == y:
            return True

    if x < MIN_COORD or y < MIN_COORD or x >= MAX_COORD or y >= MAX_COORD:
        return True

    return False


def play():
    global score, label, canvas, direction, current_snake
    try:
        label.destroy()
        canvas.destroy()
    except NameError:
        pass

    score = 0
    label = Label(root, text=f"Score is : {score}", font=('consolas', CELL_SIZE))
    label.pack()

    canvas = Canvas(root, bg="#ff06b0", height=CANVAS_SIZE, width=CANVAS_SIZE)
    canvas.pack()

    direction = "down"

    root.bind('<Left>', lambda event: change_direction('left'))
    root.bind('<Right>', lambda event: change_direction('right'))
    root.bind('<Down>', lambda event: change_direction('down'))
    root.bind('<Up>', lambda event: change_direction('up'))

    food = Food()
    snake = Snake(direction)
    current_snake = snake
    draw_player(snake)
    next_turn(snake, food)

    root.mainloop()


root = Tk()
root.title("Pascal GAME")
root.resizable(False, False)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
for folder in ("images", "masa", "pascal"):
    candidate = os.path.join(BASE_DIR, folder)
    if os.path.isdir(candidate):
        ASSETS_DIR = candidate
        break
else:
    ASSETS_DIR = BASE_DIR


def load_sprite(filename: str) -> PhotoImage:
    try:
        image = PhotoImage(file=os.path.join(ASSETS_DIR, filename))
    except TclError:
        image = PhotoImage(file=os.path.join("/home/marius/Code/Phytoncode/masagame/Snake-Game", filename))

    width, height = image.width(), image.height()

    if width == CELL_SIZE and height == CELL_SIZE:
        return image

    scale_x = Fraction(CELL_SIZE, width)
    scale_y = Fraction(CELL_SIZE, height)

    image = image.zoom(scale_x.numerator, scale_y.numerator)
    image = image.subsample(scale_x.denominator, scale_y.denominator)
    return image


HEAD_IMAGE = load_sprite("head.png")
BODY_IMAGE = load_sprite("middle.png")
TAIL_IMAGE = load_sprite("feet.png")

HEAD_IMAGE_90 = load_sprite("head_90.png")
BODY_IMAGE_90 = load_sprite("middle_90.png")
TAIL_IMAGE_90 = load_sprite("feet_90.png")

HEAD_IMAGE_180 = load_sprite("head_180.png")
BODY_IMAGE_180 = load_sprite("middle_180.png")
TAIL_IMAGE_180 = load_sprite("feet_180.png")

HEAD_IMAGE_270 = load_sprite("head_270.png")
BODY_IMAGE_270 = load_sprite("middle_270.png")
TAIL_IMAGE_270 = load_sprite("feet_270.png")

apple_dir = os.path.join("/home/marius/Code/Phytoncode/masagame/Snake-Game/", "apple")
image_files = []

counter = 0

for filename in os.listdir(apple_dir):
    if filename.endswith(".png"):
        new_name = f"bild_{counter}.png"
        counter += 1
        if filename != new_name:
            os.rename(os.path.join(apple_dir, filename), os.path.join(apple_dir, new_name))
            filename = new_name
        image_files.append(os.path.join("apple", filename))

SPRITES = {}
for image_file in image_files:
    SPRITES[image_file] = load_sprite(image_file)

filename = random.choice(list(SPRITES.keys()))
apple_img = SPRITES[filename]

global head_list
global body_list
global feet_list

head_list = [HEAD_IMAGE, HEAD_IMAGE_90, HEAD_IMAGE_180, HEAD_IMAGE_270]
body_list = [BODY_IMAGE, BODY_IMAGE_90, BODY_IMAGE_180, BODY_IMAGE_270]
feet_list = [TAIL_IMAGE, TAIL_IMAGE_90, TAIL_IMAGE_180, TAIL_IMAGE_270]

play()

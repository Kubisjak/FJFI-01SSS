__author__ = 'Kubisjak'

import tkinter as tk
import math
import time
import numpy as np
from scipy.signal import convolve2d
import matplotlib
# from matplotlib.figure import Figure
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # NavigationToolbar2TkAgg


# from matplotlib.figure import Figure


# Declarations

# Functions


def _quit():
    GUI.quit()
    GUI.destroy()


def getsize():
    global size
    if option_gsize_var.get() == OPTIONS_gsize[0]:
        size = 12
    elif option_gsize_var.get() == OPTIONS_gsize[1]:
        size = 16
    elif option_gsize_var.get() == OPTIONS_gsize[2]:
        size = 20


def getngen():
    global ngen
    if option_ngen_var.get() == OPTIONS_ngen[0]:
        ngen = 10
    elif option_ngen_var.get() == OPTIONS_ngen[1]:
        ngen = 15
    elif option_ngen_var.get() == OPTIONS_ngen[2]:
        ngen = 20


def getmode():
    global mode
    if option_transition_var.get() == OPTIONS_transition[0]:
        mode = True  # mode Automatic = True
    else:
        mode = False


def create_buffer():
    global static1, static2, static3, static4, blinker, toad, \
        glider, diehard, boat, r_pentomino, acorn, spaceship, block_switch_engine

    static1 = np.ones((2, 2))

    static2 = np.array([
        [0, 1, 1, 0],
        [1, 0, 0, 1],
        [0, 1, 1, 0]])

    static3 = np.array([
        [0, 1, 1, 0],
        [1, 0, 0, 1],
        [0, 1, 0, 1],
        [0, 0, 1, 0]])

    static4 = np.array([
        [1, 1, 0],
        [1, 0, 1],
        [0, 1, 0]])

# Oscilators

    blinker = np.array([[1, 1, 1]])

    toad = np.array([[1, 1, 1, 0], [0, 1, 1, 1]])

    glider = np.array([[1, 0, 0], [0, 1, 1], [1, 1, 0]])

# Others

    diehard = np.array([
        [0, 0, 0, 0, 0, 0, 1, 0],
        [1, 1, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 1, 1, 1]])

    boat = np.array([
        [1, 1, 0],
        [1, 0, 1],
        [0, 1, 0]])

    r_pentomino = np.array([
        [0, 1, 1],
        [1, 1, 0],
        [0, 1, 0]])

    beacon = np.array([
        [0, 0, 1, 1],
        [0, 0, 1, 1],
        [1, 1, 0, 0],
        [1, 1, 0, 0]])

    acorn = np.array([
        [0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0],
        [1, 1, 0, 0, 1, 1, 1]])

    spaceship = np.array([
        [0, 0, 1, 1, 0],
        [1, 1, 0, 1, 1],
        [1, 1, 1, 1, 0],
        [0, 1, 1, 0, 0]])

    block_switch_engine = np.array([
        [0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 1, 0, 1, 1],
        [0, 0, 0, 0, 1, 0, 1, 0],
        [0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0],
        [1, 0, 1, 0, 0, 0, 0, 0]])


def get_start_shape():
    global static1, static2, static3, static4, blinker, toad, \
        glider, diehard, boat, r_pentomino, acorn, spaceship, block_switch_engine, start_shape

    create_buffer()

    if option_start_var.get() == OPTIONS_start[0]:
        start_shape = "Random Start"  # mode Automatic = True

    elif option_start_var.get() == OPTIONS_start[1]:
        start_shape = static1

    elif option_start_var.get() == OPTIONS_start[2]:
        start_shape = static2

    elif option_start_var.get() == OPTIONS_start[3]:
        start_shape = static3

    elif option_start_var.get() == OPTIONS_start[4]:
        start_shape = static4

    elif option_start_var.get() == OPTIONS_start[5]:
        start_shape = blinker

    elif option_start_var.get() == OPTIONS_start[6]:
        start_shape = toad

    elif option_start_var.get() == OPTIONS_start[7]:
        start_shape = glider

    elif option_start_var.get() == OPTIONS_start[8]:
        start_shape = diehard

    elif option_start_var.get() == OPTIONS_start[9]:
        start_shape = r_pentomino

    elif option_start_var.get() == OPTIONS_start[10]:
        start_shape = acorn

    elif option_start_var.get() == OPTIONS_start[11]:
        start_shape = spaceship

    elif option_start_var.get() == OPTIONS_start[12]:
        start_shape = block_switch_engine

    return start_shape


def create_board(board):
    getsize()
    # Creates empty board image
    board_image = np.zeros((size, size, 3))
    board_image[:, :, 0] = board[:, :]
    board_image[:, :, 1] = board[:, :]
    board_image[:, :, 2] = board[:, :]
    return board_image


def put_in_center(cell):
    global size
    board = np.zeros(shape=(size, size))

    coordinate1 = math.floor((size - cell.shape[0])/2)
    coordinate2 = math.floor((size - cell.shape[1])/2)

    coordinate1end = size - coordinate1
    coordinate2end = size - coordinate2

    if cell.shape[0] % 2 != 0:
        coordinate1end -= 1
    if cell.shape[1] % 2 != 0:
        coordinate2end -= 1

    board[coordinate1:coordinate1end, coordinate2:coordinate2end] = cell

    return board


# Initialize
GUI = tk.Tk()
status_string_var = "Game of Life is not running yet."
current_generation = 0

# GUI.geometry("0+0")
GUI.title("01SSS - Game of Life")

# Option Bar with startin points
header = tk.Label(text="Select starting value")
header.pack(side=tk.TOP, fill=tk.BOTH)


OPTIONS_start = ["Random Start", "Static 1", "Static 2", "Static 3", "Static 4", "Blinker", "Toad",
                 "Glider", "Diehard", "Boat", "Pentomino", "Acorn", "Spaceship", "Block Switch Engine"]
option_start_var = tk.StringVar(GUI)
option_start_var.set(OPTIONS_start[0])  # default value

window_start_menu = tk.OptionMenu(GUI, option_start_var, *OPTIONS_start)
window_start_menu.pack(side=tk.TOP, fill=tk.BOTH)

# Option bar with number of runs
header = tk.Label(text="Select number of generations")
header.pack(side=tk.TOP, fill=tk.BOTH, )

OPTIONS_ngen = ["10", "15", "20"]
option_ngen_var = tk.StringVar(GUI)
option_ngen_var.set(OPTIONS_ngen[0])  # default value

window_ngen_menu = tk.OptionMenu(GUI, option_ngen_var, *OPTIONS_ngen)
window_ngen_menu.pack(side=tk.TOP, fill=tk.BOTH)

# Option bar with size of grid
header = tk.Label(text="Select the size of grid")
header.pack(side=tk.TOP, fill=tk.BOTH)

OPTIONS_gsize = ["12x12", "16x16", "20x20"]
option_gsize_var = tk.StringVar(GUI)
option_gsize_var.set(OPTIONS_gsize[0])  # default value

window_gsize_menu = tk.OptionMenu(GUI, option_gsize_var, *OPTIONS_gsize)
window_gsize_menu.pack(side=tk.TOP, fill=tk.BOTH)

# Option bar with automatic/manual transitions
header = tk.Label(text="Select type of transition")
header.pack(side=tk.TOP, fill=tk.BOTH)

OPTIONS_transition = ["Auto", "Manual"]
option_transition_var = tk.StringVar(GUI)
option_transition_var.set(OPTIONS_transition[0])  # default value

window_transition_menu = tk.OptionMenu(GUI, option_transition_var, *OPTIONS_transition)
window_transition_menu.pack(side=tk.TOP, fill=tk.BOTH)

getsize()
getmode()
getngen()
current_board = np.zeros(shape=(size, size))

# Canvas and Figure

canvas_frame = tk.Frame(GUI, width=500, height=400, bd=1)
canvas_frame.pack()


def create_figure():
    global f, canvas
    f = plt.figure(figsize=(3, 3), dpi=100)
    canvas = FigureCanvasTkAgg(f, master=canvas_frame)
    canvas.show()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    canvas.tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


create_figure()


# toolbar = NavigationToolbar2TkAgg(canvas, GUI)
# toolbar.update()

# Game of life


def count_neighbours(board):
    # Great cheat - calculate the number of neighbours using convolution
    # matrix, substract self.board = we do not want to count all cells, but only
    # the neighbours
    ncount = convolve2d(board, np.ones((3, 3)),
                        mode='same', boundary='fill') - board
    neighbours_count = np.array(ncount)
    return neighbours_count

    # print self.neighbours_count
    # return (neighbours_count == 3) | (self.board & (neighbours_count == 2))


def make_step(board):
    global size
    getsize()
    neighbours_count = count_neighbours(board)
    # We want to check the actual board and not the board that exists after eg. step 2.
    board_new = np.zeros(shape=(size, size))

    # 1. Any live cell with fewer than two live neighbours dies, as if caused by under-population.
    mask = (board == 1) & (neighbours_count < 2)
    board_new[mask] = 0

    # 2. Any live cell with two or three live neighbours lives on to the next generation.
    mask1 = (board == 1) & (neighbours_count == 2)
    board_new[mask1] = 1
    mask2 = (board == 1) & (neighbours_count == 3)
    board_new[mask2] = 1

    # 3. Any live cell with more than three live neighbours dies, as if by overcrowding.
    mask = (board == 1) & (neighbours_count > 3)
    board_new[mask] = 0

    # 4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
    mask = (board == 0) & (neighbours_count == 3)
    board_new[mask] = 1

    new_board = board_new

    return new_board


def random_start():
    getsize()
    global First, current_board, size
    First = True
    if size % 2 != 0:
        size += 1
    board = np.zeros(shape=(size, size))
    # Random start
    r = np.random.random((size - size / 2, size - size / 2))
    r[r >= 0.75] = 1
    r[r < 0.75] = 0
    board[size / 4:size - size / 4, size / 4:size - size / 4] = r
    current_board = board
    return board


First = True
Start = False
counter = 0


def game_of_life(board):
    global First, canvas, plot, Start, counter, current_generation, current_board
    Start = True
    # first time board should be already simulated !
    if First:
        current_generation = 0
        current_board = board
        current_board_img = create_board(board)
        plot = plt.imshow(current_board_img, cmap="Greys", interpolation="nearest")
        # canvas_text = plt.
        canvas.show()
        First = False
    else:
        current_board_img = create_board(board)
        plot.set_data(current_board_img)
        canvas.show()
    return


def start_up():  # Called for the first time to set up the board and decide on manual/auto advancing
    global evolutions, start_shape
    getmode()  # getmode() in order to find current mode set up
    getngen()
    getsize()
    evolutions = np.zeros((size, size, ngen+1))  # Stores every generation

    if start_shape == "Random Start":
        board = random_start()
    else:
        board = put_in_center(start_shape)

    if not mode:  # Manual advancing
        button_next.config(state=tk.NORMAL)  # Button next becomes click-able
        game_of_life(board)

    else:  # Automatic advancing
        game_of_life(board)
        button_next.config(state=tk.DISABLED)  # Disable next button

        for i in range(ngen):
            # print(i)
            next_step()
            time.sleep(0.5)
    return


def next_step():  # Makes Game of Life step
    global current_board, First, canvas, status_string_var, ngen
    change_status()
    current_board = make_step(current_board)
    game_of_life(current_board)


def change_status():  # Changes number of generation in the Output text-frame, fills evolutions vector
    global status_string_var, current_generation, text_frame_text, evolutions, current_board

    evolutions[:, :, current_generation] = current_board[:, :]  # Store every generation into evolutions
    current_generation += 1

    if current_generation != ngen:
        status_string_var = "Current generation: " + str(current_generation)
        text_frame_text.config(text=status_string_var)
    else:
        status_string_var = "Game of Life has ended after " + str(ngen) + " iterations."
        text_frame_text.config(text=status_string_var)

text_frame_label = tk.Label(GUI, text="Output:")
text_frame_label.pack(side=tk.TOP, fill=tk.BOTH)

text_frame = tk.Frame(GUI, width=350, height=50, bd=1, bg="Red")
text_frame.pack(side=tk.TOP, fill=tk.BOTH, anchor=tk.NE)

text_frame_text = tk.Label(text_frame, text=status_string_var)
text_frame_text.pack(side=tk.TOP, fill=tk.BOTH, anchor=tk.NE)

button_start = tk.Button(GUI, text="Start", command=lambda: start_up())
button_start.pack(side=tk.TOP, fill=tk.BOTH)

button_next = tk.Button(GUI, text="Next", command=next_step)
button_next.pack(side=tk.TOP, fill=tk.BOTH)

button_quit = tk.Button(GUI, text="Quit", command=_quit)
button_quit.pack(side=tk.TOP, fill=tk.BOTH)


# Game of Life ---------------------------------------------------------------------------------------------------------

GUI.mainloop()

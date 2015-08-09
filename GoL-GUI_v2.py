__author__ = 'Kubisjak'

import tkinter as tk
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


def testvariable():
    print("Starting position: " + option_start_var.get())
    print("Number of generations: " + option_ngen_var.get())
    print("Grid size: " + option_gsize_var.get())
    print("Transition mode: " + option_transition_var.get())
    return


def create_board(board):
    getsize()
    # Creates empty board image
    board_image = np.zeros((size, size, 3))
    board_image[:, :, 0] = board[:, :]
    board_image[:, :, 1] = board[:, :]
    board_image[:, :, 2] = board[:, :]
    return board_image


# Initialize
GUI = tk.Tk()
status_string_var = "Game of Life is not running yet."
current_generation = 0
should_end = False

# GUI.geometry("0+0")
GUI.title("01SSS - Game of Life")

# Option Bar with startin points
header = tk.Label(text="Select starting value")
header.pack(side=tk.TOP, fill=tk.BOTH)

OPTIONS_start = ["Random Start", "Item 1", "Item 2"]
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


def start_up(board):  # Called for the first time to set up the board and decide on manual/auto advancing
    global evolutions, should_end
    getmode()  # getmode() in order to find current mode set up
    getngen()
    getsize()
    evolutions = np.zeros((size, size, ngen+1))  # Stores every generation

    if not mode:  # Manual advancing
        button_next.config(state=tk.NORMAL)  # Button next becomes click-able
        game_of_life(board)
        print("Automatic advancing is ", mode)

    else:  # Automatic advancing
        print("Automatic advancing is ", mode)
        game_of_life(board)
        button_next.config(state=tk.DISABLED)  # Disable next button

        for i in range(ngen):
            print(i)
            next_step()
            time.sleep(0.5)

            if should_end:  # Checks if the game should have ended
                break
    return


def next_step():  # Makes Game of Life step
    global current_board, First, canvas, status_string_var, ngen
    change_status()
    if not should_end:
            current_board = make_step(current_board)
            game_of_life(current_board)


def change_status():  # Changes number of generation in the Output text-frame, fills evolutions vector
    global status_string_var, current_generation, text_frame_text, evolutions, current_board

    evolutions[:, :, current_generation] = current_board[:, :]  # Store every generation into evolutions
    end_check()
    print(evolutions[:, :, current_generation])
    current_generation += 1

    status_string_var = "Current generation: " + str(current_generation)
    text_frame_text.config(text=status_string_var)


def end_check():  # Checks if the Game of Life should end due to periodicity or kill
    global evolutions, current_generation, status_end_string_var, should_end, text_frame_text

    if (current_generation >= 1) & \
            (np.array_equal(evolutions[:, :, current_generation], evolutions[:, :, current_generation - 1])):

        should_end = True
        status_end_string_var = "Game of Life has ended after " + str(current_generation) + " generations."
        text_frame_text.config(text=status_end_string_var)

    elif (current_generation >= 2) & \
            (np.array_equal(evolutions[:, :, current_generation], evolutions[:, :, current_generation - 2])):

        should_end = True
        status_end_string_var = "Game of Life has ended after " + str(current_generation) + " generations."
        text_frame_text.config(text=status_end_string_var)

    elif current_generation == ngen:
        status_end_string_var = "Game of Life has ended after " + str(current_generation) + " generations."
        text_frame_text.config(text=status_end_string_var)
        should_end = True

    else:
        should_end = False

    print("Should end: ", should_end)
    return should_end


text_frame_label = tk.Label(GUI, text="Output:")
text_frame_label.pack(side=tk.TOP, fill=tk.BOTH)

text_frame = tk.Frame(GUI, width=350, height=50, bd=1, bg="Red")
text_frame.pack(side=tk.TOP, fill=tk.BOTH, anchor=tk.NE)

text_frame_text = tk.Label(text_frame, text=status_string_var)
text_frame_text.pack(side=tk.TOP, fill=tk.BOTH, anchor=tk.NE)

button_start = tk.Button(GUI, text="Start", command=lambda: start_up(random_start()))
button_start.pack(side=tk.TOP, fill=tk.BOTH)

button_next = tk.Button(GUI, text="Next", command=next_step)
button_next.pack(side=tk.TOP, fill=tk.BOTH)

button_quit = tk.Button(GUI, text="Quit", command=_quit)
button_quit.pack(side=tk.TOP, fill=tk.BOTH)


# Game of Life ---------------------------------------------------------------------------------------------------------

GUI.mainloop()

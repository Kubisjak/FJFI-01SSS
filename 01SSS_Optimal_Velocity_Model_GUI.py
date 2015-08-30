__author__ = 'Kubisjak'

"""
Created for 01SSS at FNSPE, CTU in Prague

Assignment: Create an Optimal Velocity model with
 - time dependent parameters
 - with reaction delay
 - optional: create GUI

"""

# Imports --------------------------------------------------------------------------------------------------------------
import tkinter as tk
from tkinter import ttk
import time
import numpy as np
import matplotlib
# from matplotlib.figure import Figure
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # NavigationToolbar2TkAgg
# ----------------------------------------------------------------------------------------------------------------------
plt.rcParams["toolbar"] = "None"  # Do not display toolbar when calling plot
# Support functions:


def _quit():
    GUI.quit()
    GUI.destroy()


def shift_plot():
    global plotShift
    x = xx[:, plotShift]
    plot(x, y)
    if plotShift < np.shape(xx)[1] - 1:
        plotShift += 1
        print(plotShift)
    else:
        print("Finished all iterations.")


def plot(x, y):
    global x_limit
    plt.clf()
    plt.plot(x, y, "ro")
    plt.tick_params(
        axis="both",
        which="both",
        bottom="off",
        top="off",
        labelbottom="on",
        right="off",
        left="off",
        labelleft="off")
    plt.xlim(0, x_limit)
    plt.tight_layout()
    plt.gcf().canvas.draw()


def auto():
    global sleep_interval
    init()
    for i in range(n - 1):  # starting value 0 -> range n-1
        time.sleep(sleep_interval)
        shift_plot()


def optimal_velocity_function(dx, d_safe, v_max):
    vx_opt = v_max * (np.tanh(dx - d_safe) + np.tanh(d_safe))
    return vx_opt


def euler_method(x, v, n_cars, h, tau, d_safe, v_max):
    # Euler method used to solve ODE
    # returns new position of car and its new velocity
    dv = np.zeros(n_cars)

    for j in range(n_cars - 1):
            dv[j] = tau ** (-1) * (optimal_velocity_function(x[j+1] - x[j], d_safe, v_max) - v[j])

    dv[n_cars - 1] = tau ** (-1) * (v_max - v[n_cars - 1])  # Speed of first car

    x_new = x + h * v
    v_new = v + h * dv

    return [x_new, v_new]


def optimal_velocity_model(n, n_cars, d_0, v_0, h, tau, d_safe, v_max):
    global x_limit, canvas, xx, vv

    car_positions = np.linspace(0, n_cars, n_cars)
    x = np.array(sorted(np.random.random(n_cars) + car_positions))  # Generation of cars with minimal distance
    x = x * d_0
    v = np.random.random(n_cars) + v_0  # Generating initial speeds not greater than v_0
    xx = np.zeros([n_cars, n])  # Matrix of locations
    vv = np.zeros([n_cars, n])  # Matrix of velocities

    for i in range(n):
        xx[:, i] = x
        vv[:, i] = v
        [x, v] = euler_method(x, v, n_cars, h, tau, d_safe, v_max)
    x_limit = xx.max()  # Interval in which will cars be


def init():
    # Sets initial global parameters
    global n_cars, d_0, tau, d_safe, v_0, v_max, plotShift, y, h, n, fps, sleep_interval, length
    n_cars_int = n_cars.get()  # number of cars
    d_0_int = d_0.get()  # initial distance
    tau_int = tau.get()  # acceleration parameter
    d_safe_int = d_safe.get()  # minimal safe distance
    v_0_int = v_0.get()  # initial speed
    v_max_int = v_max.get()  # maximum speed

    # Plotting parameters:
    plotShift = 0
    y = np.linspace(0, 0, n_cars_int)

    # Animation parameters:
    fps = 60
    sleep_interval = 1. / fps

    # Numeric parameters:
    h = 0.02  # step size in Euler's method
    n = length.get()  # number of simulation steps

    # OVM function:
    optimal_velocity_model(n, n_cars_int, d_0_int, v_0_int, h, tau_int, d_safe_int, v_max_int)


# def time_space_diagram_plot():
#     # Time-space diagram canvas frame
#     global xx, n_cars, n
#     canvas_frame_2 = tk.Frame(GUI, bd=1)
#     canvas_frame_2.grid(row=8, column=0)
#     g = plt.figure(figsize=(1, 1), dpi=150)
#     canvas = FigureCanvasTkAgg(g, master=canvas_frame_2)
#     canvas.show()
#     canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH)
#     canvas.tkcanvas.pack(side=tk.TOP, fill=tk.BOTH)
#
#     for i in range(n_cars.get()):
#         plt.plot(xx[i, :], range(n))
#     plt.tight_layout()
#     plt.gcf().canvas.draw()


def start_red_light():
    global n_cars, d_0, tau, d_safe, v_0, v_max, plotShift, y, h, n, fps, sleep_interval, length
    n_cars.set(5)
    d_0.set(1)
    tau.set(2)
    d_safe.set(2)
    v_0.set(0)
    v_max.set(100)
    length.set(100)

# GUI Code -------------------------------------------------------------------------------------------------------------
GUI = tk.Tk()
GUI.title("01SSS - Optimal Velocity Model")

# Create Canvas --------------------------------------------------------------------------------------------------------
GUI.grid_columnconfigure(0, weight=1)
GUI.grid_columnconfigure(1, weight=1)
GUI.grid_columnconfigure(2, weight=10)

# Animation canvas frame
canvas_frame = tk.Frame(GUI, bd=1)
canvas_frame.grid(row=8, column=0, columnspan=3)
f = plt.figure(figsize=(6, 1), dpi=150)
canvas = FigureCanvasTkAgg(f, master=canvas_frame)
canvas.show()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH)
canvas.tkcanvas.pack(side=tk.TOP, fill=tk.BOTH)

# Creating buttons:
header = tk.Label(GUI, text="Select parameters: ")
header.grid(row=0, column=0, sticky=tk.E)

button1 = ttk.Button(GUI, text="Make Step", command=lambda: shift_plot())
button1.grid(row=3, column=2, rowspan=2, sticky=tk.N + tk.S + tk.W + tk.E)

button2 = ttk.Button(GUI, text="Start", command=lambda: auto())
button2.grid(row=1, column=2, rowspan=2, sticky=tk.W + tk.E + tk.N + tk.S)

button2 = ttk.Button(GUI, text="RedLight Start", command=lambda: start_red_light())
button2.grid(row=5, column=2, rowspan=2, sticky=tk.W + tk.E + tk.N + tk.S)

button_quit = ttk.Button(GUI, text="Quit", command=_quit)
button_quit.grid(row=7, column=2, sticky=tk.W + tk.E + tk.N + tk.S)

# Parameter frame: -----------------------------------------------------------------------------------------------------
# Creates frame where the entry boxes required for parameter input are stored

# Number of cars
n_cars = tk.IntVar(GUI)  # Create IntVariable called n_cars
label_n_cars = tk.Label(GUI, text="Number of cars: ")  # Create label for parameter
label_n_cars.grid(row=1, column=0, sticky=tk.E)  # Place label on grid
entry_n_cars = tk.Entry(GUI, textvariable=n_cars)  # Create entry widget
entry_n_cars.grid(row=1, column=1, sticky=tk.W + tk.E)  # Place entry widget on grid

# Initial distance
d_0 = tk.IntVar(GUI)
label_d_0 = tk.Label(GUI, text="Initial distance: ")
label_d_0.grid(row=2, column=0, sticky=tk.E)
entry_d_0 = tk.Entry(GUI, textvariable=d_0)
entry_d_0.grid(row=2, column=1, sticky=tk.W + tk.E + tk.N + tk.S)

# Acceleration parameter
tau = tk.DoubleVar(GUI)  # DoubleVar holds float variable
label_tau = tk.Label(GUI, text="Acceleration parameter Tau: ")
label_tau.grid(row=3, column=0, sticky=tk.E)
entry_tau = tk.Entry(GUI, textvariable=tau)
entry_tau.grid(row=3, column=1, sticky=tk.W + tk.E + tk.N + tk.S)

# Minimal safe distance
d_safe = tk.IntVar(GUI)
label_d_safe = tk.Label(GUI, text="Minimal safe distance: ")
label_d_safe.grid(row=4, column=0, sticky=tk.E)
entry_d_safe = tk.Entry(GUI, textvariable=d_safe)
entry_d_safe.grid(row=4, column=1, sticky=tk.W + tk.E + tk.N + tk.S)

# Initial speed
v_0 = tk.IntVar(GUI)
label_v_0 = tk.Label(GUI, text="Initial speed: ")
label_v_0.grid(row=5, column=0, sticky=tk.E)
entry_v_0 = tk.Entry(GUI, textvariable=v_0)
entry_v_0.grid(row=5, column=1, sticky=tk.W + tk.E + tk.N + tk.S)

# Maximum speed
v_max = tk.IntVar(GUI)
label_v_max = tk.Label(GUI, text="Maximum speed: ")
label_v_max.grid(row=6, column=0, sticky=tk.E)
entry_v_max = tk.Entry(GUI, textvariable=v_max)
entry_v_max.grid(row=6, column=1, sticky=tk.W + tk.E + tk.N + tk.S)

# Length of animation
length = tk.IntVar(GUI)
label_time = tk.Label(GUI, text="Number of steps: ")
label_time.grid(row=7, column=0, sticky=tk.E)
entry_time = tk.Entry(GUI, textvariable=length)
entry_time.grid(row=7, column=1, sticky=tk.W + tk.E + tk.N + tk.S)

# Initialization -------------------------------------------------------------------------------------------------------
# Set default parameters
n_cars.set(20)  # Set default value for n_cars
d_0.set(15)
tau.set(4)
d_safe.set(10)
v_0.set(15)
v_max.set(100)
length.set(100)

init()

print(xx)

GUI.mainloop()

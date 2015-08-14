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
import math
import time
import numpy as np
import scipy
from scipy.signal import convolve2d
import matplotlib
# from matplotlib.figure import Figure
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # NavigationToolbar2TkAgg
plt.rcParams["toolbar"] = "None"
# ----------------------------------------------------------------------------------------------------------------------

# Support functions:


def optimal_velocity_function(dx, d_safe, v_max):
    dx_opt = 0.5*v_max*(np.tanh(dx-d_safe)+np.tanh(d_safe))
    return dx_opt


def euler_method(x, v, n_cars, h, tau, d_safe, v_max):
    # Euler method used to solve ODE
    # returns new position of car and its new velocity
    dv = np.zeros(n_cars)

    for j in range(n_cars-1):
        dv[j] = tau**(-1)*(optimal_velocity_function(x[j+1] - x[j], d_safe, v_max) - v[j])

    dv[n_cars-1] = tau**(-1)*(v_max-v[n_cars-1])

    x_new = x + h * v
    v_new = v + h * dv

    return [x_new, v_new]


def optimal_velocity_model(n, n_cars, d_0, v_0, h, tau, d_safe, v_max):
    global x_limit, canvas

    car_positions = np.linspace(0, n_cars, n_cars)
    x = np.array(sorted(np.random.random(n_cars) + car_positions))  # Generation of cars with minimal distance
    x = x * d_0
    v = np.random.random(n_cars) * v_0  # Generating initial speeds greater than v_0
    xx = np.zeros([n_cars, n])  # Matrix of locations
    vv = np.zeros([n_cars, n])  # Matrix of velocities
    x_limit = max(x) + max(x)/2

    # Creating figure and graph area
    graph1 = f.add_subplot(211)
    graph1.plot(x, np.linspace(0, 0, n_cars), "ro")
    graph1.set_title("Optimal Velocity model Animation")
    graph1.tick_params(
        axis="both",
        which="both",
        bottom="off",
        top="off",
        labelbottom="on",
        right="off",
        left="off",
        labelleft="off")
    canvas.show()

    for i in range(n):
        xx[:, i] = x
        vv[:, i] = v
        x, v = euler_method(x, v, n_cars, h, tau, d_safe, v_max)

        # Motion plotting area ---------------------------------
        # time.sleep(0.05)
        # graph1.clear()
        # graph1.plot(x, np.linspace(0, 0, n_cars), "ro")
        # graph1.set_xlim(0, x_limit)
        # canvas.draw()

    for i in range(n_cars):
        graph2 = f.add_subplot(212)
        graph2.plot(xx[i, :], range(n))
        f.tight_layout()


# GUI Code ------------------------------------------------------------------------
GUI = tk.Tk()
GUI.title("01SSS - Optimal Velocity Model")

canvas_frame = tk.Frame(GUI, bd=1)
canvas_frame.pack()

f = plt.figure(figsize=(7, 3), dpi=150)
# Create Canvas
canvas = FigureCanvasTkAgg(f, master=canvas_frame)
canvas.show()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
canvas.tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)ň

# # Physical parameters:
# n_cars = 50  # number of cars
# d_0 = 10  # minimal initial distance
# tau = 2  # acceleration parameter
# d_safe = 2  # minimal safe distance
# v_0 = 10  # initial speed
# v_max = 100  # maximum speed
#
# # Numeric parameters:
# h = 0.02  # step size in Euler's method
# n = 100  # number of simulation steps


# Setting up parameters for testing:

# Physical parameters:
n_cars = 20  # number of cars
d_0 = 15  # initial distance
tau = 2  # acceleration parameter
d_safe = 5  # minimal safe distance
v_0 = 15  # initial speed
v_max = 100  # maximum speed

# Numeric parameters:
h = 0.02  # step size in Euler's method
n = 100  # number of simulation steps

optimal_velocity_model(n, n_cars, d_0, v_0, h, tau, d_safe, v_max)

GUI.mainloop()

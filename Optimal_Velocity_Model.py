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
# ----------------------------------------------------------------------------------------------------------------------

# Support functions:


def optimal_velocity_function(dx, d_safe, v_max):
    dx_opt = 0.5*v_max*(np.tanh(dx-d_safe)+np.tanh(d_safe))
    return dx_opt

# Euler method used to solve ODE


def euler_method(x, v, n_cars, h, tau, d_safe, v_max):
    dv = np.zeros(n_cars)

    for j in range(n_cars-1):
        dv[j] = tau**(-1)*(optimal_velocity_function(x[j+1] - x[j], d_safe, v_max) - v[j])

    dv[n_cars-1] = tau**(-1)*(v_max-v[n_cars-1])
    print(dv)

    x_new = x + h * v
    print("V is: ", v)
    v_new = v + h * dv
    print("V_new is: ", v_new)

    return x_new, v_new


def optimal_velocity_model(n, n_cars, d_0, v_0, h, tau, d_safe, v_max):

    car_positions = np.linspace(0, 1, n_cars)
    x = np.array(sorted(np.random.random(n_cars) + car_positions)) * d_0  # Generation of cars with minimal distance
    v = np.random.random(n_cars) * v_0  # Generating initial speeds greater than v_0

    xx = np.zeros([n_cars, n])
    vv = np.zeros([n_cars, n])

    for i in range(n):
        xx[:, i] = x
        vv[:, i] = v
        [x, v] = euler_method(x, v, n_cars, h, tau, d_safe, v_max)

    for i in range(n_cars):
        plt.plot(xx[i, :], range(n))
    plt.show()

    return


# Setting up parameters for testing:

# Physical parameters:
n_cars = 50  # number of cars
d_0 = 10  # minimal initial distance
tau = 2  # acceleration parameter
d_safe = 2  # minimal safe distance
v_0 = 10  # initial speed
v_max = 100  # maximum speed

# Numeric parameters:
h = 0.02  # step size in Euler's method
n = 100  # number of simulation steps

optimal_velocity_model(n, n_cars, d_0, v_0,h, tau, d_safe, v_max)
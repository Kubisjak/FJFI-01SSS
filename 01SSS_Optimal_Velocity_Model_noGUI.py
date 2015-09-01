# Imports --------------------------------------------------------------------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt
# ----------------------------------------------------------------------------------------------------------------------

# Support functions:

def optimal_velocity_function(dx, d_safe, v_max):
    vx_opt = 0.5 * v_max * (np.tanh(dx - d_safe) + np.tanh(d_safe))
    return vx_opt


def euler_method(x, v, n_cars, h, t, tau, d_safe, v_max):
    # Euler method used to solve ODE
    # returns new position of car and its new velocity
    dv = np.zeros(n_cars)

    for j in range(n_cars - 1):
            dv[j] = (tau ** (-1)) * (optimal_velocity_function(x[j+1] - x[j], d_safe, v_max) - v[j])
    
    # Original speed of first car
    dv[n_cars - 1] = (tau ** (-1)) * (v_max - v[n_cars - 1])  
    
    # Acceleration of the first car - at least one braking in the middle of 
    # simulation
    dv[n_cars - 1] = (tau ** (-1)) * 0.7 * v_max * np.cos(3*np.linspace(0, 2 * np.pi, n)[t])
    
    x_new = x + (h * v)
    v_new = v + (h * dv)
    
    # Condition for case if both car acceleration and speed are negative:
    if v_new[n_cars - 1] <0:
        v_new[n_cars - 1] = 0
    
    # Condition to stop overtake - if the distance is less than d_safe, then 
    # down to 0.8 speed of car before
    for j in range(n_cars - 1):
        if x_new[j+1] - x_new[j] < d_safe:
            v_new[j] = 0.9 * v[j+1]
            
    return [x_new, v_new]


def optimal_velocity_model(n, n_cars, d_0, v_0, h, tau, d_safe, v_max):
    global x_limit, canvas, xx, vv

    car_positions = np.linspace(0, n_cars, n_cars)
    x = np.array(sorted(np.random.random(n_cars) + car_positions))  # Generation of cars with minimal distance
    x = x * d_0
    v = np.ones(n_cars) * v_0  # Generating initial speeds around v_0
    xx = np.zeros([n_cars, n])  # Matrix of locations
    vv = np.zeros([n_cars, n])  # Matrix of velocities

    for i in range(n):
        xx[:, i] = x
        vv[:, i] = v
        [x, v] = euler_method(x, v, n_cars, h, i, tau, d_safe, v_max)

    x_limit = xx.max()  # Interval in which will cars be
    return


# Setting up parameters for testing:

# Physical parameters:
n_cars = 100  # number of cars
d_0 = 10  # initial distance
tau = 1  # acceleration parameter
d_safe = 10  # minimal safe distance
v_0 = 0  # initial speed
v_max = 100  # maximum speed

# Numeric parameters:
h = 0.02  # step size in Euler's method
n = 500  # number of simulation steps

optimal_velocity_model(n, n_cars, d_0, v_0,h, tau, d_safe, v_max)

for i in range(n_cars):
    plt.plot(xx[i, :], range(n))
plt.xlabel("Distance")
plt.ylabel("Time")
plt.title("Time space diagram")
plt.title("n_cars=100, d_safe=10, v_max=100")
plt.savefig('/Users/Kubisjak/Google Drive/Skola/SSS/TSD.eps', bbox="tight", format='eps', dpi=1200)
plt.show()
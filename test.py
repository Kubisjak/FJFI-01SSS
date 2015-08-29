__author__ = 'Kubisjak'

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
from matplotlib.figure import Figure
# ----------------------------------------------------------------------------------------------------------------------

def on_button_click():
    global i
    i += 1

plotShift = 0

def main():
    global plotShift
    x = np.arange(0.0,3.0,0.01)
    y = np.sin(2*np.pi*x + plotShift)
    plot(x, y)
    plotShift += 1


def plot(x, y):
    plt.clf()
    plt.plot(x, y)
    plt.gcf().canvas.draw()

GUI = tk.Tk()
GUI.title("Figure Test")


n_cars = tk.IntVar(GUI)
n_cars.set("20")
print(n_cars)


button1 = tk.Button(GUI, text="Next", command=lambda: main())
button1.pack(side=tk.TOP, fill=tk.BOTH)

canvas_frame = tk.Frame(GUI, bd=1)
canvas_frame.pack()

f = plt.figure(figsize=(5, 4), dpi=100)
graph = f.add_subplot(111)
# t = np.arange(0.0, 3.0, 0.01)
# s = np.sin(t)

# a tk.DrawingArea
canvas = FigureCanvasTkAgg(f, master=canvas_frame)
canvas.show()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)


# for i in range(4):
#     s = (i+1)*np.sin(t)
#     input("Press Enter to continue...")
#     line1.set_data(t, s)
#     ax = canvas.figure.axes[0]
#     ax.set_xlim(min(t), max(t))
#     ax.set_ylim(min(s), max(s))
#     canvas.draw()




GUI.mainloop()
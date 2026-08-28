
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
     FigureCanvasTkAgg, NavigationToolbar2Tk)
import tkinter as tk
import numpy as np

df = pd.read_csv('data.csv')  # we read data from a csv file into a DF for plotting later

df2 = df['Maxpulse']  # focus on just one column of values for the plot


def on_closing():
    root.quit()
    root.destroy()


# Initialize Tkinter and Matplotlib Figure
root = tk.Tk()
fig, ax = plt.subplots()  # this is a way to place an axes on the plotting figure space

# Tkinter Application
frame = tk.Frame(root)
label = tk.Label(text="Matplotlib + Tkinter!")
label.config(font=("Courier", 32))
label.pack()
frame.pack()

# Create Canvas
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Plot data on Matplotlib Figure
ax.plot(df2)
canvas.draw()

# Create Toolbar
toolbar = NavigationToolbar2Tk(canvas, root, pack_toolbar=False)
toolbar.update()
toolbar.pack(side=tk.BOTTOM, fill=tk.X)

root.protocol("WM_DELETE_WINDOW", on_closing)  # introduced to close reluctant tkinter window
root.mainloop()

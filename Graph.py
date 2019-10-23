import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import json


class Graph(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.fig = Figure(figsize=(10, 7), dpi=100, tight_layout=True)
        self.fig.set_facecolor('#f0f0ed')

        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def redraw(self, input_file_location):
        json_file = open(input_file_location, "r")
        data = json.load(json_file)
        json_file.close()
        x_data = []
        y_data = []
        for time in data['recording']['path']:
            x_data.append(time['x'])
            y_data.append(time['y'])
        self.fig.clear()
        self.fig.add_subplot(111, frameon=False).scatter(x_data, y_data)
        self.canvas.draw()

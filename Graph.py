import numpy as np
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.pyplot import Figure
import json
import GraphInteractions


class Graph(tk.Frame):
    ax, original_xlim, original_ylim, coll = None, None, None, None
    data = []

    def __init__(self, master):
        super().__init__(master)
        self.fig = Figure(figsize=(10, 7), dpi=100, tight_layout=True)
        self.fig.set_facecolor('#f0f0ed')

        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def redraw(self, input_file_location):
        self.fig.clear()
        self.ax = self.fig.add_subplot(111, frameon=False, picker=10)
        self.coll = self.ax.scatter(self.data[0, :], self.data[1, :], color=self.data[4, :])
        zoom_pan = GraphInteractions.ZoomPan()
        zoom_fac = GraphInteractions.ZoomPan.zoom_factory(zoom_pan, self.ax, base_scale=1.3)
        pan_fac = GraphInteractions.ZoomPan.pan_factory(zoom_pan, self.ax)
        self.canvas.mpl_connect('pick_event', self.change_color)
        self.original_xlim = self.ax.get_xlim()
        self.original_ylim = self.ax.get_ylim()
        self.canvas.draw()

    def reset_zoom(self):
        self.ax.set_xlim(self.original_xlim)
        self.ax.set_ylim(self.original_ylim)
        self.ax.figure.canvas.draw()  # force re-draw

    def read_data(self, input_file_location):
        x_array = []
        y_array = []
        z_array = []
        t_array = []
        color_array = []
        json_file = open(input_file_location, "r")
        data = json.load(json_file)
        json_file.close()
        for time in data['recording']['path']:
            x_array.append(time['x'])
            y_array.append(time['y'])
            z_array.append(time['z'])
            t_array.append(time['t'])
        return zip(x_array, y_array, z_array, t_array)
            color_array.append('tab:blue')

    def change_color(self, event):
        print('you picked:', event.artist)
        self.canvas.draw()


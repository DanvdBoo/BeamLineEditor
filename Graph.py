import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.pyplot import Figure
import json


class Graph(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.fig = Figure(figsize=(10, 7), dpi=100, tight_layout=True)
        self.fig.set_facecolor('#f0f0ed')

        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.navigation_toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.connect(self.canvas)

    def redraw(self, input_file_location):
        x, y, z, t = zip(*self.read_data(input_file_location))
        self.fig.clear()
        self.fig.add_subplot(111, frameon=False).scatter(x, y)
        self.canvas.draw()
        self.connect(self.canvas)

    @staticmethod
    def read_data(input_file_location):
        x_array = []
        y_array = []
        z_array = []
        t_array = []
        json_file = open(input_file_location, "r")
        data = json.load(json_file)
        json_file.close()
        for time in data['recording']['path']:
            x_array.append(time['x'])
            y_array.append(time['y'])
            z_array.append(time['z'])
            t_array.append(time['t'])
        return zip(x_array, y_array, z_array, t_array)

    def connect(self, canvas):
        canvas.mpl_connect('button_press_event', onpick)
        canvas.mpl_connect('scroll_event', self.zoom)

    def zoom(self, event):
        self.navigation_toolbar.zoom(event)


def onpick(event):
    print('you pressed', event.button, event.xdata, event.ydata)

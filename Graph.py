import math
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.pyplot import Figure
import json


class Graph(tk.Frame):
    ax, original_xlim, original_ylim = None, None, None

    def __init__(self, master):
        super().__init__(master)
        self.fig = Figure(figsize=(10, 7), dpi=100, tight_layout=True)
        self.fig.set_facecolor('#f0f0ed')

        self.canvas = FigureCanvasTkAgg(self.fig, self)
        # self.navigation_toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.connect(self.canvas)

    def redraw(self, input_file_location):
        x, y, z, t = zip(*self.read_data(input_file_location))
        self.fig.clear()
        self.ax = self.fig.add_subplot(111, frameon=False)
        self.ax.scatter(x, y)
        zoom_fac = zoom_factory(self.ax, base_scale=2.)
        self.original_xlim = self.ax.get_xlim()
        self.original_ylim = self.ax.get_ylim()
        self.canvas.draw()
        self.connect(self.canvas)

    def reset_zoom(self):
        self.ax.set_xlim(self.original_xlim)
        self.ax.set_ylim(self.original_ylim)
        self.ax.figure.canvas.draw()  # force re-draw

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
        canvas.mpl_connect('button_press_event', self.onpick)

    def onpick(self, event):
        print("onpick")


def zoom_factory(ax, base_scale=2.):
    def zoom_fun(event):
        # get the current x and y limits
        cur_xlim = ax.get_xlim()
        cur_ylim = ax.get_ylim()
        # set the range
        cur_xrange = (cur_xlim[1] - cur_xlim[0])*.5
        cur_yrange = (cur_ylim[1] - cur_ylim[0])*.5
        xdata = event.xdata # get event x location
        ydata = event.ydata # get event y location
        if event.button == 'up':
            # deal with zoom in
            scale_factor = 1/base_scale
        elif event.button == 'down':
            # deal with zoom out
            scale_factor = base_scale
        else:
            # deal with something that should never happen
            scale_factor = 1
            print(event.button)
        # set new limits
        ax.set_xlim([xdata - cur_xrange*scale_factor,
                     xdata + cur_xrange*scale_factor])
        ax.set_ylim([ydata - cur_yrange*scale_factor,
                     ydata + cur_yrange*scale_factor])
        ax.figure.canvas.draw() # force re-draw

    fig = ax.get_figure() # get the figure of interest
    # attach the call back
    fig.canvas.mpl_connect('scroll_event',zoom_fun)

    #return the function
    return zoom_fun

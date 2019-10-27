import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.pyplot import Figure
import json
import GraphInteractions


class Graph(tk.Frame):
    ax, original_xlim, original_ylim, coll = None, None, None, None
    data = []
    connect_ids = []
    start, stop = None, None

    def __init__(self, master):
        super().__init__(master)
        self.fig = Figure(figsize=(10, 7), dpi=100, tight_layout=True)
        self.fig.set_facecolor('#f0f0ed')

        self.zoom_pan = GraphInteractions.ZoomPan()

        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def redraw(self, input_file_location):
        x, y, c = zip(*self.read_data(input_file_location))
        self.fig.clear()
        self.ax = self.fig.add_subplot(111, frameon=False)
        self.coll = self.ax.scatter(x, y, color=c, picker=True)
        self.data = self.coll.get_offsets()
        self.connect_ids.append(GraphInteractions.ZoomPan.zoom_factory(self.zoom_pan, self.ax, base_scale=1.3))
        self.connect_ids.extend(GraphInteractions.ZoomPan.pan_factory(self.zoom_pan, self.ax))
        self.connect_ids.append(self.canvas.mpl_connect('pick_event', self.change_color))
        self.original_xlim = self.ax.get_xlim()
        self.original_ylim = self.ax.get_ylim()
        self.canvas.draw()

    def reset_zoom(self):
        self.ax.set_xlim(self.original_xlim)
        self.ax.set_ylim(self.original_ylim)
        self.ax.figure.canvas.draw()  # force re-draw

    @staticmethod
    def read_data(input_file_location):
        x_array = []
        y_array = []
        color_array = []
        json_file = open(input_file_location, "r")
        data = json.load(json_file)
        json_file.close()
        for time in data['recording']['path']:
            x_array.append(time['x'])
            y_array.append(time['y'])
            color_array.append('tab:blue')
        return zip(x_array, y_array, color_array)

    def recolor(self, i):
        for cid in self.connect_ids:
            self.canvas.mpl_disconnect(cid)
        self.connect_ids.clear()
        x = []
        y = []
        for row in self.data:
            x.append(row[0])
            y.append(row[1])
        selected_x, selected_y = self.data[i][0]
        self.fig.clear()
        self.ax = self.fig.add_subplot(111, frameon=False)
        self.coll = self.ax.scatter(x, y, color='tab:blue', picker=True)
        self.ax.scatter(selected_x, selected_y, color='tab:red', picker=True)
        self.ax.set_xlim(self.zoom_pan.cur_xlim)
        self.ax.set_ylim(self.zoom_pan.cur_ylim)
        self.connect_ids.append(GraphInteractions.ZoomPan.zoom_factory(self.zoom_pan, self.ax, base_scale=1.3))
        self.connect_ids.extend(GraphInteractions.ZoomPan.pan_factory(self.zoom_pan, self.ax))
        self.connect_ids.append(self.canvas.mpl_connect('pick_event', self.change_color))
        self.canvas.draw()

    def change_color(self, event):
        if event.mouseevent.button != 1: return
        print(event.ind)
        self.recolor(event.ind)

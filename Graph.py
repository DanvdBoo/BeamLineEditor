import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.pyplot import Figure
import json
import GraphInteractions


class Graph(tk.Frame):
    ax, original_xlim, original_ylim, coll, pick_id = None, None, None, None, None
    move_id = None
    start_end_bool = -1  # 0 is start, 1 is end, -1 is None
    start_index, end_index, move_index = 0, None, None
    data = []
    connect_ids = []

    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.fig = Figure(figsize=(10, 7), dpi=100, tight_layout=True)
        self.fig.set_facecolor('#f0f0ed')

        self.zoom_pan = GraphInteractions.ZoomPan()
        self.master_string = tk.StringVar()

        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def redraw(self, input_file_location):
        x, y, c = zip(*self.read_data(input_file_location))
        self.fig.clear()
        self.ax = self.fig.add_subplot(111, frameon=False)
        self.coll = self.ax.scatter(x, y, color=c, picker=True)
        self.end_index = len(self.data) - 1
        self.connect_ids.append(GraphInteractions.ZoomPan.zoom_factory(self.zoom_pan, self.ax, base_scale=1.3))
        self.connect_ids.extend(GraphInteractions.ZoomPan.pan_factory(self.zoom_pan, self.ax))
        self.original_xlim = self.ax.get_xlim()
        self.original_ylim = self.ax.get_ylim()
        self.canvas.draw()

    def reset_zoom(self):
        self.ax.set_xlim(self.original_xlim)
        self.ax.set_ylim(self.original_ylim)
        self.ax.figure.canvas.draw()  # force re-draw

    def reset_start(self, master_string):
        self.start_index = 0
        master_string.set("")
        self.redraw_ext()

    def reset_end(self, master_string):
        self.end_index = len(self.data) - 1
        master_string.set("")
        self.redraw_ext()

    def read_data(self, input_file_location):
        x_array = []
        y_array = []
        color_array = []
        json_file = open(input_file_location, "r")
        file_data = json.load(json_file)
        json_file.close()
        for time in file_data['recording']['path']:
            x_array.append(time['x'])
            y_array.append(time['y'])
            self.data.append([time['x'], time['y']])
            color_array.append('tab:blue')
        return zip(x_array, y_array, color_array)

    def redraw_ext(self):
        for cid in self.connect_ids:
            self.canvas.mpl_disconnect(cid)
        self.connect_ids.clear()
        x = []
        y = []
        c = []
        for idx, row in enumerate(self.data):
            x.append(row[0])
            y.append(row[1])
            if idx < self.start_index or idx > self.end_index or\
                    (self.start_index == 0 and self.end_index == len(self.data) - 1):
                c.append('tab:blue')
            elif self.start_index < idx < self.end_index:
                c.append('c')
            elif idx == self.start_index or idx == self.end_index:
                c.append('tab:red')

        self.fig.clear()
        self.ax = self.fig.add_subplot(111, frameon=False)
        self.coll = self.ax.scatter(x, y, color=c, picker=True)
        self.ax.set_xlim(self.zoom_pan.cur_xlim)
        self.ax.set_ylim(self.zoom_pan.cur_ylim)
        self.connect_ids.append(GraphInteractions.ZoomPan.zoom_factory(self.zoom_pan, self.ax, base_scale=1.3))
        self.connect_ids.extend(GraphInteractions.ZoomPan.pan_factory(self.zoom_pan, self.ax))
        self.canvas.draw()

    def redraw_simp(self):
        for cid in self.connect_ids:
            self.canvas.mpl_disconnect(cid)
        self.connect_ids.clear()
        x = []
        y = []
        c = []
        for idx, row in enumerate(self.data):
            x.append(row[0])
            y.append(row[1])
            if idx == self.move_index:
                c.append('tab:red')
            else:
                c.append('tab:blue')
        self.fig.clear()
        self.ax = self.fig.add_subplot(111, frameon=False)
        self.coll = self.ax.scatter(x, y, color=c, picker=True)
        self.ax.set_xlim(self.zoom_pan.cur_xlim)
        self.ax.set_ylim(self.zoom_pan.cur_ylim)
        self.connect_ids.append(GraphInteractions.ZoomPan.zoom_factory(self.zoom_pan, self.ax, base_scale=1.3))
        self.connect_ids.extend(GraphInteractions.ZoomPan.pan_factory(self.zoom_pan, self.ax))
        self.canvas.draw()

    def change_color(self, event):
        if event.mouseevent.button != 1: return
        if self.start_end_bool == 0:
            self.start_index = event.ind[0]
        elif self.start_end_bool == 1:
            self.end_index = event.ind[0]
        self.redraw_ext()
        self.master_string.set('x: %.4f, y: %.4f' % (self.data[event.ind][0][0], self.data[event.ind][0][1]))

    def select_move(self, event):
        if event.mouseevent.button != 1: return
        self.move_index = event.ind[0]
        self.master.move_node_location.set('x: %.4f, y: %.4f' % (self.data[self.move_index][0],
                                                                 self.data[self.move_index][1]))
        self.redraw_simp()

    def attach_start_stop(self, master_string_var, start_end):
        self.detach_start_stop()
        self.start_end_bool = start_end
        self.master_string = master_string_var
        self.pick_id = self.canvas.mpl_connect('pick_event', self.change_color)

    def detach_start_stop(self):
        if self.pick_id is None: return
        self.start_end_bool = -1
        self.canvas.mpl_disconnect(self.pick_id)
        if self.move_id is None: return
        self.canvas.mpl_disconnect(self.move_id)

    def attach_move_node(self):
        self.detach_start_stop()
        self.pick_id = self.canvas.mpl_connect('pick_event', self.select_move)
        self.move_id = self.canvas.mpl_connect('key_press_event', self.move_node_button)

    def next_start(self, master_string, diff):
        self.start_index += diff
        if self.start_index < 0:
            self.start_index = 0
        self.redraw_ext()
        master_string.set('x: %.4f, y: %.4f' % (self.data[self.start_index][0], self.data[self.start_index][1]))

    def next_end(self, master_string, diff):
        self.end_index += diff
        if self.end_index > len(self.data) - 1:
            self.end_index = len(self.data) - 1
        self.redraw_ext()
        master_string.set('x: %.4f, y: %.4f' % (self.data[self.end_index][0], self.data[self.end_index][1]))

    def move_node_button(self, event):
        direction = ""
        if event.key == "up":
            direction = "N"
        elif event.key == "right":
            direction = "E"
        elif event.key == "down":
            direction = "S"
        elif event.key == "left":
            direction = "W"
        if direction != "":
            self.move_node(direction, float(self.master.move_entry.get()))

    def move_node(self, direction, distance):
        if direction == "N":
            self.data[self.move_index][1] += distance
        elif direction == "E":
            self.data[self.move_index][0] += distance
        elif direction == "S":
            self.data[self.move_index][1] -= distance
        elif direction == "W":
            self.data[self.move_index][0] -= distance
        self.master.move_node_location.set('x: %.4f, y: %.4f' % (self.data[self.move_index][0],
                                                                 self.data[self.move_index][1]))
        self.redraw_simp()

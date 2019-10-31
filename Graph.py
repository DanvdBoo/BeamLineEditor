import tkinter as tk

from matplotlib import colors
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.pyplot import Figure
import json
import GraphInteractions


class Graph(tk.Frame):
    ax, original_xlim, original_ylim, coll, pick_id = None, None, None, None, None
    start_end_bool = -1  # 0 is start, 1 is end, -1 is None
    start_index, end_index, move_index, remove_index = 0, None, None, None
    max_time, max_speed, max_height, min_height = 0, 0, 0, 0
    data = []
    connect_ids, move_ids = [], []
    current_color_scheme = 'd'

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

    def redraw_color(self, x, y, c):
        self.fig.clear()
        self.ax = self.fig.add_subplot(111, frameon=False)
        self.coll = self.ax.scatter(x, y, color=c, picker=True)
        self.ax.set_xlim(self.zoom_pan.cur_xlim)
        self.ax.set_ylim(self.zoom_pan.cur_ylim)
        self.connect_ids.append(GraphInteractions.ZoomPan.zoom_factory(self.zoom_pan, self.ax, base_scale=1.3))
        self.connect_ids.extend(GraphInteractions.ZoomPan.pan_factory(self.zoom_pan, self.ax))
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
        self.data.clear()
        json_file = open(input_file_location, "r")
        file_data = json.load(json_file)
        json_file.close()
        old_time, old_x, old_y = 0, file_data['recording']['path'][0]['x'], file_data['recording']['path'][0]['y']
        self.max_time, self.max_speed, self.max_height, self.min_height = 0, 0, 0, file_data['recording']['path'][0]['z']
        speed = 0
        for time in file_data['recording']['path']:
            x_array.append(time['x'])
            y_array.append(time['y'])
            time_div = time['t'] - old_time
            if time['t'] > self.max_time:
                self.max_time = time['t']
            if time_div != 0:
                speed = distance(time['x'], old_x, time['y'], old_y)/time_div
            if speed > self.max_speed:
                self.max_speed = speed
            if time['z'] > self.max_height:
                self.max_height = time['z']
            elif time['z'] < self.min_height:
                self.min_height = time['z']
            self.data.append([time['x'], time['y'], time['t'], speed, time['z']])
            color_array.append('tab:blue')
            old_time = time['t']
            old_x, old_y = time['x'], time['y']
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
            if idx == self.start_index or idx == self.end_index or idx == self.remove_index:
                c.append('tab:red')
            elif idx < self.start_index or idx > self.end_index or\
                    (self.start_index == 0 and self.end_index == len(self.data) - 1):
                c.append('tab:blue')
            elif self.start_index < idx < self.end_index:
                c.append('c')

        self.redraw_color(x, y, c)

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
        self.redraw_color(x, y, c)

    def change_color(self, event):
        if event.mouseevent.button != 1: return
        if self.start_end_bool == 0:
            self.start_index = event.ind[0]
        elif self.start_end_bool == 1:
            self.end_index = event.ind[0]
        elif self.start_end_bool == 2:
            self.remove_index = event.ind[0]
        self.redraw_ext()
        self.master_string.set('x: %.4f, y: %.4f' % (self.data[event.ind[0]][0], self.data[event.ind[0]][1]))

    def show_time(self):
        self.current_color_scheme = 't'
        for cid in self.connect_ids:
            self.canvas.mpl_disconnect(cid)
        self.connect_ids.clear()
        x = []
        y = []
        c = []
        for idx, row in enumerate(self.data):
            x.append(row[0])
            y.append(row[1])
            gradient = row[2]/self.max_time
            c.append((0, 1-gradient, gradient))
        self.redraw_color(x, y, c)

    def show_speed(self):
        self.current_color_scheme = 's'
        for cid in self.connect_ids:
            self.canvas.mpl_disconnect(cid)
        self.connect_ids.clear()
        x = []
        y = []
        c = []
        for idx, row in enumerate(self.data):
            x.append(row[0])
            y.append(row[1])
            gradient = row[3]/self.max_speed
            c.append((1-gradient, gradient, 0))
        self.redraw_color(x, y, c)

    def show_height(self):
        self.current_color_scheme = 'h'
        for cid in self.connect_ids:
            self.canvas.mpl_disconnect(cid)
        self.connect_ids.clear()
        x = []
        y = []
        c = []
        for idx, row in enumerate(self.data):
            x.append(row[0])
            y.append(row[1])
            gradient = (row[4] - self.min_height)/(self.max_height - self.min_height)
            c.append((gradient*0.5 + 0.5, gradient*0.8, gradient*0.8))
        self.redraw_color(x, y, c)

    def reset_color(self):
        self.current_color_scheme = 'd'
        for cid in self.connect_ids:
            self.canvas.mpl_disconnect(cid)
        self.connect_ids.clear()
        x = []
        y = []
        c = []
        for idx, row in enumerate(self.data):
            x.append(row[0])
            y.append(row[1])
            c.append('tab:blue')
        self.redraw_color(x, y, c)

    def attach_start_stop(self, master_string_var, start_end):
        self.detach_start_stop()
        self.start_end_bool = start_end
        self.master_string = master_string_var
        self.pick_id = self.canvas.mpl_connect('pick_event', self.change_color)

    def detach_start_stop(self):
        if self.pick_id is None: return
        self.start_end_bool = -1
        self.canvas.mpl_disconnect(self.pick_id)
        for move_id in self.move_ids:
            self.canvas.mpl_disconnect(move_id)

    def attach_move_node(self):
        def on_press(event):
            if event.mouseevent.button != 1: return
            self.move_index = event.ind[0]
            self.master.move_node_location.set('x: %.4f, y: %.4f' % (self.data[self.move_index][0],
                                                                     self.data[self.move_index][1]))

        def on_release(event):
            self.redraw_simp()

        def on_motion(event):
            if event.button != 1: return
            self.data[self.move_index][0] = event.xdata
            self.data[self.move_index][1] = event.ydata
            self.master.move_node_location.set('x: %.4f, y: %.4f' % (self.data[self.move_index][0],
                                                                     self.data[self.move_index][1]))

            self.redraw_simp()
        self.detach_start_stop()
        self.pick_id = self.canvas.mpl_connect('pick_event', on_press)
        self.move_ids.append(self.canvas.mpl_connect('key_press_event', self.move_node_button))
        self.move_ids.append(self.canvas.mpl_connect('button_release_event', on_release))
        self.move_ids.append(self.canvas.mpl_connect('motion_notify_event', on_motion))

    def attach_remove_node(self, master_string):
        self.detach_start_stop()
        self.start_end_bool = 2
        self.master_string = master_string
        self.pick_id = self.canvas.mpl_connect('pick_event', self.change_color)

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

    def move_node(self, direction, move_distance):
        if direction == "N":
            self.data[self.move_index][1] += move_distance
        elif direction == "E":
            self.data[self.move_index][0] += move_distance
        elif direction == "S":
            self.data[self.move_index][1] -= move_distance
        elif direction == "W":
            self.data[self.move_index][0] -= move_distance
        self.master.move_node_location.set('x: %.4f, y: %.4f' % (self.data[self.move_index][0],
                                                                 self.data[self.move_index][1]))
        self.redraw_simp()

    def remove_node(self):
        del self.data[self.remove_index]
        self.end_index = len(self.data) - 1
        self.redraw_ext()
        self.master_string.set('x: %.4f, y: %.4f' % (self.data[self.remove_index][0], self.data[self.remove_index][1]))

    def apply_local_speedup(self, value):
        speedup = 1
        speed = 0
        previous_time = 0
        previous_old_time = 0
        old_x, old_y = self.data[0][0], self.data[0][1]
        for idx, row in enumerate(self.data):
            if self.start_index == idx:
                speedup = 1 - float(value)/100
            elif self.end_index == idx:
                speedup = 1
            old_time = row[2]
            if old_time < previous_old_time:
                previous_old_time = old_time / 2
            row[2] = previous_time + (min(old_time - previous_old_time, 2) * speedup)
            time_div = row[2] - previous_time
            if row[2] > self.max_time:
                self.max_time = row[2]
            if time_div != 0:
                speed = distance(row[0], old_x, row[1], old_y)/time_div
            if speed > self.max_speed:
                self.max_speed = speed
            row[3] = speed
            previous_time = row[2]
            previous_old_time = old_time
            old_x, old_y = row[0], row[1]
            self.update_unknown()

    def update_unknown(self):
        if self.current_color_scheme == 'h':
            self.show_height()
        elif self.current_color_scheme == 's':
            self.show_speed()
        elif self.current_color_scheme == 't':
            self.show_time()
        else:
            self.reset_color()


def distance(a1, a2, b1, b2):
    from math import sqrt
    diff_a = a1 - a2
    diff_b = b1 - b2
    return sqrt(diff_a*diff_a+diff_b*diff_b)

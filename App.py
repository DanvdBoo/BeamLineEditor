import tkinter as tk
from tkinter import filedialog
import Graph
import BeamFactory
from functools import partial


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.file_handler = FileHandler(self)
        self.title("BeamNG.drive Line Editor")
        self.main_frame = MainFrame(self)
        top_bar = TopBar(self)
        self.config(menu=top_bar)

    def speedup_all(self):
        mf = self.main_frame
        tk.Label(mf, text="Speedup\n(all):").grid(row=2, column=0)
        mf.speedup_entry.grid(row=2, column=1)


class MainFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, width=1280, height=720)
        self.grid_propagate(0)
        self.grid(row=0, column=0)
        tk.Frame(self, width=200).grid(row=0, column=1)
        tk.Label(self, text="Input file:").grid(row=0, column=0)
        tk.Label(self, textvariable=master.file_handler.input_file_name).grid(row=0, column=1)

        self.graph = Graph.Graph(self)
        self.graph.grid(row=0, column=2, rowspan=50, pady=8, padx=10)
        self.speedup_entry = tk.Entry(self)
        self.speedup_entry.insert(tk.END, "0")

        self.start_coord, self.end_coord = tk.StringVar(), tk.StringVar()
        tk.Label(self, text="Start:").grid(row=4, column=0)
        tk.Label(self, text="End").grid(row=5, column=0)

        self.sel_start_button = tk.Button(self, text="Select start point", command=self.select_start)
        self.sel_start_button.grid(row=3, column=1)
        self.sel_end_button = tk.Button(self, text="Select end point", command=self.select_end)
        self.sel_end_button.grid(row=6, column=1)

        frame1 = tk.Frame(self)
        frame1.grid(row=3, column=0)
        tk.Button(frame1, text="<", command=partial(self.graph.next_start, self.start_coord, -1)).grid(row=0, column=0)
        tk.Button(frame1, text=">", command=partial(self.graph.next_start, self.start_coord, 1)).grid(row=0, column=1)

        frame2 = tk.Frame(self)
        frame2.grid(row=6, column=0)
        tk.Button(frame2, text="<", command=partial(self.graph.next_end, self.start_coord, -1)).grid(row=0, column=0)
        tk.Button(frame2, text=">", command=partial(self.graph.next_end, self.start_coord, 1)).grid(row=0, column=1)

        tk.Label(self, textvariable=self.start_coord).grid(row=4, column=1)
        tk.Label(self, textvariable=self.end_coord).grid(row=5, column=1)

        self.selected_speedup_entry = tk.Entry(self)
        self.selected_speedup_entry.insert(tk.END, "0")
        tk.Label(self, text="Speedup\n(selected):").grid(row=7, column=0)
        self.selected_speedup_entry.grid(row=7, column=1)

        tk.Button(self, text="Apply", command=self.apply_local_speedup).grid(row=8, column=1)

        tk.Label(self, text="Move:").grid(row=10, column=0)
        frame3 = tk.Frame(self)
        frame3.grid(row=11, column=1)
        tk.Button(frame3, text="◀", command=partial(self.move_node, "W")).grid(row=0, column=0)
        self.sel_move_button = tk.Button(frame3, text="O", command=self.select_move)
        self.sel_move_button.grid(row=0, column=1)
        tk.Button(frame3, text="▶", command=partial(self.move_node, "E")).grid(row=0, column=2)
        tk.Button(self, text="▲", command=partial(self.move_node, "N")).grid(row=10, column=1)
        tk.Button(self, text="▼", command=partial(self.move_node, "S")).grid(row=12, column=1)

        self.move_entry = tk.Entry(self)
        self.move_entry.insert(tk.END, "0.5")
        tk.Label(self, text="Move by:").grid(row=13, column=0)
        self.move_entry.grid(row=13, column=1)

        self.move_node_location = tk.StringVar()
        tk.Label(self, textvariable=self.move_node_location).grid(row=14, column=1)

        tk.Label(self, text="Remove:").grid(row=16, column=0)
        self.sel_remove_button = tk.Button(self, text="Select:", command=self.select_remove)
        self.sel_remove_button.grid(row=16, column=1)
        self.remove_node_location = tk.StringVar()
        tk.Label(self, textvariable=self.remove_node_location).grid(row=17, column=1)
        self.remove_button = tk.Button(self, text="Remove", command=self.graph.remove_node)
        self.remove_button.grid(row=17, column=0)

        self.select_start()

    def select_start(self):
        self.raise_buttons()
        self.sel_start_button.config(relief=tk.SUNKEN)
        self.graph.attach_start_stop(self.start_coord, 0)

    def select_end(self):
        self.raise_buttons()
        self.sel_end_button.config(relief=tk.SUNKEN)
        self.graph.attach_start_stop(self.end_coord, 1)

    def select_move(self):
        self.sel_move_button.config(relief=tk.SUNKEN)
        self.graph.attach_move_node()

    def select_remove(self):
        self.raise_buttons()
        self.sel_remove_button.config(relief=tk.SUNKEN)
        self.graph.attach_remove_node(self.remove_node_location)

    def raise_buttons(self):
        self.sel_end_button.config(relief=tk.RAISED)
        self.sel_start_button.config(relief=tk.RAISED)
        self.sel_move_button.config(relief=tk.RAISED)
        self.sel_remove_button.config(relief=tk.RAISED)

    def move_node(self, direction):
        self.graph.move_node(direction, float(self.move_entry.get()))

    def apply_local_speedup(self):
        self.graph.apply_local_speedup(self.selected_speedup_entry.get())


class TopBar(tk.Menu):
    def __init__(self, master):
        super().__init__(master, relief=tk.RAISED)
        file_menu = tk.Menu(self, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=master.file_handler.save, state=tk.DISABLED)
        file_menu.add_command(label="Save as", command=master.file_handler.save_as)
        option_menu = tk.Menu(self, tearoff=0)
        option_menu.add_command(label="Speedup", command=master.speedup_all(), state=tk.DISABLED)
        option_menu.add_command(label="Reset zoom", command=master.main_frame.graph.reset_zoom)
        option_menu.add_command(label="Reset start point", command=self.reset_start)
        option_menu.add_command(label="Reset end point", command=self.reset_end)
        option_menu.add_command(label="Reset start & end", command=self.reset_start_end)
        show_menu = tk.Menu(self, tearoff=0)
        show_menu.add_command(label="Default", command=master.main_frame.graph.reset_color)
        show_menu.add_command(label="Time", command=master.main_frame.graph.show_time)
        show_menu.add_command(label="Speed", command=master.main_frame.graph.show_speed)
        show_menu.add_command(label="Height", command=master.main_frame.graph.show_height)
        self.add_cascade(label="File", menu=file_menu)
        self.add_cascade(label="Options", menu=option_menu)
        self.add_cascade(label="Show", menu=show_menu)
        self.add_cascade(label="Help", state=tk.DISABLED)
        self.add_command(label="Quit", command=master.destroy)

    def open_file(self):
        self.master.file_handler.open()
        self.master.main_frame.graph.redraw(self.master.file_handler.input_file)

    def reset_start(self):
        mf = self.master.main_frame
        mf.graph.reset_start(mf.start_coord)

    def reset_end(self):
        mf = self.master.main_frame
        mf.graph.reset_end(mf.end_coord)

    def reset_start_end(self):
        self.reset_start()
        self.reset_end()


class FileHandler:
    input_file = ""
    output_file = ""

    def __init__(self, master):
        self.master = master
        self.input_file_name = tk.StringVar()

    def open(self):
        self.input_file = filedialog.askopenfilename(title="Select file",
                                                     filetypes=(("track files", "*.track.json"), ("all files", "*.*")))
        self.input_file_name.set(self.input_file.split("/")[-1])

    def save(self):
        self.output_file = filedialog.askopenfilename(title="Select file",
                                                      filetypes=(("track files", "*.track.json"), ("all files", "*.*")))

    def save_as(self):
        self.output_file = filedialog.asksaveasfilename(title="Select file", filetypes=(("track files", "*.track.json"),
                                                                                        ("all files", "*.*")))
        if ".track.json" not in self.output_file:
            self.output_file = self.output_file + ".track.json"

        mf = self.master.main_frame
        beam_fac = BeamFactory.BeamFactory(self.input_file, self.output_file)
        beam_fac.set_speedup_global(mf.speedup_entry.get())
        beam_fac.set_speedup_local(mf.selected_speedup_entry.get(), mf.graph.start_index, mf.graph.end_index)
        beam_fac.set_data(mf.graph.data)
        beam_fac.save_changes()

import tkinter as tk
from tkinter import filedialog
import Graph
import BeamNG_Speeding


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.file_handler = FileHandler(self)
        self.title("BeamNG.drive Line Editor")
        top_bar = TopBar(self)
        self.config(menu=top_bar)
        self.main_frame = MainFrame(self)

    def speedup(self):
        tk.Label(self.main_frame, text="Speedup:").grid(row=2, column=0)
        self.main_frame.speedup_entry.grid(row=2, column=1)


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


class TopBar(tk.Menu):
    def __init__(self, master):
        super().__init__(master, relief=tk.RAISED)
        file_menu = tk.Menu(self, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=master.file_handler.save, state=tk.DISABLED)
        file_menu.add_command(label="Save as", command=master.file_handler.save_as)
        option_menu = tk.Menu(self, tearoff=0)
        option_menu.add_command(label="Speedup", command=master.speedup)
        self.add_cascade(label="File", menu=file_menu)
        self.add_cascade(label="Options", menu=option_menu)
        self.add_command(label="Quit", command=master.destroy)

    def open_file(self):
        self.master.file_handler.open()
        self.master.main_frame.graph.redraw(self.master.file_handler.input_file)


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
        BeamNG_Speeding.speedup_time(int(self.master.main_frame.speedup_entry.get()), self.input_file, self.output_file)

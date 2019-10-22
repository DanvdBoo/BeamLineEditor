import tkinter as tk
from tkinter import filedialog


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.file_handler = FileHandler()
        self.title("BeamNG.drive Line Editor")
        top_bar = TopBar(self)
        self.config(menu=top_bar)
        MainFrame(self)


class MainFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, width=1280, height=720)
        self.grid_propagate(0)
        self.grid(row=0, column=0)
        tk.Label(self, text="Input file:").grid(row=0, column=0)
        tk.Label(self, textvariable=master.file_handler.input_file_name).grid(row=0, column=1)


class TopBar(tk.Menu):
    def __init__(self, master):
        super().__init__(master, relief=tk.RAISED)
        file_menu = tk.Menu(self, tearoff=0)
        file_menu.add_command(label="Open", command=master.file_handler.open)
        file_menu.add_command(label="Save", command=master.file_handler.save)
        self.add_cascade(label="File", menu=file_menu)
        self.add_command(label="Quit", command=master.destroy)


class FileHandler:
    def __init__(self):
        self.input_file = ""
        self.output_file = ""
        self.input_file_name = tk.StringVar()
        print(self.input_file)

    def open(self):
        print("Open file!")
        self.input_file = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                     filetypes=(("track files", "*.track.json"), ("all files", "*.*")))
        self.input_file_name.set(self.input_file.split("/")[-1])
        print(self.input_file)

    def save(self):
        print("Save file!")
        self.output_file = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                      filetypes=(("track files", "*.track.json"), ("all files", "*.*")))
        print(self.output_file)

import tkinter as tk
from tkinter import filedialog, Button, Label
import BeamNG_Speeding as spdg

max_file_name_size = 35


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("BeamNG.drive Line Editor")

        frame = tk.Frame(self)
        frame.grid()

        self.same_bool = tk.IntVar()

        self.input_files = Files(frame, "input", 0)
        self.output_files = Files(frame, "output", 1)

        self.select_same = tk.Checkbutton(frame, variable=self.same_bool, command=self.set_output_to_input)
        self.select_same.grid(row=2, sticky=tk.E)
        self.select_same_label = Label(frame, text="Set output to input").grid(row=2, column=1, sticky=tk.W)
        self.quit_button = Button(frame, text="Quit", command=frame.quit).grid(row=2, column=2)

    def set_output_to_input(self):
        if self.same_bool.get() == 1:
            self.output_files.set_directory(self.input_files.get_directory())


class Files(tk.Frame):
    def __init__(self, master, input_output, row):
        super().__init__(master)

        self.input_label = Label(master, text=input_output).grid(row=row, sticky=tk.W)

        self.file_name = tk.StringVar()
        self.file_name.set("")
        self.directory = ""

        self.input_file_name_text = tk.Entry(master, textvariable=self.file_name)
        self.input_file_name_text.grid(row=row, column=1, padx=5)

        self.select_file_button = Button(master, text="Browse",
                                         command=lambda: self.ask_file_location())
        self.select_file_button.grid(row=row, column=2)

    def ask_file_location(self):
        self.directory = filedialog.askopenfile(initialdir="/", title="Select file",
                                                filetypes=(("track files","*.track.json"),("all files","*.*")))
        self.set_file_name(self.directory)

    def set_file_name(self, directory):
        if directory.name.find("/"):
            file_name = directory.name.split("/")[-1]
        else:
            file_name = directory.name
        if len(file_name) > max_file_name_size:
            file_name = file_name[0:max_file_name_size-3] + "..."
        self.file_name.set(file_name)

    def get_file(self):
        return self.directory.name

    def set_directory(self, directory):
        self.directory = directory
        self.set_file_name(directory)

    def get_directory(self):
        return self.directory


if __name__ == '__main__':
    App().mainloop()

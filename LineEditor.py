import tkinter as tk
from tkinter import filedialog, Button, Label
import sys
import BeamNG_Speeding as Speeding
max_file_name_size = 35


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("BeamNG.drive Line Editor")

        frame = tk.Frame(self)
        frame.grid(pady=2, padx=5)

        self.same_bool = tk.BooleanVar()

        self.input_files = Files(frame, "input", 0)
        self.output_files = Files(frame, "output", 1)

        self.select_same = tk.Checkbutton(frame, variable=self.same_bool, command=self.set_output_to_input)
        self.select_same.grid(row=2, sticky=tk.E, pady=3)
        self.select_same_label = Label(frame, text="Set output to input").grid(row=2, column=1, sticky=tk.W)
        self.quit_button = Button(frame, text="Quit", command=sys.exit, width=7).grid(row=3, column=2)
        self.continue_button = Button(frame, text="Continue", command=frame.quit).grid(row=3, column=0)

    def set_output_to_input(self):
        if self.same_bool.get():
            self.output_files.set_directory(self.input_files.get_directory())


class Files(tk.Frame):
    def __init__(self, master, input_output, row):
        super().__init__(master)

        self.input_label = Label(master, text=input_output).grid(row=row, sticky=tk.E)

        self.file_name = tk.StringVar()
        self.file_name.set("")
        self.directory = ""

        self.input_file_name_text = tk.Entry(master, textvariable=self.file_name, width=50)
        self.input_file_name_text.grid(row=row, column=1, padx=5, pady=3)

        self.select_file_button = Button(master, text="Browse",
                                         command=lambda: self.ask_file_location(), width=7)
        self.select_file_button.grid(row=row, column=2, padx=5, pady=3)

    def ask_file_location(self):
        self.directory = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                    filetypes=(("track files","*.track.json"),("all files","*.*")))
        self.set_file_name(self.directory)

    def set_file_name(self, directory):
        self.file_name.set(self.directory)

    def get_file(self):
        return self.file_name.get()

    def set_directory(self, directory):
        self.directory = directory
        self.set_file_name(directory)

    def get_directory(self):
        return self.directory


class SecondScreen(tk.Tk):
    def __init__(self, input_dir, output_dir):
        super().__init__()

        self.input_file_location = input_dir
        self.output_file_location = output_dir

        self.title("BeamNG.drive Line Editor")

        frame = tk.Frame(self)
        frame.grid(padx=5, pady=5)

        speedup = 0
        self.done_text = tk.StringVar()
        self.done_text.set("")

        self.speedup_label = Label(frame, text="Speedup %").grid(row=0, column=0, sticky=tk.W)
        self.speedup_entry = tk.Entry(frame)
        self.speedup_entry.grid(row=0, column=1)
        self.speedup_entry.insert(0, speedup)

        self.speedup_button = Button(frame, text="Start", command=self.calculate).grid(row=0, column=2)
        self.quit_button = Button(frame, text="Quit", command=frame.quit).grid(row=1, column=2)
        self.done_label = Label(frame, textvariable=self.done_text).grid(row=1, column=1)

    def calculate(self):
        self.done_text.set("")
        print(self.speedup_entry.get())
        Speeding.speedup_time(int(self.speedup_entry.get()), self.input_file_location, self.output_file_location)
        self.done_text.set("Done!")


if __name__ == '__main__':
    app = App()
    app.mainloop()
    input_directory = app.input_files.get_file()
    output_directory = app.output_files.get_file()
    app.destroy()
    app2 = SecondScreen(input_directory, output_directory).mainloop()

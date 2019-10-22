import tkinter as tk
from tkinter import filedialog, Tk, Button
import BeamNG_Speeding as spdg

max_file_name_size = 35


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("BeamNG.drive Line Editor")

        frame = tk.Frame(self)
        frame.pack()

        input_ui = Files(frame, "input")
        output_ui = Files(frame, "output")

        self.quit_button = Button(self, text="Quit", command=frame.quit).pack(side=tk.RIGHT, padx=5, pady=5)


class Files(tk.Frame):
    def __init__(self, master, input_output):
        super().__init__(master)
        self.pack(fill=tk.X)

        self.file_name = tk.StringVar()
        self.file_name.set("None")
        self.directory = ""

        self.select_file_button = Button(self, text="Select " + input_output + " file",
                                         command=lambda: self.ask_file_location()).pack(side=tk.LEFT, padx=5)
        self.input_file_name_text = tk.Label(self, textvariable=self.file_name).pack(side=tk.LEFT, padx=5)

    def ask_file_location(self):
        self.directory = filedialog.askopenfile(initialdir="/", title="Select file",
                                                filetypes=(("track files","*.track.json"),("all files","*.*")))
        file_name = self.directory.name.split("/")[-1]
        if len(file_name) > max_file_name_size:
            file_name = file_name[0:max_file_name_size-3] + "..."
        self.file_name.set(file_name)

    def get_file(self):
        return self.directory.name


if __name__ == '__main__':
    App().mainloop()

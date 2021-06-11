import tkinter as tk
from datetime import datetime

import pandas as pd



class Logging(tk.Frame):
    def __init__(self,mod, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if mod=="on":
            self.BG_COLOR = "gray12"
            self.BG_COLOR_2 = "#1c2c5c"
            self.FG_COLOR = "white"
            self.FG_COLOR_2 = "SteelBlue1"
            self.GLOBAL_FONT = ("Calibri", 11, "normal")
            self.BOLD_FONT = ("Calibri", 11, "bold")
        else:
            self.BG_COLOR = "white"
            self.BG_COLOR_2 = "yellow"
            self.FG_COLOR = "black"
            self.FG_COLOR_2 = "red"
            self.GLOBAL_FONT = ("Calibri", 11, "normal")
            self.BOLD_FONT = ("Calibri", 11, "bold")

        self.logging_text = tk.Text(self, height=10, width=60, state=tk.DISABLED, bg=self.BG_COLOR, fg=self.FG_COLOR_2,
                                    font=self.GLOBAL_FONT, highlightthickness=False, bd=0)
        self.logging_text.pack(side=tk.TOP)

    def add_log(self, message: str):

        """
        Add a new log message to the tk.Text widget, placed at the top, with the current UTC time in front of it.
        :param message: The new log message.
        :return:
        """

        self.logging_text.configure(state=tk.NORMAL)  # Unlocks the tk.Text widgets
        self.logging_text.insert("1.0", datetime.utcnow().strftime("%a %H:%M:%S :: ") + message + "\n")
        self.logging_text.configure(state=tk.DISABLED)  # Locks the tk.Text widget to avoid accidentally inserting in it

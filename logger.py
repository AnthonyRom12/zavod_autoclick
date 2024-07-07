import tkinter as tk


class Logger:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def log(self, message):
        self.text_widget.configure(state=tk.NORMAL)
        self.text_widget.insert(tk.END, message + "\n")
        self.text_widget.configure(state=tk.DISABLED)
        self.text_widget.yview(tk.END)

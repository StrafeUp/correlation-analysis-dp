import tkinter as tk


class StdRedirector(object):
    def __init__(self, text_widget):
        self.text_field = text_widget

    def write(self, text):
        self.text_field.config(state=tk.NORMAL)
        self.text_field.insert(tk.END, text)
        self.text_field.config(state=tk.DISABLED)

    def flush(self):
        pass

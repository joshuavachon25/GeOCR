import os
import tkinter as tk
import webbrowser
from tkinter import ttk
import ttkbootstrap as tkb


class Settings(tkb.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Paramètres")
        self.geometry("500x500")
        self.transient(parent)
        self.update_idletasks()
        self.grab_set()

        tkb.Label(self, text='Paramètres', font='Helvetica 18').pack(fill='x', padx=10, pady=10)
        group_default = tkb.Labelframe(self, text='Valeurs par défaut')
        group_default.pack(expand=True, fill='both', padx=10, pady=10)

        self.wait_window(self)

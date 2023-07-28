import os
import tkinter as tk
import webbrowser
from tkinter import ttk
import ttkbootstrap as tkb
from geocr.DataTable import DataTable


class Projects(tkb.Toplevel):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.title("Projets")
        self.geometry("500x500")
        self.transient(parent)
        self.update_idletasks()
        self.grab_set()
        self.DB = db

        tkb.Label(self, text='Projets', font='Helvetica 18').pack(fill='x', padx=10, pady=10)

        frame = tkb.Frame(self)
        frame.pack(expand=True, fill='both')

        self.db_view = DataTable(frame, 'projects', self.DB)
        self.db_view.pack(fill='y', expand=True, side='left')
        options = tkb.Labelframe(frame, text="Gestion des données")
        options.pack(fill='y', expand=True, side='left', padx=10, pady=10)

        self.wait_window(self)

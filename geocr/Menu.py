import os
import tkinter as tk
import webbrowser
from tkinter import ttk
import ttkbootstrap as tkb
from geocr.Settings import Settings
from geocr.Geoindex import Geoindex
from geocr.Projects import Projects


class Menu(tkb.Frame):
    def __init__(self, parent, db):
        super().__init__(parent, style='primary.TFrame')
        self.parent = parent
        self.DB = db
        btn_geoindex = tkb.Button(self, text='Geoindex', command=self.open_geoindex)
        btn_geoindex.pack(fill='y', side='left')
        btn_projects = tkb.Button(self, text='Projets', command=self.open_projects)
        btn_projects.pack(fill='y', side='left')
        btn_about = tkb.Button(self, text='À propos', command=lambda: os.startfile('https://github.com/joshuavachon25'))
        btn_about.pack(fill='y', side='left')
        btn_settings = tkb.Button(self, text='Paramètres', command=self.open_settings)
        btn_settings.pack(fill='y', side='left')

    def open_settings(self):
        Settings(self.parent)

    def open_projects(self):
        Projects(self.parent, self.DB)

    def open_geoindex(self):
        Geoindex(self.parent, self.DB)

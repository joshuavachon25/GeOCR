import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from geocr.PropertyLabel import PropertyLabel
import os
import ttkbootstrap as tkb


class Details(tkb.Labelframe):
    def __init__(self, parent, add_archive_callback, search_in_db):
        super().__init__(parent, text='Propriétés')
        self.src = None
        self.filename = None
        self.ext = None
        self.path = None
        self.image = None
        self.label = None
        self.search_in_db = search_in_db

        self.properties = tkb.Frame(self)
        self.properties.pack(fill='x', expand=True)

        action_list = tk.Frame(self)
        action_list.pack(fill='x', padx=10, pady=(0, 10))
        button_open = tkb.Button(action_list, text="Ouvrir le fichier", command=lambda: self.open_image())
        button_open.pack(side="left")
        self.button_add = tkb.Button(action_list, text="Ajouter aux archives", command=lambda: self.add_archive(add_archive_callback))
        self.button_add.pack(side="right")

    def show_details(self, path):
        image = Image.open(path)
        self.path = path
        self.image = image
        self.clear_properties()
        self.get_info()

    def open_image(self):
        if self.image is not None:
            self.image.show()

    def add_archive(self, callback):
        name = tkb.dialogs.dialogs.Querybox.get_string(prompt="Nommez cette source", title="Nom de l'archive")
        print(self.image.info)
        if name is not None:
            path = self.path
            zones = f"1; Zone 1; 0, 0, {self.image.width}, 0, {self.image.height}, {self.image.width}, 0, {self.image.height}"
            project = ""
            params = ""
            tags = ""
            status = "NOUVEAU"
            year = 0
            default_values = (path, name, zones, project, params, tags, status, year, self.image.width, self.image.height)
            callback(default_values)

    def clear_properties(self):
        for widget in self.properties.winfo_children():
            widget.destroy()

    def get_info(self):
        head, tail = os.path.split(self.path)
        self.ext = tail.split('.')[-1]
        results = self.search_in_db(self.path)
        self.filename = tail.replace('.'+self.ext, '')
        PropertyLabel(self.properties, self.filename, 'Nom du fichier')
        PropertyLabel(self.properties, str(self.ext).upper(), 'Extension')
        PropertyLabel(self.properties, self.image.width, 'Largeur')
        PropertyLabel(self.properties, self.image.height, 'Hauteur')
        if 'dpi' in self.image.info: PropertyLabel(self.properties, int(self.image.info['dpi'][0]), 'DPI')
        if 'Software' in self.image.info: PropertyLabel(self.properties, self.image.info['Software'][0], 'Logiciel')
        if len(results):
            str_results = str(results).replace('[','').replace(']', '').replace('(', '').replace(')', '').replace(',,', ',')[0:-1]
            PropertyLabel(self.properties, str_results, 'ID (BDD): ')


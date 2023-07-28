import os
import string
import tkinter as tk
from tkinter import ttk, END
import ttkbootstrap as tkb


class FileExplorer(tkb.Labelframe):
    def __init__(self, parent, show_exif):
        super().__init__(parent, text='Explorateur de fichiers')
        self.show_exif = show_exif
        nav_frame = tkb.Frame(self)
        drives = self.get_drives()
        self.nav_drive = tkb.Combobox(nav_frame, values=drives, state='readonly', width=5)
        self.nav_drive.set(drives[0])
        self.current_path = drives[0]
        self.nav_drive.pack(side='left')
        self.nav_url = tkb.Entry(nav_frame)
        self.nav_url.pack(side='left', expand=True, fill='both')
        self.nav_btn = tkb.Button(nav_frame, text='Aller')
        self.nav_btn.pack(side='left', fill='both')
        nav_frame.pack(fill='x', padx=10, pady=(10, 0))

        self.tree = ttk.Treeview(self)
        self.tree['columns'] = ("Type", "Nom", "Taille")
        self.tree.column('#0', width=0, stretch=False)
        self.tree.column("Type", anchor='e', width=24, stretch=False)
        self.tree.column("Nom", anchor='w', width=120)
        self.tree.column("Taille", anchor='w', width=70)
        self.tree.heading('#0', text='', anchor='w')
        self.tree.heading('Type', text='', anchor='e')
        self.tree.heading('Nom', text='Nom', anchor='w')
        self.tree.heading('Taille', text='Taille', anchor='w')
        self.tree.bind("<Double-1>", self.change_folder)
        self.list_folder()

        self.nav_drive.bind('<<ComboboxSelected>>', lambda event: self.set_current())

        self.tree.pack(expand=True, fill='both', padx=10, pady=(0, 10))

    def set_current(self):
        self.current_path = self.nav_drive.get()
        self.list_folder()

    def get_drives(self):
        possible_drive = string.ascii_uppercase
        drives = []
        for each_drive in possible_drive:
            if os.path.exists(each_drive + ":\\"):
                drives.append(each_drive + ":\\")
        return drives

    def list_folder(self):
        self.clear_list()
        self.nav_url.delete(0, END)
        self.nav_url.insert(0, self.current_path.replace(self.nav_drive.get(), ""))
        if os.path.splitdrive(self.current_path)[0] != self.current_path.replace("\\", ""):
            self.tree.insert(parent='', index='end', values=('..', '..', ''))
        try:
            for file in os.listdir(self.current_path):
                if not os.path.isfile(self.current_path + "\\" + file) and file[0] not in ['.', '$', '~']:
                    self.tree.insert(parent='', index='end', values=('📁', file, ''))
                else:
                    if os.path.splitext(file)[1] in [".jpg", ".png", ".gif", ".tiff", ".bmp", ".webm", ".avif"]:
                        self.tree.insert(parent='', index='end', values=('', file, str(round(os.path.getsize(self.current_path + "\\" + file) / 1024 ** 2, 2)) + 'mo'))
        finally:
            pass

    def change_folder(self, event):
        selected = self.tree.focus()
        values = self.tree.item(selected, 'values')
        if not values:
            pass
        elif values[1] == "..":
            self.current_path = self.current_path.replace("\\" + os.path.basename(self.current_path), "")
            if len(self.current_path) == 2:
                self.current_path += "\\"
            self.list_folder()
        elif os.path.isfile(self.current_path + "\\" + values[1]):
            self.show_exif(self.current_path + "\\" + values[1])
        else:
            if os.path.splitdrive(self.current_path)[0] + "\\" != self.current_path:
                self.current_path += "\\" + values[1]
            else:
                self.current_path += values[1]
            self.list_folder()

    def clear_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

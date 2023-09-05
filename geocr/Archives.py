import os
import tkinter as tk
import webbrowser
from tkinter import ttk

import tkintermapview
import helpers.ImageHelper as ImageHelper
import ttkbootstrap as tkb
from PIL import Image, ImageTk


class Archives(tkb.Toplevel):
    def __init__(self, parent, db, item):
        super().__init__(parent)
        self.current_zone = None
        self.title("Archives")
        self.geometry("1200x800")
        self.transient(parent)
        self.update_idletasks()
        self.grab_set()
        self.DB = db
        self.item = self.DB.search_in_db_by_id(item)[0]
        self.current_zone = None

        self.columnconfigure(0, uniform='a', weight=4)
        self.columnconfigure(1, uniform='a', weight=1)
        self.rowconfigure(0, uniform='a', weight=2)
        self.rowconfigure(1, uniform='a', weight=7)
        self.rowconfigure(2, uniform='a', weight=1)

        self.viewer = ArchivesViewer(self, self.item)
        self.viewer.grid(column=0, row=0, rowspan=3, sticky='nsew', padx=10, pady=10)
        ImageHelper.show_preview(self.viewer, self.item[0], mode='canvas')

        self.zones_editor = tkb.Frame(self)
        self.zones_editor.grid(column=1, row=0, rowspan=3, sticky='nsew', padx=10, pady=10)

        self.zones = Zones(self.item[3])
        self.zone_rect = self.viewer.img.create_polygon([(0, 0), (0, 0), (0, 0), (0, 0)], outline='blue', tags='currentZone')

        self.zones_details = tkb.Notebook(self.zones_editor)
        self.zones_details.pack(expand=True, fill='both')

        self.panel_info = DetailPanel(self.zones_details, self.viewer.place_point)
        self.panel_image = ImagePanel(self.zones_details)
        self.panel_ocr = OCRPanel(self.zones_details)

        self.panel_info.pack(expand=True, fill='both')
        self.panel_image.pack(expand=True, fill='both')
        self.panel_ocr.pack(expand=True, fill='both')
        self.zones_details.add(self.panel_info, text='Détails')
        self.zones_details.add(self.panel_image, text='Image')
        self.zones_details.add(self.panel_ocr, text='OCR')
        self.zones_details.bind('<<NotebookTabChanged>>', self.change_panel)

        self.zones_list = tkb.Treeview(self.zones_editor, columns=("id", "nom"), show='tree')
        self.zones_list.pack(fill='x')
        self.zones_list.column('#0', width=0, stretch=False)
        self.zones_list.column("id", anchor='w', width=24, stretch=False)
        self.zones_list.column("nom", anchor='w', minwidth=20, stretch=True)
        self.zones_list.bind('<<TreeviewSelect>>', self.show_zone)

        self.zones_action = tkb.Frame(self.zones_editor)
        self.zones_action.pack(fill='x')
        tkb.Button(self.zones_action, text='+', command=self.add_zone).pack(expand=True, fill='both')
        tkb.Button(self.zones_action, text='Sauvegarder', command=self.save_data, bootstyle='success').pack(expand=True, fill='both')

        self.wait_window(self)

    def refresh_zones(self):
        for item in self.zones_list.get_children():
            self.zones_list.delete(item)
        for zone in self.zones.zones:
            self.zones_list.insert('', 'end', values=(zone.id, zone.name))

    def add_zone(self):
        self.zones.add_zone()
        self.refresh_zones()

    def change_panel(self, event):
        panel = self.zones_details.index(self.zones_details.select())

    def open_zone(self, zone):
        self.current_zone = zone

    def show_zone(self, event):
        tmp = self.zones_list.focus()
        zone = self.zones_list.item(tmp, 'values')[0]
        self.current_zone = self.zones.get_data_zone(int(zone))
        # for child in self.panel_info.winfo_children():
        #      child.configure(state='disable')
        self.viewer.img.coords('currentZone', self.current_zone.coords)

    def save_data(self):
        pass


class ArchivesViewer(tkb.Frame):
    def __init__(self, master, item):
        super().__init__(master)
        self.item = item
        self.img = tkb.Canvas(self, autostyle=False)
        self.img.pack(fill='both', expand=True)

    def place_point(self, point):
        self.img.bind('<Button-1>', lambda event: self.update_point(event, point))

    def update_point(self, event, point):
        print('P', point, event.x, event.y)
        self.img.unbind('<Button-1>')


class DetailPanel(tkb.Frame):
    def __init__(self, master, place_point):
        super().__init__(master)
        self.disabled = True
        self.detailsAction = tkb.Frame(self)
        self.detailsAction.pack(fill='x')
        tkb.Button(self.detailsAction, text='P1', command=lambda: place_point(1), bootstyle='primary').pack(expand=True, fill='x', side='left')
        tkb.Button(self.detailsAction, text='P2', command=lambda: place_point(2), bootstyle='primary').pack(expand=True, fill='x', side='left')
        tkb.Button(self.detailsAction, text='P3', command=lambda: place_point(3), bootstyle='primary').pack(expand=True, fill='x', side='left')
        tkb.Button(self.detailsAction, text='P4', command=lambda: place_point(4), bootstyle='primary').pack(expand=True, fill='x', side='left')
        self.delete_zone = tkb.Button(self, text='Supprimer la zone', bootstyle='danger')
        self.delete_zone.pack(fill='x')


class ImagePanel(tkb.Frame):
    def __init__(self, master):
        super().__init__(master)


class OCRPanel(tkb.Frame):
    def __init__(self, master):
        super().__init__(master)


class Zones:
    def __init__(self, data):
        self.data = data
        if self.data == '':
            self.zones = []
            self.next_id = 1
            return
        self.zones = self.get_all_zones()
        self.next_id = len(self.zones)

    def get_all_zones(self):
        zones = []
        for zone in self.data.split('&'):
            zones.append(Zone(zone))
        return zones

    def get_data_zone(self, zid):
        return self.zones[zid - 1]

    def format_for_save(self):
        str_zones = []
        for zone in self.zones:
            str_zones.append(zone.get_string())
        return '&'.join(str_zones)

    def add_zone(self):
        self.zones.append(Zone(f"{self.next_id};Zone {self.next_id};0,0,0,0,0,0,0,0;'';''"))
        self.data = self.format_for_save()
        self.next_id += 1

    def remove_zone(self, id_to_remove):
        i = None
        for index, zone in self.zones:
            if zone.id == id_to_remove:
                i = index
        self.zones.pop(i)
        self.data = self.format_for_save()


class Zone:
    def __init__(self, data):
        self.data = data
        self.id = ''
        self.name = ''
        self.coords = [(0, 0), (0, 0), (0, 0), (0, 0)]
        self.image = ''
        self.text = ''
        self.get_zone()

    def get_string(self):
        output = [self.id, self.name, self.get_coords_str(), self.image, self.text]
        print(output)
        return ';'.join(output)

    def get_zone(self):
        column = self.data.split(';')
        if len(column) < 5:
            return
        self.id = column[0]
        self.name = column[1]
        self.coords = self.get_coords(column[2])
        self.image = column[3]
        self.text = column[4]

    def get_coords_str(self):
        v = self.coords
        return f'{v[0][0]},{v[0][1]},{v[1][0]},{v[1][1]},{v[2][0]},{v[2][1]},{v[3][0]},{v[3][1]}'

    def get_coords(self, data):
        if data == '':
            return [(0, 0), (0, 0), (0, 0), (0, 0)]
        else:
            v = data.split(',')
            return [(v[0], v[1]), (v[2], v[3]), (v[4], v[5]), (v[6], v[7])]


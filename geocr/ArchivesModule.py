import os
import tkinter as tk
import webbrowser
from tkinter import ttk
import tkintermapview
import ttkbootstrap as tkb
import helpers.ImageHelper as ImageHelper
from PIL import Image, ImageTk


class ArchivesWindow(tkb.Toplevel):
    def __init__(self, parent, db, item):
        super().__init__(parent)
        self.panelsFrame = None
        self.toolbarFrame = None
        self.canvasFrame = None
        self.current_zone = None
        self.title("Archives")
        self.geometry("1200x800")
        self.transient(parent)
        self.update_idletasks()
        self.grab_set()
        self.DB = db
        self.item = self.DB.search_in_db_by_id(item)[0]
        self.list_zones = Zones(self.item[3], self.item)
        self.current_zone = None

        self.columnconfigure(0, uniform='a', weight=4)
        self.columnconfigure(1, uniform='a', weight=1)
        self.rowconfigure(0, uniform='a', weight=1)
        self.rowconfigure(1, uniform='a', weight=15)

        self.canvas()
        self.toolbar()
        self.panels()
        ImageHelper.show_preview(self.canvasFrame, self.item[0], mode='canvas')

        self.wait_window(self)

    def canvas(self):
        self.canvasFrame = tkb.Frame(self)
        self.canvasFrame.grid(column=0, row=1, sticky='nsew', padx=10, pady=10)
        self.canvasFrame.canvas = tkb.Canvas(self.canvasFrame, autostyle=False)
        self.canvasFrame.canvas.pack(fill='both', expand=True)
        # self.canvasFrame.canvas.create_polygon(self.current_zone.coords, outline='blue', tags='currentZone')

    def toolbar(self):
        self.toolbarFrame = tkb.Frame(self, style='primary.TFrame')
        self.toolbarFrame.grid(column=0, row=0, sticky="nsew")
        self.list_zones.zones = self.list_zones.get_all_zones()
        self.toolbarFrame.layer_combobox = tkb.Combobox(self.toolbarFrame, values=self.list_zones.zones_label, bootstyle="success", state='readonly')
        self.toolbarFrame.layer_combobox.pack(side='left')
        self.toolbarFrame.layer_combobox.current(0)
        self.current_zone = self.list_zones.get_data_zone(0)
        print(f"CHAT {self.current_zone.coords}")
        self.canvasFrame.canvas.create_polygon(self.current_zone.coords, outline='blue', tags='currentZone')
        tkb.Button(self.toolbarFrame, text="Nouvelle zone").pack(side='left')

    def panels(self):
        self.panelsFrame = tkb.Frame(self)
        self.panelsFrame.grid(column=1, row=0, rowspan=3, sticky='nsew', padx=10, pady=10)
        self.panelsFrame.pipeline = tkb.Notebook(self.panelsFrame)
        self.panelsFrame.pipeline.pack(expand=True, fill='both')
        self.tab_zones()
        self.tab_image()
        self.tab_ocr()

    def tab_zones(self):
        self.panelsFrame.pipeline.zones = tkb.Frame(self.panelsFrame.pipeline)
        self.panelsFrame.pipeline.zones.pack()
        self.panelsFrame.pipeline.add(self.panelsFrame.pipeline.zones, text='Détails')
        self.panelsFrame.pipeline.zones.content = tkb.Frame(self.panelsFrame.pipeline.zones)
        self.panelsFrame.pipeline.zones.content.pack(fill='x')
        tkb.Button(self.panelsFrame.pipeline.zones.content, text='P1', command=lambda: self.action_move_point(1), bootstyle='primary').pack(expand=True, fill='x', side='left')
        tkb.Button(self.panelsFrame.pipeline.zones.content, text='P2', command=lambda: self.action_move_point(2), bootstyle='primary').pack(expand=True,fill='x',side='left')
        tkb.Button(self.panelsFrame.pipeline.zones.content, text='P3', command=lambda: self.action_move_point(3), bootstyle='primary').pack(expand=True,fill='x',side='left')
        tkb.Button(self.panelsFrame.pipeline.zones.content, text='P4', command=lambda: self.action_move_point(4), bootstyle='primary').pack(expand=True,fill='x',side='left')

    def tab_image(self):
        self.panelsFrame.pipeline.image = tkb.Frame(self.panelsFrame.pipeline)
        self.panelsFrame.pipeline.image.pack()
        self.panelsFrame.pipeline.add(self.panelsFrame.pipeline.image, text='Image')
        self.panelsFrame.pipeline.image.content = tkb.Frame(self.panelsFrame.pipeline.image)
        self.panelsFrame.pipeline.image.content.pack(fill='x')

    def tab_ocr(self):
        self.panelsFrame.pipeline.ocr = tkb.Frame(self.panelsFrame.pipeline)
        self.panelsFrame.pipeline.ocr.pack()
        self.panelsFrame.pipeline.add(self.panelsFrame.pipeline.ocr, text='OCR')
        self.panelsFrame.pipeline.ocr.content = tkb.Frame(self.panelsFrame.pipeline.ocr)
        self.panelsFrame.pipeline.ocr.content.pack(fill='x')

    def action_move_point(self, point):
        self.canvasFrame.canvas.bind('<Button-1>', lambda event: self.fn_update_point(event, point))

    def fn_update_point(self, event, point):
        print('P', point, event.x, event.y)
        self.canvasFrame.canvas.unbind('<Button-1>')

# class ArchiveCanvas(tkb.Frame):
#     def __init__(self, master, item):
#         super().__init__(master)
#         self.item = item
#
#     def place_point(self, point):
#         self.img.bind('<Button-1>', lambda event: self.update_point(event, point))
#
#     def update_point(self, event, point):
#         print('P', point, event.x, event.y)
#         self.img.unbind('<Button-1>')


class Zones:
    def __init__(self, data, img):
        self.data = data
        self.img = img
        self.zones_label = []
        if self.data == '':
            self.zones = []
            self.next_id = 1
            return
        self.zones = self.get_all_zones()
        self.next_id = len(self.zones)

    def get_all_zones(self):
        zones = []
        liste = self.data.split('&')
        if len(liste) > 0:
            for index, zone in enumerate(self.data.split('&')):
                print(zone)
                zones.append(Zone(zone, self.img))
                self.zones_label.append(f"Zone {index}")
        else:
            zones.append(Zone(self.data, self.img))
        return zones

    def get_data_zone(self, zid):
        return self.zones[zid - 1]

    def format_for_save(self):
        str_zones = []
        for zone in self.zones:
            str_zones.append(zone.get_string())
        return '&'.join(str_zones)

    def add_zone(self):
        self.zones.append(Zone(f"{self.next_id};Zone {self.next_id};0,0,0,0,0,0,0,0", self.img))
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
    def __init__(self, data, img):
        self.data = data
        self.img = img
        print(data)
        self.id = 1
        self.name = ''
        self.coords = [(0, 0), (0, 0), (0, 0), (0, 0)]
        self.converted = [(0, 0), (0, 0), (0, 0), (0, 0)]
        self.image = ''
        self.text = ''
        self.get_zone()

    def get_string(self):
        output = [self.id, self.name, self.get_coords_str()]
        print(output)
        return ';'.join(output)

    def get_zone(self):
        column = self.data.split(';')
        if len(column) < 3:
            return
        self.id = column[0]
        self.name = column[1]
        self.coords = self.get_coords(column[2])
        self.converted = [(self.coords[0][0], self.coords[0][1])]

    def convert_for_canvas(self, i, j):
        pass

    def get_coords_str(self):
        v = self.coords
        return f'{v[0][0]},{v[0][1]},{v[1][0]},{v[1][1]},{v[2][0]},{v[2][1]},{v[3][0]},{v[3][1]}'

    def get_coords(self, data):
        if data == '':
            return [(0, 0), (0, 0), (0, 0), (0, 0)]
        else:
            v = data.split(',')
            return [(v[0], v[1]), (v[2], v[3]), (v[4], v[5]), (v[6], v[7])]


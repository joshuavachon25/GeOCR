from PIL import Image, ImageTk
from ttkbootstrap.constants import *
import ttkbootstrap as tkb
from ttkbootstrap.style import Bootstyle


class PropertyLabel(tkb.Frame):
    def __init__(self, parent, value, text):
        super().__init__(parent)
        self.columnconfigure((0, 1), uniform='a', weight=1)
        self.rowconfigure(0, uniform='a', weight=1)
        tkb.Label(self, text=text, font='14').grid(column=0, row=0, sticky='e', padx=10)
        tkb.Label(self, text=value, font='14').grid(column=1, row=0, sticky='w', padx=10)
        self.pack(fill='x', expand=True)
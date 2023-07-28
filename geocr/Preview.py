from PIL import Image, ImageTk
import ttkbootstrap as tkb


class Preview(tkb.Labelframe):
    def __init__(self, parent):
        super().__init__(parent, text='Prévisualisation')
        self.path = None
        self.image = None
        self.img = tkb.Label(self, image=None, anchor='center')
        self.img.pack(expand=True, fill='both')
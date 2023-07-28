from geocr.Menu import Menu
from geocr.DBViewer import DBViewer
from geocr.Preview import Preview
from geocr.FileExplorer import FileExplorer
from geocr.Details import Details
from geocr.Databases import Databases
from helpers.ImageHelper import *
import ttkbootstrap as tkb


class App(tkb.Window):
    # Initialisation de l'application
    def __init__(self):
        super().__init__(themename="litera")
        self.state('zoomed')
        self.title('GeOCR')
        self.geometry('1024x768')
        self.minsize(800, 600)
        self.iconbitmap('assets/ui/icon.ico')
        self.DB = Databases()

        self.columnconfigure((0,1,2), uniform='a', weight=1)
        self.rowconfigure(0, uniform='a', weight=1)
        self.rowconfigure((1, 2),  uniform='a', weight=10)

        self.top_bar = Menu(self, self.DB)
        self.top_bar.grid(column=0, row=0, columnspan=3, sticky='nsew')

        self.files = FileExplorer(self, show_exif=self.show_exif)
        self.files.grid(column=0, row=1, sticky='nsew', padx=10, pady=10)

        self.preview = Preview(self)
        self.preview.grid(column=1, row=1, sticky='nsew', padx=10, pady=10)

        self.exif = Details(self, add_to_sources=self.add_to_sources, search_in_db=self.search_in_db)
        self.exif.grid(column=2, row=1, sticky='nsew', padx=10, pady=10)

        self.db = DBViewer(self, self.DB)
        self.db.grid(column=0, row=2, columnspan=3, sticky='nsew', padx=10, pady=10)

    def show_exif(self, path):
        show_preview(self.preview, path)
        self.exif.show_details(path)

    def add_to_sources(self, data):
        self.DB.add_to_sources(data, self.db.db_view)

    def search_in_db(self, path):
        return self.DB.search_in_db_by_path(path=path)


# Ouverture de l'application
app = App()
app.mainloop()

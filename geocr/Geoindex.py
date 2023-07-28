import ttkbootstrap as tkb

from geocr.DataTable import DataTable


class Geoindex(tkb.Toplevel):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.title("Geoindex")
        self.geometry("500x500")
        self.transient(parent)
        self.update_idletasks()
        self.grab_set()
        self.DB = db

        tkb.Label(self, text='Geoindex', font='Helvetica 18').pack(fill='x', padx=10, pady=10)

        frame = tkb.Frame(self)
        frame.pack(expand=True, fill='both')

        self.db_view = DataTable(frame, 'geoindex', self.DB)
        self.db_view.pack(fill='y', expand=True, side='left')
        options = tkb.Labelframe(frame, text="Gestion des données")
        options.pack(fill='y', expand=True, side='left', padx=10, pady=10)

        self.wait_window(self)
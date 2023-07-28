from geocr.Archives import Archives
from geocr.DataTable import DataTable
import ttkbootstrap as tkb


class DBViewer(tkb.Labelframe):
    def __init__(self, parent, db):
        super().__init__(parent, text='Bases de données')
        self.parent = parent
        self.DB = db
        self.db_view = DataTable(self, 'sources', db)
        self.db_view.table.view.bind('<Double-1>', self.open_archive)
        self.DB.refresh_table_sources(self.db_view)
        self.previous_selection = None

    def open_archive(self, event):
        selected_items = self.db_view.table.view.selection()
        if not selected_items or (self.previous_selection == selected_items):
            return
        else:
            self.previous_selection = selected_items
            item_values = self.db_view.table.view.item(selected_items, 'values')
            Archives(self.parent, self.DB, item_values[0])

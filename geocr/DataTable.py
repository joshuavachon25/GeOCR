import ttkbootstrap as tkb
from ttkbootstrap.tableview import Tableview


class DataTable(tkb.Frame):
    def __init__(self, parent, schema, db):
        super().__init__(parent)
        self.DB = db
        self.schema = schema
        self.sources = ["ID", "Nom", "Projet", "Statut", "Tags"]
        self.geoindex = ["Nom", "Ref", "Type", "Catégorie"]
        self.projects = ["Nom", "Actif"]
        self.options = {"sources": self.sources, "geoindex": self.geoindex, "projects": self.projects}
        self.current_schema = self.options[self.schema]
        self.table = Tableview(self, coldata=self.current_schema, paginated=True, searchable=True, autoalign=True, bootstyle='primary')
        self.table.pack(expand=True, fill='both')

        self.pack(expand=True, fill='both', side='left', padx=10, pady=10)

    def refresh_table(self, results, cols):
        self.table.delete_rows()
        print(results)
        for result in results:
            values = []
            for c in cols:
                values.append(result[c])
            self.table.insert_row('end', values=values)

        self.table.load_table_data()

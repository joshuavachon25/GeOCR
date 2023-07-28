from tkinter import ttk


class CustomTreeView(ttk.Treeview):
    def __init__(self, parent, columns):
        super().__init__(parent)
        self['columns'] = columns
        self.column('#0', width=0, stretch=False)
        self.heading('#0', text='', anchor='w')
        for col in columns:
            self.column(col, minwidth=20)
            self.heading(col, text=col, anchor='w')

    def clear_list(self):
        for item in self.get_children():
            self.delete(item)

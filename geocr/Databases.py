import tkinter as tk
from tkinter import ttk
import sqlite3
from geocr.DataTable import DataTable
import ttkbootstrap as tkb


class Databases:
    def __init__(self):
        super().__init__()
        self.db = sqlite3.connect('geocr.db')
        self.dbmaster = self.db.cursor()
        self.init_db()

    def add_to_sources(self, data, view):
        self.dbmaster.execute(''' INSERT INTO sources(path,name,zones,project,params,tags,status,year,width,height) VALUES(?,?,?,?,?,?,?,?,?,?)''', data)
        self.db.commit()
        self.refresh_table_sources(view)

    def search_in_db_by_path(self, path):
        self.dbmaster.execute(f''' SELECT oid FROM sources WHERE path = "{path}" ''')
        return self.dbmaster.fetchall()

    def search_in_db_by_id(self, oid):
        self.dbmaster.execute(f''' SELECT * FROM sources WHERE oid = "{oid}" ''')
        return self.dbmaster.fetchall()

    def refresh_table_sources(self, view):
        self.dbmaster.execute(''' SELECT *, oid FROM sources''')
        results = self.dbmaster.fetchall()
        view.refresh_table(results, (10, 1, 3, 6, 5))

    def get_table(self):
        pass

    def get_query(self):
        pass

    def init_db(self):
        self.dbmaster.execute("""CREATE TABLE IF NOT EXISTS sources (
                path TEXT,
                name TEXT,
                zones TEXT,
                project TEXT,
                params TEXT,
                tags TEXT,
                status TEXT,
                year INTEGER,
                width INTEGER,
                height INTEGER
            )
            """)

        self.dbmaster.execute("""CREATE TABLE IF NOT EXISTS geoindex (
                name TEXT,
                has_ref INTEGER DEFAULT 0,
                ref INTEGER,
                epsg INTEGER DEFAULT 4326,
                type TEXT DEFAULT "point",
                geom TEXT DEFAULT "0.0, 0.0",
                categorie TEXT
            )
            """)

        self.dbmaster.execute("""CREATE TABLE IF NOT EXISTS projects (
                name TEXT
            )
            """)
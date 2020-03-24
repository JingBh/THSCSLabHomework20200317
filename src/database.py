import os
import re
import sqlite3

from xlrd import open_workbook

from get_path import get_path
from progress import Progress


class Database:

    def __init__(self, path="database/default.db"):
        self.path = get_path(path)
        self.conn = sqlite3.connect(self.path)

    def cursor(self):
        return self.conn.cursor()

    def commit(self):
        self.conn.commit()

    def create_tables(self):
        path = get_path("database/default.sql")
        sql = open(path, "rb").read().decode()
        self.cursor().execute(sql)
        self.commit()

    def truncate(self):
        self.cursor().execute("DROP TABLE IF EXISTS `data`")
        self.commit()
        self.create_tables()

    def select(self, sql, *args):
        return self.cursor().execute(sql, *args).fetchall()

    def load_data_source(self, path="database/source", progress: Progress = None):
        c = self.cursor()
        path = get_path(path)
        for root, dirs, files in os.walk(path):
            number = len(files)
            progress_step = 1 / number
            progress_value = 0
            if progress:
                progress.set(progress_value)
            for filename in files:
                obj = DataSource(filename)
                date = obj.get_date()
                data = obj.get_data()
                sql = "INSERT INTO `data` VALUES ('%s', ?, ?, ?, ?, ?)" % date
                c.executemany(sql, data)
                self.commit()
                progress_value += progress_step
                if progress:
                    progress.set(progress_value)
        if progress:
            progress.set(1)

    def close(self):
        self.conn.close()


class DataSource:

    def __init__(self, path, root="database/source"):
        self.path = get_path(root + "/" + path)
        self.filename = self.path.split(os.path.sep)[-1]

    def get_date(self):
        pattern = r'[0-9]{4}-[0-9]{2}-[0-9]{2}'
        return re.search(pattern, self.filename).group()

    def get_data(self):
        wb = open_workbook(self.path, True)
        table = wb.sheet_by_index(0)
        result = []
        for rowx in range(1, table.nrows):
            row = table.row_values(rowx)
            result.append(row[1:6])
        return result

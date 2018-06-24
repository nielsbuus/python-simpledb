import pathlib
import json


class SimpleDB:

    def __init__(self, storage_dir = "."):
        self.tables = {}
        self.directory = pathlib.Path(storage_dir).absolute()
        self.directory.mkdir(parents=True, exist_ok=True)

    def table(self, table_name):
        if not table_name is self.tables:
            table = SimpleTable(self, table_name, [])
            table.load_from_disk()
            self.tables[table_name] = table
        return self.tables.get(table_name)


class SimpleTable:

    def __init__(self, simple_db: SimpleDB, table_name, table_rows):
        self.table_name = table_name
        self.table_rows = table_rows
        self.table_file = simple_db.directory.joinpath(self.table_name + ".json")

    def insert(self, dict1 = None, **dict2):
        if isinstance(dict1, dict):
            chosen_dict = dict1
        else:
            chosen_dict = dict2

        self.table_rows.append(chosen_dict)
        self.save_to_disk()

    def where(self, **conditions):
        return SimpleTableScope(self, conditions)

    def delete(self):
        self.where().delete()

    def all(self):
        return self.where().to_list()

    def count(self):
        return len(self.all())

    def save_to_disk(self):
        json.dump(self.table_rows, self.table_file.open("w"), indent=2)

    def load_from_disk(self):
        if self.table_file.exists():
            self.table_rows = json.load(self.table_file.open("r"))

    def __repr__(self):
        return "SimpleDB table | " + self.table_name + " | " + self.all().__str__()

    def _set_table_rows(self, rows):
        self.table_rows = rows
        self.save_to_disk()


class SimpleTableScope:

    def __init__(self, simple_table, scope):
        self.simple_table = simple_table
        self.scope = scope

    def first(self):
        list = self.to_list()
        if len(list) > 0:
            return list[0]

    def last(self):
        list = self.to_list()
        if len(list) > 0:
            return list[-1]

    def update(self, **attributes):
        for row in self.to_list():
            for attr, val in attributes.items():
                row[attr] = val
        self.simple_table.save_to_disk()

    def delete(self):
        remaining_rows = [row for row in self.simple_table.table_rows if row not in self.to_list()]
        self.simple_table._set_table_rows(remaining_rows)

    def count(self):
        return len(self.to_list())

    def to_list(self):
        results = []
        for row in self.simple_table.table_rows:
            match = True
            for attr, val in self.scope.items():
                if not row.get(attr) == val:
                    match = False
            if match:
                results.append(row)
        return results

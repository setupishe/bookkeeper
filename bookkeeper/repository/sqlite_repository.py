from inspect import get_annotations
from abstract_repository import AbstractRepository, T
import sqlite3

class SQLiteRepository(AbstractRepository[T]):
    def __init__(self, db_file: str, cls: type) -> None:
        self.db_file = db_file
        self.table_name = cls.__name__.lower()
        self.fields = get_annotations(cls, eval_str=True)
        self.fields.pop('pk')
    def add(self, obj: T) -> int:
        names = ', '.join(self.fields.keys())
        p = ', '.join("?" * len(self.fields))

        values = [getattr(obj, x) for x in self.fields]
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
        cur.execute('PRAGMA foreign_keys = ON')
        cur.execute(
            f'INSERT INTO {self.table_name} ({names}) VALUES({p})', values)
        obj.pk = cur.lastrowid
        con.close()
        return obj.pk

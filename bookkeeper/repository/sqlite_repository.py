from inspect import get_annotations
from bookkeeper.repository.abstract_repository import AbstractRepository, T
from typing import Any
import sqlite3
from datetime import datetime

class SQLiteRepository(AbstractRepository[T]):
    def __init__(self, db_file: str, cls: type) -> None:
        self.db_file = db_file
        self.table_name = cls.__name__.lower()
        self.cls = cls
        self.fields = get_annotations(cls, eval_str=True)
        self.fields.pop('pk')
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            res = cur.execute('SELECT name FROM sqlite_master')
            db_tables = [t[0].lower() for t in res.fetchall()]
            if self.table_name not in db_tables:
                col_names = ', '.join(self.fields.keys())
                q = f'CREATE TABLE {self.table_name} (' \
                    f'"pk" INTEGER PRIMARY KEY AUTOINCREMENT, {col_names})'
                print(col_names)
                cur.execute(q)
        con.close()

    def add(self, obj: T) -> int:
        """
        Добавить объект в репозиторий, вернуть id объекта,
        также записать id в атрибут pk.
        """
        if getattr(obj, 'pk', None) != 0:
            raise ValueError(f'trying to add object {obj} with filled `pk` attribute')

        names = ', '.join(self.fields.keys())
        p = ', '.join("?" * len(self.fields))
        values = [getattr(obj, x) for x in self.fields] #TODO: сделать отдельную функцию с обработкой datetime
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            q = f'INSERT INTO {self.table_name} ({names}) VALUES ({p})'
            cur.execute(q, values)
            obj.pk = cur.lastrowid
        con.close()
        return obj.pk


    def __generate_object(self, db_row: tuple) -> T:
        obj = self.cls(self.fields)
        for field, value in zip(self.fields, db_row[1:]):
            setattr(obj, field, value)
        obj.pk = db_row[0]
        return obj

    def get(self, pk: int) -> T | None:
        """ Получить объект по id """
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            q = f'SELECT * FROM {self.table_name} WHERE pk = {pk}'
            row = cur.execute(q).fetchone()
        con.close()

        if row is None:
            return None

        return self.__generate_object(row)

    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        """
        Получить все записи по некоторому условию
        where - условие в виде словаря {'название_поля': значение}
        если условие не задано (по умолчанию), вернуть все записи
        """
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            q = f'SELECT * FROM {self.table_name}'
            if where is None:
                rows = cur.execute(q).fetchall()
            else:
                q += f' WHERE '
                for i, key in enumerate(where):
                    q += key + ' = ?'
                    if i < len(where) - 1:
                        q += ' AND '
                rows = cur.execute(q, list(where.values())).fetchall()

            if rows is None:
                return []

            res = [self.__generate_object(row) for row in rows]
        con.close()

        return res

    def update(self, obj: T) -> None:
        """ Обновить данные об объекте. Объект должен содержать поле pk. """
        if obj.pk == 0:
            raise ValueError('attempt to update object with unknown primary key')
        values = [getattr(obj, x) for x in self.fields]
        names = self.fields.keys()
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            q = f'UPDATE {self.table_name} SET '
            for i, name in enumerate(names):
                q += f'{name} = ?'
                if i < len(names) - 1:
                    q += ', '
            q += f'WHERE pk = {obj.pk}'
            cur.execute(q, values)
        con.close()

    def delete(self, pk: int) -> None:
        """ Удалить запись """
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            q = f'SELECT * FROM {self.table_name} WHERE pk = {pk}'
            res = cur.execute(q).fetchall()
            if len(res) == 0:
                raise KeyError('primary key not found')
            q = f'DELETE FROM {self.table_name} WHERE pk = {pk}'
            cur.execute(q)
        con.close()



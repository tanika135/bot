import datetime
import sqlite3
import os
from abc import ABC, abstractmethod
from sqlite3 import Connection


class DB:
    _connection = None
    _history = None
    _result = None

    def __init__(self):
        try:
            sql_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'sqlite_python.db')
            self._connection = sqlite3.connect(sql_path)
            self._history = History(self._connection)
            self._result = Result(self._connection)

        except sqlite3.Error as error:
            print("Ошибка при подключении к sqlite", error)

    def __del__(self):
        if self._connection:
            cursor = self._connection.cursor()
            cursor.close()

    def add_history(self, command: str, chat_id: int, results: list = []):
        command_id = self._history.add({
            'command': command,
            'chat_id': int(chat_id)
        })

        if results and command_id:
            for hotel in results:
                self._result.add({
                    'command_id': command_id,
                    'hotel': f'Отель: {hotel["name"]} цена: {hotel["price"]} расстояние: {hotel["distance"]} '
                })

    def read_history(self, chat_id: int, limit: int) -> list:
        commands = self._history.list(chat_id=chat_id, limit=limit)
        result = []

        if commands:
            for command in commands:
                record = list(command)
                record.append(self._result.list(command[0], 0))
                result.append(record)

        return result


class TableInterface(ABC):

    @abstractmethod
    def add(self, data: dict) -> int:
        return 0

    @abstractmethod
    def list(self, chat_id: int, limit: int = 0) -> list:
        return []


class History(TableInterface):
    _connection = None

    def __init__(self, connection: Connection):
        self._connection = connection
        sqlite_create_table_query = '''CREATE TABLE IF NOT EXISTS history (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    chat_id INTEGER NOT NULL,
                                    name TEXT NOT NULL,
                                    date datetime);'''

        self._cursor = self._connection.cursor()
        self._cursor.execute(sqlite_create_table_query)
        self._connection.commit()

    def add(self, data) -> int:
        cursor = self._connection.cursor()
        now = datetime.datetime.now()

        record = (data['chat_id'], data['command'], now.strftime("%d/%m/%Y %H:%M:%S"))
        cursor.execute("INSERT INTO history (chat_id, name, date) VALUES(?, ?, ?);", record)

        self._connection.commit()
        result = cursor.lastrowid
        cursor.close()
        return result

    def list(self, chat_id: int, limit: int= 0) -> list:
        cursor = self._connection.cursor()
        cursor.execute("SELECT * FROM history WHERE chat_id = ? ORDER BY id DESC LIMIT ? ;", (chat_id, limit))
        result = cursor.fetchall()
        cursor.close()
        return result


class Result(TableInterface):
    _connection = None

    def __init__(self, connection: Connection):
        self._connection = connection
        sqlite_create_table_query = '''CREATE TABLE IF NOT EXISTS result (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    command_id INTEGER NOT NULL,
                                    hotel TEXT NOT NULL
                                    );'''

        self._cursor = self._connection.cursor()
        self._cursor.execute(sqlite_create_table_query)
        self._connection.commit()

    def add(self, data) -> int:
        cursor = self._connection.cursor()

        record = (data['command_id'], data['hotel'])
        cursor.execute("INSERT INTO result (command_id, hotel) VALUES(?, ?);", record)

        self._connection.commit()
        result = cursor.lastrowid
        cursor.close()
        return result

    def list(self, command_id: int, limit: int = 0) -> list:
        cursor = self._connection.cursor()
        cursor.execute("SELECT * FROM result WHERE command_id = ? ORDER BY id DESC;", (command_id,))
        result = cursor.fetchall()
        cursor.close()
        return result

import sqlite3
import typing
import json
from textwrap import dedent
from rich import print


class Sqlmanager:
    """
    A class for interacting with a SQLite database.

    Args
    ----
    DbName: str
        The name of the database file.
    TableName: str
        The name of the table in the database.

    Examples
    --------
    >>> db = Db(DbName="Data.sql", TableName="DataTable")
    >>> db[0] = {"Name": "Alice", "Age": 30, "City": "New York"}
    >>> db[1] = {"Name": "Bob", "Age": 25, "City": "Los Angeles"}
    >>> db[2] = {"Name": "Charlie", "Age": 35, "City": "Chicago"}
    >>> db[3] = {"Name": "David", "Age": 40, "City": "Houston"}
    >>> db[4] = {"Name": "Eve", "Age": 30, "City": "Phoenix"}

    This will create or update the table "DataTable" with the provided data.

    >>> db.clear()

    This will clear the table.
    """

    def __init__(self, DbName: str = "Data.sql", TableName: str = "DataTable") -> None:
        """
        Initializes the database with the specified name and table.

        Args
        ----
        DbName: str
            The name of the database file.
        TableName: str
            The name of the table in the database.

        Examples
        --------
        >>> db = Db(DbName="Data.sql", TableName="DataTable")
        """
        self.DbName: str = DbName
        self.TableName: str = TableName
        self.conn: sqlite3.Connection = sqlite3.connect(self.DbName)
        self.cursor: sqlite3.Cursor = self.conn.cursor()
        self.addlist: typing.Callable[..., None] = self._addConstructor()

    def _addConstructor(self) -> typing.Callable[..., None]:
        """
        Creates the necessary table in the database.
        """
        self.cursor.execute(dedent(f'''
        CREATE TABLE IF NOT EXISTS {self.TableName} (
            D TEXT
        )'''))

        def add(*args: typing.Any, **kwargs: typing.Any) -> None:
            assert len(args) == 0, "Unexpected positional arguments"
            assert all(isinstance(k, str) for k in kwargs), "Keys must be strings"
            jsonData = json.dumps(kwargs)
            self.cursor.execute(f'INSERT INTO {self.TableName} (D) VALUES (?)', (jsonData,))
            self.conn.commit()
        return add

    def __setitem__(self, index: int, value: typing.Dict[str, typing.Any]) -> None:
        """
        Sets the value at the specified index.

        Args
        ----
            index (int): The index to set the value for.
            value (Dict[str, Any]): The value to set at the specified index.

        Raises
        ------
            IndexError: If the index is out of range.

        Examples
        --------
        >>> db = Db(ValuesType=dict)
        >>> db[0] = {"name": "Alice", "age": 25}
        """
        assert isinstance(index, int), "Index must be an integer"
        self.cursor.execute(f"SELECT COUNT(*) FROM {self.TableName}")
        count = self.cursor.fetchone()[0]
        if count == 0 or not (-count <= index < count):
            raise IndexError("Index out of range")
        if index < 0:
            index += count
        jsonData = json.dumps(value)
        self.cursor.execute(
            f'UPDATE {self.TableName} SET D=? WHERE rowid=(SELECT rowid FROM {self.TableName} LIMIT 1 OFFSET ?)',
            (jsonData, index))
        self.conn.commit()

    def __getitem__(self, index: typing.Union[int, slice]) -> typing.Any:
        """
        Gets the value at the specified index.

        Args
        ----
            index (Union[int, slice]): The index to get the value for.

        Raises
        ------
            IndexError: If the index is out of range.

        Examples
        --------
        >>> db = Db(ValuesType=dict)
        >>> db[0] = {"name": "Alice", "age": 25}
        >>> print(db[0])
        {'name': 'Alice', 'age': 25}

        >>> print(db[-1])
        {'name': 'Alice', 'age': 25}
        """

        if isinstance(index, int):
            self.cursor.execute(f"SELECT COUNT(*) FROM {self.TableName}")
            count = self.cursor.fetchone()[0]
            if count == 0:
                raise IndexError("Index out of range, table is empty")
            elif -count <= index < count:
                if index < 0:
                    index += count
                self.cursor.execute(f"SELECT D FROM {self.TableName} LIMIT 1 OFFSET ?", (index,))
                result = self.cursor.fetchone()
                if result:
                    return json.loads(result[0])
                else:
                    raise IndexError("Index out of range")
            else:
                raise IndexError("Index out of range")
        elif isinstance(index, slice):
            start = index.start or 0
            stop = index.stop
            step = index.step or 1
            self.cursor.execute(f"SELECT COUNT(*) FROM {self.TableName}")
            count = self.cursor.fetchone()[0]
            if count == 0:
                return []
            if start < 0:
                start += count
            if stop is not None:
                if stop < 0:
                    stop += count
                stop = min(count, stop)
            else:
                stop = count
            start = max(0, min(count, start))
            query = f"SELECT D FROM {self.TableName} LIMIT ? OFFSET ?"
            params = [stop - start, start]
            self.cursor.execute(query, params)
            results = self.cursor.fetchall()[::step]
            return [json.loads(result[0]) for result in results]
        else:
            raise TypeError("Invalid index type for list-like data")

    def __delitem__(self, index: int) -> None:
        """
        Deletes the value at the specified index.

        Args
        ----
            index (int): The index to delete the value for.

        Raises
        ------
            IndexError: If the index is out of range.

        Examples
        --------
        >>> db = Db(ValuesType=dict)
        >>> db[0] = {"name": "Alice", "age": 25}
        >>> del db[0]
        """
        assert isinstance(index, int), "Index must be an integer"
        self.cursor.execute(f"SELECT COUNT(*) FROM {self.TableName}")
        count = self.cursor.fetchone()[0]
        if count == 0 or not (-count <= index < count):
            raise IndexError("Index out of range")
        if index < 0:
            index += count
        self.cursor.execute(
            f'DELETE FROM {self.TableName} WHERE rowid=(SELECT rowid FROM {self.TableName} LIMIT 1 OFFSET ?)',
            (index,))
        self.conn.commit()

    def extend(self, data_list: typing.List[typing.Dict[str, typing.Any]]) -> None:
        """
        Appends the elements of data_list to the end of the list-like data.

        Args
        ----
            data_list (List[Dict[str, Any]]): The list of dictionaries to append to the list-like data.

        Raises
        ------
            TypeError: If data_list is not a list of dictionaries.

        Examples
        --------
        >>> db = Db(ValuesType=dict)
        >>> db.extend([{"name": "Alice", "age": 25}, {"name": "Bob", "age": 30}])
        """
        assert isinstance(data_list, list), "Data must be a list"
        for data in data_list:
            assert isinstance(data, dict), "Elements of data_list must be dictionaries"
        jsonDataList = [(json.dumps(data),) for data in data_list]
        self.cursor.executemany(f'INSERT INTO {self.TableName} (D) VALUES (?)', jsonDataList)
        self.conn.commit()

    def append(self, data: typing.Dict[str, typing.Any]) -> None:
        """
        Appends the dictionary data to the end of the list-like data.

        Args
        ----
            data (Dict[str, Any]): The dictionary to append to the list-like data.

        Raises
        ------
            TypeError: If data is not a dictionary.

        Examples
        --------
        >>> db = Db(ValuesType=dict)
        >>> db.append({"name": "Alice", "age": 25})
        """
        assert isinstance(data, dict), "Data must be a dictionary"
        jsonData = json.dumps(data)
        self.cursor.execute(f'INSERT INTO {self.TableName} (D) VALUES (?)', (jsonData,))
        self.conn.commit()

    def pop(self, index: int = -1) -> typing.Dict[str, typing.Any]:
        """
        Removes and returns the value at the specified index.

        Args
        ----
            index (int, optional): The index of the value to remove. Defaults to -1.

        Raises
        ------
            IndexError: If the index is out of range.

        Examples
        --------
        >>> db = Db(ValuesType=dict)
        >>> db[0] = {"name": "Alice", "age": 25}
        >>> db.pop(0)
        {'name': 'Alice', 'age': 25}
        """
        assert isinstance(index, int), "Index must be an integer"

        jsonData = self[index]
        self.__delitem__(index)
        return jsonData

    def clear(self) -> None:
        """
        Removes all values from the list-like data.

        Examples
        --------
        >>> db = Db(ValuesType=dict)
        >>> db[0] = {"name": "Alice", "age": 25}
        >>> db.clear()
        >>> print(db)
        []
        """
        self.cursor.execute(f'DELETE FROM {self.TableName}')
        self.conn.commit()

    def __iter__(self) -> typing.Iterator[typing.Dict[str, typing.Any]]:
        """
        Returns an iterator over the list-like data.

        Examples
        --------
        >>> db = Db(ValuesType=dict)
        >>> db[0] = {"name": "Alice", "age": 25}
        >>> db[1] = {"name": "Bob", "age": 30}
        >>> for item in db:
        ...     print(item)
        {'name': 'Alice', 'age': 25}
        {'name': 'Bob', 'age': 30}
        """
        self.cursor.execute(f"SELECT D FROM {self.TableName}")
        results = self.cursor.fetchall()
        for result in results:
            yield json.loads(result[0])

    def __len__(self) -> int:
        """
        Returns the number of values in the list-like data.

        Examples
        --------
        >>> db = Db(ValuesType=dict)
        >>> db[0] = {"name": "Alice", "age": 25}
        >>> len(db)
        1
        """
        self.cursor.execute(f"SELECT COUNT(*) FROM {self.TableName}")
        return self.cursor.fetchone()[0]

    def __repr__(self) -> str:
        """
        Returns a string representation of the list-like data.

        Examples
        --------
        >>> db = Db(ValuesType=dict)
        >>> db[0] = {"name": "Alice", "age": 25}
        >>> print(db)
        [{'name': 'Alice', 'age': 25}]
        """
        self.cursor.execute(f"SELECT D FROM {self.TableName}")
        results = self.cursor.fetchall()
        return json.dumps([json.loads(result[0]) for result in results])

    def remove(self, data: typing.Dict[str, typing.Any]) -> None:
        """
        Removes the first occurrence of the dictionary data from the list-like data.

        Args
        ----
            data (Dict[str, Any]): The dictionary to remove from the list-like data.

        Raises
        ------
            TypeError: If data is not a dictionary.

        Examples
        --------
        >>> db = Db(ValuesType=dict)
        >>> db[0] = {"name": "Alice", "age": 25}
        >>> db.remove({"name": "Alice", "age": 25})
        """
        assert isinstance(data, dict), "Data must be a dictionary"
        jsonData = json.dumps(data)
        self.cursor.execute(f'DELETE FROM {self.TableName} WHERE D = ?', (jsonData,))
        self.conn.commit()

    def count(self, data: typing.Dict[str, typing.Any]) -> int:
        """
        Returns the number of occurrences of the dictionary data in the list-like data.

        Args
        ----
            data (Dict[str, Any]): The dictionary to count in the list-like data.

        Raises
        ------
            TypeError: If data is not a dictionary.

        Examples
        --------
        >>> db = Db(ValuesType=dict)
        >>> db[0] = {"name": "Alice", "age": 25}
        >>> db.count({"name": "Alice", "age": 25})
        1
        """
        assert isinstance(data, dict), "Data must be a dictionary"
        jsonData = json.dumps(data)
        self.cursor.execute(f'SELECT COUNT(*) FROM {self.TableName} WHERE D = ?', (jsonData,))
        return self.cursor.fetchone()[0]

    def index(self, data: typing.Dict[str, typing.Any]) -> int:
        """
        Returns the index of the first occurrence of the dictionary data in the list-like data.

        Args
        ----
            data (Dict[str, Any]): The dictionary to find the index of in the list-like data.

        Examples
        --------
        >>> db = Db(ValuesType=dict)
        >>> db[0] = {"name": "Alice", "age": 25}
        >>> db.index({"name": "Alice", "age": 25})
        0
        """
        assert isinstance(data, dict), "Data must be a dictionary"
        jsonData = json.dumps(data)
        self.cursor.execute(f'SELECT rowid FROM {self.TableName} WHERE D = ?', (jsonData,))
        result = self.cursor.fetchone()
        if result is not None:
            return result[0] - 1  # SQLite rowids are 1-indexed, but Python lists are 0-indexed
        else:
            return -1


if __name__ == "__main__":

    db = Sqlmanager()

    # db.addlist(name="Johndoe", age=30, city="New York")
    # db.addlist(name="Johndoe2", age=31, city="New")
    # db[-1] = {"name": "subhash", "age": 99, "city": "india"}
    # del db[1]
    # print(db)
    # print(db.count({"name": "subhash"}))
    # print(db.index({"name": "Johndoe"}))

    # db.remove({"name": "subhash", "age": 99, "city": "india"})
    # print(db[:])

    # db.clear()
    # print(db)
    # for i in db:
        # print(i)
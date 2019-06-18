from .filesqlitedb import FileSQLiteDB
import pickle as pkl
import asyncio


__all__ = ["Keystore"]

class Keystore(FileSQLiteDB):
    def __init__(self, *args, flag_auto_commit=True, **kwargs):
        super().__init__(*args, **kwargs)
        self.flag_auto_commit = flag_auto_commit
    async def async_commit(self):
        """
        Asynchronous version of commit().

        https://stackoverflow.com/questions/52682336/async-sqlite-python
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, lambda: self.commit())

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            pass
        return default

    def __getitem__(self, key):
        conn = self.get_conn()
        cursor = conn.execute("select value from data where key = ?", (key,))
        __res = cursor.fetchone()
        if __res is None:
            print(f"KEYSTORE VAI RAISAR para '{key}")
            raise KeyError(f"Key not found: '{key}'")

        _res = __res[0]
        res = self._unpickle(_res)
        print(f"KEYSTORE RETORNANDO '{res}' PARA '{key}'")
        return res

    def __setitem__(self, key, value):
        n = self.execute("select count(*) from data where key = ?", (key,)).fetchone()[0]
        value_ = self._pickle(value)
        if n > 0:
            self.execute("update data set value = ? where key = ?", (value_, key))
        else:
            self.execute("insert into data values (?, ?)", (key, value_))
        if self.flag_auto_commit:
            self.commit()
        return value


    # OVERRIDEN

    def _create_schema(self, cursor):
        """Responsible for executing the CREATE TABLE statements"""
        conn = self.get_conn()
        conn.execute("create table data (key string not null primary key,"
                            "value text)")
        conn.execute("create index data_key on data (key)")
        self.commit()

    def _pickle(self, obj):
        return pkl.dumps(obj)

    def _unpickle(self, s):
        return pkl.loads(s)
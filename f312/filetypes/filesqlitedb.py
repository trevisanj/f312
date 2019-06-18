import shutil
import os
from collections import OrderedDict
import sqlite3
import a107


__all__ = ["FileSQLiteDB", "get_table_info"]


class FileSQLiteDB(object):
    """Represents a SQLite database file.

    This class is not supposed to be instantialized. It serves as an ancestor for other classes
    that implement specific database schemas."""

    def __init__(self, filename):
        self.__conn = None

        self.filename = filename
        self.ensure_schema()

    # # You should override this
    #   ========================

    def _create_schema(self, cursor):
        """Responsible for executing the CREATE TABLE statements"""
        pass

    def _populate(self):
        """Responsible for that initial kick to a DB with all tables created, but empty"""
        pass

    # # Interface
    #   =========

    def execute(self, *args, **kwargs):
        """Executes a query; wraps connection.execute().

        Returns:
            cursor
        """
        conn = self.__get_conn()
        return conn.execute(*args, **kwargs)

    def test(self, filename):
        """Tries to run harmless SQL statement thereby checking if the database is sane."""
        self.__get_conn(filename=filename)
        self.get_table_names()

    def save_as(self, filename):
        """Closes connection, copies DB file, and opens again pointing to new file.

        **Note** if filename equals current filename, does nothing!
        """
        if filename != self.filename:
            self.__ensure_filename()
            self.__close_if_open()
            shutil.copyfile(self.filename, filename)
            self.__get_conn(filename=filename)

    def commit(self):
        self.get_conn().commit()

    def ensure_schema(self):
        """Create file and schema if it does not exist yet."""
        self.__ensure_filename()
        if not os.path.isfile(self.filename):
            self.create_schema()

    def close_if_open(self):
        return self.__close_if_open()

    def delete(self):
        """Removes .sqlite file. **CAREFUL** needless say"""
        self.__ensure_filename()
        self.__close_if_open()
        os.remove(self.filename)

    def create_schema(self):
        """Creates database schema"""
        self.__ensure_filename()
        self.__create_schema()

    def populate(self):
        """Series of INSERT statements to populate database with its initial contents"""
        self.__ensure_filename()
        self._populate()

    def get_conn(self, flag_force_new=False):
        """
        Returns a "seasoned" sqlite3.Connection object.

        Args:
            flag_force_new: returns a new connection irrespective of one already being open.
                            Does **not** close existing open connection

        """
        self.__ensure_filename()
        return self.__get_conn(flag_force_new)

    def get_column_names(self, tablename):
        info = self.get_table_info(tablename)
        return list(info.keys())

    def get_table_info(self, tablename):
        """Returns information about fields of a specific table

        Returns:  {"fieldname": row, ...}
        """
        conn = self.__get_conn()

        return get_table_info(conn, tablename)

        if len(ret) == 0:
            raise RuntimeError("Cannot get info for table '{}'".format(tablename))

        return ret

    def get_table_names(self):
        # http://stackoverflow.com/questions/305378/list-of-tables-db-schema-dump-etc-using-the-python-sqlite3-api

        conn = self.__get_conn()

        return self.__get_table_names(conn)

    # # Internal gear
    #   =============

    def __get_table_names(self, conn):
        # Note: passing conn as argument is needed to avoid cyclic recursion, because
        r = conn.execute("select name from sqlite_master where type = 'table'")
        names = [row["name"] for row in r]
        return names

    def __conn_is_open(self):
        """Tests sqlite3 connection, returns T/F"""
        if self.__conn is None:
            return False

        try:
            self.__get_table_names(self.__conn)
            return True
        except sqlite3.ProgrammingError as e:
            return False

    def __get_conn(self, flag_force_new=False, filename=None):
        """Returns connection to database. Tries to return existing connection, unless flag_force_new

        Args:
            flag_force_new:
            filename:

        Returns: sqlite3.Connection object

        **Note** this is a private method because you can get a connection to any file, so it has to
                 be used in the right moment
        """
        flag_open_new = flag_force_new or not self.__conn_is_open()

        if flag_open_new:
            if filename is None:
                filename = self.filename
            # funny that __get_conn() calls _get_conn() but that's it
            conn = self.__get_conn_really(filename)
            self.__conn = conn
        else:
            conn = self.__conn
        return conn

    def __get_conn_really(self, filename):
        # https://stackoverflow.com/questions/1829872/how-to-read-datetime-back-from-sqlite-as-a-datetime-instead-of-string-in-python
        conn = sqlite3.connect(filename, detect_types=sqlite3.PARSE_DECLTYPES)
        # I think this will give rows with both numeric and string indexes
        conn.row_factory = sqlite3.Row

        return conn

    def __close_if_open(self):
        if self.__conn_is_open():
            self.__conn.close()
            self.__conn = None

    def __ensure_filename(self):
        if self.filename is None:
            raise RuntimeError("'filename' attribute is not set")

    def __create_schema(self):
        conn = self.get_conn()
        self._create_schema(conn.cursor())
        conn.commit()


def get_table_info(conn, tablename):
    """
    Returns information about fields of a specific table

    Args:
        conn: sqlite3 Connection object
        tablename: string

    Returns:
        {"fieldname": row, ...}
    """

    r = conn.execute("pragma table_info('{}')".format(tablename))
    ret = OrderedDict(((row["name"], row) for row in r))
    return ret



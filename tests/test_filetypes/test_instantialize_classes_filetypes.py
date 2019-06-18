import os
import f312.filetypes as ft


def test_DataFile():
    _ = ft.DataFile()
    print(_)


def test_FilePy():
    _ = ft.FilePy()


def test_FileSQLiteDB(tmpdir):
    os.chdir(str(tmpdir))
    _ = ft.FileSQLiteDB("yamayama.sqlite")


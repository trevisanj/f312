import datetime
from .datafile import DataFile
import a107
import re

__all__ = ["FilePy"]


class FilePy(DataFile):
    """
    Base class for a configuration file saved as a .py Python source script

    **Usage**: Inherit this class and implemente _load_from_module() and _make_code().

    File header is automatic, just worry about the code
    """
    # ABSTRACT

    def _load_from_module(self, module):
        """This method should populate self-attributes based on the module argument"""
        raise NotImplementedError()

    def _make_code(self):
        """This method should create Python code based on self-attributes for the purpose of saving the file.
        """
        raise NotImplementedError()

    # OVERRIDE

    def _do_load(self, filename):
        module = a107.import_module(filename)
        self._load_from_module(module)

    def _do_save_as(self, filename):
        with open(filename, "w") as h:
            h.write("{}\n".format(self.__get_header()))
            h.write(self._make_code())

    def init_default(self):
        raise RuntimeError("Resource not available")

    # PRIVATE

    def __test_magic(self, filename):
        with open(filename, "r") as file:
            line = file.readline()
            if not re.match(r"\s*#\s*-\*-\s*\s*{}\s*-\*-".format(self.classname), line):
                raise RuntimeError("File '{}' does not appear to be a '{}' (expected first line of code:"
                                   " \"{}\")".format(filename, self.classname, self._get_magic()))

    def __get_header(self):
        """
        Returns string to be at top of file"""

        return "{}\n#\n# @ Now @ {}\n#\n".format(self._get_magic(), datetime.datetime.now())


    def __get_magic(self):
        """
        Returns string to be written the first line of .py file

        **Note** Newline character **not** included
        """

        return "# -*- {} -*-".format(self.classname)



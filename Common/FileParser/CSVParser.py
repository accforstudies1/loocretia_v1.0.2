#!/usr/bin/env python

# ************************************
#   This file contains an CSV Parser
# ************************************

from . import BaseParser
import csv


class CSVParser(BaseParser):
    """
        This class parse a csv file
    """

    # *****************
    #   Constructor
    # *****************
    def __init__(self, ai_file_path: str = "", ai_delimiter: str = ";"):
        super().__init__(ai_file_path)

        # Members
        # ************
        self.__m_delimiter = ai_delimiter

    # ******************
    #  Overridden methods
    # ********************
    def _decode(self, ai_file_path: str):
        w_result = False

        # Open and read the csv file
        # *******************************
        with open(ai_file_path, "r", newline='', encoding="utf-8") as w_file:
            # Decode the first line
            w_reader = csv.DictReader(w_file, delimiter=self.__m_delimiter, quotechar="\"")
            w_index_line = 0
            for w_row in w_reader:
                # Fill the data
                self._m_data[w_index_line] = w_row
                w_index_line += 1

            w_result = bool(self._m_data)

        return w_result

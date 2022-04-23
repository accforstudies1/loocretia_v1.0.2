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
        with open(ai_file_path, "r", newline='') as w_file:
            w_reader = csv.reader(w_file, delimiter=self.__m_delimiter, quotechar="\"")

            # Decode the first line
            w_first_line = next(w_reader)
            w_nb_words_expected = len(w_first_line)

            # Read the other lines
            w_index_line = 0
            w_result = True
            for w_line in w_reader:
                # Fill the data
                if len(w_line) == w_nb_words_expected:
                    self._m_data[w_index_line] = {}
                    for w_index_column in range(w_nb_words_expected):
                        self._m_data[w_index_line][w_index_column] = w_line[w_index_column]

                # Line error
                else:
                    self._m_data.clear()
                    w_result = False
                    break

            if w_result:
                w_result = bool(self._m_data)

        return w_result

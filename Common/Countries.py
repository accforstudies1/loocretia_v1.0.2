#!/usr/bin/env python

# ***********************************
#   This file contains a class that
#   handles countries from twitter
# ************************************

from Common.FileParser import CSVParser


class CountriesTwitter:
    """
        This class handles
        a list of countries for twitter request
    """

    # *******************
    #  Constructor
    # *******************
    def __init__(self, ai_file_path: str, ai_delimiter: str = ","):
        """
        :param ai_file_path: CSV file containing all countries
        """
        # Members
        # ***********
        self.__m_dict_id_value = {}
        self.__m_dict_value_id = {}
        self.__m_is_valid = False

        # Read the file
        w_parser = CSVParser(ai_file_path, ai_delimiter)
        if w_parser.read():
            for w_object in w_parser.data.values():
                w_id = w_object["id"]
                w_value = w_object["value"]
                self.__m_dict_id_value[w_value] = w_id
            self.__m_is_valid = bool(self.__m_dict_id_value)

    # ***************
    #   Getter
    # ***************
    @property
    def ids(self) -> list[str]:
        return list(self.__m_dict_id_value.keys())

    @property
    def values(self) -> list[str]:
        return list(self.__m_dict_id_value.keys())

    @property
    def is_valid(self) -> bool:
        return self.__m_is_valid

    # ***************
    #  Operations
    # ***************
    def get_id(self, ai_value: str) -> str:
        """
        Get country id
        :param ai_value:
        :return: Id of the value or empty string if not found
        """

        w_id = ""

        if self.__m_is_valid:
            # Check first in the cache
            if ai_value in self.__m_dict_value_id.keys():
                w_id = self.__m_dict_value_id[ai_value]
            # Check by looking into the country dict => O(N)
            else:
                for w_key, w_value in self.__m_dict_id_value.items():
                    if w_value == ai_value:
                        self.__m_dict_value_id[w_value] = w_key
                        w_id = w_key
                        break

        return w_id



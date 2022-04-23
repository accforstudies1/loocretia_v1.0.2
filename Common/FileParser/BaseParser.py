#!/usr/bin/env python

# ******************************
#   This file contains the base class for each
#   file parser
# ************************************************

from abc import abstractmethod, ABCMeta
import os


class BaseParser(metaclass=ABCMeta):
    """
        This class is the base class of each
        file parser (abstract class)
    """

    # ***************
    #   Constructor
    # ****************
    def __init__(self, ai_file_path: str = ""):
        # Members
        # ***********
        self.__m_is_valid = False
        self.__m_file_path = ai_file_path
        self._m_data = {}

    # *****************
    #   Getter
    # *****************
    @property
    def is_valid(self) -> bool:
        return self.__m_is_valid

    @property
    def data(self) -> dict:
        return self._m_data

    # ****************
    #   Operations
    # *****************
    def read(self, ai_file_path: str = "", ai_force: bool = False) -> bool:
        """
        Read the file
        :param ai_file_path:
        :param ai_force:
        :return: True if the file has been properly read and decoded
        """

        if not self.__m_is_valid or ai_force:
            self.__m_is_valid = False
            w_file_path = ai_file_path if bool(ai_file_path) else self.__m_file_path

            # Decode the file
            if os.path.isfile(w_file_path):
                self.__m_is_valid = self._decode(w_file_path)

        return self.__m_is_valid

    # *******************
    #   Abstract methods
    # ********************
    @abstractmethod
    def _decode(self, ai_file_path: str) -> bool:
        """
        Parse the file
        :param ai_file_path:
        :return: True if file has been parsed
        """
        pass

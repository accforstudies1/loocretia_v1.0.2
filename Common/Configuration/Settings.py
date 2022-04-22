#!/usr/bin/env python

# *************************************
#   This file contains a class
#   that read a configuration file
# *************************************

import json
import os


class Settings:
    """
        This class reads a configuration file
    """

    # Constants
    # ****************
    __Key = "Settings"

    # ********************
    #  Static members
    # *********************
    DefaultInstance = Settings()

    # ******************
    #   Constructor
    # ******************
    def __init__(self, ai_config_file_path: str = "Config.json"):
        # Members
        # **************
        self.__m_config_file_path = ai_config_file_path
        self.__m_configuration = {}
        self.__m_is_valid = False

    # ***************
    #   Getter
    # ***************
    @property
    def data(self) -> dict:
        return self.__m_configuration

    @property
    def is_valid(self) -> bool:
        return self.__m_is_valid

    # ***************
    #  Operations
    # ***************
    def read(self, ai_config_file_path: str = "", ai_force: bool = false) -> bool:
        """
        Parse the configuration file
        :param ai_config_file_path:
        :param ai_force:
        :return: True if the configuration path has been parsed
        """
        if not self.__m_is_valid or ai_force:
            self.__m_is_valid = False

            w_file_path = ai_config_file_path if bool(ai_config_file_path) else self.__m_config_file_path

            # Decode the file => Json file
            # ********************************
            if os.path.is_file(w_file_path):
                with open(w_file_path, "r") as w_file:
                    w_json_data = json.load(w_file)

                    # Get the data
                    # ****************
                    if (type(w_json_data) is dict) and (Settings.__Key in w_json_data.keys()):
                        self.__m_configuration = w_json_data[Settings.__Key]
                        self.__m_is_valid = True

        return self.__m_is_valid

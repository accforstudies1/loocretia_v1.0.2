#!/usr/bin/env python

# *********************************
#   This file contains a class
#   that holds credentials data
# *********************************

from Common.Configuration import Settings
import logging


class Credentials:
    """
        This class hold special credentials
    """

    # ******************
    #   Constructor
    # *******************
    def __init__(self, ai_settings: Settings = Settings.instance()):
        # Members
        # ***********
        self.__m_user_key = ""
        self.__m_user_secret = ""
        self.__m_access_token = ""
        self.__m_access_token_secret = ""
        self.__m_is_valid = False

        # Configure the logger
        self.__m_logger = logging.getLogger(__name__)
        self.__m_logger.setLevel(logging.DEBUG)
        w_console_handler = logging.StreamHandler()
        w_console_handler.setFormatter(logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s"))
        self.__m_logger.addHandler(w_console_handler)

        # Load from config
        self.__load_from_config(ai_settings)

    # *********************
    #   Getter / Setter
    # **********************
    @property
    def user_key(self) -> str:
        return self.__m_user_key

    @property
    def user_secret(self) -> str:
        return self.__m_user_secret

    @property
    def access_token(self) -> str:
        return self.__m_access_token

    @property
    def access_token_secret(self) -> str:
        return self.__m_access_token_secret

    @property
    def is_valid(self) -> bool:
        return self.__m_is_valid

    @user_key.setter
    def user_key(self, ai_user_key: str):
        if bool(ai_user_key):
            self.__m_user_key = ai_user_key

    @user_secret.setter
    def user_secret(self, ai_user_secret: str):
        if bool(ai_user_secret):
            self.__m_user_secret = ai_user_secret

    @access_token.setter
    def access_token(self, ai_token: str):
        if bool(ai_token):
            self.__m_access_token = ai_token

    @access_token_secret.setter
    def access_token_secret(self, ai_token_secret: str):
        if bool(ai_token_secret):
            self.__m_access_token_secret = ai_token_secret

    # *********************
    #   Operations
    # **********************
    def validate(self):
        """
        Validate the current credentials (check if each field is not empty)
        :return: True if it has been validated
        """
        self.__m_is_valid = bool(self.__m_user_secret) and bool(self.__m_user_key) \
            and bool(self.__m_access_token) and bool(self.__m_access_token_secret)

        return self.__m_is_valid

    # ***********************
    #   Operator overload
    # ***********************
    def __eq__(self, other) -> bool:
        if not isinstance(other, Credentials):
            return False

        return self.__m_user_secret == other.__m_user_secret \
            and self.__m_user_secret == other.__m_user_secret \
            and self.__m_access_token == other.__m_access_token \
            and self.__m_access_token_secret == other.__m_access_token_secret \
            and self.__m_is_valid == other.__m_is_valid

    # ********************
    #  Private methods
    # ********************
    @staticmethod
    def __check_value_type(ai_value, ai_type, ai_default_value):
        """
        Check if the value corresponds to the type
        :param ai_value:
        :param ai_type:
        :param ai_default_value: default value if the value is not an instance of the type
        :return: value or default value if type does not match
        """
        w_value = ai_default_value

        if type(w_value) is ai_type:
            w_value = ai_value

        return w_value

    def __load_from_config(self, ai_settings: Settings) -> bool:
        """
        Load credentials from settings
        :param ai_settings:
        :return: True if the credentials has been loaded from Settings
        """

        # Load each property
        # **********************
        if ai_settings.read():
            self.__m_is_valid = True

            # Consumer part
            w_consumer_dict = ai_settings.get("consumer")
            if type(w_consumer_dict) is dict:
                if {"key", "secret"} <= w_consumer_dict.keys():
                    self.__m_user_key = self.__check_value_type(w_consumer_dict["key"], str, "")
                    self.__m_user_secret = self.__check_value_type(w_consumer_dict["secret"], str, "")
                    self.__m_is_valid &= bool(self.__m_user_secret) and bool(self.__m_user_secret)
                else:
                    self.__m_logger.error("Consumer key has not been found")
                    self.__m_is_valid = False
            else:
                self.__m_is_valid = False

            # Token part
            if self.__m_is_valid:
                w_token_dict = ai_settings.get("token")
                if type(w_token_dict) is dict:
                    if {"access", "access_secret"} <= w_token_dict.keys():
                        self.__m_access_token = self.__check_value_type(w_token_dict["access"], str, "")
                        self.__m_access_token_secret = self.__check_value_type(w_token_dict["access_secret"], str, "")
                        self.__m_is_valid &= bool(self.__m_access_token) and bool(self.__m_access_token_secret)
                else:
                    self.__m_is_valid = False
                    self.__m_logger.error("Token key has not been found")
        else:
            self.__m_logger.error("Settings are not valid")

        return self.__m_is_valid

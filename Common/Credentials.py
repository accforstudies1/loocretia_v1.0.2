#!/usr/bin/env python

# *********************************
#   This file contains a class
#   that holds credentials data
# *********************************

from Common.Configuration import Settings


class Credentials:
    """
        This class hold special credentials
    """

    # ******************
    #   Constructor
    # *******************
    def __init__(self, ai_read_from_default_config: bool = True):
        # Members
        # ***********
        self.__m_user_key = ""
        self.__m_user_secret = ""
        self.__m_access_token = ""
        self.__m_access_token_secret = ""
        self.__m_is_valid = False

        # Load from default value
        if ai_read_from_default_config:
            self.__load_from_default_config()

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

    def __load_from_default_config(self):
        """
        Load credentials from default config
        :return:
        """
        w_configuration_instance = Settings.instance()

        # Load each property
        # **********************
        self.__m_is_valid = True

        # Consumer part
        w_consumer_dict = w_configuration_instance.get("consumer")
        if type(w_consumer_dict) is dict:
            if {"key", "secret"} <= w_consumer_dict.keys():
                self.__m_user_key = self.__check_value_type(w_consumer_dict["key"], str, "")
                self.__m_user_secret = self.__check_value_type(w_consumer_dict["secret"], str, "")
                self.__m_is_valid &= bool(self.__m_user_secret) and bool(self.__m_user_secret)
            else:
                self.__m_is_valid = False
        else:
            self.__m_is_valid = False

        # Token part
        if self.__m_is_valid:
            w_token_dict = w_configuration_instance.get("token")
            if type(w_token_dict) is dict:
                if {"access", "access_secret"} <= w_token_dict.keys():
                    self.__m_access_token = self.__check_value_type(w_token_dict["access"], str, "")
                    self.__m_access_token_secret = self.__check_value_type(w_token_dict["access_secret"], str, "")
                    self.__m_is_valid &= bool(self.__m_access_token) and bool(self.__m_access_token_secret)
            else:
                self.__m_is_valid = False

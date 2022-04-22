#/!usr/bin/env python

# *********************************
#   This file contains a class
#   that holds credentials data
# *********************************

class Credentials:
    """
        This class hold special credentials
    """

    # *******************
    #   Static methods
    # *******************

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


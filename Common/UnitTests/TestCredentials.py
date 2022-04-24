#!/usr/bin/env python

# ************************
#   Test for Credentials
#   1 - Load from configuration file
# *************************************

import unittest
from Common import Credentials
from Common.Configuration import Settings


class TestCredentials(unittest.TestCase):
    """
        1- Load from configuration file
    """

    def test_load_from_config(self):
        w_settings = Settings("Resources/Config.json")
        w_expected_credentials = Credentials()
        w_observed_credentials = Credentials(w_settings)

        # Fill the expected values
        w_expected_credentials.user_key = "OCgWzDW6PaBvBeVimmGBqdAg1"
        w_expected_credentials.user_secret = "tBKnmyg5Jfsewkpmw74gxHZbbZkGIH6Ee4rsM0lD1vFL7SrEIM"
        w_expected_credentials.access_token = "1449663645412065281-LNjZoEO9lxdtxPcmLtM35BRdIKYHpk"
        w_expected_credentials.access_token_secret = "FL3SGsUWSzPVFnG7bNMnyh4vYK8W1SlABBNtdF7Xcbh7a"
        w_expected_credentials.validate()

        # Check if credentials are the same
        self.assertTrue(w_observed_credentials.is_valid, "Credentials loaded from a configuration is not correct")
        self.assertEqual(w_expected_credentials, w_observed_credentials, "Credentials are not the same")


if __name__ == "__main__":
    unittest.main()

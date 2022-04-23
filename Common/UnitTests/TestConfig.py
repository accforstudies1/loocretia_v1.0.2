#!/usr/bin/env python

# **************************************************
#   Test Config
#
#   1 - Test if a config is properly loaded
#   2 - Test if the default config is properly loaded
# ****************************************************

import unittest
from Common.Configuration import Settings


class TestConfig(unittest.TestCase):
    """
        1 - Test if a config is properly loaded
        2 - Test if the default config is properly loaded
    """

    def test_config(self):
        w_settings = Settings.instance("Resources/Config.json")
        w_data = {
            "consumer": {
                "key": "OCgWzDW6PaBvBeVimmGBqdAg1",
                "secret": "tBKnmyg5Jfsewkpmw74gxHZbbZkGIH6Ee4rsM0lD1vFL7SrEIM"
            },
            "token": {
                "access": "1449663645412065281-LNjZoEO9lxdtxPcmLtM35BRdIKYHpk",
                "access_secret": "FL3SGsUWSzPVFnG7bNMnyh4vYK8W1SlABBNtdF7Xcbh7a",
                "bearer": "AAAAAAAAAAAAAAAAAAAAAH%2BVaAEAAAAAuxxHepI5%2FMY%2Ff%2B2nulbSFq1i%2BuI%3D9hHztVwJDjmWMI5Ith0udnNzi1lOvwCC1sJNz6ifWHly85tm6z"
            }
        }
        self.assertEqual(True, w_settings.read(), "Configuration does not seem valid")
        self.assertIs(dict, type(w_settings.data), "The configuration is not a dict")

        # Read the configuration
        self.assertDictEqual(w_data, w_settings.data, "Configuration is not correct")


if __name__ == "__main__":
    unittest.main()

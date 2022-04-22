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

    def test_anonymous_config(self):
        w_settings = Settings("Resources/Config.json")
        self.assertEqual(True, w_settings.read(), "Configuration is not seemed valid")
        self.assertIs(dict, type(w_settings.data), "The configuration is not a dict")

        # Read the configuration


if __name__ == "__main__":
    unittest.main()




#!/usr/bin/env python

# ******************************************************
#   Test the CSV Parser
#   1 - Test an empty CSV file => Read NOK
#   2 - Test a good CSV file => Read OK and Data OK
# ******************************************************

import unittest
from Common.FileParser import CSVParser

class TestCSVParser(unittest.TestCase):
    """
        1 - Test an empty CSV file => Read NOK
        2 - Test a good CSV file => Read OK and Data OK
    """

    def test_empty_file(self):
        w_parser = CSVParser("Resources/Empty.csv")
        self.assertFalse(w_parser.read())

    def test_good_file(self):
        w_data_expected = {
            0: {
                "Id": "0",
                "Attr1": "Tr",
                "Attr2": "Uy",
                "Attr3": "Ui"
            },
            1: {
                "Id": "4",
                "Attr1": "Ji",
                "Attr2": "Li",
                "Attr3": "Lo"
            }
        }
        w_parser = CSVParser("Resources/Test.csv", ",")

        # Check if data has been parsed properly
        self.assertTrue(w_parser.read(), "An error when decoded the proper CSV file")
        self.assertDictEqual(w_data_expected, w_parser.data, "Data has not been parsed as expected")


if __name__ == "__main__":
    unittest.main()



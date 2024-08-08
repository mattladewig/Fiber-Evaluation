import unittest
from unittest.mock import patch
from io import StringIO
import json
import sys
from tests.loss_calc import main

class TestMain(unittest.TestCase):
    def test_main_with_required_arguments(self):
        # Test case with all required arguments provided
        args = ["--tx_power", "10", "--rx_power", "5", "--fiber_type", "s", "--wavelength", "1310", "--fiber_length", "1000", "--num_connectors", "2", "--num_splices", "1"]
        expected_output = """
Summary of Inputs and Results:
    Transmission Power: 10.0 mW
    Received Power: 5.0 mW
    Observed Loss: -5.0000 mW / 3.01 dBm loss
    Fiber Type: singlemode
    Wavelength: 1310 nm
    Fiber Length: 1000.0 meters
    Number of Mated Connectors: 2
    Number of Splices: 1
    Calculated Loss Budget: 4.05 dB
    Validation Result: The observed loss of -5.0000 mW / 3.01 dBm loss is within the acceptable loss budget of 4.05.
"""

        with patch("sys.stdout", new=StringIO()) as fake_out:
            with patch.object(sys, "argv", args):
                main()
                self.assertEqual(fake_out.getvalue().strip(), expected_output.strip())

    def test_main_without_optional_arguments(self):
        # Test case without optional arguments
        args = ["--tx_power", "10", "--rx_power", "5"]
        expected_output = """
Summary of Inputs and Results:
    Transmission Power: 10.0 mW
    Received Power: 5.0 mW
    Observed Loss: -5.0000 mW / 3.01 dBm loss
"""

        with patch("sys.stdout", new=StringIO()) as fake_out:
            with patch.object(sys, "argv", args):
                main()
                self.assertEqual(fake_out.getvalue().strip(), expected_output.strip())

    def test_main_with_json_output(self):
        # Test case with JSON output
        args = ["--tx_power", "10", "--rx_power", "5", "--json"]
        expected_output = {
            "Transmission Power": "10.0 mW",
            "Received Power": "5.0 mW",
            "Observed Loss": "-5.0000 mW / 3.01 dBm loss"
        }

        with patch("sys.stdout", new=StringIO()) as fake_out:
            with patch.object(sys, "argv", args):
                main()
                self.assertEqual(json.loads(fake_out.getvalue().strip()), expected_output)

if __name__ == "__main__":
    unittest.main()